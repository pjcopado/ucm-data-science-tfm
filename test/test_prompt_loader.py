import os
import sys
import pytest

# Set the root directory to import own modules
root_dir = os.path.dirname(os.getcwd())
sys.path.append(root_dir)

from project.modules.prompt_loader import PromptLoader  # noqa: E402


@pytest.fixture
def prompt_loader(tmp_path):
    # Create a temporary directory for prompts
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    return PromptLoader(prompt_dir=str(prompt_dir))


def test_load_prompt_success(prompt_loader, tmp_path):
    # Create a sample prompt file
    prompt_file = tmp_path / "prompts" / "sample_prompt.txt"
    prompt_content = """
    <|begin_of_text|><|start_header_id|>user<|end_header_id|>
    Generate a SQL query to answer this question: `{user_question}`
    {instructions}
    DDL statements:
    {database_schema}
    Initial query:
    {initial_query}
    Error encountered:
    {error_description}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    The initial query contained error(s).
    Please correct the SQL query and answer the question `{user_question}`:
    ```sql
    """
    with open(prompt_file, 'w') as f:
        f.write(prompt_content)

    # Load the prompt using PromptLoader
    loaded_content = prompt_loader.load_prompt("sample_prompt.txt")
    assert loaded_content == prompt_content


def test_load_prompt_file_not_found(prompt_loader):
    with pytest.raises(FileNotFoundError):
        prompt_loader.load_prompt("non_existent_prompt.txt")


def test_list_prompts(prompt_loader, tmp_path):
    # Create sample prompt files
    prompt_files = ["prompt1.txt", "prompt2.txt", "not_a_prompt.md"]
    for file_name in prompt_files:
        with open(tmp_path / "prompts" / file_name, 'w') as f:
            f.write("content")

    # List prompts using PromptLoader
    prompts = prompt_loader.list_prompts()
    assert "prompt1.txt" in prompts
    assert "prompt2.txt" in prompts
    assert "not_a_prompt.md" not in prompts


def test_list_prompts_directory_not_found():
    prompt_loader = PromptLoader(prompt_dir="./non_existent_dir")
    with pytest.raises(FileNotFoundError):
        prompt_loader.list_prompts()
