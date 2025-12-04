import os
from groq import Groq
from utils.security_tools import (
    check_password_strength, 
    analyze_phishing_email, 
    wifi_security_recommendation, 
    check_url_safety
)

class CyberSecurityAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("API Key is missing. Please check your .env file.")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"

    def process_query(self, user_input, chat_history):
        """
        Processes the user query. 
        1. Checks if a specific security tool is needed.
        2. If not, streams a response from the AI.
        """
        user_lower = user_input.lower()
        
        # --- 1. TOOL ROUTING (Manual checks for specific tools) ---
        
        # Password Check
        if "password" in user_lower and "check" in user_lower:
            # Basic extraction: grab the last word or text in quotes
            import re
            match = re.search(r'["\']([^"\']+)["\']', user_input)
            password = match.group(1) if match else user_input.split()[-1]
            
            score, feedback = check_password_strength(password)
            yield f"**🔒 Password Strength: {score}/100**\n\n"
            for tip in feedback:
                yield f"• {tip}\n"
            return

        # Phishing Check
        if "phishing" in user_lower or "analyze email" in user_lower:
            result = analyze_phishing_email(user_input)
            yield f"**📧 Phishing Analysis:**\n"
            yield f"Risk Level: **{result['risk_level']}**\n\n"
            yield result['analysis']
            return

        # WiFi Check
        if "wifi" in user_lower:
            # Heuristic to guess usage type
            usage = "browsing"
            if "bank" in user_lower: usage = "banking"
            elif "work" in user_lower: usage = "work"
            
            yield f"**📶 WiFi Security Advice:**\n"
            yield wifi_security_recommendation(usage)
            return

        # --- 2. PURE AI RESPONSE (For everything else) ---
        
        # Construct messages with history for context
        messages = [
            {"role": "system", "content": "You are Echelon AI, a cybersecurity expert. Provide concise, practical security advice."}
        ]
        
        # Add a few recent messages from history to keep conversation flowing
        if chat_history:
            for msg in chat_history[-6:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"⚠️ Error: {str(e)}"
