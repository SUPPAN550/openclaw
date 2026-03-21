#!/usr/bin/env python
"""Fix propagation.py to remove stream_mode from get_graph_args"""
import subprocess

# First, read the current content
result = subprocess.run(
    ["docker", "exec", "tradingagents", "cat", "/app/tradingagents/graph/propagation.py"],
    capture_output=True,
    text=True
)
content = result.stdout

# Replace the old code
old_code = '''    def get_graph_args(self, callbacks: Optional[List] = None) -> Dict[str, Any]:
        """Get arguments for the graph invocation.

        Args:
            callbacks: Optional list of callback handlers for tool execution tracking.
                       Note: LLM callbacks are handled separately via LLM constructor.
        """
        config = {"recursion_limit": self.max_recur_limit}
        if callbacks:
            config["callbacks"] = callbacks
        return {
            "stream_mode": "values",
            "config": config,
        }'''

new_code = '''    def get_graph_args(self, callbacks: Optional[List] = None) -> Dict[str, Any]:
        """Get arguments for the graph invocation.

        Args:
            callbacks: Optional list of callback handlers for tool execution tracking.
                       Note: LLM callbacks are handled separately via LLM constructor.
        """
        config = {"recursion_limit": self.max_recur_limit}
        if callbacks:
            config["callbacks"] = callbacks
        # Note: stream_mode is not needed for invoke (only for astream)
        # LangGraph 1.0 doesn't support stream_mode in invoke
        return {
            "config": config,
        }'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("Found and replaced the old code")
else:
    print("Could not find the old code to replace")
    print("Content sample:")
    print(content[-500:])
    exit(1)

# Write back to the container
import base64
encoded = base64.b64encode(content.encode()).decode()
subprocess.run(
    ["docker", "exec", "tradingagents", "bash", "-c", f"echo '{encoded}' | base64 -d > /app/tradingagents/graph/propagation.py"],
    check=True
)
print("Successfully updated propagation.py")
