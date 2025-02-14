import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class InsightGenerator:
    def __init__(self, model_name="google/flan-t5-xl"):
        """
        Initializes the response generator with a model optimized for reasoning.
        With local model -> model_name="./models/flan-t5-xl"
        With Hugging Face model -> model_name="google/flan-t5-xl"
        """
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Loading model on {self.device}...")

            # Load the model and tokenizer once
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)

            print("Model loaded successfully.")

        except Exception as e:
            raise RuntimeError(f"Error loading the model: {str(e)}")

    def generate_response(self, user_question, sql_result):
        """
        Generates a human language response based on the user's question and the SQL result.

        Args:
            user_question (str): Original question from the user.
            sql_result (str | int | float): Result of the SQL query.

        Returns:
            str: Generated response in natural and explanatory language.
        """
        if not user_question.strip():
            return "No valid question received from the user."

        if not sql_result:
            return "No data found to answer the query."

        # 🔹 **New Improved Prompt for Reasoning**
        prompt = f"""
        Example 1:
        Question: "What were the sales in Germany in August 2021?"
        SQL Result: 1291206,76
        Expected Response: "In August 2021, the sales in Germany amounted to 1,291,206.76 euros."

        Example 2:
        Question: "What was the total revenue in the food category in December 2022?"
        SQL Result: 48,950
        Expected Response: "In December 2022, the total revenue in the food category was 48,950 dollars. This month is usually high in sales due to the demand for holiday products."

        Example 3:
        Question: "How many units were sold in the sports category in April 2022?"
        SQL Result: 12,000
        Expected Response: "In April 2022, the sports category sold 12,000 units, reflecting a high interest in sports equipment with the arrival of good weather."

        Now answer the following question similarly but not identically with your own reasoning, reasoning the context correctly:
        Question: "{user_question}"
        SQL Result: {sql_result}
        Expected Response:
        """

        try:
            # Tokenization
            inputs = self.tokenizer(
                prompt, return_tensors="pt", padding=True, truncation=True
            ).to(self.device)

            # 🔹 **Optimized Generation**
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=150,  # Allows longer responses
                do_sample=True,
                temperature=0.7,  # More control over variability
                top_p=0.9,
                num_return_sequences=1,
            )

            # Decoding the generated text
            response = self.tokenizer.decode(
                outputs[0], skip_special_tokens=True
            ).strip()

            return response if response else "Could not generate a valid response."

        except Exception as e:
            return f"Error generating the response: {str(e)}"
