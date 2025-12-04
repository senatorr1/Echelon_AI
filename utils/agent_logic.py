import os
import time
from groq import Groq, APIConnectionError, RateLimitError, APIStatusError

# --- CONFIGURATION ---
# Ideally, set this in your environment variables. 
# For now, replace strictly if you are running locally without env vars.
API_KEY = os.environ.get("GROQ_API_KEY") or "YOUR_GROQ_API_KEY_HERE"

class RobustAgent:
    def __init__(self, api_key, model="mixtral-8x7b-32768"):
        """
        Initializes the agent with a secure client, a specific model, 
        and an empty memory buffer.
        """
        if not api_key or "YOUR_GROQ_API_KEY" in api_key:
            raise ValueError("Please provide a valid Groq API Key.")
            
        self.client = Groq(api_key=api_key)
        self.model = model
        
        # SYSTEM PROMPT:
        # This is the 'personality' and rule set. 
        # We instruct it to be direct, adaptable, and avoid generic filler.
        self.system_instruction = {
            "role": "system",
            "content": (
                "You are a highly capable, flexible AI assistant. "
                "1. ADAPTABILITY: Adapt your tone to the user. If they are technical, be technical. "
                "If they are casual, be casual. "
                "2. NO FLUFF: Do not start responses with 'As an AI language model' or 'Here is the answer'. "
                "Just give the answer directly. "
                "3. CLARIFICATION: If a user prompt is vague (e.g., 'Fix it'), analyze the chat history "
                "to understand context. If you truly cannot understand, ask a specific clarifying question "
                "instead of giving a generic response."
            )
        }
        
        # MEMORY:
        # Initialize conversation history with the system instruction.
        self.conversation_history = [self.system_instruction]

    def add_to_history(self, role, content):
        """Adds a message to the memory buffer."""
        self.conversation_history.append({"role": role, "content": content})

    def chat(self, user_input):
        """
        The main processing loop.
        1. Accepts user input.
        2. Appends to history.
        3. Sends the WHOLE history to the AI (so it has context).
        4. Receives and stores the answer.
        """
        # Add user's message to memory
        self.add_to_history("user", user_input)

        try:
            # Making the API call with the full context
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7, # Balanced between creative and precise
                max_tokens=1024, # Allow for detailed answers
                top_p=1,
                stream=False,
                stop=None,
            )

            # Extract the response
            bot_response = completion.choices[0].message.content
            
            # Add the AI's response to memory so it remembers it next time
            self.add_to_history("assistant", bot_response)
            
            return bot_response

        except RateLimitError:
            return "Error: We hit the Groq rate limit. Please wait a moment and try again."
        except APIConnectionError:
            return "Error: Could not connect to Groq. Check your internet connection."
        except APIStatusError as e:
            return f"Error: The API returned a status error: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    def clear_memory(self):
        """Resets the conversation if things get too cluttered."""
        self.conversation_history = [self.system_instruction]
        print("\n[Memory Wiped: Starting Fresh Context]\n")

# --- EXECUTION LOOP ---

def main():
    print("Initializing Robust Agent...")
    try:
        # Instantiate the agent
        agent = RobustAgent(API_KEY)
        print(f"Agent Ready. Using model: {agent.model}")
        print("Type 'quit' to exit, or 'clear' to reset memory.\n")

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit"]:
                print("Shutting down.")
                break
            
            if user_input.lower() == "clear":
                agent.clear_memory()
                continue
            
            if not user_input:
                print("Please type something.")
                continue

            # Get response
            print("Agent is thinking...", end="\r")
            response = agent.chat(user_input)
            
            # Clear the "thinking" line and print response
            print(" " * 20, end="\r") 
            print(f"Agent: {response}\n")
            print("-" * 30)

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

if __name__ == "__main__":
    main()
