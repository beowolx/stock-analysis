# CrewAI Stock Analysis

An AI-powered stock analysis tool that leverages multiple AI agents to provide comprehensive market research, financial analysis, and SEC filing insights. The system uses specialized agents to analyze company financials, market trends, and regulatory filings to deliver detailed investment insights.

## Setup

1. Install `uv` package manager:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install [ollama](https://ollama.com/) and pull the model you want used for stock analysis (for example, `deepseek-r1:7b`):

```bash
ollama pull deepseek-r1:7b
```

3. Execute the following command to use the Modefile:

```bash
ollama create deepseek-r1:7b -f ./Modelfile 
```

4. Install dependencies:

```bash
uv sync
```

5. Configure environment:

```bash
cp .env.example .env
```

Then edit `.env` and add your API keys.

## Running

Start the project:

```bash
uv run main.py
```
