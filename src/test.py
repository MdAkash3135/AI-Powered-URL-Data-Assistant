from sqlalchemy import Function
from litellm import completion

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature.",
                    },
                },
                "required": ["location"],
            }
        }
    }
]

messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]

response = completion(
  model="ollama/llama3.1",
  messages=messages,
  tools=tools
)
print(response.choices[0].message.tool_calls[0].function)

Function(arguments='{"location": "Boston, MA", "unit": "fahrenheit"}', name='get_current_weather')
