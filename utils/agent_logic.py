import os
import re
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
            raise ValueError("API Key is missing. Check your .env file.")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"

    def process_query(self, user_input, full_chat_history):
        """
        Process user query:
        1. Check if a specific security tool is needed.
        2. If not, use the LLM for advice using full chat history.
        Yields chunks of text (streaming).
        """
        user_lower = user_input.lower()

        # --- TOOL ROUTING ---
        
        # 1. Password Checker
        if "password" in user_lower and "check" in user_lower:
            # Extract password (quoted or last word)
            match = re.search(r'["\']([^"\']+)["\']', user_input)
            password = match.group(1) if match else user_input.split()[-1]
            
            score, feedback = check_password_strength(password)
            
            response = f"""**🔐 Password Analysis:**
**Strength Score:** {score}%

**Recommendations:**
"""
            for tip in feedback:
                response += f"• {tip}\n"
            
            yield response
            return

        # 2. Phishing Analysis
        if "phishing" in user_lower or "analyze email" in user_lower:
            yield "**📧 Phishing Analysis:**\n"
            result = analyze_phishing_email(user_input)
            yield f"**Risk Level:** {result['risk_level']}\n\n"
            yield f"{result['analysis']}\n"
            return

        # 3. WiFi Security
        if "wifi" in user_lower and "public" in user_lower:
            recommendation = wifi_security_recommendation("general") # Default to general if specific type not found
            yield f"**📶 WiFi Advice:**\n{recommendation}"
            return
            
        # 4. URL Safety
        if "url" in user_lower and "check" in user_lower:
             # Extract URL
            url_match = re.search(r'(https?://[^\s]+)', user_input)
            if url_match:
                url = url_match.group(1)
                yield f"**🔍 Checking URL:** {url}...\n"
                result = check_url_safety(url)
                if result['status'] == 'success':
                    yield f"**Status:** {result['safety_color']} {result['safety_status']}\n"
                    yield f"**Advice:** {result['recommendation']}"
                else:
                    yield f"**Result:** {result['message']}"
                return

        # --- LLM FALLBACK (General Advice) ---
        try:
            # Construct messages with context
            messages = [{
                "role": "system", 
                "content": "You are Echelon AI, a cybersecurity expert. Provide helpful, accurate, and practical advice on digital safety. Be concise."
            }]
            
            # Add recent history (last 5 interactions) to maintain context
            if full_chat_history:
                for msg in full_chat_history[-5:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})
            
            messages.append({"role": "user", "content": user_input})

            # Call Groq API with streaming
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                stream=True
            )

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield f"⚠️ I encountered an error: {str(e)}"
