import functools
from collections import OrderedDict

import gradio as gr

from modules import shared

loaders_and_params = OrderedDict({
    'Transformers': [
        'cpu_memory',
        'gpu_memory',
        'trust_remote_code',
        'load_in_8bit',
        'threshold',
        'bf16',
        'cpu',
        'disk',
        'auto_devices',
        'load_in_4bit',
        'use_double_quant',
        'quant_type',
        'compute_dtype',
        'trust_remote_code',
        'attention_info',
        'flash_attention',
        'xformers',
        'sdp_attention',
        'no_cache',
        'alpha_value',
        'rope_freq_base',
        'compress_pos_emb',
        'transformers_info'
    ],
    'ExLlama_HF': [
        'gpu_split',
        'nohalf2',
        'flash_attention',
        'quant_attn',
        'fused_mlp',
        'max_seq_len',
        'alpha_value',
        'rope_freq_base',
        'compress_pos_emb',
        'cfg_cache',
        'exllama_HF_info',
    ],
    'ExLlamav2_HF': [
        'gpu_split',
        'max_seq_len',
        'cfg_cache',
        'alpha_value',
        'compress_pos_emb',
    ],
    'ExLlama': [
        'gpu_split',
        'nohalf2',
        'flash_attention',
        'quant_attn',
        'max_seq_len',
        'alpha_value',
        'rope_freq_base',
        'compress_pos_emb',
        'exllama_info',
    ],
    'ExLlamav2': [
        'gpu_split',
        'max_seq_len',
        'alpha_value',
        'compress_pos_emb',
    ],
    'AutoGPTQ': [
        'triton',
        'quant_attn',
        'fused_mlp',
        'wbits',
        'groupsize',
        'warmup_autotune',
        'autogptq_act_order',
        'gpu_memory',
        'cpu_memory',
        'cpu',
        'disk',
        'trust_remote_code',      
        'attention_info',
        'flash_attention',
        'xformers',
        'sdp_attention',
        'disable_exllama',
        'no_cache',
        'autogptq_info',
    ],
    'GPTQ-for-LLaMa': [
        'wbits',
        'groupsize',
        'model_type',
        'pre_layer',
        'autograd',
        'v1',
        'quant_attn',
        'fused_mlp',
        'warmup_autotune',
        'attention_info',
        'flash_attention',
        'xformers',
        'sdp_attention',
        'no_cache',
        'alpha_value',
        'compress_pos_emb',
        'gptq_for_llama_info'
    ],
    'llama.cpp': [
        'n_ctx',
        'n_gpu_layers',
        'tensor_split',
        'n_batch',
        'threads',
        'no_mmap',
        'low_vram',
        'mlock',
        'mul_mat_q',
        'llama_cpp_seed',
        'alpha_value',
        'rope_freq_base',
        'compress_pos_emb',
        'cpu',
    ],
    'llamacpp_HF': [
        'n_ctx',
        'n_gpu_layers',
        'tensor_split',
        'n_batch',
        'threads',
        'no_mmap',
        'low_vram',
        'mlock',
        'llama_cpp_seed',
        'mul_mat_q',
        'alpha_value',
        'rope_freq_base',
        'compress_pos_emb',
        'cpu',
        'cfg_cache',
        'llamacpp_HF_info',
    ],
    'ctransformers': [
        'n_ctx',
        'n_gpu_layers',
        'n_batch',
        'threads',
        'model_type',
        'no_mmap',
        'mlock'
    ]
})

loaders_samplers = {
    'Transformers': {
        'temperature',
        'top_p',
        'top_k',
        'typical_p',
        'epsilon_cutoff',
        'eta_cutoff',
        'tfs',
        'top_a',
        'repetition_penalty',
        'additive_repetition_penalty',
        'repetition_penalty_range',
        'encoder_repetition_penalty',
        'no_repeat_ngram_size',
        'min_length',
        'seed',
        'do_sample',
        'penalty_alpha',
        'num_beams',
        'length_penalty',
        'early_stopping',
        'mirostat_mode',
        'mirostat_tau',
        'mirostat_eta',
        'guidance_scale',
        'negative_prompt',
        'ban_eos_token',
        'add_bos_token',
        'skip_special_tokens',
        'auto_max_new_tokens',
    },
    'ExLlama_HF': {
        'temperature',
        'top_p',
        'top_k',
        'typical_p',
        'epsilon_cutoff',
        'eta_cutoff',
        'tfs',
        'top_a',
        'repetition_penalty',
        'additive_repetition_penalty',
        'repetition_penalty_range',
        'encoder_repetition_penalty',
        'no_repeat_ngram_size',
        'min_length',
        'seed',
        'do_sample',
        'mirostat_mode',
        'mirostat_tau',
        'mirostat_eta',
        'guidance_scale',
        'negative_prompt',
        'ban_eos_token',
        'add_bos_token',
        'skip_special_tokens',
        'auto_max_new_tokens',
    },
    'ExLlama': {
        'temperature',
        'top_p',
        'top_k',
        'typical_p',
        'repetition_penalty',
        'repetition_penalty_range',
        'seed',
        'guidance_scale',
        'negative_prompt',
        'ban_eos_token',
        'auto_max_new_tokens',
    },
    'ExLlamav2': {
        'temperature',
        'top_p',
        'top_k',
        'repetition_penalty',
        'repetition_penalty_range',
        'seed',
        'ban_eos_token',
        'auto_max_new_tokens',
    },
    'ExLlamav2_HF': {
        'temperature',
        'top_p',
        'top_k',
        'typical_p',
        'epsilon_cutoff',
        'eta_cutoff',
        'tfs',
        'top_a',
        'repetition_penalty',
        'repetition_penalty_range',
        'encoder_repetition_penalty',
        'no_repeat_ngram_size',
        'min_length',
        'seed',
        'do_sample',
        'mirostat_mode',
        'mirostat_tau',
        'mirostat_eta',
        'guidance_scale',
        'negative_prompt',
        'ban_eos_token',
        'add_bos_token',
        'skip_special_tokens',
        'auto_max_new_tokens',
    },
    'AutoGPTQ': {
        'temperature',
        'top_p',
        'top_k',
        'typical_p',
        'epsilon_cutoff',
        'eta_cutoff',
        'tfs',
        'top_a',
        'repetition_penalty',
        'additive_repetition_penalty',
        'repetition_penalty_range',
        'encoder_repetition_penalty',
        'no_repeat_ngram_size',
        'min_length',
        'seed',
        'do_sample',
        'penalty_alpha',
        'num_beams',
        'length_penalty',
        'early_stopping',
        'mirostat_mode',
        'mirostat_tau',
        'mirostat_eta',
        'guidance_scale',
        'negative_prompt',
        'ban_eos_token',
        'add_bos_token',
        'skip_special_tokens',
        'auto_max_new_tokens',
    },
    'GPTQ-for-LLaMa': {
        'temperature',
        'top_p',
        'top_k',
        'typical_p',
        'epsilon_cutoff',
        'eta_cutoff',
        'tfs',
        'top_a',
        'repetition_penalty',
        'additive_repetition_penalty',
        'repetition_penalty_range',
        'encoder_repetition_penalty',
        'no_repeat_ngram_size',
        'min_length',
        'seed',
        'do_sample',
        'penalty_alpha',
        'num_beams',
        'length_penalty',
        'early_stopping',
        'mirostat_mode',
        'mirostat_tau',
        'mirostat_eta',
        'guidance_scale',
        'negative_prompt',
        'ban_eos_token',
        'add_bos_token',
        'skip_special_tokens',
        'auto_max_new_tokens',
    },
    'llama.cpp': {
        'temperature',
        'top_p',
        'top_k',
        'tfs',
        'repetition_penalty',
        'mirostat_mode',
        'mirostat_tau',
        'mirostat_eta',
        'ban_eos_token',
    },
    'llamacpp_HF': {
        'temperature',
        'top_p',
        'top_k',
        'typical_p',
        'epsilon_cutoff',
        'eta_cutoff',
        'tfs',
        'top_a',
        'repetition_penalty',
        'additive_repetition_penalty',
        'repetition_penalty_range',
        'encoder_repetition_penalty',
        'no_repeat_ngram_size',
        'min_length',
        'seed',
        'do_sample',
        'mirostat_mode',
        'mirostat_tau',
        'mirostat_eta',
        'guidance_scale',
        'negative_prompt',
        'ban_eos_token',
        'add_bos_token',
        'skip_special_tokens',
        'auto_max_new_tokens',
    },
    'ctransformers': {
        'temperature',
        'top_p',
        'top_k',
        'repetition_penalty',
        'repetition_penalty_range',
    }
}

loaders_model_types = {
    'GPTQ-for-LLaMa': [
        "None",
        "llama",
        "opt",
        "gptj",
        "gptneox"
    ],
    'ctransformers': [
        "None",
        "gpt2",
        "gptj",
        "gptneox",
        "llama",
        "mpt",
        "dollyv2",
        "replit",
        "starcoder",
        "gptbigcode",
        "falcon"
    ],
}


@functools.cache
def list_all_samplers():
    all_samplers = set()
    for k in loaders_samplers:
        for sampler in loaders_samplers[k]:
            all_samplers.add(sampler)

    return sorted(all_samplers)


def blacklist_samplers(loader):
    all_samplers = list_all_samplers()
    if loader == 'All':
        return [gr.update(visible=True) for sampler in all_samplers]
    else:
        return [gr.update(visible=True) if sampler in loaders_samplers[loader] else gr.update(visible=False) for sampler in all_samplers]


def get_model_types(loader):
    if loader in loaders_model_types:
        return loaders_model_types[loader]

    return ["None"]


def get_gpu_memory_keys():
    return [k for k in shared.gradio if k.startswith('gpu_memory')]


@functools.cache
def get_all_params():
    all_params = set()
    for k in loaders_and_params:
        for el in loaders_and_params[k]:
            all_params.add(el)

    if 'gpu_memory' in all_params:
        all_params.remove('gpu_memory')
        for k in get_gpu_memory_keys():
            all_params.add(k)

    return sorted(all_params)


def make_loader_params_visible(loader):
    params = []
    all_params = get_all_params()
    if loader in loaders_and_params:
        params = loaders_and_params[loader]

        if 'gpu_memory' in params:
            params.remove('gpu_memory')
            params += get_gpu_memory_keys()

    return [gr.update(visible=True) if k in params else gr.update(visible=False) for k in all_params]
