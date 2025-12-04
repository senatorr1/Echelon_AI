import os
from groq import Groq
import json

class BusinessAdvisor:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.conversation_stage = "initial"
        # We keep the profile to help the AI give better context-aware answers
        self.student_profile = {
            "path": None,  # "business" or "service"
            "skills": [],
            "capital": None,
            "interests": []
        }
    
    def process_income_query(self, user_input, conversation_history=None): 
        """
        Main processing function that routes based on stage but uses AI for content.
        """
        # 1. INITIAL STAGE: Detect what the user wants
        if self.conversation_stage == "initial":
            yield from self._handle_initial_query(user_input, conversation_history)
        
        # 2. GATHERING INFO: AI extracts details (Capital/Skills)
        elif self.conversation_stage == "gathering_info":
            yield from self._gather_info_dynamic(user_input, conversation_history)
        
        # 3. RECOMMENDATIONS: AI generates ideas based on profile
        elif self.conversation_stage == "recommendations":
            yield from self._provide_ai_recommendations(user_input, conversation_history)
        
        # 4. PLANNING: AI creates a custom plan for WHATEVER the user chose
        elif self.conversation_stage == "action_planning":
            yield from self._create_ai_action_plan(user_input, conversation_history)
        
        # 5. FALLBACK: General conversation
        else:
            yield from self._general_conversation(user_input, conversation_history)

    def _handle_initial_query(self, user_input, history):
        """
        Uses AI to understand intent. No more rigid keyword looping.
        """
        # Ask AI to classify the user's input
        classification_prompt = f"""
        Analyze this user input: "{user_input}"
        Determine if they want to:
        1. "business" (sell products, start a company, trade)
        2. "service" (freelance, use skills, consult, work)
        3. "general" (just saying hi, asking general questions, or unclear)
        
        Reply ONLY with one word: "business", "service", or "general".
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": classification_prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.1
            )
            intent = response.choices[0].message.content.strip().lower()
        except:
            intent = "general"

        if "business" in intent:
            self.student_profile["path"] = "business"
            self.conversation_stage = "gathering_info"
            yield "🏢 **Awesome! You want to start a business.**\n\nTo help you best, **how much capital (money) do you have available to invest?** (e.g., ₦0, ₦20k, ₦100k?)"
        
        elif "service" in intent:
            self.student_profile["path"] = "service"
            self.conversation_stage = "gathering_info"
            yield "🛠️ **Great choice! Service-based income is excellent.**\n\nTo recommend the right gigs, **what skills do you have?** (e.g., writing, coding, cooking, teaching, or 'no skills yet')"
        
        else:
            # If general, just chat normally but try to guide them
            yield from self._general_conversation(user_input, history)

    def _gather_info_dynamic(self, user_input, history):
        """
        Uses AI to extract capital or skills from natural language.
        """
        path = self.student_profile["path"]
        
        if path == "business":
            # Just save the input as capital context and move on
            self.student_profile["capital"] = user_input
            self.conversation_stage = "recommendations"
            yield from self._provide_ai_recommendations(user_input, history)
            
        elif path == "service":
            # Save input as skills and move on
            self.student_profile["skills"].append(user_input)
            self.conversation_stage = "recommendations"
            yield from self._provide_ai_recommendations(user_input, history)

    def _provide_ai_recommendations(self, user_input, history):
        """
        PURE AI GENERATION: No database. Generates ideas based on the specific user profile.
        """
        profile_desc = f"Path: {self.student_profile['path']}, Capital/Status: {self.student_profile['capital']}, Skills: {self.student_profile['skills']}"
        
        prompt = f"""
        User Profile: {profile_desc}
        User Input: "{user_input}"
        
        Task: Act as a Nigerian business expert. Suggest 3 specific, realistic income opportunities for this student.
        
        Requirements:
        - Must be viable in Nigeria.
        - Must fit their capital/skill level.
        - Format neatly with bold titles and emojis.
        - For each, briefly mention "Potential Income" and "Startup Cost".
        
        End the response by asking: "Which one of these interests you? Or do you have something else in mind?"
        """
        
        yield from self._stream_ai_response(prompt)
        
        # Move to planning stage so next reply generates a plan
        self.conversation_stage = "action_planning"

    def _create_ai_action_plan(self, user_input, history):
        """
        PURE AI GENERATION: Creates a plan for ANYTHING the user typed.
        """
        # If user says "none of these" or asks a random question, switch to general chat
        if any(x in user_input.lower() for x in ["no", "none", "different", "change"]):
             yield from self._general_conversation(user_input, history)
             return

        prompt = f"""
        The user wants to start this: "{user_input}"
        Their Context: {self.student_profile}
        
        Task: Create a detailed, step-by-step action plan for this specific opportunity in Nigeria.
        
        Include:
        1. **Immediate Next Steps** (First 3 days)
        2. **Estimated Costs** (Breakdown in Naira)
        3. **Marketing Strategy** (How to get customers)
        4. **Risk Warning**
        
        Tone: Encouraging but realistic.
        """
        
        yield from self._stream_ai_response(prompt)
        
        yield "\n\n**💡 Need help with a specific step? Just ask!**"

    def _general_conversation(self, user_input, history):
        """
        Handles any input that doesn't fit the strict stages.
        """
        # Construct context from previous messages if available
        context_msgs = []
        if history:
            # Grab last 4 meaningful messages
            for msg in history[-4:]:
                context_msgs.append({"role": msg["role"], "content": msg["content"]})
        
        system_msg = {
            "role": "system",
            "content": f"You are a helpful business advisor for students. Current Context: {self.student_profile}. Be flexible. If they want to start over, say so."
        }
        
        messages = [system_msg] + context_msgs + [{"role": "user", "content": user_input}]
        
        try:
            stream = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"I'm having trouble connecting. (Error: {str(e)})"

    def _stream_ai_response(self, prompt):
        """Helper to stream AI response"""
        try:
            stream = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error generating response: {str(e)}"
