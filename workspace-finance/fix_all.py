# Create analyst files and update __init__.py

import os
import shutil

# List of analysts to create
analysts = ['sector', 'industry', 'peer', 'valuation', 'catalyst', 'earnings', 'insider', 'regulatory']

base = '/app/tradingagents/agents/analysts/'
template = os.path.join(base, 'social_media_analyst.py')

for name in analysts:
    target = os.path.join(base, f'{name}_analyst.py')
    if not os.path.exists(target):
        shutil.copy(template, target)
        with open(target, 'r') as f:
            content = f.read()
        content = content.replace('social_media_analyst', f'{name}_analyst')
        content = content.replace('create_social_media_analyst', f'create_{name}_analyst')
        content = content.replace('Social Media Analyst', f'{name.title()} Analyst')
        with open(target, 'w') as f:
            f.write(content)
        print(f'Created {name}')

# Update __init__.py
init_file = '/app/tradingagents/agents/__init__.py'
with open(init_file, 'r') as f:
    content = f.read()

new_imports = '''
from .analysts.sector_analyst import create_sector_analyst
from .analysts.industry_analyst import create_industry_analyst
from .analysts.peer_analyst import create_peer_analyst
from .analysts.valuation_analyst import create_valuation_analyst
from .analysts.catalyst_analyst import create_catalyst_analyst
from .analysts.earnings_analyst import create_earnings_analyst
from .analysts.insider_analyst import create_insider_analyst
from .analysts.regulatory_analyst import create_regulatory_analyst'''

if 'sector_analyst' not in content:
    content = content.replace('from .analysts.social_media_analyst import create_social_media_analyst',
                               'from .analysts.social_media_analyst import create_social_media_analyst' + new_imports)

with open(init_file, 'w') as f:
    f.write(content)

print('Updated __init__.py')
print('Done!')
