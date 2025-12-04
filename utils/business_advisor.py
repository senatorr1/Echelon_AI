import os
import re
from groq import Groq
from knowledge.business_opportunities import *

class BusinessAdvisor:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.conversation_stage = "initial"
        self.student_profile = {
            "path": None,  # "business" or "service"
            "skills": [],
            "capital": 0,
            "time_available": None,
            "goals": {},
            "interests": []
        }
    
    def process_income_query(self, user_input, conversation_history=None): 
        """
        Main processing function for income generation queries.
        Returns streaming response.
        """
        # Stage 1: Initial greeting / intent detection
        if self.conversation_stage == "initial":
            yield from self._handle_initial_query(user_input, conversation_history)
        
        # Stage 2: Path selection (business vs service)
        elif self.conversation_stage == "path_selection":
            yield from self._handle_path_selection(user_input, conversation_history)
        
        # Stage 3: Information gathering
        elif self.conversation_stage == "gathering_info":
            yield from self._gather_student_info(user_input, conversation_history)
        
        # Stage 4: Recommendations
        elif self.conversation_stage == "recommendations":
            yield from self._provide_recommendations(user_input, conversation_history)
        
        # Stage 5: Detailed planning
        elif self.conversation_stage == "action_planning":
            yield from self._create_action_plan(user_input, conversation_history)
        
        # Default: General conversation
        else:
            yield from self._general_business_conversation(user_input, conversation_history)
    
    def _handle_initial_query(self, user_input, conversation_history=None):
        """Handle first interaction with enhanced flexibility"""
        user_lower = user_input.lower()
        
        # Keywords for intent detection
        income_keywords = ["money", "income", "earn", "business", "service", "broke", 
                          "financial", "hustle", "startup", "freelance", "side",
                          "funds", "bills", "job", "work", "consult", "advise", "capital", "skill",
                          "need", "help", "generate", "source", "idea", "opportunity", "make", "cash",
                          "side-gig", "extra", "selling", "trade"]
        
        has_intent = any(keyword in user_lower for keyword in income_keywords)
        
        if has_intent:
            # Check for direct intent (Business or Service) to skip the menu
            is_business_intent = any(word in user_lower for word in ["business", "startup", "selling", "product", "e-commerce", "trade"])
            is_service_intent = any(word in user_lower for word in ["service", "skills", "freelance", "consult", "tutoring", "design", "writing", "coding"])

            if is_business_intent and not is_service_intent:
                self.student_profile["path"] = "business"
                self.conversation_stage = "gathering_info"
                yield """🏢 **Great! You're ready to explore business opportunities.**

Businesses typically involve buying/selling products or running operations. Let's get straight to what you need:

**1. How much capital (money) can you invest to start?**
   - ₦0 (no money available)
   - ₦5,000 - ₦20,000 (small amount)
   - ₦20,000 - ₦50,000 (moderate)
   - ₦50,000+ (good starting capital)

**2. What type of business interests you?**
   - Online (e-commerce, dropshipping)
   - Physical products (clothing, accessories, food)
   - Not sure

*Please share your answers, and I'll recommend suitable businesses!*
"""
                return

            elif is_service_intent and not is_business_intent:
                self.student_profile["path"] = "service"
                self.conversation_stage = "gathering_info"
                yield """🛠️ **Excellent choice! Services need minimal capital.**

Service-based income means using your skills to help others. Let's discover what you can offer:

**1. What skills do you have?**
   Examples: Writing, design, coding, teaching, social media, video editing, etc.

**2. What do people often ask you for help with?**

**3. What subjects or activities do you excel at?**

*Share whatever comes to mind - don't worry if you think you have "no skills"! We'll figure it out together.* 😊
"""
                return

            else:
                # General intent: Offer selection menu
                self.conversation_stage = "path_selection"
                yield """👋 **Welcome to Income Generation Guidance!**

I'm here to help you start making money as a student. I can guide you whether you want to:

🏢 **Start a Business** - Selling products, running operations
🛠️ **Offer Services** - Using your skills to help others

**What interests you more?**
1️⃣ Starting a business
2️⃣ Offering services  
3️⃣ Not sure - help me decide

*(Just type 1, 2, 3, or tell me in your own words)*
"""
        else:
            # FIX: Use general conversation for non-intent inputs (e.g., "Hi", "Who are you?")
            yield from self._general_business_conversation(user_input, conversation_history)

    def _handle_path_selection(self, user_input, conversation_history=None):
        """Handle business vs service selection with flexible fallback"""
        user_lower = user_input.lower()
        
        if any(w in user_lower for w in ["business", "startup", "selling"]) or "1" in user_input:
            self.student_profile["path"] = "business"
            self.conversation_stage = "gathering_info"
            yield """🏢 **Great! Let's explore business opportunities.**

Businesses typically involve buying/selling products or running operations. Before I recommend specific businesses, I need to understand your situation:

**1. How much capital (money) can you invest to start?**
   - ₦0 (no money available)
   - ₦5,000 - ₦20,000 (small amount)
   - ₦20,000 - ₦50,000 (moderate)
   - ₦50,000+ (good starting capital)

**2. What type of business interests you?**
   - Online (e-commerce, dropshipping)
   - Physical products (clothing, accessories, food)
   - Not sure

*Please share your answers, and I'll recommend suitable businesses!*
"""
        
        elif any(w in user_lower for w in ["service", "freelance", "skill"]) or "2" in user_input:
            self.student_profile["path"] = "service"
            self.conversation_stage = "gathering_info"
            yield """🛠️ **Excellent choice! Services need minimal capital.**

Service-based income means using your skills to help others. This is perfect for students because:
✅ Little to no startup cost
✅ Flexible schedule
✅ Can start immediately

**Let's discover what you can offer. Tell me:**

**1. What skills do you have?**
   Examples: Writing, design, coding, teaching, social media, video editing, etc.

**2. What do people often ask you for help with?**

**3. What subjects or activities do you excel at?**

*Share whatever comes to mind - don't worry if you think you have "no skills"! We'll figure it out together.* 😊
"""
        
        elif "not sure" in user_lower or "3" in user_input or "don't know" in user_lower:
            self.conversation_stage = "gathering_info"
            yield """🤔 **No problem! Let's figure this out together.**

I'll ask a few quick questions to understand you better:

**Question 1: Capital & Resources**
How much money can you invest to start something?
- A) ₦0 - I have no money
- B) ₦5,000 - ₦30,000
- C) ₦30,000+

**Question 2: Time Availability**
How much time can you dedicate per week?
- A) 5-10 hours (very limited)
- B) 10-20 hours (moderate)
- C) 20+ hours (plenty of time)

**Question 3: Skills & Interests**
Which describes you better?
- A) I'm creative (design, content, art)
- B) I'm technical (coding, tech, analysis)
- C) I'm people-oriented (teaching, communication)
- D) I'm unsure

*Just answer with the letters (e.g., "A, B, C") or describe in your own words!*
"""
        
        else:
            # FIX: If input is unclear, use general conversation to clarify instead of a static error
            yield from self._general_business_conversation(user_input, conversation_history)
    
    def _gather_student_info(self, user_input, conversation_history=None):
        """Gather information about student's situation"""
        user_lower = user_input.lower()
        
        # Extract capital
        capital_match = re.search(r'₦?(\d+[,\d]*)', user_input)
        if capital_match:
            capital_str = capital_match.group(1).replace(',', '')
            self.student_profile["capital"] = int(capital_str)
        elif any(word in user_lower for word in ["no money", "₦0", "zero", "broke", "nothing"]):
            self.student_profile["capital"] = 0
        
        # Extract skills
        skill_keywords = ["writing", "design", "coding", "teaching", "social media", 
                         "video", "photography", "speaking", "communication", "tech",
                         "creative", "analytical", "people", "teaching"]
        
        found_skills = [skill for skill in skill_keywords if skill in user_lower]
        if found_skills:
            self.student_profile["skills"].extend(found_skills)
        
        # Move to recommendations
        self.conversation_stage = "recommendations"
        yield from self._provide_recommendations(user_input, conversation_history)
    
    def _provide_recommendations(self, user_input, conversation_history=None):
        """Provide personalized recommendations"""
        path = self.student_profile["path"]
        capital = self.student_profile["capital"]
        
        if path == "service" or capital == 0:
            # Hybrid approach for services
            try:
                # 1. Try AI matching with database
                skill_interpretation_prompt = f"""Based on these skills/interests: "{user_input}"
Identify the TOP 3 service opportunities from this list that best match:

AVAILABLE SERVICES:
1. Web Development (coding, tech)
2. Graphic Design (creative, visual)
3. Social Media Management (social media, marketing)
4. Freelance Writing (writing, communication)
5. Video Editing (creative, tech)
6. Online Tutoring (teaching, knowledge sharing)
7. Typing & Document Services (typing, administrative, fast typing)
8. Data Entry & Virtual Assistant (organization, admin)
9. Transcription Services (typing, listening)
10. Event Hosting & MC (public speaking, presenting, confidence)
11. Workshop/Conference Speaking (speaking, expertise, teaching)
12. Voice-Over Services (good voice, speaking, clear speech)
13. Moving & Delivery Services (physical strength, stamina, reliable)
14. Event Setup & Teardown (strong, physical work, labor)
15. Cleaning & Housekeeping (detail-oriented, organized, physical)
16. Personal Shopping & Errands (reliable, organized, helpful)

Respond ONLY with 3 numbers (e.g., "10, 11, 12"). If NO services match well, respond with "GENERATE_CUSTOM".
"""
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": skill_interpretation_prompt}],
                    model="llama-3.1-8b-instant",
                    temperature=0.3
                )
                ai_recommendations = response.choices[0].message.content.strip()
                
                if "GENERATE_CUSTOM" in ai_recommendations.upper():
                    yield from self._generate_custom_opportunities(user_input, conversation_history)
                    return
                
                # Parse indices
                numbers = re.findall(r'\d+', ai_recommendations)
                recommended_indices = [int(n) - 1 for n in numbers[:3] if n.isdigit()]
                
                all_service_opportunities = []
                for category in SERVICES.values():
                    all_service_opportunities.extend(category["opportunities"])
                
                recommended_opportunities = [all_service_opportunities[i] for i in recommended_indices if i < len(all_service_opportunities)]
                
                if recommended_opportunities:
                    response_text = f"""✨ **Perfect! Based on your skills, here are the BEST opportunities for you:**\n\n"""
                    for i, opp in enumerate(recommended_opportunities, 1):
                        response_text += f"""**{i}. {opp['title']}** ⭐
💰 Potential: {opp['potential_income']['month_1']} (Month 1) → {opp['potential_income']['month_6']} (Month 6)
⏱️ Time to first income: {opp['time_to_first_income']}
💵 Capital needed: {opp['capital']}
📚 Skills needed: {', '.join(opp['skills_needed'][:3])}\n\n"""
                    
                    response_text += """**What would you like to do?**
• Type **1, 2, or 3** for a detailed action plan
• Say **"show me custom ideas"** for AI-generated unique opportunities
• Ask **"tell me more about [service name]"** for details
"""
                    self.conversation_stage = "action_planning"
                    yield response_text
                    return
                
            except Exception as e:
                # Fallback to custom generation on error
                yield from self._generate_custom_opportunities(user_input, conversation_history)
        
        elif path == "business":
            # Recommend businesses based on capital
            opportunities = get_opportunities_by_capital(capital)
            suitable_businesses = [opp for opp in opportunities if "capital_needed" in opp][:3]
            
            response = f"""🏢 **Based on your ₦{capital:,} capital, here are suitable businesses:**\n\n"""
            
            if suitable_businesses:
                for i, biz in enumerate(suitable_businesses, 1):
                    response += f"""**{i}. {biz['title']}**
💵 Capital needed: {biz['capital_needed']}
💰 Potential: {biz['potential_income']['month_1']} (Month 1) → {biz['potential_income']['month_6']} (Month 6)
⏱️ Time to start: {biz['time_to_first_income']}\n\n"""
            else:
                response += """With your current capital, I'd recommend starting with **service-based income** first to build funds.\n"""
            
            response += """\n**Interested in any of these? Tell me which number, and I'll give you a complete startup guide!** 📋"""
            
            self.conversation_stage = "action_planning"
            yield response
    
    def _generate_custom_opportunities(self, user_input, conversation_history=None):
        """Generate custom opportunities using AI"""
        try:
            context = self._build_conversation_context()
            custom_prompt = f"""A Nigerian student has these skills/abilities: "{user_input}"
{context}

Generate 3 SPECIFIC, PRACTICAL income opportunities they can start with minimal capital.
For EACH opportunity, provide:
1. Service/Business Name
2. How it works (2-3 sentences)
3. Startup capital needed (in Naira)
4. Expected income (Month 1, Month 3, Month 6)
5. First 3 action steps
6. Target customers
7. Where to find clients

Make opportunities realistic for Nigerian students, low barrier to entry, and actionable.
Format with clear headers.
"""
            yield "🎨 **AI-GENERATED CUSTOM OPPORTUNITIES FOR YOUR UNIQUE SKILLS:**\n\n"
            yield "_These are personalized suggestions based on your specific abilities!_\n\n"
            
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": custom_prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.7,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            
            yield """\n\n**💡 What's Next?**
• Say **"show me more ideas"** for different suggestions
• Say **"expand on #1"** for a detailed plan
• Say **"show database options"** to see proven templates

**Ready to start?** Pick one and let's create your action plan! 🚀
"""
            self.conversation_stage = "action_planning"
            
        except Exception as e:
            yield from self._general_business_conversation(user_input, conversation_history)
    
    def _build_conversation_context(self):
        context = ""
        if self.student_profile["path"]: context += f"\nPreferred path: {self.student_profile['path']}"
        if self.student_profile["capital"] > 0: context += f"\nAvailable capital: ₦{self.student_profile['capital']:,}"
        if self.student_profile["skills"]: context += f"\nIdentified skills: {', '.join(self.student_profile['skills'])}"
        return context

    def _create_action_plan(self, user_input, conversation_history=None):
        """Create detailed action plan with flexible fallback"""
        user_lower = user_input.lower()
        
        # 1. Handle Custom/Expand requests
        if any(w in user_lower for w in ["custom", "unique", "creative", "more ideas", "show database"]):
            yield from self._generate_custom_opportunities(user_input, conversation_history)
            return

        if "expand" in user_lower:
            # Route to general conversation to interpret "expand on #1" contextually
            yield from self._general_business_conversation(user_input, conversation_history)
            return

        # 2. Try to match selection from Database
        selected = None
        all_opportunities = []
        for category in SERVICES.values(): all_opportunities.extend(category["opportunities"])
        for category in BUSINESSES.values(): all_opportunities.extend(category["opportunities"])
        
        # Match by title
        for opp in all_opportunities:
            if opp['title'].lower() in user_lower:
                selected = opp
                break
        
        # Match by number
        if not selected:
            number_match = re.search(r'\b([123])\b', user_input)
            if number_match:
                idx = int(number_match.group(1)) - 1
                selected = all_opportunities[idx] if idx < len(all_opportunities) else None
        
        if selected:
            # Generate Plan from DB
            response = f"""📋 **COMPLETE ACTION PLAN: {selected['title']}**\n\n"""
            response += f"""**💰 FINANCIAL BREAKDOWN**
Initial Investment: {selected.get('capital', selected.get('capital_needed', '₦0'))}
Month 1 Income: {selected['potential_income']['month_1']}
Month 6 Income: {selected['potential_income']['month_6']}

**⏱️ TIMELINE**
Time to First Income: {selected['time_to_first_income']}

**📚 SKILLS NEEDED**
{chr(10).join(f'✓ {skill}' for skill in selected['skills_needed'])}

**🚀 STEP-BY-STEP ACTION PLAN:**
{chr(10).join(f'{i}. {step}' for i, step in enumerate(selected.get('action_plan', selected.get('startup_steps', [])), 1))}

**🎯 YOUR NEXT STEPS:**
1. **Save this plan**
2. **Start Step 1**
3. **Set a goal**

**Need help with a step? Just ask!**
"""
            yield response
        else:
            # FIX: If no selection matched, use General Conversation to handle the query
            yield from self._general_business_conversation(user_input, conversation_history)
    
    def _general_business_conversation(self, user_input, conversation_history=None):
        """Handle general business questions using AI with full context"""
        try:
            system_prompt = f"""You are a flexible business advisor for Nigerian students.
Student Profile:
- Path: {self.student_profile.get('path', 'undecided')}
- Capital: ₦{self.student_profile.get('capital', 0):,}
- Skills: {', '.join(self.student_profile.get('skills', ['unknown']))}

Goal: Provide practical, encouraging advice.
Context: The user might be asking a specific question, trying to choose an option, or just chatting.
If they are in 'path_selection' or 'action_planning' mode but ask a question, answer the question and then gently guide them back to the next step.
"""
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent history for context
            if conversation_history:
                for msg in conversation_history[-8:]:
                    if msg["role"] in ["user", "assistant"]:
                        messages.append({"role": msg["role"], "content": msg["content"]})
            
            messages.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant",
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            yield f"I encountered an error: {str(e)}. Please try rephrasing."

    def reset_conversation(self):
        self.conversation_stage = "initial"
        self.student_profile = {
            "path": None, "skills": [], "capital": 0,
            "time_available": None, "goals": {}, "interests": []
        }
