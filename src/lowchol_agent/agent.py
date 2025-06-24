"""
Main agent functionality for cholesterol risk analysis.
"""

import os
from typing import List
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import Tool
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .dish_analyzer import extract_ingredients
from .cholesterol_scorer import score_ingredients
from .ocr_processor import extract_text_from_image


class LowCholAgent:
    """Main agent class for cholesterol risk analysis."""
    
    def __init__(self):
        """Initialize the agent with required components."""
        load_dotenv()
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables!")
        
        self.model = init_chat_model("gpt-4o-mini", model_provider="openai")
        self.tools = self._create_tools()
        self.agent_executor = self._create_agent()
    
    def _extract_ingredients_tool(self, dish_name: str) -> str:
        """Extract ingredients from a dish name."""
        ingredients = extract_ingredients(dish_name, self.model)
        return f"Ingredients: {', '.join(ingredients)}"

    def _score_ingredients_tool(self, ingredients_str: str) -> str:
        """Score ingredients for cholesterol risk. Input should be comma-separated ingredients."""
        # Parse ingredients from string
        if "Ingredients:" in ingredients_str:
            ingredients_str = ingredients_str.split("Ingredients:")[1]
        ingredients = [i.strip() for i in ingredients_str.split(",") if i.strip()]
        
        level, reason = score_ingredients(ingredients)
        return f"{level} – {reason}"

    def _image_to_text_tool(self, image_path: str) -> str:
        """Extract text from an image file using OCR."""
        text = extract_text_from_image(image_path)
        return f"Text extracted from image: {text}"
    
    def _create_tools(self) -> List[Tool]:
        """Create the tools available to the agent."""
        return [
            Tool(
                name="extract_ingredients",
                func=self._extract_ingredients_tool,
                description="Extract ingredients from a dish name. Input: dish name as string."
            ),
            Tool(
                name="score_cholesterol_risk",
                func=self._score_ingredients_tool,
                description="Score ingredients for cholesterol risk. Input: comma-separated list of ingredients."
            ),
            Tool(
                name="extract_text_from_image",
                func=self._image_to_text_tool,
                description="Extract text from an image using OCR. Input: path to image file (jpg, png, etc.)."
            )
        ]
    
    def _create_agent(self) -> AgentExecutor:
        """Create and configure the agent executor."""
        system = '''Respond to the human as helpfully and accurately as possible. You are a nutrition assistant that helps analyze dishes for cholesterol risk and can also extract text from images.

IMPORTANT WORKFLOW: When analyzing dishes for cholesterol risk, you MUST always:
1. First extract ingredients using the extract_ingredients tool 
2. Then score the ingredients using score_cholesterol_risk tool
3. NEVER pass dish names directly to score_cholesterol_risk - it only works with ingredient lists

You have access to the following tools:

{tools}

Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```

Follow this format:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}
```

Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation'''

        human = '''{input}

{agent_scratchpad}

(reminder to respond in a JSON blob no matter what)'''

        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", human),
        ])

        # Create the agent
        agent = create_structured_chat_agent(self.model, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def analyze_dish(self, dish_name: str) -> str:
        """
        Analyze a dish for cholesterol risk.
        
        Args:
            dish_name: Name of the dish to analyze
            
        Returns:
            Analysis result as string
        """
        result = self.agent_executor.invoke({
            "input": f"Analyze the cholesterol risk of: {dish_name}"
        })
        return result["output"]
    
    def analyze_image(self, image_path: str) -> str:
        """
        Extract text from an image and analyze cholesterol risk for each dish.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Analysis result as string
        """
        result = self.agent_executor.invoke({
            "input": f"Extract text from this image: {image_path}. Then identify all dishes/food items from the extracted text and analyze the cholesterol risk for each dish separately. Provide a clear summary showing each dish and its cholesterol risk level."
        })
        return result["output"] 