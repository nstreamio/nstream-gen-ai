```sh
poetry run python src/stream_operators/main.py execute "Give me the stock price for AAAA"
poetry run python src/stream_operators/main.py execute "Stream stock prices for AAAA"
poetry run python src/stream_operators/main.py execute "Convert stock price for AAAA using an exchange rate of 1.2"
poetry run python src/stream_operators/main.py execute "Discount stock price for AAAA by 10%"
poetry run python src/stream_operators/main.py execute "Create a function to convert stock prices for AAAA with an exchange rate of 1.2"
poetry run python src/stream_operators/main.py execute "Create a function to discount stock prices for AAAA by 10%"
poetry run python src/stream_operators/main.py execute "Alert me if stock price for AAAA goes below 20"
poetry run python src/stream_operators/main.py execute "Create a function to alert me if stock price for AAAA goes below 20"
poetry run python src/stream_operators/main.py execute "Accumulate stock prices for AAAA using average with a window size of 5"
poetry run python src/stream_operators/main.py execute "Create a function to accumulate stock prices for AAAA using average with a window size of 5"

poetry run python src/stream_operators/main.py read-adhoc AAAA
poetry run python src/stream_operators/main.py read-streaming AAAA
poetry run python src/stream_operators/main.py accumulate-direct AAAA avg --operation-config '{"window_size": 5}'
poetry run python src/stream_operators/main.py accumulate-generate AAAA avg --operation-config '{"window_size": 5}'
poetry run python src/stream_operators/main.py map-direct AAAA '{"description": "apply exchange rate", "parameters": {"exchange_rate": "1.2"}}'
poetry run python src/stream_operators/main.py map-direct AAAA '{"description": "discount price by 10%", "parameters": {"discount": "0.1"}}'
poetry run python src/stream_operators/main.py map-generate AAAA '{"description": "apply exchange rate", "parameters": {"exchange_rate": "1.2"}}'
poetry run python src/stream_operators/main.py map-generate AAAA '{"description": "discount price by 10%", "parameters": {"discount": "0.1"}}'
poetry run python src/stream_operators/main.py filter-direct AAAA '{"description": "flag any values under 20", "parameters": {"threshold": 20}}'
poetry run python src/stream_operators/main.py filter-generate AAAA '{"description": "flag any values under 20", "parameters": {"threshold": 20}}'
```
