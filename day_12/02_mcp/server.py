from mcp.server.fastmcp import FastMCP

mcp =FastMCP("merdian-loans")

RATES= {"home":8.4, "car":9.5, "personal":12.5,"business":12.5}

@mcp.tool()
def get_rate(product:str) -> float:
    """Today's annual interrest rate is % for 'home' , 'car', 'personal', 'business'."""
    return RATES.get(product.lower(),0.0)

@mcp.tool()
def calculate_emi(principal:float, annual_rate:float,years:int) -> float:
    """Monthly emi in USD foa a loan amount for annual rate in %  and a tenure in years"""
    r,n = annual_rate/1200 , years *12
    return round(principal * r*(1+r) ** n/((1+r) ** n-1),2)

if __name__ =="__main__":
    mcp.run()
