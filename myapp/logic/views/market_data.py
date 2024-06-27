from openbb import obb
obb.account.login(pat="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoX3Rva2VuIjoiZGxRSGJMV01Ldmx2WmpZRXU0aU5ON3FkelRuZDVGSUVrb0hMM1E1biIsImV4cCI6MTc1MDYxMjMzOH0.FkB1V2PkwqbdJm9rf-ogPYtpdZG4FtYaJxmlbr20Y3Q") # type: ignore

importent = ["""
             help(obb.equity.price.historical)
             obb.equity
             

"""]

#https://docs.openbb.co/platform/getting_started/quickstart
from openbb import obb

# Get the price of a stock
quote_data = obb.equity.price.quote(symbol="AAPL", provider="yfinance") # type: ignore
print(quote_data.to_df())



# run python market_data.py