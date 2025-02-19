import subprocess
import threading
import queue
import time
from .system_logger import Logger

logger = Logger("LLM Handler")


class LLMHandler:
    def __init__(
        self,
        model_name,
        system_prompt,
        n_ctx=4096,
        n_gpu_layers=50,
        temperature=0,
        top_p=0.95,
        prompt_cache="./data/prompt_cahe.bin"
    ):
        
        self.model_path = f"llm_generator/models/gguf/{model_name}.gguf"
            
        cmd = [
            "llama-cli",
            "--model", str(self.model_path),
            "--n_gpu_layers", str(n_gpu_layers),
            "--flash-attn",
            "--interactive",
            "--interactive-first",
            "--multiline-input",
            "--ctx-size", str(n_ctx),
            "--temp", str(temperature),
            "--top_p", str(top_p),
            "-no-cnv",
            "--keep", "-1",
            "-sp",
            "--in-suffix", "<|start_header_id|>assistant<|end_header_id|>\n\n",
            "-p", str(system_prompt)
        ]

        logger.info(f"Starting model: {" ".join(cmd)}")

        # Arrancamos llama.cpp como un subproceso con pipes para stdin y stdout
        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        # Cola para almacenar líneas de la salida
        self.stdout_queue = queue.Queue()

        # Hilo lector que va recogiendo las líneas de stdout
        def _reader_thread():
            for line in self.process.stdout:
                self.stdout_queue.put(line)

        self.reader = threading.Thread(target=_reader_thread, daemon=True)
        self.reader.start()

        self._consume_until_model_ready(timeout=900)


    def _consume_until_model_ready(self, timeout=900):
        t0 = time.time()
        while True:
            try:
                line = self.stdout_queue.get(timeout=1)
            except queue.Empty:
                if (time.time() - t0) > timeout:
                    logger.warn("[llama.cpp >] Timeout waiting for 'user' turn.")
                    break
                continue

            if "error:" in line.lower():
                logger.error(f"[llama.cpp >] {line}")
                raise RuntimeError(line)

            logger.debug(f"[llama.cpp >] {line.strip()}")

            if line.strip() == "== Running in interactive mode. ==":
                break

        time.sleep(15)



    def _consume_until_reverse_prompt(self, timeout=900):
        t0 = time.time()
        captured = []
        capturing = False
        while True:
            try:
                line = self.stdout_queue.get(timeout=1)
            except queue.Empty:
                if (time.time() - t0) > timeout:
                    logger.warn("[llama.cpp >] Timeout waiting for 'user' turn.")
                    break
                continue

            if "error:" in line:
                logger.error(f"[llama.cpp >] Error: {line}")
                raise RuntimeError(line)

            logger.debug(f"[llama.cpp >] {line.strip()}")

            if line.strip() == "<|start_header_id|>assistant<|end_header_id|>":
                capturing = True 
                continue

            if capturing:
                captured.append(line)

            if capturing and "<|eot_id|>" in line:
                break

        return "".join(captured).replace("<|eot_id|>", "").strip()



    def generate(
        self,
        prompt
    ) -> str:

        prompt = str(prompt)

        if self.process.poll() is not None:
            logger.error("llama.cpp process failed.")
            raise RuntimeError("[LLM Handler] llama.cpp process failed.")

        logger.info(f"Sending prompt: {prompt}")

        # Mandamos el prompt al stdin
        send_prompt = prompt + "\n\\\n"
        self.process.stdin.write(send_prompt)
        self.process.stdin.flush()

        output = self._consume_until_reverse_prompt(timeout=120)

        # Opcional: podrías limpiar la repetición del prompt o hacer un parse más avanzado
        return output



    def close(self):
        """
        Cierra el proceso llama.cpp si sigue activo.
        """
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            logger.info("llama.cpp process finished")
