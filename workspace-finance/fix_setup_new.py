# Fix setup.py to add all new analysts

new_analysts = [
    'sector',
    'industry', 
    'peer',
    'valuation',
    'catalyst',
    'earnings',
    'insider',
    'regulatory',
]

with open('/app/tradingagents/graph/setup.py', 'r') as f:
    content = f.read()

# Add imports
if 'sector_analyst' not in content:
    old_import = 'from tradingagents.agents import *'
    new_import = '''from tradingagents.agents import *
from tradingagents.agents.analysts.sector_analyst import create_sector_analyst
from tradingagents.agents.analysts.industry_analyst import create_industry_analyst
from tradingagents.agents.analysts.peer_analyst import create_peer_analyst
from tradingagents.agents.analysts.valuation_analyst import create_valuation_analyst
from tradingagents.agents.analysts.catalyst_analyst import create_catalyst_analyst
from tradingagents.agents.analysts.earnings_analyst import create_earnings_analyst
from tradingagents.agents.analysts.insider_analyst import create_insider_analyst
from tradingagents.agents.analysts.regulatory_analyst import create_regulatory_analyst'''
    content = content.replace(old_import, new_import)

# Add node blocks for each new analyst
if '"sector"' not in content:
    insert_pos = '''        if "smart_money" in selected_analysts:
            analyst_nodes["smart_money"] = create_smart_money_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["smart_money"] = self.tool_nodes["smart_money"]
            done_nodes["smart_money"] = analyst_done_node

'''

    new_nodes = insert_pos
    for name in new_analysts:
        new_nodes += f'''
        if "{name}" in selected_analysts:
            analyst_nodes["{name}"] = create_{name}_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["{name}"] = self.tool_nodes["{name}"]
            done_nodes["{name}"] = analyst_done_node
'''

    content = content.replace(insert_pos, new_nodes)

with open('/app/tradingagents/graph/setup.py', 'w') as f:
    f.write(content)

print('Updated setup.py')
