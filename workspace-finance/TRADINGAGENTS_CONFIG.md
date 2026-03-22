# TradingAgents Local API Configuration
# 
# These are the working configuration values for the local TradingAgents API

TRADINGAGENTS_API_URL=http://localhost:8000
TRADINGAGENTS_TOKEN=ta-sk-xdowGc70-xMFt5GfQYZJFnPN313JzOImEaHOgbgAfTfB7-FuWDFdv24FgWOkCg-0gurQqHIvjxVdinbtdbPZKg

# Note: The local API requires authentication via:
# 1. JWT access token (obtained via email verification code)
# 2. Persistent API tokens (created via POST /v1/tokens)
#
# The token above was created through the email verification flow:
# 1. POST /v1/auth/request-code with valid email format (e.g., admin@local.com)
# 2. Get the dev_code from response
# 3. POST /v1/auth/verify-code with email and code to get JWT access_token
# 4. Use JWT to create persistent API token via POST /v1/tokens
