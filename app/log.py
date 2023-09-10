"""
The app logger
"""

import logging
from app.kodlokal_app import APP_NAME

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log = logging.getLogger(APP_NAME)
