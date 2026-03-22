# Fix __init__.py to import all new analysts

new_imports = '''
from .analysts.sector_analyst import create_sector_analyst
from .analysts.industry_analyst import create_industry_analyst
from .analysts.peer_analyst import create_peer_analyst
from .analysts.valuation_analyst import create_valuation_analyst
from .analysts.catalyst_analyst import create_catalyst_analyst
from .analysts.earnings_analyst import create_earnings_analyst
from .analysts.insider_analyst import create_insider_analyst
from .analysts.regulatory_analyst import create_regulatory_analyst'''

with open('/app/tradingagents/agents/__init__.py', 'r') as f:
    content = f.read()

# Check if already added
if 'sector_analyst' not in content:
    content = content.replace(
        'from .analysts.social_media_analyst import create_social_media_analyst',
        'from .analysts.social_media_analyst import create_social_media_analyst\n' + new_imports
    )
    
    with open('/app/tradingagents/agents/__init__.py', 'w') as f:
        f.write(content)
    print('Updated __init__.py')
else:
    print('Already updated')
