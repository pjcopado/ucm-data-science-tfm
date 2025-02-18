from jinja2 import Template
from .prompt_loader import PromptLoader
from .system_logger import Logger

logger = Logger("Prompt Render")


class PromptTemplate:
    def __init__(self, model_name):
        self.template_path = f"/code/llm_generator/templates/{model_name}.jinja"
        with open(self.template_path, "r", encoding="utf-8") as f:
            template_str = f.read()
        self.jinja_template = Template(template_str)
        self.prompt_loader = PromptLoader(prompt_dir=f"/code/llm_generator/prompts/{model_name}")

    def generate_prompt(
        self,
        role,
        prompt_file,
        user_input=None,
        user_instructions=None,
        db_schema=None,
        similarity_list=None,
        error_list=None,
        initial_query=None,
        query_result=None,
        query_generated=None,
        bos_token="<|begin_of_text|>",
        add_generation_prompt=False
    ):
        logger.info("Loading prompt file...")
                
        format_params = {
            "user_input": str(user_input).strip(),
            "user_instructions": str(user_instructions).strip(),
            "db_schema": db_schema,
            "historic_query": "",
            "error_description": "",
            "initial_query": "",
            "query_result": str(query_result).strip(),
            "query_generated": str(query_generated).strip()
        }

        if similarity_list:
            historic_lines = [
                f"   • SIMILARITY {sim}: {item['user_input']} -> {item['query']}"
                for item, sim in similarity_list
            ]
            format_params["historic_query"] = "HISTORIC SIMILAR QUERY:\n" + "\n".join(historic_lines)

        if error_list:
            error_lines = [
                f"   • ERROR {i} -> {error}"
                for i, error in enumerate(error_list, start=1)
            ]
            format_params["error_description"] = "ERRORS:\n" + "\n".join(error_lines)
            format_params["initial_query"] = initial_query if initial_query else ""

        prompt_content = self.prompt_loader.load_prompt(prompt_file)
        prompt_formatted = Template(prompt_content).render(**format_params)
        logger.info(f"Prompt rendered: {prompt_formatted}")

        messages = [
            {
                "role": role,
                "content": prompt_formatted
            }
        ]

        prompt_render = self.jinja_template.render(
            messages=messages,
            bos_token=bos_token,
            add_generation_prompt=add_generation_prompt
        )

        return prompt_render



    def generate_prompt_combined(
        self,
        main_role,
        main_prompt_file,
        second_role,
        second_prompt_file,
        user_input,
        user_instructions,
        db_schema,
        error_list,
        initial_query,
        bos_token="<|begin_of_text|>",
        add_generation_prompt=False
    ):
        logger.info("Loading prompt file...")
        
        format_params = {
            "user_question": user_input.strip(),
            "user_instructions": user_instructions.strip(),
            "db_schema": db_schema,
            "error_description": "",
            "initial_query": ""
        }
        if error_list:
            error_lines = [
                f"   • ERROR {i} -> {error}"
                for i, error in enumerate(error_list, start=1)
            ]
            format_params["error_description"] = "ERRORS:\n" + "\n".join(error_lines)
            format_params["initial_query"] = initial_query if initial_query else ""

        main_prompt_content = self.prompt_loader.load_prompt(main_prompt_file)
        main_prompt_formatted = Template(main_prompt_content).render(**format_params)
        logger.info(f"Prompt rendered: {main_prompt_formatted}")
        messages = [
            {
                "role": main_role,
                "content": main_prompt_formatted
            }
        ]

        second_prompt_content = self.prompt_loader.load_prompt(second_prompt_file)
        second_prompt_formatted = Template(second_prompt_content).render(**format_params)
        logger.info(f"Prompt rendered: {second_prompt_formatted}")
        second_messages = [
            {
                "role": second_role,
                "content": second_prompt_formatted
            }
        ]

        # Combinar ambas listas de mensajes
        messages.extend(second_messages)

        prompt_render = self.jinja_template.render(
            messages=messages,
            bos_token=bos_token,
            add_generation_prompt=add_generation_prompt
        )

        return prompt_render
