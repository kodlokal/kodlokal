# Kodlokal server

## Install

```bash
git clone git@github.com:kodlokal/kodlokal-gateway.git
cd kodlokal-gateway
python -m venv v
pip install -r requirements.txt
# download models
mkdir models && cd models
wget https://huggingface.co/TheBloke/stablecode-completion-alpha-3b-4k-GGML/resolve/main/stablecode-completion-alpha-3b-4k.ggmlv1.q5_1.bin
wget https://huggingface.co/TheBloke/WizardCoder-15B-1.0-GGML/resolve/main/WizardCoder-15B-1.0.ggmlv3.q5_1.bin
```

## Run

```
# run small model
KODLOKAL_SIZE=xs gunicorn --timeout 60 -w 1 -b localhost:3737 app:app

# run medium model
KODLOKAL_SIZE=m  gunicorn --timeout 60 -w 1 -b localhost:3737 app:app
```
