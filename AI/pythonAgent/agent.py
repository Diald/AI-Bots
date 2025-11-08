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
    
def explain_code(code):
    try:
        prompt = f"You are a senior software engineer. Analyze and explain the following code. Code: {code}"
        response = client.chat.completions.create(
            model="llama2:7b",
            messages=[
                {"role":"system", "content":"You are a helpful code analysis assistant."},
                {"role":"user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    file_path = input("Enter the path of the code file to analyze: ")
    code = read_file(file_path)
    print("Analyzing code....")
    res = explain_code(code)
    print("Explaination....")
    print(res)
    
if __name__=="__main__":
    main()
    
