# Kodlokal Server

## Install

```bash
git clone git@github.com:kodlokal/kodlokal-gateway.git
cd kodlokal-gateway
python -m venv v
pip install -r requirements.txt
# download some models and note their types (in config.py in huggingface)
mkdir models && cd models
wget https://huggingface.co/TheBloke/stablecode-completion-alpha-3b-4k-GGML/resolve/main/stablecode-completion-alpha-3b-4k.ggmlv1.q5_1.bin
```

Configure `config.py` by copying from `config.py.sample`


## Run

```
# run small model
gunicorn --timeout 60 -w 1 -b localhost:3737 app:app

# run medium model
gunicorn --timeout 60 -w 1 -b localhost:3737 app:app
```
