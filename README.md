# Kodlokal Server

AI Local Inference Server for the GPU Poor and GPU-less.

Used for the emacs package https://github.com/kodlokal/kodlokal.el

## Install

Install python requirements
```bash
git clone https://github.com/kodlokal/kodlokal.git
cd kodlokal
python -m venv v
source v/bin/activate
pip install -r requirements.txt
pip install ctransformers[cuda] # only if you have CUDA environment for an Nvidia GPU
```

Download some models and note their types. For huggingface models
check config.py.

```
mkdir models && cd models
wget https://huggingface.co/TheBloke/stablecode-completion-alpha-3b-4k-GGML/resolve/main/stablecode-completion-alpha-3b-4k.ggmlv1.q4_0.bin
wget https://huggingface.co/SlyEcho/open_llama_3b_v2_ggml/resolve/main/open-llama-3b-v2-q4_0.bin
```

Configure `config.py` by copying from `config.py.sample`


## Run

Run the model. Use Ctrl+C  or Command+C on Mac to stop it.

```
python run.py
```

## Configuration

Configure `config.py` and restart. If you want remove a model, comment out or remove all its config:

```
HOST = '127.0.0.1'
PORT = 3737
THREADS = 1
TIMEOUT=60
MODELS_FOLDER = './models/'
TEXT_MODEL = 'open-llama-3b-v2-q4_0.bin'
TEXT_MODEL_TYPE = 'llama'
TEXT_TEMPERATURE = 0.37
TEXT_MAX_NEW_TOKENS = 73
TEXT_GPU_LAYERS = 0
TEXT_CONTEXT_LENGTH = 2048
CODE_MODEL =  'stablecode-completion-alpha-3b-4k.ggmlv1.q4_0.bin'
CODE_MODEL_TYPE = 'gpt-neox'
CODE_TEMPERATURE = 0.20
CODE_MAX_NEW_TOKENS = 37
CODE_GPU_LAYERS = 0
CODE_CONTEXT_LENGTH = 2048
CHAT_MODEL = 'llama-2-7b-chat.ggmlv3.q4_0.bin'
CHAT_MODEL_TYPE = 'llama'
CHAT_TEMPERATURE = 0.37
CHAT_MAX_NEW_TOKENS = 73
CHAT_GPU_LAYERS = 0
CHAT_CONTEXT_LENGTH = 2048
```

### GPU layers

If you have a GPU which supports it, you may use the right value by
entering a value and checking your GPU memory usage using the
`nvidia-smi` command line tool.

```
nvidia-smi
```

## Development

Fork this repo and send a PR>


Run tests:

```
ENV=test python -m pytest
```

Run styler:

```
pycodestyle app tests
```

Run formatter

```
yapf -ir app tests
```

Linter

```
pylint app
```
