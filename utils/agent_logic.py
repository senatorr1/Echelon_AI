import os
from groq import Groq, APIConnectionError, RateLimitError, APIStatusError

class RobustAgent:
    def __init__(self, api_key, model="mixtral-8x7b-32768"):
        """
        Initializes the agent.
        :param api_key: Your Groq API Key
        :param model: The specific AI model to use (default: mixtral-8x7b-32768)
        """
        self.client = Groq(api_key=api_key)
        self.model = model
        
        # SYSTEM PROMPT: The core personality
        self.system_instruction = {
            "role": "system",
            "content": (
                "You are a highly capable AI assistant suited for business and general tasks. "
                "1. PRECISE: Be direct. No filler phrases like 'As an AI...'. "
                "2. CONTEXT AWARE: Remember previous details in this conversation. "
                "3. ADAPTIVE: If the user asks for code, provide code. If they ask for business advice, provide strategy."
            )
        }
        
        # MEMORY: Starts with just the system instruction
        self.conversation_history = [self.system_instruction]

    def chat(self, user_input):
        """
        Sends a message to the AI and gets a response.
        """
        # 1. Add user message to memory
        self.conversation_history.append({"role": "user", "content": user_input})

        try:
            # 2. Call the API with the FULL conversation history
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )

            # 3. Extract response
            bot_response = completion.choices[0].message.content
            
            # 4. Save AI response to memory (so it remembers next time)
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            
            return bot_response

        except RateLimitError:
            return "Error: Rate limit reached. Please wait a moment."
        except APIConnectionError:
            return "Error: Connection lost. Please check your internet."
        except Exception as e:
            return f"Error: {str(e)}"

    def clear_memory(self):
        """Wipes the conversation history to start fresh."""
        self.conversation_history = [self.system_instruction]
