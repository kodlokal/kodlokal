# Kodlokal Server

## Install

Install python requirements
```bash
git clone git@github.com:kodlokal/ziroton.git
cd ziroton
python -m venv v
pip install -r requirements.txt
pip install ctransformers[cuda] # only if you have CUDA environment for an Nvidia GPU
```

Download some models and note their types. For huggingface models
check config.py.

```
mkdir models && cd models
wget https://huggingface.co/TheBloke/stablecode-completion-alpha-3b-4k-GGML/resolve/main/stablecode-completion-alpha-3b-4k.ggmlv1.q5_1.bin
```

Configure `config.py` by copying from `config.py.sample`


## Run

Run the model. Use Ctrl+C  or Command+C on Mac to stop it.

```
python app.py
```

## Configuration

Configure `config.py` and restart

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
CODE_MODEL =  'stablecode-completion-alpha-3b-4k.ggmlv1.q4_0.bin'
CODE_MODEL_TYPE = 'gpt-neox'
CODE_TEMPERATURE = 0.20
CODE_MAX_NEW_TOKENS = 37
CODE_GPU_LAYERS = 0
```

### GPU layers

If you have a GPU which supports it, you may use the right value by
entering a value and checking your GPU memory usage using the
`nvidia-smi` command line tool.

```
nvidia-smi
```
