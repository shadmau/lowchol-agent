"""
Dish analysis functionality for extracting ingredients from dish names.
"""

from typing import List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel


def extract_ingredients(dish_name: str, model: BaseChatModel) -> List[str]:
    """
    Extract ingredients from a dish name using AI.
    
    Args:
        dish_name: Name of the dish to analyze
        model: Chat model instance for AI processing
        
    Returns:
        List of likely ingredients found in the dish
    """
    system = SystemMessage(
        content="You are a nutrition assistant. Extract a list of likely ingredients (comma-separated) from the given dish name."
    )
    user = HumanMessage(content=f"Dish: {dish_name}")
    response = model.invoke([system, user])

    content = response.content
    if isinstance(content, dict):
        line = str(content.get('text', content)).strip().lower()
    elif isinstance(content, list):
        line = str(content[0]).strip().lower()
    else:
        line = str(content).strip().lower()
    
    if "ingredients:" in line:
        line = line.split("ingredients:")[1]
    
    return [ingredient.strip() for ingredient in line.split(",") if ingredient.strip()] 