# Fix setup.py to add all new analysts imports and nodes

with open('/app/tradingagents/graph/setup.py', 'r') as f:
    content = f.read()

# Add imports
if 'from tradingagents.agents.analysts.sector_analyst' not in content:
    content = content.replace(
        'from tradingagents.agents import *',
        '''from tradingagents.agents import *
from tradingagents.agents.analysts.sector_analyst import create_sector_analyst
from tradingagents.agents.analysts.industry_analyst import create_industry_analyst
from tradingagents.agents.analysts.peer_analyst import create_peer_analyst
from tradingagents.agents.analysts.valuation_analyst import create_valuation_analyst
from tradingagents.agents.analysts.catalyst_analyst import create_catalyst_analyst
from tradingagents.agents.analysts.earnings_analyst import create_earnings_analyst
from tradingagents.agents.analysts.insider_analyst import create_insider_analyst
from tradingagents.agents.analysts.regulatory_analyst import create_regulatory_analyst'''
    )

# Add node blocks
new_nodes = '''
        if "sector" in selected_analysts:
            analyst_nodes["sector"] = create_sector_analyst(self.quick_thinking_llm, self.data_collector)
            tool_nodes["sector"] = self.tool_nodes["sector"]
            done_nodes["sector"] = analyst_done_node

        if "industry" in selected_analysts:
            analyst_nodes["industry"] = create_industry_analyst(self.quick_thinking_llm, self.data_collector)
            tool_nodes["industry"] = self.tool_nodes["industry"]
            done_nodes["industry"] = analyst_done_node

        if "peer" in selected_analysts:
            analyst_nodes["peer"] = create_peer_analyst(self.quick_thinking_llm, self.data_collector)
            tool_nodes["peer"] = self.tool_nodes["peer"]
            done_nodes["peer"] = analyst_done_node

        if "valuation" in selected_analysts:
            analyst_nodes["valuation"] = create_valuation_analyst(self.quick_thinking_llm, self.data_collector)
            tool_nodes["valuation"] = self.tool_nodes["valuation"]
            done_nodes["valuation"] = analyst_done_node

        if "catalyst" in selected_analysts:
            analyst_nodes["catalyst"] = create_catalyst_analyst(self.quick_thinking_llm, self.data_collector)
            tool_nodes["catalyst"] = self.tool_nodes["catalyst"]
            done_nodes["catalyst"] = analyst_done_node

        if "earnings" in selected_analysts:
            analyst_nodes["earnings"] = create_earnings_analyst(self.quick_thinking_llm, self.data_collector)
            tool_nodes["earnings"] = self.tool_nodes["earnings"]
            done_nodes["earnings"] = analyst_done_node

        if "insider" in selected_analysts:
            analyst_nodes["insider"] = create_insider_analyst(self.quick_thinking_llm, self.data_collector)
            tool_nodes["insider"] = self.tool_nodes["insider"]
            done_nodes["insider"] = analyst_done_node

        if "regulatory" in selected_analysts:
            analyst_nodes["regulatory"] = create_regulatory_analyst(self.quick_thinking_llm, self.data_collector)
            tool_nodes["regulatory"] = self.tool_nodes["regulatory"]
            done_nodes["regulatory"] = analyst_done_node
'''

if '"sector"' not in content:
    content = content.replace(
        '        if "smart_money" in selected_analysts:\n            analyst_nodes["smart_money"] = create_smart_money_analyst(',
        new_nodes + '\n        if "smart_money" in selected_analysts:\n            analyst_nodes["smart_money"] = create_smart_money_analyst('
    )

with open('/app/tradingagents/graph/setup.py', 'w') as f:
    f.write(content)

print('Fixed setup.py')
