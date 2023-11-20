from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI
import sys
from datetime import datetime

# Set the OpenAI API key
client = OpenAI()
models = {"3": "gpt-3.5-turbo-1106", "4": "gpt-4-1106-preview"}
model_to_use = "gpt-4-1106-preview"
session_id = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + model_to_use
console = Console()

messages = []

def set_system_message():
    # Create the system message
    message_text = f"You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture."
    messages.append({"role": "system", "content": message_text})

def get_response(user_message_text):
    if user_message_text:
        messages.append({"role": "user", "content": user_message_text})
    
    # Get the response from the model
    completion = client.chat.completions.create(
        messages=messages,
        model=model_to_use
    )
    response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response})
    # Return the response
    return response

if __name__ == "__main__":
    while(True):
        option = input("Model? (3 or 4): ")
        if option == "3" or option == "4":
            model_to_use = models[option]
            break
        else:
            sys.exit("Invalid option. Exiting.")

    set_system_message()
    print(f"Conversation started with {model_to_use}. Type 'retry' to get a different response to your last message, 'reset' to start a new convo with the current model, 'reset 3' , 'exit' to quit.")
    print("")
    #print(f"Total tokens used in initial prompt: {total_tokens}")
    while(True):
        user_input = input("User: ")
        if user_input == "exit":
            break
        elif user_input == "retry":
            # Can't be picked as the first message:
            if len(messages) == 1:
                print("Can't retry the first message.")
                continue
            # We take away the last message from the messages list, and then try again:
            messages.pop()
            response = get_response()
            md = Markdown(response)
            print(f"GPT:")
            console.print(md)
        elif user_input.startswith("reset"):
            # If there are more than 5 characters, grab the number that comes after 'reset':
            if len(user_input) > 5:
                parts = user_input.split(" ")
                model = parts[1]
                if model == "3" or model == "4":
                    model_to_use = models[model]
                else:
                    sys.exit("Invalid option. Exiting.")
            messages = []
            set_system_message()
            print(f"Conversation restarted with {model_to_use}.")
            print("")
        else:
            response = get_response(user_input)
            md = Markdown(response)
            print(f"GPT:")
            console.print(md)