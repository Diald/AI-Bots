import json
from pydantic import ValidationError 
from mcp.schema import MCPToolCall

class MCPProtocolError(Exception):
    pass

def parse_mcp_output(raw_output: str) ->MCPToolCall:
    '''Enforces strict MCP compliance. '''
    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        raise MCPProtocolError("LLM Output is not valid JSON")
    
    try:
        return MCPToolCall(**parsed)
    except ValidationError as e:
        raise MCPProtocolError(f"MCP Schema violation {e}")