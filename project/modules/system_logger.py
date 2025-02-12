import logging

class logger():
    
    def __init__(name):
        logger = logging.getLogger(name)
        if not logger.handlers:  # Evitar duplicación de handlers si ya está configurado
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

        return logger
