from openai import OpenAI
from dotenv import load_dotenv #to load environment variables in your application
import os 
import subprocess

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


def read_file(file_path):
    '''reads code from a given file path'''
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found in the given path {file_path}"
    
# explainer 
#security reviewer - detects vulnerabilities 
# code improver - suggests fixes / optimize 

def explain_code(code, role="explainer"):
    try:
        role_prompts = {
            "explainer":"You are a senior software engineer. Explain in simple words what this code does and why it's written that way",
            "security":"You are a DevSecOps expert. Find and explain any potential security vulnerabilities or bad practices in this code",
            "improver":"You are a software reviewer. Suggest specific improvements to optimize or refactor this code for performance and readability."
        }
        system_prompt = role_prompts.get(role, role_prompts["explainer"])
        response = client.chat.completions.create(
            model="llama2:7b",
            messages=[
                {"role":"system", "content":system_prompt},
                {"role":"user", "content": code}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    print("-------Code review AI agent------")
    file_path = input("Enter the path of the code file to analyze: ")
    code = read_file(file_path)
    print("\n choose analysis type: ")
    print("1. explain code \n 2. security review\n 3. suggest improvements")
    choice = input("\n Enter your choice (1/2/3): ")
    roles = {1:"explainer", 2:"security", 3:"improver"}
    role = roles.get(choice, "explainer")
    print(f"\n running as {role.upper()}...")
    res = explain_code(code, role=role)
    print("Explaination....")
    print(res)
    
if __name__=="__main__":
    main()
    
