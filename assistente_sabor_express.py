import anthropic
import json
import dotenv 
import os

dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
MODEL_NAME = "claude-3-opus-20240229"

