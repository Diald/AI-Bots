import os
import json
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "models/gemini-2.5-flash"

MCP_URL = "http://localhost:3333"


class MCPAgent:

    def get_tools(self):
        resp = requests.get(f"{MCP_URL}/tools")
        resp.raise_for_status()
        return resp.json()

    def call_tool(self, name, arguments):
        payload = {
            "name": name,
            "arguments": arguments
        }
        resp = requests.post(f"{MCP_URL}/call", json=payload)
        resp.raise_for_status()
        return resp.json()

    def decide_tool(self, task, tools):
        prompt = f"""
You are an MCP-compatible agent.

Your job is to select ONE tool.

Task:
{task}

Available tools (JSON schema):
{json.dumps(tools, indent=2)}

Rules:
- Respond with ONLY raw JSON
- Do NOT add explanations
- Do NOT use markdown
- Do NOT add backticks

Valid response format:
{{
  "tool": "<tool_name>",
  "arguments": {{ ... }}
}}

If no tool applies, respond exactly:
{{ "tool": "none" }}
"""

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return json.loads(response.text)
    def run(self, task):
        tools = self.get_tools()
        decision = self.decide_tool(task, tools)

        if decision.get("tool") == "none":
            return {"message": "no suitable tool"}

        return self.call_tool(
            decision["tool"],
            decision.get("arguments", {})
        )


if __name__ == "__main__":
    agent = MCPAgent()
    print(agent.run("Check security of this code: eval(user_input)"))
