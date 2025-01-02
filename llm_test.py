import torch
from transformers import pipeline
import argparse

def generate_car_keywords(description):
    """
    Generate car keywords in the format 'car_model-year' based on the provided description.

    Args:
        description (str): The description of the car.

    Returns:
        str: The generated keywords.
    """
    # Initialize the text generation pipeline
    model_id = "/home/ncdbproj/NCDBContent/TextToArt/llama-3.2-1B-Instruct"
    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.float16
    )

    # Prepare the messages
    messages = [
        {"role": "system", "content": "Answer with the simplest words possible."},
        {"role": "user", "content": f"extract key words about the car wanted from the description in the format of 'car_model-year' without any additional words. Description: {description}"},
    ]


    # Generate outputs
    outputs = pipe(
        messages,
        max_new_tokens=32,
    )

    # Return the generated text
    output = outputs[0]["generated_text"]
    # Extract 'content' from the assistant's response
    for message in output:
        if message.get("role") == "assistant":
            output = message.get("content", "")
            return output

    return ""  # Return an empty string if no assistant response is found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate car keywords from a description.")
    parser.add_argument("--description", type=str, required=True, help="The description of the car.")
    args = parser.parse_args()

    result = generate_car_keywords(args.description)
    print(result)