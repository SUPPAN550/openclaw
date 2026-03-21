#!/usr/bin/env python
import subprocess
import sys

# Run a simple test inside the container
cmd = [
    "docker", "exec", "tradingagents", "/bin/sh", "-c",
    "cd /app && /app/.venv/bin/python -c '"
    "from langgraph.graph import StateGraph; "
    "from tradingagents.agents.utils.agent_states import AgentState; "
    "sg = StateGraph(AgentState); "
    "compiled = sg.compile(); "
    "import inspect; "
    "print(inspect.signature(compiled.invoke))"
    "'"
]

result = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
