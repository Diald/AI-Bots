from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import re
from collections import Counter

app = FastAPI()


tools = {
    "summarize_text":{
        "description": "Summarize a block of text", 
        "input_schema":{
            "text": "string"
        }
    },
    "security_scan":{
        "description":"detect insecure coding patterns",
        "input_schema":{
            "code":"string"
        }
    }
}

@app.get("/tools")
def list_tools():
    return tools

class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]
#here it represents schema for a tool call made by an LLM
# where name is the name of tool being called and arguments is the i/p passed to that tool

def summarize_text(text: str, max_sentences: int = 3)-> str:
    '''Non LLM based summarizer'''
    sentences = re.split(r'(?<=[.!?])\s+', text)
    words = re.findall(r'\w+', text.lower())
    
    if not sentences or words:
        return ""
    word_freq = Counter(words)
    
    sentence_scores = {}
    for sentence in sentences:
        score = 0 
        for word in re.findall(r'/w+', sentence.lower()):
            score += word_freq[word]
        sentence_scores[sentence] = score
    top_sentences = sorted(
        sentence_scores, 
        key = sentence_scores.get, 
        reverse=True
    )[:max_sentences]
    return " ".join(top_sentences)


def security_scan(code: str)-> str:
    insecure = ["eval(", "exec(", "pickle.loads", "os.system"]
    findings = [p for p in insecure if p in code]
    if not findings:
        return "no obvious insecure coding patterns found..."
    return f"!!!Insecure coding patterns found!!! {' ,'.join(findings)}"


@app.post("/call")
def call_tool(payload: ToolCall):
    if payload.name not in tools:
        raise HTTPException(status_code = 400, detail="Unknown tool")
    if payload.name=="summarize_text":
        text = payload.arguments.get("text")
        if not text:
            raise HTTPException(status_code=400, detail="Text is not provided ?")
        return {
            "tool": payload.name,
            "result": summarize_text(text)
        }
    if payload.name=="security_scan":
        code = payload.arguments.get("code")
        if not code:
            raise HTTPException(status_code=400, detail="Code is not provided ?")
        return {
            "tool":payload.name,
            "result":security_scan(code)
        }
    raise HTTPException(status_code=500, detail="tool execution failed")
