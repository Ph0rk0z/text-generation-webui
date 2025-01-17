# Text generation web UI Testing
### Here there be dragons. (But V1 and V2 GPTQ support)

- Allow 4bit loras and use of Autograd + AutoGPTQ for inference 
- Use GPT-J 4-bits (GPTQv1/v2)
- GPT-NeoXT 4-bits (GPTQv1/v2)
- 8 bit threshold slider, default 1.5 (pre compute 7.0)
- V1 Models work in --autograd (declare with --v1)
- V2 Models work in both.
- Offloading works in autograd with --gpu-memory but doesn't 100% hodl while generating
- Offloading with llama_inference_offload, fastest multi-gpu besides exllama
- Autograd + quant_attn beating Autogtpq on P6000!
- Only load one 4bit lora at a time and apply with no loras before switching.
- Train 4-bit loras with Autograd and hopefully soon AutoGPTQ
- exLlama support (compute 7 and up for benefits)
- more parameters from UI for remote hosts


#### Depends on:
https://github.com/Ph0rk0z/GPTQ-Merged (dual module branch)

~~https://github.com/sterlind/peft~~ (now auto patches)

06/13/24
```
Kept the loaders, hopefully no bugs
```

04/5/24
```
Update gradio to 4.25
```

02/18/24
```
Exllama V1 is back and llama.cpp HF require you copy tokenizers
to the respective model folders.
```


10/27/23
```
If loading fails due to flash attention and your system doesn't support it:
please pip uninstall flash-attn and flash_attn.
```


10/16/23
```
Update exllamav2 to use the new 8bit cache. So far no issues.
Tested LoRA, multi-gpu and CFG on 70b models.
```

10/11/23
```
GPTQ Merged fixed to work with new PEFT.
```

10/8/23
```
Exllamav2 lora support and updating to pytorch 2.1.0 
```

9/9/23
```
Update exllama to the latest version because rope settings are changed.
They will not work properly with the previous versions. This is a breaking change.
It now reads a default rope base value from the model config. Overriding rope base
with your own will use that, alpha value will apply to the inferred base.
```

8/10/23
```
Add scaled ROPE to GPTQ classic. Requires you install git transformers.
Doesn't work with fused attention (FP16 cards) for autograd or with llama offloading yet.
AutoGPTQ will work when it exposes the option. Previous option was to edit
config files which is not great for alpha.
```

8/6/23
```
Fixed big model settings saving bug. Flash attention 2 for exllama. Works with LoRA.
Added ability to disable fused attention for regular exllama as well so you can load
LoRA there. Generally you want to pick fused or flash but not both.

Make sure to install it from it's repo or pip. 
```

7/31/23
```
Flexgen is removed. If you need it d/l the backup and use that.
```

7/1/23
```
Add Panchovix's RoPE scaling. Longer context with no SuperHOT. 
Uninstall the pip module if you use it and probably don't use it if you want latest fixes.
```

6/24/23
```
Merge the new model page. Hope to break out Autograd into it's own loader soon.
```

6/17/23
```
New branch https://github.com/Ph0rk0z/text-generation-webui-testing/tree/model-page
Uses the new loader based model loading. All the kinks aren't worked out yet.
Definitely required in the future as new inference methods are added.
Not sure how I feel about it so I'll try it out for a few days first.
```

6/8/23
```
exllama support merged
insane inference speed and working multi-gpu
```

5/30/23
```
Dirty lora support for AutoGPTQ. You need my fork or merged PR,
also get PEFT current pip install git+https://github.com/huggingface/peft
No training yet.
```

5/17/23
```
Update submodules, supporting a new method of splitting that makes 65b possible over 2, 
even janky cards at higher speed. No more OOM on 65b at full context.
```

5/8/23
```
I think autograd problem is fixed.. equal or faster than GPTQ
Update the submodules git submodule update --recursive --remote
```

4/22/23
```
New --mlp-attn, slightly faster on some contexts but no lora support added yet.
both --xformers and --sdp-attention prevent the 30b from going OOM at full context.
```

4/18/23
```
Using the patch for PEFT and no longer depends on PEFT fork.
Makes it easier to run main branch side by side.
Rewrote the GPTQ loader as well to be more compact.
You may have to update tokenizers agian and install colorama from pip.
```

4/11/23
```
Update to new PEFT version
https://github.com/sterlind/peft
```

4/10/23
```
pip install deepspeed -U
pip install xmformers
Xformers install will upgrade torch to 2.0
YOU WILL HAVE TO RECOMPILE YOUR CUDA KERNELS!!
```

4/8/23 - Update transformers!
```
pip install tokenizers==0.13.1
pip install protobuf==3.20.0
pip install git+https://github.com/huggingface/transformers
```
Repos are linked as submodules.. you may have to update them: https://stackoverflow.com/a/1032653
```
git submodule update --remote
```

#### Why?

* 13b and 30b llama response times for me become usable with a lora or not.
* Changes aren't so clean to be accepted as a p/r

#### How?

* Clone and re-use your oobabooga/text-generation-webui conda environment.
* Build GPTQ kernel with python setup.py install after cloing into repositories/
* Also build and install patched PEFT.

#### Windows?

* I don't know, can't use it. Try WSL

#### Credits

* https://github.com/johnsmith0031/alpaca_lora_4bit
* https://github.com/0cc4m/GPTQ-for-LLaMa

#### Example Commands
```
python server.py --model llama-30b --chat --autograd --wbits 4 
python server.py --model opt-13b --chat --autograd --wbits 4 --lora opt-13b-lora-1.0ep
python server.py --model oasst-sft-1-pythia-12b --chat --autograd --wbits 4 --model_type gptneox
python server.py --model oasst-sft-1-pythia-12b --chat --autograd --wbits 4 --model_type gptneox --v1
python server.py --model llama-7b-4bit-128g --chat --groupsize 128 --wbits 4 --model_type llama
python server.py --model llama-30b-4bit-128g --chat --autograd --groupsize 128  --wbits 4 --model_type llama

```

|![Image1](https://github.com/oobabooga/screenshots/raw/main/print_instruct.png) | ![Image2](https://github.com/oobabooga/screenshots/raw/main/print_chat.png) |
|:---:|:---:|
|![Image1](https://github.com/oobabooga/screenshots/raw/main/print_default.png) | ![Image2](https://github.com/oobabooga/screenshots/raw/main/print_parameters.png) |

## Features

* 3 interface modes: default (two columns), notebook, and chat.
* Multiple model backends: [Transformers](https://github.com/huggingface/transformers), [llama.cpp](https://github.com/ggerganov/llama.cpp) (through [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)), [ExLlamaV2](https://github.com/turboderp/exllamav2), [AutoGPTQ](https://github.com/PanQiWei/AutoGPTQ), [AutoAWQ](https://github.com/casper-hansen/AutoAWQ), [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM).
* Dropdown menu for quickly switching between different models.
* Large number of extensions (built-in and user-contributed), including Coqui TTS for realistic voice outputs, Whisper STT for voice inputs, translation, [multimodal pipelines](https://github.com/oobabooga/text-generation-webui/tree/main/extensions/multimodal), vector databases, Stable Diffusion integration, and a lot more. See [the wiki](https://github.com/oobabooga/text-generation-webui/wiki/07-%E2%80%90-Extensions) and [the extensions directory](https://github.com/oobabooga/text-generation-webui-extensions) for details.
* [Chat with custom characters](https://github.com/oobabooga/text-generation-webui/wiki/03-%E2%80%90-Parameters-Tab#character).
* Precise chat templates for instruction-following models, including Llama-2-chat, Alpaca, Vicuna, Mistral.
* LoRA: train new LoRAs with your own data, load/unload LoRAs on the fly for generation.
* Transformers library integration: load models in 4-bit or 8-bit precision through bitsandbytes, use llama.cpp with transformers samplers (`llamacpp_HF` loader), CPU inference in 32-bit precision using PyTorch.
* OpenAI-compatible API server with Chat and Completions endpoints -- see the [examples](https://github.com/oobabooga/text-generation-webui/wiki/12-%E2%80%90-OpenAI-API#examples).

## How to install

1) Clone or [download](https://github.com/oobabooga/text-generation-webui/archive/refs/heads/main.zip) the repository.
2) Run the `start_linux.sh`, `start_windows.bat`, `start_macos.sh`, or `start_wsl.bat` script depending on your OS.
3) Select your GPU vendor when asked.
4) Once the installation ends, browse to `http://localhost:7860/?__theme=dark`.
5) Have fun!

To restart the web UI in the future, just run the `start_` script again. This script creates an `installer_files` folder where it sets up the project's requirements. In case you need to reinstall the requirements, you can simply delete that folder and start the web UI again.

The script accepts command-line flags. Alternatively, you can edit the `CMD_FLAGS.txt` file with a text editor and add your flags there.

To get updates in the future, run `update_wizard_linux.sh`, `update_wizard_windows.bat`, `update_wizard_macos.sh`, or `update_wizard_wsl.bat`.

<details>
<summary>
Setup details and information about installing manually
</summary>

### One-click-installer

The script uses Miniconda to set up a Conda environment in the `installer_files` folder.

If you ever need to install something manually in the `installer_files` environment, you can launch an interactive shell using the cmd script: `cmd_linux.sh`, `cmd_windows.bat`, `cmd_macos.sh`, or `cmd_wsl.bat`.

* There is no need to run any of those scripts (`start_`, `update_wizard_`, or `cmd_`) as admin/root.
* To install the requirements for extensions, you can use the `extensions_reqs` script for your OS. At the end, this script will install the main requirements for the project to make sure that they take precedence in case of version conflicts.
* For additional instructions about AMD and WSL setup, consult [the documentation](https://github.com/oobabooga/text-generation-webui/wiki).
* For automated installation, you can use the `GPU_CHOICE`, `USE_CUDA118`, `LAUNCH_AFTER_INSTALL`, and `INSTALL_EXTENSIONS` environment variables. For instance: `GPU_CHOICE=A USE_CUDA118=FALSE LAUNCH_AFTER_INSTALL=FALSE INSTALL_EXTENSIONS=TRUE ./start_linux.sh`.

### Manual installation using Conda

Recommended if you have some experience with the command-line.

#### 0. Install Conda

https://docs.conda.io/en/latest/miniconda.html

On Linux or WSL, it can be automatically installed with these two commands ([source](https://educe-ubc.github.io/conda.html)):

```
curl -sL "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" > "Miniconda3.sh"
bash Miniconda3.sh
```

#### 1. Create a new conda environment

```
conda create -n textgen python=3.11
conda activate textgen
```

#### 2. Install Pytorch

| System | GPU | Command |
|--------|---------|---------|
| Linux/WSL | NVIDIA | `pip3 install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu121` |
| Linux/WSL | CPU only | `pip3 install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cpu` |
| Linux | AMD | `pip3 install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/rocm5.6` |
| MacOS + MPS | Any | `pip3 install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2` |
| Windows | NVIDIA | `pip3 install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu121` |
| Windows | CPU only | `pip3 install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2` |

The up-to-date commands can be found here: https://pytorch.org/get-started/locally/.

For NVIDIA, you also need to install the CUDA runtime libraries:

```
conda install -y -c "nvidia/label/cuda-12.1.1" cuda-runtime
```

If you need `nvcc` to compile some library manually, replace the command above with

```
conda install -y -c "nvidia/label/cuda-12.1.1" cuda
```

#### 3. Install the web UI

```
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui
pip install -r <requirements file according to table below>
```

Requirements file to use:

| GPU | CPU | requirements file to use |
|--------|---------|---------|
| NVIDIA | has AVX2 | `requirements.txt` |
| NVIDIA | no AVX2 | `requirements_noavx2.txt` |
| AMD | has AVX2 | `requirements_amd.txt` |
| AMD | no AVX2 | `requirements_amd_noavx2.txt` |
| CPU only | has AVX2 | `requirements_cpu_only.txt` |
| CPU only | no AVX2 | `requirements_cpu_only_noavx2.txt` |
| Apple | Intel | `requirements_apple_intel.txt` |
| Apple | Apple Silicon | `requirements_apple_silicon.txt` |

### Start the web UI

```
conda activate textgen
cd text-generation-webui
python server.py
```

Then browse to

`http://localhost:7860/?__theme=dark`

##### AMD GPU on Windows

1) Use `requirements_cpu_only.txt` or `requirements_cpu_only_noavx2.txt` in the command above.

2) Manually install llama-cpp-python using the appropriate command for your hardware: [Installation from PyPI](https://github.com/abetlen/llama-cpp-python#installation-with-hardware-acceleration).
    * Use the `LLAMA_HIPBLAS=on` toggle.
    * Note the [Windows remarks](https://github.com/abetlen/llama-cpp-python#windows-remarks).

3) Manually install AutoGPTQ: [Installation](https://github.com/PanQiWei/AutoGPTQ#install-from-source).
    * Perform the from-source installation - there are no prebuilt ROCm packages for Windows.

##### Older NVIDIA GPUs

1) For Kepler GPUs and older, you will need to install CUDA 11.8 instead of 12:

```
pip3 install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cu118
conda install -y -c "nvidia/label/cuda-11.8.0" cuda-runtime
```

2) bitsandbytes >= 0.39 may not work. In that case, to use `--load-in-8bit`, you may have to downgrade like this:
    * Linux: `pip install bitsandbytes==0.38.1`
    * Windows: `pip install https://github.com/jllllll/bitsandbytes-windows-webui/raw/main/bitsandbytes-0.38.1-py3-none-any.whl`

##### Manual install

The `requirements*.txt` above contain various wheels precompiled through GitHub Actions. If you wish to compile things manually, or if you need to because no suitable wheels are available for your hardware, you can use `requirements_nowheels.txt` and then install your desired loaders manually.

### Alternative: Docker

```
For NVIDIA GPU:
ln -s docker/{nvidia/Dockerfile,nvidia/docker-compose.yml,.dockerignore} .
For AMD GPU: 
ln -s docker/{amd/Dockerfile,intel/docker-compose.yml,.dockerignore} .
For Intel GPU:
ln -s docker/{intel/Dockerfile,amd/docker-compose.yml,.dockerignore} .
For CPU only
ln -s docker/{cpu/Dockerfile,cpu/docker-compose.yml,.dockerignore} .
cp docker/.env.example .env
#Create logs/cache dir : 
mkdir -p logs cache
# Edit .env and set: 
#   TORCH_CUDA_ARCH_LIST based on your GPU model
#   APP_RUNTIME_GID      your host user's group id (run `id -g` in a terminal)
#   BUILD_EXTENIONS      optionally add comma separated list of extensions to build
# Edit CMD_FLAGS.txt and add in it the options you want to execute (like --listen --cpu)
# 
docker compose up --build
```

* You need to have Docker Compose v2.17 or higher installed. See [this guide](https://github.com/oobabooga/text-generation-webui/wiki/09-%E2%80%90-Docker) for instructions.
* For additional docker files, check out [this repository](https://github.com/Atinoda/text-generation-webui-docker).

### Updating the requirements

From time to time, the `requirements*.txt` change. To update, use these commands:

```
conda activate textgen
cd text-generation-webui
pip install -r <requirements file that you have used> --upgrade
```
</details>

<details>
<summary>
List of command-line flags
</summary>

#### Basic settings

| Flag                                       | Description |
|--------------------------------------------|-------------|
| `-h`, `--help`                             | show this help message and exit |
| `--multi-user`                             | Multi-user mode. Chat histories are not saved or automatically loaded. WARNING: this is likely not safe for sharing publicly. |
| `--character CHARACTER`                    | The name of the character to load in chat mode by default. |
| `--model MODEL`                            | Name of the model to load by default. |
| `--lora LORA [LORA ...]`                   | The list of LoRAs to load. If you want to load more than one LoRA, write the names separated by spaces. |
| `--model-dir MODEL_DIR`                    | Path to directory with all the models. |
| `--lora-dir LORA_DIR`                      | Path to directory with all the loras. |
| `--model-menu`                             | Show a model menu in the terminal when the web UI is first launched. |
| `--settings SETTINGS_FILE`                 | Load the default interface settings from this yaml file. See `settings-template.yaml` for an example. If you create a file called `settings.yaml`, this file will be loaded by default without the need to use the `--settings` flag. |
| `--extensions EXTENSIONS [EXTENSIONS ...]` | The list of extensions to load. If you want to load more than one extension, write the names separated by spaces. |
| `--verbose`                                | Print the prompts to the terminal. |
| `--chat-buttons`                           | Show buttons on the chat tab instead of a hover menu. |

#### Model loader

| Flag                                       | Description |
|--------------------------------------------|-------------|
| `--loader LOADER`                          | Choose the model loader manually, otherwise, it will get autodetected. Valid options: Transformers, llama.cpp, llamacpp_HF, ExLlamav2_HF, ExLlamav2, AutoGPTQ, AutoAWQ, GPTQ-for-LLaMa, QuIP#. |

#### Accelerate/transformers

| Flag                                        | Description |
|---------------------------------------------|-------------|
| `--cpu`                                     | Use the CPU to generate text. Warning: Training on CPU is extremely slow. |
| `--auto-devices`                            | Automatically split the model across the available GPU(s) and CPU. |
|  `--gpu-memory GPU_MEMORY [GPU_MEMORY ...]` | Maximum GPU memory in GiB to be allocated per GPU. Example: --gpu-memory 10 for a single GPU, --gpu-memory 10 5 for two GPUs. You can also set values in MiB like --gpu-memory 3500MiB. |
| `--cpu-memory CPU_MEMORY`                   | Maximum CPU memory in GiB to allocate for offloaded weights. Same as above. |
| `--disk`                                    | If the model is too large for your GPU(s) and CPU combined, send the remaining layers to the disk. |
| `--disk-cache-dir DISK_CACHE_DIR`           | Directory to save the disk cache to. Defaults to `cache/`. |
| `--load-in-8bit`                            | Load the model with 8-bit precision.|
| `--threshold`                               | Threshold for 8bit precision for older cards. It will use more memory while performing infrerence so watch out. NaN == too high. OOM == too low.|
| `--bf16`                                    | Load the model with bfloat16 precision. Requires NVIDIA Ampere GPU. |
| `--no-cache`                                | Set `use_cache` to False while generating text. This reduces the VRAM usage a bit with a performance cost. |
| `--xformers`                                | Use xformer's memory efficient attention. This should increase your tokens/s. |
| `--sdp-attention`                           | Use torch 2.0's sdp attention. |
| `--flash-attention`                         | Use Flash Attention 2. This drastically reduces the VRAM cost |
| `--use_flash_attention_2`                   | Set use_flash_attention_2=True while loading the transformers model. |
| `--trust-remote-code`                       | Set trust_remote_code=True while loading a model. Necessary for ChatGLM and Falcon. |
| `--no-cache`                                | Set `use_cache` to `False` while generating text. This reduces VRAM usage slightly, but it comes at a performance cost. |
| `--trust-remote-code`                       | Set `trust_remote_code=True` while loading the model. Necessary for some models. |
| `--no_use_fast`                             | Set use_fast=False while loading the tokenizer (it's True by default). Use this if you have any problems related to use_fast. |
| `--use_flash_attention_2`                   | Set use_flash_attention_2=True while loading the model. |

#### bitsandbytes 4-bit

⚠️  Requires minimum compute of 7.0 on Windows at the moment.

| Flag                                        | Description |
|---------------------------------------------|-------------|
| `--load-in-4bit`                            | Load the model with 4-bit precision (using bitsandbytes). |
| `--use_double_quant`                        | use_double_quant for 4-bit. |
| `--compute_dtype COMPUTE_DTYPE`             | compute dtype for 4-bit. Valid options: bfloat16, float16, float32. |
| `--quant_type QUANT_TYPE`                   | quant_type for 4-bit. Valid options: nf4, fp4. |

#### llama.cpp

| Flag        | Description |
|-------------|-------------|
| `--tensorcores`  | Use llama-cpp-python compiled with tensor cores support. This increases performance on RTX cards. NVIDIA only. |
| `--flash-attn`   | Use flash-attention. |
| `--n_ctx N_CTX` | Size of the prompt context. |
| `--threads` | Number of threads to use. |
| `--threads-batch THREADS_BATCH` | Number of threads to use for batches/prompt processing. |
| `--no_mul_mat_q` | Disable the mulmat kernels. |
| `--n_batch` | Maximum number of prompt tokens to batch together when calling llama_eval. |
| `--no-mmap`   | Prevent mmap from being used. |
| `--mlock`     | Force the system to keep the model in RAM. |
| `--n-gpu-layers N_GPU_LAYERS` | Number of layers to offload to the GPU. |
| `--tensor_split TENSOR_SPLIT`       | Split the model across multiple GPUs. Comma-separated list of proportions. Example: 18,17. |
| `--numa`      | Activate NUMA task allocation for llama.cpp. |
| `--logits_all`| Needs to be set for perplexity evaluation to work. Otherwise, ignore it, as it makes prompt processing slower. |
| `--no_offload_kqv` | Do not offload the K, Q, V to the GPU. This saves VRAM but reduces the performance. |
| `--cache-capacity CACHE_CAPACITY`   | Maximum cache capacity (llama-cpp-python). Examples: 2000MiB, 2GiB. When provided without units, bytes will be assumed. |
| `--row_split`                               | Split the model by rows across GPUs. This may improve multi-gpu performance. |
| `--streaming-llm`                           | Activate StreamingLLM to avoid re-evaluating the entire prompt when old messages are removed. |
| `--attention-sink-size ATTENTION_SINK_SIZE` | StreamingLLM: number of sink tokens. Only used if the trimmed prompt doesn't share a prefix with the old prompt. |

#### ExLlamav2

| Flag             | Description |
|------------------|-------------|
|`--gpu-split`     | Comma-separated list of VRAM (in GB) to use per GPU device for model layers. Example: 20,7,7. |
|`--max_seq_len MAX_SEQ_LEN`           | Maximum sequence length. |
|`--cfg-cache`                         | ExLlamav2_HF: Create an additional cache for CFG negative prompts. Necessary to use CFG with that loader. |
|`--no_flash_attn`                     | Force flash-attention to not be used. |
|`--cache_8bit`                        | Use 8-bit cache to save VRAM. |
|`--cache_4bit`                        | Use Q4 cache to save VRAM. |
|`--num_experts_per_token NUM_EXPERTS_PER_TOKEN` |  Number of experts to use for generation. Applies to MoE models like Mixtral. |

#### AutoGPTQ

| Flag             | Description |
|------------------|-------------|
| `--triton`                     | Use triton. |
| `--quant_attn`  | Ennable the use of fused attention, faster but slightly more vram. |
| `--fused_mlp`        | Triton mode only: enable the use of fused MLP, which will use lots more vram. |
| `--autogptq_act_order`                   | For models that don't have a quantize_config.json, this parameter is used to define whether to use group size and act_order together  |
| `--disable_exllama`            | Disable ExLlama kernel, which can improve inference speed on some systems. |
| `--disable_exllamav2`          | Disable ExLlamav2 kernel. |

#### ExLlama

| Flag             | Description |
|------------------|-------------|
|`--gpu-split`     | Comma-separated list of VRAM (in GB) to use per GPU device for model layers, e.g. `20,7,7` |
|`--nohalf2`       | Disable half2 so pascal can somewhat use exllama. its still not good  |
|`--max_seq_len MAX_SEQ_LEN`           | Maximum sequence length. |
|`--cfg-cache`                         | ExLlama_HF: Create an additional cache for CFG negative prompts. Necessary to use CFG with that loader, but not necessary for CFG with base ExLlama. |

#### GPTQ-for-LLaMa

| Flag                      | Description |
|---------------------------|-------------|
| `--wbits WBITS`           | GPTQ: Load a pre-quantized model with specified precision in bits. 2, 3, 4 and 8 are supported. |
| `--model_type MODEL_TYPE` | GPTQ: Model type of pre-quantized model. Currently LLaMA, OPT, GPT-NeoX, and GPT-J are supported. |
| `--groupsize GROUPSIZE`   | GPTQ: Group size. |
| `--pre_layer PRE_LAYER [PRE_LAYER ...]`  | The number of layers to allocate to the GPU. Setting this parameter enables CPU offloading for 4-bit models. For multi-gpu, write the numbers separated by spaces, eg `--pre_layer 30 60`. |
| `--checkpoint CHECKPOINT` | The path to the quantized checkpoint file. If not specified, it will be automatically detected. |
| `--autograd`   | GPTQ: Autograd implementation to use 4bit lora and run multiple models. Will now automatically select loader. |
| `--v1`   | GPTQ: Explicitly declare a GPTQv1 model to load into autograd. |
| `--quant_attn`         | (triton/Autograd) Enable quant attention.
| `--warmup_autotune`    | (triton) Enable warmup autotune.
| `--fused_mlp`          | (triton/Autograd) Enable fused mlp.
| `--autogptq`           | Load with autogptq. Look in shared.py for more options like triton or using act order w/ groupsize kernel

#### HQQ

| Flag        | Description |
|-------------|-------------|
| `--hqq-backend` | Backend for the HQQ loader. Valid options: PYTORCH, PYTORCH_COMPILE, ATEN. |

#### DeepSpeed

| Flag                                  | Description |
|---------------------------------------|-------------|
| `--deepspeed`                         | Enable the use of DeepSpeed ZeRO-3 for inference via the Transformers integration. |
| `--nvme-offload-dir NVME_OFFLOAD_DIR` | DeepSpeed: Directory to use for ZeRO-3 NVME offloading. |
| `--local_rank LOCAL_RANK`             | DeepSpeed: Optional argument for distributed setups. |

#### RoPE (for llama.cpp, ExLlamaV2, and transformers)

| Flag             | Description |
|------------------|-------------|
| `--alpha_value ALPHA_VALUE`           | Positional embeddings alpha factor for NTK RoPE scaling. Use either this or `compress_pos_emb`, not both. |
| `--rope_freq_base ROPE_FREQ_BASE`     | If greater than 0, will be used instead of alpha_value. Those two are related by `rope_freq_base = 10000 * alpha_value ^ (64 / 63)`. |
| `--compress_pos_emb COMPRESS_POS_EMB` | Positional embeddings compression factor. Should be set to `(context length) / (model's original context length)`. Equal to `1/rope_freq_scale`. |

#### Gradio

| Flag                                  | Description |
|---------------------------------------|-------------|
| `--listen`                            | Make the web UI reachable from your local network. |
| `--listen-port LISTEN_PORT`           | The listening port that the server will use. |
| `--listen-host LISTEN_HOST`           | The hostname that the server will use. |
| `--share`                             | Create a public URL. This is useful for running the web UI on Google Colab or similar. |
| `--auto-launch`                       | Open the web UI in the default browser upon launch. |
| `--gradio-auth USER:PWD`              | Set Gradio authentication password in the format "username:password". Multiple credentials can also be supplied with "u1:p1,u2:p2,u3:p3". |
| `--gradio-auth-path GRADIO_AUTH_PATH` | Set the Gradio authentication file path. The file should contain one or more user:password pairs in the same format as above. |
| `--ssl-keyfile SSL_KEYFILE`           | The path to the SSL certificate key file. |
| `--ssl-certfile SSL_CERTFILE`         | The path to the SSL certificate cert file. |

#### API

| Flag                                  | Description |
|---------------------------------------|-------------|
| `--api`                               | Enable the API extension. |
| `--public-api`                        | Create a public URL for the API using Cloudfare. |
| `--public-api-id PUBLIC_API_ID`       | Tunnel ID for named Cloudflare Tunnel. Use together with public-api option. |
| `--api-port API_PORT`                 | The listening port for the API. |
| `--api-key API_KEY`                   | API authentication key. |
| `--admin-key ADMIN_KEY`               | API authentication key for admin tasks like loading and unloading models. If not set, will be the same as --api-key. |
| `--nowebui`                           | Do not launch the Gradio UI. Useful for launching the API in standalone mode. |

#### Multimodal

| Flag                                  | Description |
|---------------------------------------|-------------|
| `--multimodal-pipeline PIPELINE`      | The multimodal pipeline to use. Examples: `llava-7b`, `llava-13b`. |

</details>

## Documentation

https://github.com/oobabooga/text-generation-webui/wiki

## Downloading models

Models should be placed in the folder `text-generation-webui/models`. They are usually downloaded from [Hugging Face](https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads).

* GGUF models are a single file and should be placed directly into `models`. Example:

```
text-generation-webui
└── models
    └── llama-2-13b-chat.Q4_K_M.gguf
```

* The remaining model types (like 16-bit transformers models and GPTQ models) are made of several files and must be placed in a subfolder. Example:

```
text-generation-webui
├── models
│   ├── lmsys_vicuna-33b-v1.3
│   │   ├── config.json
│   │   ├── generation_config.json
│   │   ├── pytorch_model-00001-of-00007.bin
│   │   ├── pytorch_model-00002-of-00007.bin
│   │   ├── pytorch_model-00003-of-00007.bin
│   │   ├── pytorch_model-00004-of-00007.bin
│   │   ├── pytorch_model-00005-of-00007.bin
│   │   ├── pytorch_model-00006-of-00007.bin
│   │   ├── pytorch_model-00007-of-00007.bin
│   │   ├── pytorch_model.bin.index.json
│   │   ├── special_tokens_map.json
│   │   ├── tokenizer_config.json
│   │   └── tokenizer.model
```

In both cases, you can use the "Model" tab of the UI to download the model from Hugging Face automatically. It is also possible to download it via the command-line with 

```
python download-model.py organization/model
```

Run `python download-model.py --help` to see all the options.

## Google Colab notebook

https://colab.research.google.com/github/oobabooga/text-generation-webui/blob/main/Colab-TextGen-GPU.ipynb

## Community

* Subreddit: https://www.reddit.com/r/oobabooga/
* Discord: https://discord.gg/jwZCF2dPQN

## Acknowledgment

In August 2023, [Andreessen Horowitz](https://a16z.com/) (a16z) provided a generous grant to encourage and support my independent work on this project. I am **extremely** grateful for their trust and recognition.
