from llama_cpp import Llama
from backend.github_rest import create_repo, create_or_update_file
from dotenv import load_dotenv
import json
import re

load_dotenv()

MODEL_PATH = "models/model.gguf"
llm = Llama(model_path=MODEL_PATH, n_threads=4)

print("\n GitHub Agent Ready! (type 'exit' to quit)\n")

def get_structured_command(user_input):
    """Ask LLM to return structured json command"""
    prompt = f"""
You are a GitHub automation agent.
The user will ask things like:
- create a repo called ai-test
- make a project named demo and add a README
- create repo "projectx" and add file index.js with console.log('hi')

Your job: Output ONLY JSON with fields:
{{
 "intent": "create_repo" OR "add_file" OR "chat",
 "repo": "<repo_name or empty>",
 "path": "<file path if any>",
 "content": "<file content if any>"
}}

User input: "{user_input}"
Respond ONLY with JSON, nothing else.
"""

    res = llm.create_chat_completion(
        messages=[{"role": "system","content":"You format commands"},
                  {"role":"user","content":prompt}],
        max_tokens=200,
        temperature=0.2)
    
    text = res["choices"][0]["message"]["content"]

    # clean up accidental markdown code fencing
    text = re.sub(r'```json|```', '', text).strip()

    try:
        return json.loads(text)
    except:
        return {"intent":"chat","repo":"","path":"","content":""}

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    command = get_structured_command(user_input)


    if command["intent"] == "create_repo" and command["repo"]:
        resp = create_repo(command["repo"], "Repo created by AI agent", private=True)
        print("Repo created:", resp.get("html_url", resp))
        continue

    if command["intent"] == "add_file" and command["repo"] and command["path"]:
        resp = create_or_update_file(command["repo"], command["path"], command["content"])
        print("File added/updated:", resp)
        continue

    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
        max_tokens=200,
        temperature=0.7,
    )

    print("Assistant:", response["choices"][0]["message"]["content"])
