import logging

class Logger:
    def __init__(self, name=None, log_file='./output/app.log'):
        """
        Inicializa el logger.
        :param name: Nombre del logger. Si es None, usa el nombre del módulo (__name__).
        :param log_file: Archivo donde se guardarán los logs.
        """
        if name is None:
            name = __name__  # Usa el nombre del módulo donde se instancia el logger

        self.logger = logging.getLogger(name)

        if not self.logger.hasHandlers():  # Evita agregar múltiples handlers
            self.logger.setLevel(logging.DEBUG)

            # Configurar handler para consola
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] [%(name)s] %(message)s')
            console_handler.setFormatter(console_formatter)

            # Configurar handler para archivo
            file_handler = logging.FileHandler(log_file, mode='a')  # 'a' para append
            file_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] [%(name)s] %(message)s')
            file_handler.setFormatter(file_formatter)

            # Agregar handlers al logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def __getattr__(self, attr):
        """Permite acceder directamente a los métodos del logger."""
        return getattr(self.logger, attr)
