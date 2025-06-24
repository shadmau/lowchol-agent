"""
Cholesterol risk scoring functionality for ingredients.
"""

from typing import List, Tuple, Set

# High-risk ingredients for cholesterol/saturated fat
HIGH_RISK_KEYWORDS: Set[str] = {
    "butter", "cream", "heavy cream", "ghee", "egg yolk", "cheese",
    "parmesan", "cheddar", "whole milk", "lamb", "beef", "bacon", "sausage"
}

# Low-risk ingredients (healthier options)
LOW_RISK_KEYWORDS: Set[str] = {
    "tofu", "lentil", "steamed", "grilled", "chickpea", "bean",
    "broccoli", "spinach", "quinoa"
}


def _contains_keyword(keyword_set: Set[str], ingredient: str) -> bool:
    """
    Check if any keyword appears as substring in ingredient.
    
    Args:
        keyword_set: Set of keywords to search for
        ingredient: Ingredient name to check
        
    Returns:
        True if any keyword is found in the ingredient
    """
    ingredient_lower = ingredient.lower()
    return any(keyword in ingredient_lower for keyword in keyword_set)


def score_ingredients(ingredients: List[str]) -> Tuple[str, str]:
    """
    Score ingredients for cholesterol risk level.
    
    Args:
        ingredients: List of ingredient names
        
    Returns:
        Tuple of (risk_level, reason) where:
        - risk_level: "🔴 High", "🟡 Medium", or "🟢 Low"
        - reason: Explanation for the risk level
    """
    score = 0
    
    for ingredient in ingredients:
        if _contains_keyword(HIGH_RISK_KEYWORDS, ingredient):
            score += 4  # +4 per high-risk ingredient
        elif _contains_keyword(LOW_RISK_KEYWORDS, ingredient):
            score -= 1  # -1 per low-risk ingredient

    # Determine risk level based on score
    if score >= 4:  # 1 high-risk ingredient is enough
        return "🔴 High", "contains high saturated-fat ingredients"
    elif score <= 1:
        return "🟢 Low", "mostly lean/plant-based ingredients"
    else:
        return "🟡 Medium", "mixed nutritional profile" 