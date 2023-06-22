import ast
import sys
from pathlib import Path

from modules import shared
from modules.logging_colors import logger
from modules.relative_imports import RelativeImport

with RelativeImport("repositories/exllama"):
    from generator import ExLlamaGenerator
    from model import ExLlama, ExLlamaCache, ExLlamaConfig
    from tokenizer import ExLlamaTokenizer

class ExllamaModel:
    def __init__(self):
        pass

    @classmethod
    def from_pretrained(self, path_to_model):

        path_to_model = Path(f'{shared.args.model_dir}') / Path(path_to_model)
        tokenizer_model_path = path_to_model / "tokenizer.model"
        model_config_path = path_to_model / "config.json"

        # Find the model checkpoint
        model_path = None
        for ext in ['.safetensors', '.pt', '.bin']:
            found = list(path_to_model.glob(f"*{ext}"))
            if len(found) > 0:
                if len(found) > 1:
                    logger.warning(f'More than one {ext} model has been found. The last one will be selected. It could be wrong.')

                model_path = found[-1]
                break

        config = ExLlamaConfig(str(model_config_path))
        config.model_path = str(model_path)

        # Tuning
        config.matmul_recons_thd = 8
        config.fused_mlp_thd = 2
        config.sdp_thd = 8
        config.matmul_fused_remap = False

        if (shared.args.nohalf2):
            config.rmsnorm_no_half2 = True
            config.rope_no_half2 = True
            config.matmul_no_half2 = True
            config.silu_no_half2 = True

        if (shared.args.gpu_split):
            config.set_auto_map(shared.args.gpu_split)
            config.gpu_peer_fix = True

        model = ExLlama(config)
        tokenizer = ExLlamaTokenizer(str(tokenizer_model_path))
        cache = ExLlamaCache(model)
        generator = ExLlamaGenerator(model, tokenizer, cache)


        result = self()
        result.config = config
        result.model = model
        result.cache = cache
        result.tokenizer = tokenizer
        result.generator = generator
        return result, result

    def generate_with_streaming(self, prompt, state, stopping_strings):
        self.generator.settings.temperature = state['temperature']
        self.generator.settings.top_p = state['top_p']
        self.generator.settings.top_k = state['top_k']
        self.generator.settings.typical = state['typical_p']
        self.generator.settings.token_repetition_penalty_max = state['repetition_penalty']
        if state['ban_eos_token']:
            self.generator.disallow_tokens([self.tokenizer.eos_token_id])
        else:
            self.generator.disallow_tokens(None)

        self.generator.end_beam_search()
        ids = self.generator.tokenizer.encode(prompt)
        self.generator.gen_begin_reuse(ids)
        initial_len = self.generator.sequence[0].shape[0]
        has_leading_space = False

        all_stopping_strings = []
        # custom_stopping_strings
        custom_stopping_strings = state.get('custom_stopping_strings', '')
        all_stopping_strings += ast.literal_eval(f'[{custom_stopping_strings}]')
        # stopping_strings
        if stopping_strings is not None:
            all_stopping_strings += stopping_strings
            all_stopping_strings += state.get('stopping_strings', [])
        # stop_by_newline
        if state.get('stop_by_newline', False):
            all_stopping_strings += ['\n']
        all_stopping_strings = list(set(all_stopping_strings))

        tem_text = ''
        for i in range(state['max_new_tokens']):
            token = self.generator.gen_single_token()
            if i == 0 and self.generator.tokenizer.tokenizer.IdToPiece(int(token)).startswith('▁'):
                has_leading_space = True

            decoded_text = self.generator.tokenizer.decode(self.generator.sequence[0][initial_len:])
            if has_leading_space:
                decoded_text = ' ' + decoded_text

            tem_text = decoded_text
            yield_text = None
            for string in all_stopping_strings:
                if string in tem_text:
                    # extract tem_text from beginning to the string
                    new_yield_text = tem_text[:tem_text.find(string)]
                    # compare with yield_text, pick the shorter one
                    if yield_text is None or len(new_yield_text) < len(yield_text):
                        yield_text = new_yield_text
            if yield_text is not None:
                # yield the text before the stopping string, then end the generation
                yield yield_text
                break

            ends_with_substring = False
            for string in all_stopping_strings:
                # if tem_text endswith substring, don't yield anything yet
                for i in range(len(string)):
                    if tem_text.endswith(string[:i+1]):
                        ends_with_substring = True
                        break
            # none substring match, yield and clear the tem_text
            if not ends_with_substring:
                yield tem_text

            if token.item() == self.generator.tokenizer.eos_token_id or shared.stop_everything:
                break

    def generate(self, prompt, state, stopping_strings):
        output = ''
        for output in self.generate_with_streaming(prompt, state, stopping_strings):
            pass

        return output

    def encode(self, string, **kwargs):
        return self.tokenizer.encode(string)
