from app import app
from waitress import serve

if __name__ == "__main__":
  serve(app,
        host=app.config['HOST'],
        port=app.config['PORT'],
        threads=app.config['THREADS'],
        channel_timeout=app.config['TIMEOUT'])
