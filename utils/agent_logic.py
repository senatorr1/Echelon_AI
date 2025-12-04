import os
import re
from groq import Groq
from utils.security_tools import *

class CyberSecurityAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # Removed self.conversation_history = [] as it is passed via Streamlit
    
    def process_query(self, user_input, full_chat_history=None):
        """Process user query with conversation memory and flexible tool routing"""
        try:
            # Route to appropriate tool
            user_lower = user_input.lower()
            
            # --- FLEXIBILITY FIX 3: Broader Password Check keywords ---
            if "password" in user_lower and any(word in user_lower for word in ["check", "strength", "analyze", "test", "how good", "score"]):
                # Extract password from query
                password_match = re.search(r'["\']([^"\']+)["\']', user_input)
                if password_match:
                    password = password_match.group(1)
                    score, feedback = check_password_strength(password)
                    response = f"**Password Analysis:**\nStrength Score: {score}%\n\n**Recommendations:**\n" + "\n".join(f"• {item}" for item in feedback)
                    yield response
                    return
            
            # --- FLEXIBILITY FIX 4: Broader Phishing Check keywords ---
            elif any(word in user_lower for word in ["phishing", "email", "scam", "suspicious", "fraud", "malicious", "sender"]):
                email_match = re.search(r'["\']([^"\']+)["\']', user_input)
                if email_match:
                    email_text = email_match.group(1)
                    result = analyze_phishing_email(email_text)
                    response = f"**Phishing Analysis:**\nRisk Level: {result['risk_level']}\n\n{result['analysis']}"
                    yield response
                    return
            
            # --- FLEXIBILITY FIX 5: Broader WiFi Check keywords ---
            elif any(word in user_lower for word in ["wifi", "network", "hotspot", "wireless", "internet security"]):
                response = "For WiFi security:\n• Use VPN on public networks\n• Avoid banking on public WiFi\n• Enable firewall\n• Use WPA3 encryption"
                yield response
                return
            
            # General Cybersecurity Advice (default LLM path)
            
            # Build conversation context from chat history
            messages = [
                {
                    "role": "system",
                    "content": """You are a highly flexible and knowledgeable cybersecurity expert. Provide helpful, accurate advice about cybersecurity, online safety, and digital protection.
                    
KEY INSTRUCTION: Be extremely flexible in understanding the user's question and maintain context from the history provided.
"""
                }
            ]
            
            # Add recent chat history for context (last 10 messages)
            if full_chat_history and len(full_chat_history) > 0:
                recent_history = full_chat_history[-10:]  # Last 10 messages
                for msg in recent_history:
                    # Only add conversational roles
                    if msg["role"] in ["user", "assistant"]:
                         messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
            
            # Add current user input
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Default: Use Groq for general questions with conversation memory
            response = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant",
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                        
        except Exception as e:
            yield f"I encountered an error: {str(e)}. Please check your API key and try again."
