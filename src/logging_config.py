import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler("app.log", mode = 'w'),
        logging.StreamHandler()
    ]
)
