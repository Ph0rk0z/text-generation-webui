from pathlib import Path

import torch
from peft import PeftModel
from transformers import is_torch_xpu_available

import modules.shared as shared
from modules.logging_colors import logger
from modules.models import reload_model

from colorama import init, Fore, Back, Style
from modules.relative_imports import RelativeImport

def add_lora_to_model(lora_names):
    if (shared.args.autograd) and shared.args.loader == 'GPTQ-for-LLaMa':
        autograd_add_wrapper(lora_names)
    elif 'GPTQForCausalLM' in shared.model.__class__.__name__ or shared.args.loader == 'AutoGPTQ':
        add_lora_autogptq(lora_names)
    elif shared.model.__class__.__name__ in ['Exllamav2Model', 'Exllamav2HF'] or shared.args.loader in ['ExLlamav2', 'ExLlamav2_HF']:
        add_lora_exllamav2(lora_names)
    elif shared.model.__class__.__name__ in ['ExllamaModel', 'ExllamaHF'] or shared.args.loader == 'ExLlama':
        add_lora_exllama(lora_names)
    else:
        add_lora_transformers(lora_names)


def autograd_add_wrapper(lora_names):

    # Delete and reload.
    if len(lora_names) == 0:
        reload_model()
        shared.lora_names = []
        return

    # Add Autograd Lora
    elif len(lora_names) >= 1:
       lora_path = get_lora_path(lora_names[0])
       if (shared.args.quant_attn) or (shared.args.fused_mlp):
           autograd_inject(lora_path)
       else:
           autograd_add(lora_path)
       print(Style.BRIGHT + Fore.YELLOW + 'Autograd Lora Added:', lora_path)
       return

def autograd_add (lora_path):

    #Loras Do not Stack yet.

    with RelativeImport("repositories/GPTQ-Merged/src/alpaca_lora_4bit"):
        from monkeypatch.peft_tuners_lora_monkey_patch import replace_peft_model_with_gptq_lora_model
    replace_peft_model_with_gptq_lora_model()
      
    from peft import PeftModel
    #Not sure what happens in offload    
    print(Style.BRIGHT + Fore.YELLOW + 'Autograd Add Lora', lora_path)
    shared.model = PeftModel.from_pretrained(shared.model, lora_path, device_map={'': 0}, torch_dtype=torch.float32)
    
    from modules.GPTQ_loader import finalize_autograd
    finalize_autograd(shared.model)
    print(Style.BRIGHT + Fore.RED + 'Note: Only one lora works with 4bit for the time being.\nPlease only add one at a time and remove all loras before switching!')


def autograd_inject (lora_path):

    # it's a bit redundant
    with RelativeImport("repositories/GPTQ-Merged/src/alpaca_lora_4bit"):
        from autograd_4bit import Autograd4bitQuantLinear, make_quant_for_4bit_autograd

    shared.model.half() # Required here
    for n, m in shared.model.named_modules():
       if isinstance(m, Autograd4bitQuantLinear):
          if (shared.args.v1 == True):
              m.zeros = m.zeros.half()
          m.scales = m.scales.half()
          m.bias = m.bias.half()

    if (shared.args.quant_attn): 
        from model_attn_mlp_patch import make_quant_attn
        make_quant_attn(shared.model, is_v1_model=shared.args.v1)
        print(Style.BRIGHT + Fore.YELLOW + 'Autograd: quant_attn')
    if (shared.args.fused_mlp):
        from model_attn_mlp_patch import make_fused_mlp
        make_fused_mlp(shared.model, is_v1_model=shared.args.v1)
        print(Style.BRIGHT + Fore.YELLOW + 'Autograd: fused_mlp')


    from model_attn_mlp_patch import inject_lora_layers
    # Lora
    inject_lora_layers(shared.model, str(lora_path))
    print(Style.BRIGHT + Fore.YELLOW + 'Autograd Inject Lora', lora_path)


def get_lora_path(lora_name):
    p = Path(lora_name)
    if p.exists():
        lora_name = p.parts[-1]

    return Path(f"{shared.args.lora_dir}/{lora_name}")

def add_lora_exllamav2(lora_names):

    from peft import PeftModel
    from exllamav2 import ExLlamaV2Lora

    if len(lora_names) == 0:
        shared.model.lora.unload()
        shared.model.lora = None
        shared.lora_names = []
        return
    else:
        if len(lora_names) > 1:
            logger.warning('Only the first one in the list will be loaded.')

        lora_path = get_lora_path(lora_names[0])

        logger.info("Applying the following LoRAs to {}: {}".format(shared.model_name, ', '.join([lora_names[0]])))
        if shared.model.__class__.__name__ == 'Exllamav2Model':
            lora = ExLlamaV2Lora.from_directory(shared.model.model, str(lora_path))
            shared.model.lora = lora
        else:
            lora = ExLlamaV2Lora.from_directory(shared.model.ex_model, str(lora_path))
            shared.model.lora = lora

        shared.lora_names = [lora_names[0]]
        return

def add_lora_exllama(lora_names):

    try:
        from exllama.lora import ExLlamaLora
    except:
        try:
            from repositories.exllama.lora import ExLlamaLora
        except:
            logger.error("Could not find the file repositories/exllama/lora.py. Make sure that exllama is cloned inside repositories/ and is up to date.")
            return

    if len(lora_names) == 0:
        if shared.model.__class__.__name__ == 'ExllamaModel':
            shared.model.generator.lora = None
        else:
            shared.model.lora = None

        shared.lora_names = []
        return
    else:
        if len(lora_names) > 1:
            logger.warning('ExLlama can only work with 1 LoRA at the moment. Only the first one in the list will be loaded.')

        lora_path = get_lora_path(lora_names[0])
        lora_config_path = lora_path / "adapter_config.json"
        for file_name in ["adapter_model.safetensors", "adapter_model.bin"]:
            file_path = lora_path / file_name
            if file_path.is_file():
                lora_adapter_path = file_path

        logger.info("Applying the following LoRAs to {}: {}".format(shared.model_name, ', '.join([lora_names[0]])))
        if shared.model.__class__.__name__ == 'ExllamaModel':
            lora = ExLlamaLora(shared.model.model, str(lora_config_path), str(lora_adapter_path))
            shared.model.generator.lora = lora
        else:
            lora = ExLlamaLora(shared.model.ex_model, str(lora_config_path), str(lora_adapter_path))
            shared.model.lora = lora

        shared.lora_names = [lora_names[0]]
        return

def add_lora_exllamav2(lora_names):

    from exllamav2 import ExLlamaV2Lora

    if isinstance(shared.model.loras, list):
        for lora in shared.model.loras:
            lora.unload()

    if len(lora_names) > 0:
        logger.info("Applying the following LoRAs to {}: {}".format(shared.model_name, ', '.join(lora_names)))
        shared.model.loras = []
        for lora_name in lora_names:
            lora_path = get_lora_path(lora_name)
            if shared.model.__class__.__name__ == 'Exllamav2Model':
                lora = ExLlamaV2Lora.from_directory(shared.model.model, str(lora_path))
            else:
                lora = ExLlamaV2Lora.from_directory(shared.model.ex_model, str(lora_path))

            shared.model.loras.append(lora)

        shared.lora_names = lora_names
    else:
        shared.lora_names = []
        shared.model.loras = None


def add_lora_autogptq(lora_names):
    '''
    Adapted from https://github.com/Ph0rk0z/text-generation-webui-testing
    '''

    from peft import PeftModel

    try:
        from auto_gptq import get_gptq_peft_model
        from auto_gptq.utils.peft_utils import GPTQLoraConfig
    except:
        logger.error("This version of AutoGPTQ does not support LoRA. You need to install from source or wait for a new release.")
        return

    if len(lora_names) == 0:
        reload_model()
        shared.lora_names = []
        return
    else:
        if len(lora_names) > 1:
            logger.warning('AutoGPTQ can only work with 1 LoRA at the moment. Only the first one in the list will be loaded.')
        if shared.args.quant_attn:
            logger.warning('Quant Attention + AutoGPTQ may break Lora loading, turn it off!')

        peft_config = GPTQLoraConfig(
            inference_mode=True,
        )

        lora_path = get_lora_path(lora_names[0])
        logger.info("Applying the following LoRAs to {}: {}".format(shared.model_name, ', '.join([lora_names[0]])))
        shared.model = get_gptq_peft_model(shared.model, peft_config, lora_path)
        shared.lora_names = [lora_names[0]]
        return


def add_lora_transformers(lora_names):

    from peft import PeftModel

    prior_set = set(shared.lora_names)
    added_set = set(lora_names) - prior_set
    removed_set = prior_set - set(lora_names)

    # If no LoRA needs to be added or removed, exit
    if len(added_set) == 0 and len(removed_set) == 0:
        return

    # Add a LoRA when another LoRA is already present
    if len(removed_set) == 0 and len(prior_set) > 0 and "__merged" not in shared.model.peft_config.keys():
        logger.info(f"Adding the LoRA(s) named {added_set} to the model")
        for lora in added_set:
            shared.model.load_adapter(get_lora_path(lora), lora)

        if len(lora_names) > 1:
            merge_loras()

        shared.lora_names = lora_names
        return

    # If any LoRA needs to be removed, start over
    if len(removed_set) > 0:
        shared.model = shared.model.unload()

    if len(lora_names) > 0:
        params = {}
        if not shared.args.cpu:
            if shared.args.load_in_4bit or shared.args.load_in_8bit:
                params['peft_type'] = shared.model.dtype
            else:
                params['dtype'] = shared.model.dtype
                if hasattr(shared.model, "hf_device_map"):
                    params['device_map'] = {"base_model.model." + k: v for k, v in shared.model.hf_device_map.items()}

        logger.info("Applying the following LoRAs to {}: {}".format(shared.model_name, ', '.join(lora_names)))
        shared.model = PeftModel.from_pretrained(shared.model, get_lora_path(lora_names[0]), adapter_name=lora_names[0], **params)
        for lora in lora_names[1:]:
            shared.model.load_adapter(get_lora_path(lora), lora)

        if len(lora_names) > 1:
            merge_loras()

        if not shared.args.load_in_8bit and not shared.args.cpu:
            shared.model.half()
            if not hasattr(shared.model, "hf_device_map"):
                if torch.backends.mps.is_available():
                    device = torch.device('mps')
                    shared.model = shared.model.to(device)
                elif is_torch_xpu_available():
                    device = torch.device("xpu:0")
                    shared.model = shared.model.to(device)
                else:
                    shared.model = shared.model.cuda()

    shared.lora_names = lora_names


def merge_loras():
    if len(list({shared.model.peft_config[adapter].r for adapter in shared.model.peft_config.keys()})) > 1:
        logger.warning("The loaded LoRAs cannot be merged, as they have dissimilar ranks. Only the first one will be active.")
        return

    shared.model.add_weighted_adapter(shared.lora_names, [1] * len(shared.lora_names), "__merged")
    shared.model.set_adapter("__merged")
