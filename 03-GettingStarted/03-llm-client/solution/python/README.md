# Running this sample

This sample demonstrates an MCP client that integrates with Azure OpenAI for LLM capabilities.

You're recommended to install `uv` but it's not a must, see [instructions](https://docs.astral.sh/uv/#highlights)

## Prerequisites

Before running this sample, you need to set up Azure OpenAI and configure the required environment variables.

### Environment Variables

Create a `.env` file in this directory or set the following environment variables:

```bash
export AZURE_OPENAI_API_KEY="your-api-key-here"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o"  # Optional, defaults to 'gpt-4o'
export AZURE_OPENAI_API_VERSION="2024-02-01"  # Optional, defaults to '2024-02-01'
```

## -0- Create a virtual environment

```bash
python -m venv venv
```

## -1- Activate the virtual environment

```bash
venv\Scripts\activate
```

## -2- Install the dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install "mcp[cli]"
pip install openai
pip install python-dotenv
```

## -3- Run the sample


```bash
python client.py
```

You should see an output similar to:

```text
LISTING RESOURCES
Resource:  ('meta', None)
Resource:  ('nextCursor', None)
Resource:  ('resources', [])
                    INFO     Processing request of type ListToolsRequest                                                                               server.py:534
LISTING TOOLS
Tool:  add
Tool {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}
CALLING LLM
TOOL:  {'function': {'arguments': '{"a":2,"b":20}', 'name': 'add'}, 'id': 'call_BCbyoCcMgq0jDwR8AuAF9QY3', 'type': 'function'}
[05/08/25 21:04:55] INFO     Processing request of type CallToolRequest                                                                                server.py:534
TOOLS result:  [TextContent(type='text', text='22', annotations=None)]
```
