import os

class PromptLoader:
    def __init__(self, prompt_dir="./prompts"):
        """
        Inicializa el cargador de prompts.
        Args:
            prompt_dir (str): Ruta a la carpeta donde se encuentran los prompts.
        """
        self.prompt_dir = prompt_dir

    def load_prompt(self, file_name):
        """
        Carga el contenido de un archivo de prompt.
        Args:
            file_name (str): Nombre del archivo del prompt.

        Returns:
            str: Contenido del prompt.
        """
        file_path = os.path.join(self.prompt_dir, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_name} no existe en {self.prompt_dir}.")
        
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def list_prompts(self):
        """
        Lista todos los prompts disponibles en el directorio.

        Returns:
            list: Lista de nombres de archivos de prompts.
        """
        if not os.path.exists(self.prompt_dir):
            raise FileNotFoundError(f"La carpeta {self.prompt_dir} no existe.")
        
        return [f for f in os.listdir(self.prompt_dir) if f.endswith(".txt")]
