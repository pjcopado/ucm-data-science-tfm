import subprocess
import threading
import queue
import time

class LLMHandler:
    def __init__(
        self,
        model_name="mistral-7b-instruct-v0.2.Q4_K_M",
        system_prompt="",
        n_ctx=4096,
        n_gpu_layers=16,
        temperature=0.7,
        top_p=0.9
    ):
        self.model_path = f"./models/gguf/{model_name}.gguf"

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
            "--repeat_penalty", "1.1",
            "--keep", "-1",
            "-p", str(system_prompt),
            "--in-suffix", "<|start_header_id|>assistant<|end_header_id|>\n\n",
            "-sp"
        ]

        print("[LLMHandler] Starting model:", " ".join(cmd))

        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        self.stdout_queue = queue.Queue()

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
                    print("[WARN][LLMHandler] Timeout waiting for 'user' turn.")
                    break
                continue

            print("[LLMHandler][llama.cpp >]", line, end="")

            if line.strip() == "== Running in interactive mode. ==":
                break

            if "error:" in line:
                print("[ERROR][LLMHandler] Error:", line)
                break

        time.sleep(5)

    def generate(self, prompt) -> str:
        if self.process.poll() is not None:
            raise RuntimeError("[LLMHandler] llama.cpp process failed.")

        print("[LLMHandler] Sending prompt: ", prompt)

        send_prompt = prompt + "\n\\\n"
        self.process.stdin.write(send_prompt)
        self.process.stdin.flush()

        output = self._consume_until_reverse_prompt(timeout=120)

        return output.strip()

    def _consume_until_reverse_prompt(self, timeout=900):
        t0 = time.time()
        captured = []
        capturing = False
        while True:
            try:
                line = self.stdout_queue.get(timeout=1)
            except queue.Empty:
                if (time.time() - t0) > timeout:
                    print("[WARN][LLMHandler] Timeout waiting for 'user' turn.")
                    break
                continue

            if line.strip() == "<|start_header_id|>assistant<|end_header_id|>":
                capturing = True
                continue

            if capturing and "<|eot_id|>" in line:
                break

            if capturing:
                captured.append(line)

            if "error:" in line:
                print("[ERROR][LLMHandler] Error:", line)
                break

        return "".join(captured).replace("<|eot_id|>", "").strip()

    def close(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            print("[LLMHandler] llama.cpp process finished")
