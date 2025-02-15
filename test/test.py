def test_query_generation(model, tokenizer, questions_with_expected_queries):
    results = []
    for question, expected_query in questions_with_expected_queries:
        prompt = f"Pregunta: {question}\nQuery SQL:"
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=200)
        generated_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
        results.append((question, generated_query, generated_query == expected_query))
    return results
