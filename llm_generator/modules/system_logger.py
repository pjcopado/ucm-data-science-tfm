import os
import logging


class Logger:
    def __init__(self, name: str = None):
        """
        Inicializa el logger.
        :param name: Nombre del logger. Si es None, usa el nombre del módulo (__name__).
        :param log_file: Archivo donde se guardarán los logs.
        """

        if name is None:
            name = __name__  # Usa el nombre del módulo donde se instancia el logger

        log_dir = "/llm_generator/output"
        log_file = os.path.join(log_dir, "app.log")

        # Ensure the log directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Open the log file
        with open(log_file, "w") as f:
            f.write("")  # Create or clear the log file

        self.name = name
        self.log_file = log_file

        self.logger = logging.getLogger(name)

        if not self.logger.hasHandlers():  # Evita agregar múltiples handlers
            self.logger.setLevel(logging.DEBUG)

            # Configurar handler para consola
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                "%(asctime)s - [%(levelname)s] [%(name)s] %(message)s"
            )
            console_handler.setFormatter(console_formatter)

            # Configurar handler para archivo
            file_handler = logging.FileHandler(log_file, mode="a")  # 'a' para append
            file_formatter = logging.Formatter(
                "%(asctime)s - [%(levelname)s] [%(name)s] %(message)s"
            )
            file_handler.setFormatter(file_formatter)

            # Agregar handlers al logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def __getattr__(self, attr):
        """Permite acceder directamente a los métodos del logger."""
        return getattr(self.logger, attr)
