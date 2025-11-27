"""
Business Advisory Engine
Handles conversational business/service guidance for students
"""

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
        Main processing function for income generation queries
        Returns streaming response
        """
        user_lower = user_input.lower()
        
        # Stage 1: Initial greeting / intent detection
        if self.conversation_stage == "initial":
            yield from self._handle_initial_query(user_input)
        
        # Stage 2: Path selection (business vs service)
        elif self.conversation_stage == "path_selection":
            yield from self._handle_path_selection(user_input)
        
        # Stage 3: Information gathering
        elif self.conversation_stage == "gathering_info":
            yield from self._gather_student_info(user_input)
        
        # Stage 4: Recommendations
        elif self.conversation_stage == "recommendations":
            yield from self._provide_recommendations(user_input)
        
        # Stage 5: Detailed planning
        elif self.conversation_stage == "action_planning":
            yield from self._create_action_plan(user_input)
        
        # Default: general conversation
        else:
            yield from self._general_business_conversation(user_input)
    
    def _handle_initial_query(self, user_input):
        """Handle first interaction"""
        user_lower = user_input.lower()
        
        # Detect income-related intent
        income_keywords = ["money", "income", "earn", "business", "service", "broke", 
                          "financial", "hustle", "startup", "freelance", "side"]
        
        has_intent = any(keyword in user_lower for keyword in income_keywords)
        
        if has_intent:
            response = """👋 **Welcome to Income Generation Guidance!**

I'm here to help you start making money as a student. I can guide you whether you want to:

🏢 **Start a Business** - Selling products, running operations
🛠️ **Offer Services** - Using your skills to help others

📊 **Or Not Sure?** - I can help you figure out the best path!

**What interests you more?**
1️⃣ Starting a business
2️⃣ Offering services  
3️⃣ Not sure - help me decide

*(Just type 1, 2, 3, or tell me in your own words)*
"""
            self.conversation_stage = "path_selection"
            yield response
        else:
            # General greeting
            response = """Hello! 👋 

I'm your **Business & Income Generation Advisor**. I help students like you discover ways to make money through:

💼 Starting businesses  
🛠️ Offering services  
💡 Monetizing your skills

**Want to get started? Just tell me:**
- "I want to make money"
- "Help me start a business"
- "What services can I offer?"
- Or ask any income-related question!

How can I help you today? 😊
"""
            yield response
    
    def _handle_path_selection(self, user_input):
        """Handle business vs service selection"""
        user_lower = user_input.lower()
        
        if "business" in user_lower or "1" in user_input:
            self.student_profile["path"] = "business"
            response = """🏢 **Great! Let's explore business opportunities.**

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
            self.conversation_stage = "gathering_info"
            yield response
        
        elif "service" in user_lower or "2" in user_input:
            self.student_profile["path"] = "service"
            response = """🛠️ **Excellent choice! Services need minimal capital.**

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
            self.conversation_stage = "gathering_info"
            yield response
        
        elif "not sure" in user_lower or "3" in user_input or "don't know" in user_lower:
            response = """🤔 **No problem! Let's figure this out together.**

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
            self.conversation_stage = "gathering_info"
            yield response
        
        else:
            # Unclear response, ask again
            response = """I'm not quite sure what you'd prefer! 😅

Let me ask differently: **What sounds more interesting to you?**

🏢 **Business** - Example: Selling thrift clothes, phone accessories, snacks, dropshipping
🛠️ **Service** - Example: Graphic design, tutoring, social media management, writing

Or just tell me: **"I'm not sure, help me decide"** and I'll guide you through some questions!
"""
            yield response
    
    def _gather_student_info(self, user_input):
        """Gather information about student's situation"""
        user_lower = user_input.lower()
        
        # Extract capital information
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
        
        # Provide recommendations based on gathered info
        self.conversation_stage = "recommendations"
        yield from self._provide_recommendations(user_input)
    
    def _provide_recommendations(self, user_input):
        """Provide personalized recommendations using hybrid approach"""
        path = self.student_profile["path"]
        capital = self.student_profile["capital"]
        skills = self.student_profile["skills"]
        
        if path == "service" or capital == 0:
            # HYBRID APPROACH: Try database first, then AI generation
            
            # Step 1: Try AI-powered matching with database
            try:
                # Get AI interpretation of skills and match to database
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

Respond ONLY with 3 numbers (e.g., "10, 11, 12") - the services that BEST match the skills mentioned.
If NO services match well, respond with "GENERATE_CUSTOM"
"""
                
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": skill_interpretation_prompt}],
                    model="llama-3.1-8b-instant",
                    temperature=0.3
                )
                
                ai_recommendations = response.choices[0].message.content.strip()
                
                # Check if AI wants custom generation
                if "GENERATE_CUSTOM" in ai_recommendations.upper():
                    # Use custom AI generation
                    yield from self._generate_custom_opportunities(user_input)
                    return
                
                # Parse AI response to get service indices
                import re
                numbers = re.findall(r'\d+', ai_recommendations)
                recommended_indices = [int(n) - 1 for n in numbers[:3] if n.isdigit()]
                
                # Map indices to actual opportunities
                all_service_opportunities = []
                for category in SERVICES.values():
                    all_service_opportunities.extend(category["opportunities"])
                
                recommended_opportunities = [
                    all_service_opportunities[i] 
                    for i in recommended_indices 
                    if i < len(all_service_opportunities)
                ]
                
                # If AI matching worked, show those + offer custom generation
                if recommended_opportunities:
                    response_text = f"""✨ **Perfect! Based on your skills, here are the BEST opportunities for you:**\n\n"""
                    
                    for i, opp in enumerate(recommended_opportunities, 1):
                        response_text += f"""**{i}. {opp['title']}** ⭐
💰 Potential: {opp['potential_income']['month_1']} (Month 1) → {opp['potential_income']['month_6']} (Month 6)
⏱️ Time to first income: {opp['time_to_first_income']}
💵 Capital needed: {opp['capital']}
📚 Skills needed: {', '.join(opp['skills_needed'][:3])}

"""
                    
                    response_text += """\n**💡 These match your profile perfectly!**

**What would you like to do?**
• Type **1, 2, or 3** for detailed action plan
• Say **"show me custom ideas"** for AI-generated unique opportunities
• Ask **"tell me more about [service name]"** for details
"""
                    
                    self.conversation_stage = "action_planning"
                    yield response_text
                    return
                
            except Exception as e:
                print(f"AI matching error: {e}")
                # Fall through to custom generation
            
            # Step 2: If database matching failed, use custom AI generation
            yield from self._generate_custom_opportunities(user_input)
        
        elif path == "business":
            # Recommend businesses based on capital
            opportunities = get_opportunities_by_capital(capital)
            
            response = f"""🏢 **Based on your ₦{capital:,} capital, here are suitable businesses:**\n\n"""
            
            # Filter businesses within capital range
            suitable_businesses = [
                opp for opp in opportunities 
                if "capital_needed" in opp
            ][:3]
            
            if suitable_businesses:
                for i, biz in enumerate(suitable_businesses, 1):
                    response += f"""**{i}. {biz['title']}**
💵 Capital needed: {biz['capital_needed']}
💰 Potential: {biz['potential_income']['month_1']} (Month 1) → {biz['potential_income']['month_6']} (Month 6)
⏱️ Time to start: {biz['time_to_first_income']}

"""
            else:
                response += """With your current capital, I'd recommend starting with **service-based income** first to:
1. Build capital
2. Learn business basics
3. Start earning immediately

Would you like me to show you service opportunities instead? 🛠️
"""
            
            response += """\n**Interested in any of these? Tell me which number, and I'll give you a complete startup guide!** 📋
"""
            
            self.conversation_stage = "action_planning"
            yield response
    
    def _generate_custom_opportunities(self, user_input):
        """Generate custom opportunities using AI for unique skills"""
        try:
            # Build conversation history for context
            conversation_context = self._build_conversation_context()
            
            custom_prompt = f"""A Nigerian student has these skills/abilities: "{user_input}"

{conversation_context}

Generate 3 SPECIFIC, PRACTICAL income opportunities they can start with minimal capital.

For EACH opportunity, provide:
1. Service/Business Name (creative, specific)
2. How it works (2-3 sentences)
3. Startup capital needed (in Naira)
4. Expected income (Month 1, Month 3, Month 6 in Naira)
5. First 3 action steps
6. Target customers
7. Where to find clients

Make opportunities:
- Realistic for Nigerian students
- Low barrier to entry
- Practical and actionable
- Creative but feasible

Format each opportunity clearly with headers.
"""
            
            response_text = "🎨 **AI-GENERATED CUSTOM OPPORTUNITIES FOR YOUR UNIQUE SKILLS:**\n\n"
            response_text += "_These are personalized suggestions based on your specific abilities!_\n\n"
            response_text += "═══════════════════════════════════════\n\n"
            
            yield response_text
            
            # Stream AI-generated opportunities
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": custom_prompt}],
                model="llama-3.1-8b-instant",
                temperature=0.7,  # Higher creativity
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            
            # Add follow-up options
            followup = """\n\n═══════════════════════════════════════

**💡 What's Next?**

These are custom opportunities I generated just for you! 

**Want more?**
• Say **"show me more ideas"** for different suggestions
• Say **"expand on #1"** (or 2, 3) for detailed action plan
• Say **"show database options"** to see proven service templates

**Ready to start?** Pick one and let's create your action plan! 🚀
"""
            
            yield followup
            self.conversation_stage = "action_planning"
            
        except Exception as e:
            error_response = f"""I encountered an error generating custom opportunities: {str(e)}

Let me show you some versatile services that work for many skills:

**1. Personal Assistant Services** - Help busy people with tasks
**2. Campus Courier** - Deliver items around campus  
**3. Skill Teaching** - Teach your unique skill to others

Which interests you? Or describe your skills differently and I'll try again!
"""
            yield error_response
    
    def _build_conversation_context(self):
        """Build context from student profile"""
        context = ""
        if self.student_profile["path"]:
            context += f"\nPreferred path: {self.student_profile['path']}"
        if self.student_profile["capital"] > 0:
            context += f"\nAvailable capital: ₦{self.student_profile['capital']:,}"
        if self.student_profile["skills"]:
            context += f"\nIdentified skills: {', '.join(self.student_profile['skills'])}"
        return context if context else ""
    
    def _create_action_plan(self, user_input):
        """Create detailed action plan for chosen opportunity"""
        user_lower = user_input.lower()
        
        # Check if user wants custom AI generation
        if any(phrase in user_lower for phrase in ["custom", "unique", "creative", "surprise", "different", "more ideas"]):
            yield from self._generate_custom_opportunities(user_input)
            return
        
        # Check if user wants to expand on AI-generated option
        expand_match = re.search(r'expand.*?(\d+)', user_lower)
        if expand_match:
            response = """To create a detailed action plan for that AI-generated option, please **describe it more specifically** or choose from our proven database opportunities.

Say **"show database options"** to see structured opportunities with complete action plans!
"""
            yield response
            return
        
        # Try to match opportunity selection
        selected = None
        
        # Search for opportunity name in user input
        all_opportunities = []
        for category in SERVICES.values():
            all_opportunities.extend(category["opportunities"])
        for category in BUSINESSES.values():
            all_opportunities.extend(category["opportunities"])
        
        for opp in all_opportunities:
            if opp['title'].lower() in user_lower:
                selected = opp
                break
        
        # Or check for number selection
        if not selected:
            number_match = re.search(r'\b([123])\b', user_input)
            if number_match:
                idx = int(number_match.group(1)) - 1
                # This is simplified - in production you'd track which options were shown
                selected = all_opportunities[idx] if idx < len(all_opportunities) else None
        
        if selected:
            # Generate comprehensive action plan from database
            response = f"""📋 **COMPLETE ACTION PLAN: {selected['title']}**\n\n"""
            response += f"""═══════════════════════════════════════

**💰 FINANCIAL BREAKDOWN**
Initial Investment: {selected.get('capital', selected.get('capital_needed', '₦0'))}
Month 1 Income: {selected['potential_income']['month_1']}
Month 3 Income: {selected['potential_income']['month_3']}
Month 6 Income: {selected['potential_income']['month_6']}

**⏱️ TIMELINE**
Time to First Income: {selected['time_to_first_income']}

**📚 SKILLS NEEDED**
{chr(10).join(f'✓ {skill}' for skill in selected['skills_needed'])}

**🛠️ TOOLS YOU'LL NEED**
{chr(10).join(f'• {tool}' for tool in selected['tools'])}

═══════════════════════════════════════

**🚀 STEP-BY-STEP ACTION PLAN:**

{chr(10).join(f'{i}. {step}' for i, step in enumerate(selected['action_plan'], 1))}

═══════════════════════════════════════

**🎯 TARGET CLIENTS/CUSTOMERS**
{chr(10).join(f'• {client}' for client in selected.get('target_clients', ['General public']))}

**📢 WHERE TO FIND CLIENTS**
{chr(10).join(f'• {channel}' for channel in selected.get('marketing_channels', ['Social media', 'Word of mouth']))}

═══════════════════════════════════════
"""
            
            if 'risks' in selected:
                response += f"""\n**⚠️ POTENTIAL RISKS**
{chr(10).join(f'• {risk}' for risk in selected['risks'])}
"""
            
            if 'success_tips' in selected:
                response += f"""\n**💡 SUCCESS TIPS**
{chr(10).join(f'✓ {tip}' for tip in selected['success_tips'])}
"""
            
            response += """

═══════════════════════════════════════

**🎯 YOUR NEXT STEPS (Do This Today!):**

1. **Save this plan** - Export this chat for reference
2. **Start Step 1** - Begin with the first action item above
3. **Set a goal** - "I will complete Week 1 by [date]"
4. **Track progress** - Check off each step as you complete it

**Need help with any specific step? Just ask!** 

Want to explore other opportunities? Say "show me more options"! 🚀
"""
            
            yield response
        else:
            # Ask for clarification or offer options
            response = """I'm not sure which opportunity you're interested in. Here's what you can do:

**From Database (Proven Plans):**
• Type the **number** (1, 2, or 3) from options shown earlier
• Type the **name** of the service (e.g., "graphic design")
• Say **"show me options again"**

**AI-Generated (Custom Ideas):**
• Say **"show me custom ideas"** for unique opportunities
• Say **"generate creative options"** for your specific skills

What would you like to do? 😊
"""
            yield response
    
    def _general_business_conversation(self, user_input):
        """Handle general business questions using AI"""
        try:
            system_prompt = f"""You are a business advisor helping students start income-generating activities.

Student profile:
- Path: {self.student_profile.get('path', 'undecided')}
- Capital: ₦{self.student_profile.get('capital', 0):,}
- Skills: {', '.join(self.student_profile.get('skills', ['unknown']))}

Provide practical, actionable advice. Be encouraging and realistic. Focus on opportunities suitable for Nigerian students.
"""
            
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.1-8b-instant",
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            yield f"I encountered an error: {str(e)}. Please try rephrasing your question!"
    
    def reset_conversation(self):
        """Reset conversation state for new query"""
        self.conversation_stage = "initial"
        self.student_profile = {
            "path": None,
            "skills": [],
            "capital": 0,
            "time_available": None,
            "goals": {},
            "interests": []
        }