"""
MCP Client with Azure OpenAI Integration

This client connects to an MCP server and uses Azure OpenAI for LLM capabilities.

Required environment variables:
- AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
- AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint URL
- AZURE_OPENAI_DEPLOYMENT_NAME: Your Azure OpenAI deployment name (optional, defaults to 'gpt-4o')
- AZURE_OPENAI_API_VERSION: API version to use (optional, defaults to '2024-02-01')

Example:
    export AZURE_OPENAI_API_KEY="your-api-key-here"
    export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
    export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o"
    export AZURE_OPENAI_API_VERSION="2024-02-01"
"""

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# llm
import os
from openai import AzureOpenAI
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="mcp",  # Executable
    args=["run", "server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

def call_llm(prompt, functions):
    # Azure OpenAI configuration
    # These should be set as environment variables
    azure_openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
    
    if not azure_openai_api_key or not azure_openai_endpoint:
        raise ValueError("Azure OpenAI API key and endpoint must be set as environment variables")

    client = AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint
    )

    print("CALLING LLM")
    response = client.chat.completions.create(
        model=azure_openai_deployment,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        tools=functions,
        temperature=1.0,
        max_tokens=1000,
        top_p=1.0
    )

    response_message = response.choices[0].message
    
    functions_to_call = []

    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            print("TOOL: ", tool_call)
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            functions_to_call.append({ "name": name, "args": args })

    return functions_to_call

def convert_to_llm_tool(tool):
    tool_schema = {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": tool.inputSchema["properties"]
            }
        }
    }

    return tool_schema

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()

            # List available resources
            resources = await session.list_resources()
            print("LISTING RESOURCES")
            for resource in resources:
                print("Resource: ", resource)

            # List available tools
            tools = await session.list_tools()
            print("LISTING TOOLS")

            functions = []

            for tool in tools.tools:
                print("Tool: ", tool.name)
                print("Tool", tool.inputSchema["properties"])
                functions.append(convert_to_llm_tool(tool))
            
            prompt = "Add 2 to 20"

            # ask LLM what tools to all, if any
            functions_to_call = call_llm(prompt, functions)

            # call suggested functions
            for f in functions_to_call:
                result = await session.call_tool(f["name"], arguments=f["args"])
                print("TOOLS result: ", result.content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())



