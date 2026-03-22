import os
import shutil

# List of new analysts to create
new_analysts = [
    'sector',       # 板块分析
    'industry',     # 行业分析
    'peer',         # 竞品分析
    'valuation',    # 估值分析
    'catalyst',     # 催化剂分析
    'earnings',     # 盈利分析
    'insider',      # 内幕消息
    'regulatory',   # 监管分析
]

base_path = '/app/tradingagents/agents/analysts/'
template_path = os.path.join(base_path, 'social_media_analyst.py')

# Copy template for each new analyst
for name in new_analysts:
    target_path = os.path.join(base_path, f'{name}_analyst.py')
    
    # Copy file
    shutil.copy(template_path, target_path)
    
    # Read and modify
    with open(target_path, 'r') as f:
        content = f.read()
    
    # Replace strings
    content = content.replace('social_media_analyst_node', f'{name}_analyst_node')
    content = content.replace('create_social_media_analyst', f'create_{name}_analyst')
    content = content.replace('Social Analyst', f'{name.title()} Analyst')
    content = content.replace('social_media_analyst', f'{name}_analyst')
    
    with open(target_path, 'w') as f:
        f.write(content)
    
    print(f'Created {name}_analyst.py')

print('Done!')
