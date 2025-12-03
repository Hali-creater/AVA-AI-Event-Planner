import os

def read_prompt(file_path):
    """Reads the prompt from a file."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Prompt file not found."

def get_llm_response(prompt, user_input):
    """
    This is a placeholder for the actual interaction with an LLM.
    In a real implementation, this function would send the prompt and user input
    to an LLM API and return the response.
    """
    # Placeholder response for demonstration purposes
    return f"LLM Response based on '{user_input}'"

def main():
    """
    Main function to run the agent.
    """
    prompt_file = "prompt.md"
    prompt = read_prompt(prompt_file)

    if "not found" in prompt:
        print(prompt)
        return

    print("Agent is running. Type 'exit' to quit.")

    # Initialize conversation history with the system prompt
    conversation_history = [
        {"role": "system", "content": prompt}
    ]

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # Add user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # In a real implementation, you'd pass the conversation history to the LLM
        # For now, we'll just use the latest user input and the initial prompt

        # Get response from the placeholder LLM function
        llm_response = get_llm_response(prompt, user_input)

        # Add LLM response to conversation history
        conversation_history.append({"role": "assistant", "content": llm_response})

        print(f"Ava: {llm_response}")

if __name__ == "__main__":
    main()
