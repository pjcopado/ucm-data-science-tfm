from huggingface_hub import snapshot_download # noqa
from transformers import AutoTokenizer, AutoModelForCausalLM


model_dir = "../models/llama-3-sqlcoder-8b"
# model_dir = "../models/nsql-llama-2-7B-GGUF"

# Download the model from Hugging Face
snapshot_download(repo_id="defog/llama-3-sqlcoder-8b", local_dir=model_dir)
# snapshot_download(repo_id="TheBloke/nsql-llama-2-7B-GGUF", local_dir=model_dir)

# Load the model and tokenizer from the local directory
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForCausalLM.from_pretrained(model_dir)
