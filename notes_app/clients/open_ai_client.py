import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get("open_ai_api")


messages = []
system_msg = input("What type of chatbot would you like to create? \n Be as descriptive as possible: ")
messages.append({"role": "system", "content": system_msg})

print("Say hello to your new assistant!")
while input != "quit()":
    message = input()
    messages.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    print("\n" + reply + "\n")