from pathlib import Path

import torch

import modules.shared as shared
from modules.models import reload_model


def add_lora_to_model(lora_name):

    if not(shared.args.autograd):
       from peft import PeftModel

    # If a LoRA had been previously loaded, or if we want
    # to unload a LoRA, reload the model
    if shared.lora_name != "None" or lora_name == "None":
        shared.lora_name = shared.args.lora = None
        reload_model()
        
    shared.lora_name = lora_name
    if shared.args.autograd and shared.lora_name != "None":
       import sys

       sys.path.insert(0, str(Path("repositories/GPTQ-Merged/src/alpaca_lora_4bit")))
       import autograd_4bit, quant
       from autograd_4bit import Autograd4bitQuantLinear
       
       sys.path.insert(0, 'repositories/peft/src')
       from peft import PeftModel
       from peft.tuners.lora import Linear4bitLt
       print('Loading', lora_name)
       shared.model = PeftModel.from_pretrained(shared.model, Path(f"loras/{lora_name}"), device_map={'': 0}, torch_dtype=torch.float32)
       from modules.GPTQ_loader import finalize_autograd
       finalize_autograd(shared.model)

    else:
      if lora_name != "None":
         print(f"Adding the LoRA {lora_name} to the model...")
         params = {}
         if not shared.args.cpu:
             params['dtype'] = shared.model.dtype
             if hasattr(shared.model, "hf_device_map"):
                 params['device_map'] = {"base_model.model."+k: v for k, v in shared.model.hf_device_map.items()}
             elif shared.args.load_in_8bit:
                 params['device_map'] = {'': 0}
            
         shared.model = PeftModel.from_pretrained(shared.model, Path(f"loras/{lora_name}"), **params)
         if not shared.args.load_in_8bit and not shared.args.cpu:
             shared.model.half()
             if not hasattr(shared.model, "hf_device_map"):
                 if torch.has_mps:
                     device = torch.device('mps')
                     shared.model = shared.model.to(device)
                 else:
                     shared.model = shared.model.cuda()

