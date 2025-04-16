from mcp.server.fastmcp import FastMCP
from constants import TOKYO_AREA_TO_CODE, CUISINE_TO_CODE
from typing import Optional
from utils import fetch_restaurants, fetch_restaurant_details

# Create an MCP server for Tablog restaurant data
mcp = FastMCP("Tablog Restaurant Guide")


@mcp.tool()
def list_areas_of_tokyo() -> str:
    """Returns a list of all Tokyo areas available for searching restaurants"""
    areas = list(TOKYO_AREA_TO_CODE.keys())
    return "\n".join(areas)


@mcp.tool()
def list_cuisines_of_tokyo() -> str:
    """Returns a list of all cuisine types available for searching restaurants"""
    cuisines = list(CUISINE_TO_CODE.keys())
    return "\n".join(cuisines)


@mcp.tool()
async def search_restaurants_in_tokyo(area: str, cuisine: str, max_price: Optional[int] = None) -> str:
    """
    Search for restaurants in a specific Tokyo area and cuisine type.

    IMPORTANT: Before calling this tool, you MUST know the valid options for 'area' and 'cuisine'.
    Use the 'list_areas_of_tokyo' tool to get valid Tokyo areas.
    Use the 'list_cuisines_of_tokyo' tool to get valid cuisine types.
    If the user's request doesn't specify a valid area or cuisine from these lists, ask for clarification or suggest options from the lists.

    Parameters:
    - area: A valid Tokyo area obtained from 'list_areas_of_tokyo'.
    - cuisine: A valid cuisine type obtained from 'list_cuisines_of_tokyo'.
    - max_price: Optional maximum price per person in yen (e.g. 5000 means up to ¥5,000 per person). If not specified, restaurants at all price points will be returned.

    Returns a list of restaurant recommendations, or an error message if inputs are invalid.
    """
    # Look up the area and cuisine codes
    area_code = TOKYO_AREA_TO_CODE.get(area)
    cuisine_code = CUISINE_TO_CODE.get(cuisine)
    
    if not area_code:
        return f"Error: Area '{area}' not found. Use the list_areas_of_tokyo tool to see available areas."
    
    if not cuisine_code:
        return f"Error: Cuisine '{cuisine}' not found. Use the list_cuisines_of_tokyo tool to see available cuisines."
    
    # Fetch restaurant data
    restaurants = fetch_restaurants(area_code, cuisine_code, max_price)
    restaurants = sorted(restaurants, key=lambda x: x.rating, reverse=True)

    return '\n\n'.join([restaurant.to_string() for restaurant in restaurants])


@mcp.tool()
def get_restaurant_details(restaurant_url: str) -> str:
    """
    Get detailed information about a restaurant from its URL.

    Parameters:
    - restaurant_url: The URL of the restaurant to get details for.

    Returns a string containing the restaurant's details including name, tagline, rating, cost and text from the restaurant's page.
    """
    restaurant = fetch_restaurant_details(restaurant_url)
    return restaurant.to_string()



if __name__ == "__main__":
    mcp.run()
