# Fix trading_graph.py properly

with open('/app/tradingagents/graph/trading_graph.py', 'r') as f:
    lines = f.readlines()

# Find and fix the section around smart_money
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Look for the closing of smart_money tool node
    if '"smart_money": ToolNode(' in line:
        # Copy until we find the closing of this section
        new_lines.append(line)
        i += 1
        brace_count = 0
        while i < len(lines):
            l = lines[i]
            new_lines.append(l)
            brace_count += l.count('[') - l.count(']')
            brace_count += l.count('{') - l.count('}')
            i += 1
            if brace_count == 0 and ']' in lines[i-1]:
                break
        # Now add the new tool nodes with proper indentation
        new_lines.append('            },  # end smart_money\n')
        new_lines.append('\n')
        new_lines.append('            "sector": ToolNode([\n')
        new_lines.append('                get_news,\n')
        new_lines.append('            ]),\n')
        new_lines.append('            "industry": ToolNode([\n')
        new_lines.append('                get_news,\n')
        new_lines.append('            ]),\n')
        new_lines.append('            "peer": ToolNode([\n')
        new_lines.append('                get_news,\n')
        new_lines.append('            ]),\n')
        new_lines.append('            "valuation": ToolNode([\n')
        new_lines.append('                get_news,\n')
        new_lines.append('            ]),\n')
        new_lines.append('            "catalyst": ToolNode([\n')
        new_lines.append('                get_news,\n')
        new_lines.append('            ]),\n')
        new_lines.append('            "earnings": ToolNode([\n')
        new_lines.append('                get_news,\n')
        new_lines.append('            ]),\n')
        new_lines.append('            "insider": ToolNode([\n')
        new_lines.append('                get_news,\n')
        new_lines.append('            ]),\n')
        new_lines.append('            "regulatory": ToolNode([\n')
        new_lines.append('                get_news,\n')
        new_lines.append('            ]),\n')
    else:
        new_lines.append(line)
        i += 1

with open('/app/tradingagents/graph/trading_graph.py', 'w') as f:
    f.writelines(new_lines)

print('Fixed trading_graph.py')
