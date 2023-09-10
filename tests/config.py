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
CODE_MODEL_TYPE =  'gpt-neox' # 'llama
CODE_TEMPERATURE = 0.11
CODE_MAX_NEW_TOKENS = 37
CODE_GPU_LAYERS = 0