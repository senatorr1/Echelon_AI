"""
Business Opportunities Knowledge Base
Contains services, businesses, and actionable plans for students
"""

# Service-based opportunities (minimal capital needed)
SERVICES = {
    "tech_services": {
        "name": "Technology Services",
        "opportunities": [
            {
                "title": "Web Development",
                "skills_needed": ["HTML/CSS", "JavaScript", "Basic design sense"],
                "capital": "₦0 - ₦5,000",
                "time_to_first_income": "2-4 weeks",
                "potential_income": {
                    "month_1": "₦10,000 - ₦30,000",
                    "month_3": "₦50,000 - ₦100,000",
                    "month_6": "₦100,000 - ₦200,000+"
                },
                "tools": ["VS Code (free)", "GitHub (free)", "Netlify/Vercel (free hosting)"],
                "action_plan": [
                    "Week 1: Learn basic HTML/CSS/JavaScript (FreeCodeCamp)",
                    "Week 2: Build 3 portfolio websites (personal, business, portfolio)",
                    "Week 3: Join Facebook groups, offer services at ₦15,000-25,000",
                    "Week 4: Get first client, deliver quality work, ask for referrals",
                    "Month 2+: Increase prices, build reputation, get recurring clients"
                ],
                "target_clients": ["Small businesses", "Startups", "Individuals needing portfolios"],
                "marketing_channels": ["Facebook groups", "Twitter", "LinkedIn", "Direct outreach"]
            },
            {
                "title": "Graphic Design",
                "skills_needed": ["Creativity", "Basic design principles", "Canva/Photoshop"],
                "capital": "₦0",
                "time_to_first_income": "1-2 weeks",
                "potential_income": {
                    "month_1": "₦10,000 - ₦25,000",
                    "month_3": "₦40,000 - ₦80,000",
                    "month_6": "₦80,000 - ₦150,000+"
                },
                "tools": ["Canva (free)", "Photoshop (trial/affordable)", "Figma (free)"],
                "action_plan": [
                    "Week 1: Master Canva, learn design basics on YouTube",
                    "Week 1-2: Create 10 sample designs (logos, flyers, social media posts)",
                    "Week 2: Post samples on Instagram/Behance, join design groups",
                    "Week 2-3: Offer discounted services (₦2,000-5,000) for testimonials",
                    "Month 2+: Build portfolio, increase rates, get retainer clients"
                ],
                "target_clients": ["Small businesses", "Event planners", "Social media managers"],
                "marketing_channels": ["Instagram", "Facebook", "WhatsApp Status", "Behance"]
            },
            {
                "title": "Social Media Management",
                "skills_needed": ["Social media knowledge", "Content creation", "Communication"],
                "capital": "₦0",
                "time_to_first_income": "1-3 weeks",
                "potential_income": {
                    "month_1": "₦15,000 - ₦40,000",
                    "month_3": "₦50,000 - ₦100,000",
                    "month_6": "₦100,000 - ₦200,000+"
                },
                "tools": ["Canva", "Buffer/Hootsuite (free tiers)", "Meta Business Suite"],
                "action_plan": [
                    "Week 1: Study successful brand accounts, learn content strategies",
                    "Week 1-2: Create sample content calendars and posts",
                    "Week 2-3: Reach out to small businesses, offer free trial (1 week)",
                    "Week 3-4: Convert trial clients to paid (₦15,000-30,000/month)",
                    "Month 2+: Manage 3-5 clients, scale pricing"
                ],
                "target_clients": ["Local businesses", "Personal brands", "Startups"],
                "marketing_channels": ["Direct messages", "LinkedIn", "Local business groups"]
            }
        ]
    },
    "content_services": {
        "name": "Content Creation Services",
        "opportunities": [
            {
                "title": "Freelance Writing",
                "skills_needed": ["Good writing skills", "Research ability", "Grammar knowledge"],
                "capital": "₦0",
                "time_to_first_income": "1-2 weeks",
                "potential_income": {
                    "month_1": "₦10,000 - ₦30,000",
                    "month_3": "₦40,000 - ₦80,000",
                    "month_6": "₦80,000 - ₦150,000+"
                },
                "tools": ["Grammarly (free)", "Google Docs", "Hemingway Editor"],
                "action_plan": [
                    "Week 1: Create 3-5 writing samples (blog posts, articles)",
                    "Week 1-2: Sign up on Fiverr, Upwork, create portfolio",
                    "Week 2-3: Apply for 20+ jobs daily, start with low rates",
                    "Week 3-4: Get first clients, deliver excellent work, get reviews",
                    "Month 2+: Increase rates, build reputation, get direct clients"
                ],
                "target_clients": ["Bloggers", "Businesses", "Marketing agencies"],
                "marketing_channels": ["Fiverr", "Upwork", "LinkedIn", "Content platforms"]
            },
            {
                "title": "Video Editing",
                "skills_needed": ["Basic editing", "Creativity", "Patience"],
                "capital": "₦0 - ₦10,000",
                "time_to_first_income": "2-4 weeks",
                "potential_income": {
                    "month_1": "₦15,000 - ₦40,000",
                    "month_3": "₦50,000 - ₦100,000",
                    "month_6": "₦100,000 - ₦250,000+"
                },
                "tools": ["CapCut (free)", "DaVinci Resolve (free)", "Adobe Premiere (paid)"],
                "action_plan": [
                    "Week 1-2: Learn basic editing on YouTube, practice daily",
                    "Week 2-3: Edit sample videos (fake commercials, vlogs)",
                    "Week 3-4: Post samples, reach out to YouTubers/businesses",
                    "Month 2: Get clients, charge ₦5,000-15,000 per video",
                    "Month 3+: Specialize (ads, YouTube, events), increase rates"
                ],
                "target_clients": ["YouTubers", "Businesses", "Event organizers"],
                "marketing_channels": ["Twitter", "Instagram", "YouTube", "Fiverr"]
            }
        ]
    },
    "education_services": {
        "name": "Education & Tutoring",
        "opportunities": [
            {
                "title": "Online Tutoring",
                "skills_needed": ["Subject expertise", "Teaching ability", "Patience"],
                "capital": "₦0",
                "time_to_first_income": "1 week",
                "potential_income": {
                    "month_1": "₦20,000 - ₦50,000",
                    "month_3": "₦60,000 - ₦120,000",
                    "month_6": "₦120,000 - ₦250,000+"
                },
                "tools": ["Zoom (free)", "Google Meet", "WhatsApp", "YouTube"],
                "action_plan": [
                    "Week 1: Identify subjects you excel in, create lesson plans",
                    "Week 1-2: Advertise in student groups, offer free demo class",
                    "Week 2: Start with 3-5 students at ₦2,000-5,000/hour",
                    "Month 2: Get testimonials, increase rates, add group classes",
                    "Month 3+: Scale to 10-15 students, consider creating courses"
                ],
                "target_clients": ["Primary/secondary students", "University students", "Adults learning new skills"],
                "marketing_channels": ["WhatsApp Status", "Facebook groups", "School forums", "Word of mouth"]
            }
        ]
    },
    "administrative_services": {
        "name": "Administrative & Data Services",
        "opportunities": [
            {
                "title": "Typing & Document Services",
                "skills_needed": ["Fast typing", "Attention to detail", "Microsoft Office"],
                "capital": "₦0",
                "time_to_first_income": "3-7 days",
                "potential_income": {
                    "month_1": "₦15,000 - ₦40,000",
                    "month_3": "₦50,000 - ₦100,000",
                    "month_6": "₦80,000 - ₦180,000+"
                },
                "tools": ["Microsoft Word/Google Docs", "WhatsApp", "Email"],
                "action_plan": [
                    "Week 1: Advertise typing services in student groups (₦500-2,000 per project)",
                    "Week 1: Offer to type assignments, CVs, business documents",
                    "Week 2: Get 3-5 clients, deliver fast with excellent formatting",
                    "Week 3: Increase rates based on urgency and document length",
                    "Month 2+: Add transcription, CV design, get recurring clients"
                ],
                "target_clients": ["Students needing assignments typed", "Professionals needing CVs", "Researchers needing transcription"],
                "marketing_channels": ["Campus notice boards", "WhatsApp Status", "Student groups", "LinkedIn"]
            },
            {
                "title": "Data Entry & Virtual Assistant",
                "skills_needed": ["Typing speed", "Organization", "Basic computer skills"],
                "capital": "₦0",
                "time_to_first_income": "1-2 weeks",
                "potential_income": {
                    "month_1": "₦20,000 - ₦50,000",
                    "month_3": "₦60,000 - ₦120,000",
                    "month_6": "₦100,000 - ₦200,000+"
                },
                "tools": ["Microsoft Excel/Google Sheets", "Email", "Cloud storage"],
                "action_plan": [
                    "Week 1: Create Upwork/Fiverr profile showcasing typing speed",
                    "Week 1-2: Apply for data entry gigs (₦5,000-15,000 per project)",
                    "Week 2-3: Deliver quality work quickly, get 5-star reviews",
                    "Week 3-4: Expand to virtual assistant tasks (email, scheduling)",
                    "Month 2+: Get retainer clients (₦30,000-50,000/month)"
                ],
                "target_clients": ["Small businesses", "Entrepreneurs", "Real estate agents", "Researchers"],
                "marketing_channels": ["Upwork", "Fiverr", "LinkedIn", "Local business groups"]
            },
            {
                "title": "Transcription Services",
                "skills_needed": ["Fast typing", "Good listening", "Patience"],
                "capital": "₦0",
                "time_to_first_income": "1-2 weeks",
                "potential_income": {
                    "month_1": "₦15,000 - ₦35,000",
                    "month_3": "₦40,000 - ₦90,000",
                    "month_6": "₦80,000 - ₦150,000+"
                },
                "tools": ["Text editor", "Headphones", "Transcription software (free)"],
                "action_plan": [
                    "Week 1: Sign up on Rev.com, GoTranscript, or local platforms",
                    "Week 1-2: Practice with sample audio, improve accuracy",
                    "Week 2-3: Take beginner transcription jobs",
                    "Week 3-4: Build reputation, aim for ₦500-1,500 per audio hour",
                    "Month 2+: Specialize (legal, medical), charge premium rates"
                ],
                "target_clients": ["Podcasters", "Researchers", "Content creators", "Legal professionals"],
                "marketing_channels": ["Rev.com", "Fiverr", "Upwork", "Direct outreach to podcasters"]
            }
        ]
    },
    "speaking_services": {
        "name": "Speaking & Presentation Services",
        "opportunities": [
            {
                "title": "Event Hosting & MC Services",
                "skills_needed": ["Public speaking", "Confidence", "Good voice", "Crowd control"],
                "capital": "₦0 - ₦5,000",
                "time_to_first_income": "1-3 weeks",
                "potential_income": {
                    "month_1": "₦10,000 - ₦30,000",
                    "month_3": "₦50,000 - ₦100,000",
                    "month_6": "₦100,000 - ₦250,000+"
                },
                "tools": ["Professional attire", "Microphone (optional)", "Business cards"],
                "action_plan": [
                    "Week 1: Offer to host small campus events for free (build portfolio)",
                    "Week 2: Record videos of yourself hosting, create Instagram page",
                    "Week 2-3: Reach out to event planners, churches, student associations",
                    "Week 3-4: Charge ₦5,000-15,000 for small events",
                    "Month 2+: Network aggressively, charge ₦20,000-50,000+ per event"
                ],
                "target_clients": ["Event planners", "Churches", "Student associations", "Corporate events", "Weddings"],
                "marketing_channels": ["Instagram", "TikTok", "Event planner networks", "Word of mouth"]
            },
            {
                "title": "Workshop & Conference Speaker",
                "skills_needed": ["Public speaking", "Expertise in topic", "Confidence"],
                "capital": "₦0",
                "time_to_first_income": "2-4 weeks",
                "potential_income": {
                    "month_1": "₦10,000 - ₦40,000",
                    "month_3": "₦40,000 - ₦100,000",
                    "month_6": "₦80,000 - ₦200,000+"
                },
                "tools": ["Presentation slides (PowerPoint/Canva)", "LinkedIn profile"],
                "action_plan": [
                    "Week 1: Identify your expertise area (tech, entrepreneurship, etc.)",
                    "Week 1-2: Create 2-3 presentation topics with outlines",
                    "Week 2-3: Reach out to hackathons, student clubs, bootcamps offering to speak",
                    "Week 3-4: Start with free talks to build portfolio and testimonials",
                    "Month 2+: Charge ₦10,000-50,000 per session, target corporate workshops"
                ],
                "target_clients": ["Hackathons", "Tech bootcamps", "Student clubs", "Startups", "Corporate training"],
                "marketing_channels": ["LinkedIn", "Twitter", "Event organizer groups", "Direct outreach"]
            },
            {
                "title": "Voice-Over Services",
                "skills_needed": ["Good speaking voice", "Clear pronunciation", "Audio editing"],
                "capital": "₦5,000 - ₦15,000",
                "time_to_first_income": "2-3 weeks",
                "potential_income": {
                    "month_1": "₦10,000 - ₦30,000",
                    "month_3": "₦40,000 - ₦80,000",
                    "month_6": "₦80,000 - ₦150,000+"
                },
                "tools": ["Good microphone (₦5,000-10,000)", "Audacity (free)", "Quiet recording space"],
                "action_plan": [
                    "Week 1: Invest in basic USB microphone, practice recording",
                    "Week 1-2: Create sample voice-over demos (ads, explainers, audiobooks)",
                    "Week 2-3: Sign up on Fiverr, Upwork, Voices.com",
                    "Week 3-4: Start with low rates (₦2,000-5,000 per project)",
                    "Month 2+: Build portfolio, specialize, increase to ₦10,000-30,000"
                ],
                "target_clients": ["YouTube creators", "Advertisers", "E-learning platforms", "Audiobook producers"],
                "marketing_channels": ["Fiverr", "Upwork", "YouTube creator groups", "LinkedIn"]
            }
        ]
    },
    "physical_services": {
        "name": "Physical & Manual Labor Services",
        "opportunities": [
            {
                "title": "Moving & Delivery Services",
                "skills_needed": ["Physical strength", "Reliability", "Time management"],
                "capital": "₦0 - ₦10,000",
                "time_to_first_income": "3-7 days",
                "potential_income": {
                    "month_1": "₦20,000 - ₦60,000",
                    "month_3": "₦60,000 - ₦150,000",
                    "month_6": "₦100,000 - ₦250,000+"
                },
                "tools": ["Bicycle/motorcycle (optional)", "Strong bags/cart", "Phone for coordination"],
                "action_plan": [
                    "Week 1: Advertise moving services in campus groups (₦2,000-5,000 per move)",
                    "Week 1: Offer to help students move between hostels/apartments",
                    "Week 2: Partner with online stores for delivery (₦500-2,000 per delivery)",
                    "Week 3: Build reputation for reliability, get referrals",
                    "Month 2+: Consider getting motorcycle for faster deliveries, scale pricing"
                ],
                "target_clients": ["Students moving hostels", "Online stores", "Local businesses", "Events"],
                "marketing_channels": ["Campus notice boards", "WhatsApp groups", "Student associations", "Instagram"]
            },
            {
                "title": "Event Setup & Teardown Crew",
                "skills_needed": ["Physical strength", "Teamwork", "Following instructions"],
                "capital": "₦0",
                "time_to_first_income": "1-2 weeks",
                "potential_income": {
                    "month_1": "₦15,000 - ₦40,000",
                    "month_3": "₦50,000 - ₦100,000",
                    "month_6": "₦80,000 - ₦180,000+"
                },
                "tools": ["Work gloves (optional)", "Phone", "Reliable availability"],
                "action_plan": [
                    "Week 1: Contact event planners offering setup/cleanup services",
                    "Week 1-2: Offer services to campus events, churches, parties",
                    "Week 2-3: Charge ₦3,000-8,000 per event depending on size",
                    "Week 3-4: Build team of 2-3 reliable friends, scale operations",
                    "Month 2+: Get recurring clients, charge premium for reliability"
                ],
                "target_clients": ["Event planners", "Churches", "Hotels", "Conference centers", "Party organizers"],
                "marketing_channels": ["Direct outreach to event planners", "Word of mouth", "Event venues"]
            },
            {
                "title": "Cleaning & Housekeeping Services",
                "skills_needed": ["Attention to detail", "Reliability", "Physical stamina"],
                "capital": "₦2,000 - ₦5,000",
                "time_to_first_income": "3-7 days",
                "potential_income": {
                    "month_1": "₦20,000 - ₦50,000",
                    "month_3": "₦60,000 - ₦120,000",
                    "month_6": "₦100,000 - ₦200,000+"
                },
                "tools": ["Basic cleaning supplies (₦2,000-3,000)", "Uniform/professional attire"],
                "action_plan": [
                    "Week 1: Buy basic supplies (soap, broom, mop, gloves)",
                    "Week 1: Advertise dorm/apartment cleaning (₦2,000-5,000 per clean)",
                    "Week 2: Offer weekly cleaning subscriptions (₦8,000-15,000/month)",
                    "Week 3: Target busy professionals, students during exams",
                    "Month 2+: Build team, scale to 10-15 regular clients"
                ],
                "target_clients": ["Busy students", "Working professionals", "Hostels", "Offices", "Airbnb hosts"],
                "marketing_channels": ["WhatsApp Status", "Campus groups", "Hostel notice boards", "Instagram"]
            },
            {
                "title": "Personal Shopping & Errands",
                "skills_needed": ["Organization", "Reliability", "Good communication"],
                "capital": "₦0 - ₦5,000",
                "time_to_first_income": "1 week",
                "potential_income": {
                    "month_1": "₦15,000 - ₦40,000",
                    "month_3": "₦50,000 - ₦100,000",
                    "month_6": "₦80,000 - ₦180,000+"
                },
                "tools": ["Reliable phone", "Transportation (optional)", "Payment apps"],
                "action_plan": [
                    "Week 1: Offer to run errands for busy professionals/students",
                    "Week 1: Charge ₦1,000-3,000 per errand (shopping, pickup, drop-off)",
                    "Week 2: Build reputation for speed and reliability",
                    "Week 3: Get recurring clients who need weekly shopping",
                    "Month 2+: Offer packages (5 errands/week = ₦10,000-20,000)"
                ],
                "target_clients": ["Busy professionals", "Elderly people", "Students during exams", "New parents"],
                "marketing_channels": ["WhatsApp", "Neighbourhood groups", "Church announcements", "Direct outreach"]
            }
        ]
    }
}

# Business opportunities (require capital)
BUSINESSES = {
    "low_capital": {
        "name": "Low Capital Businesses (₦5,000 - ₦50,000)",
        "opportunities": [
            {
                "title": "Thrift Clothing Resale (Okrika)",
                "capital_needed": "₦10,000 - ₦30,000",
                "skills_needed": ["Fashion sense", "Negotiation", "Marketing"],
                "time_to_first_income": "1-2 weeks",
                "potential_income": {
                    "month_1": "₦20,000 - ₦50,000",
                    "month_3": "₦60,000 - ₦120,000",
                    "month_6": "₦100,000 - ₦200,000+"
                },
                "startup_steps": [
                    "Capital: ₦20,000 for initial stock",
                    "Week 1: Visit thrift markets, buy quality pieces (₦500-1,500 each)",
                    "Week 1: Clean, iron, photograph items professionally",
                    "Week 2: List on Instagram/Facebook with good descriptions",
                    "Week 2-3: Price at 2-3x cost, negotiate smartly",
                    "Month 2+: Reinvest profits, build following, do sales"
                ],
                "risks": ["Fashion trends change", "Quality issues", "Competition"],
                "success_tips": ["Focus on quality over quantity", "Good photography is key", "Build trust with customers"]
            },
            {
                "title": "Phone Accessories Sales",
                "capital_needed": "₦15,000 - ₦40,000",
                "skills_needed": ["Product knowledge", "Customer service", "Trend awareness"],
                "time_to_first_income": "1 week",
                "potential_income": {
                    "month_1": "₦15,000 - ₦40,000",
                    "month_3": "₦50,000 - ₦100,000",
                    "month_6": "₦80,000 - ₦180,000+"
                },
                "startup_steps": [
                    "Capital: ₦20,000-30,000 for inventory",
                    "Week 1: Source suppliers (Computer Village, online wholesalers)",
                    "Week 1: Buy popular items (cases, chargers, earphones, screen protectors)",
                    "Week 1-2: Set up Instagram shop with product photos",
                    "Ongoing: Sell on campus, online, to friends - 50-100% markup",
                    "Month 2+: Expand inventory based on what sells"
                ],
                "risks": ["Damage/theft", "Fake products", "Phone model changes"],
                "success_tips": ["Know your target phone models", "Quality over cheap prices", "Offer warranties"]
            },
            {
                "title": "Snack/Food Business",
                "capital_needed": "₦10,000 - ₦30,000",
                "skills_needed": ["Cooking/baking", "Hygiene awareness", "Consistency"],
                "time_to_first_income": "3-7 days",
                "potential_income": {
                    "month_1": "₦20,000 - ₦60,000",
                    "month_3": "₦60,000 - ₦150,000",
                    "month_6": "₦100,000 - ₦300,000+"
                },
                "startup_steps": [
                    "Capital: ₦15,000-25,000 for ingredients and packaging",
                    "Week 1: Choose product (chin-chin, cupcakes, small chops, etc.)",
                    "Week 1: Test recipe, get feedback, perfect it",
                    "Week 1-2: Get NAFDAC-compliant packaging, create brand name",
                    "Week 2+: Sell to classmates, in hostels, take pre-orders",
                    "Month 2+: Scale production, consider vendors/distributors"
                ],
                "risks": ["Food safety", "Spoilage", "Competition"],
                "success_tips": ["Consistency in quality and taste", "Proper packaging", "Word-of-mouth is key"]
            }
        ]
    },
    "medium_capital": {
        "name": "Medium Capital Businesses (₦50,000 - ₦200,000)",
        "opportunities": [
            {
                "title": "Dropshipping Business",
                "capital_needed": "₦50,000 - ₦100,000",
                "skills_needed": ["Digital marketing", "Customer service", "E-commerce"],
                "time_to_first_income": "2-4 weeks",
                "potential_income": {
                    "month_1": "₦30,000 - ₦80,000",
                    "month_3": "₦100,000 - ₦200,000",
                    "month_6": "₦200,000 - ₦500,000+"
                },
                "startup_steps": [
                    "Capital: ₦50,000-80,000 for ads and initial orders",
                    "Week 1: Research trending products, find reliable suppliers",
                    "Week 1-2: Create Instagram/Facebook shop, design brand",
                    "Week 2-3: Run targeted ads (₦10,000-20,000 budget)",
                    "Week 3-4: Process orders, ensure fast delivery",
                    "Month 2+: Scale ads, automate processes, expand product line"
                ],
                "risks": ["Supplier reliability", "Shipping delays", "Ad costs"],
                "success_tips": ["Test products before scaling", "Excellent customer service", "Fast response times"]
            }
        ]
    }
}

# Discovery questions for uncertain students
DISCOVERY_QUESTIONS = {
    "skills_assessment": [
        "What subjects or activities do you naturally excel at?",
        "What do friends/family often ask you for help with?",
        "What hobbies or interests do you have?",
        "Are you more creative (design, art) or analytical (numbers, logic)?",
        "Do you prefer working with people or independently?"
    ],
    "capital_assessment": [
        "How much money can you invest to start? (Be realistic)",
        "Do you have any savings you can use?",
        "Can you get financial support from family?",
        "Would you prefer starting with ₦0 or can you invest ₦10k-50k?"
    ],
    "time_assessment": [
        "How many hours per week can you dedicate to this?",
        "Do you need income immediately or can you wait 2-4 weeks?",
        "Are you looking for part-time or full-time income?",
        "What's your academic schedule like?"
    ],
    "goal_assessment": [
        "What's your monthly income target?",
        "Why do you want to make money? (Specific needs or general income?)",
        "Do you want quick cash or to build something long-term?",
        "Are you interested in online or offline opportunities?"
    ]
}

# Problem-solution matching
COMMON_STUDENT_PROBLEMS = {
    "no_capital": {
        "problem": "I have no money to invest",
        "solutions": [
            "Freelance services (writing, design, social media)",
            "Online tutoring",
            "Virtual assistant work",
            "Content creation"
        ]
    },
    "limited_time": {
        "problem": "I have very little free time due to school",
        "solutions": [
            "Freelance gigs (work on your schedule)",
            "Weekend businesses (food, events)",
            "Passive income (digital products once created)"
        ]
    },
    "no_skills": {
        "problem": "I don't have any marketable skills",
        "solutions": [
            "Learn high-income skills (1-2 months): web design, video editing",
            "Start with easy services: virtual assistant, data entry",
            "Reselling businesses: thrift, accessories",
            "Learn as you earn: offer services while improving"
        ]
    },
    "need_quick_money": {
        "problem": "I need money urgently (this week/month)",
        "solutions": [
            "Gig work: TaskRabbit-style services, deliveries",
            "Quick sales: sell unused items, campus services",
            "Immediate services: tutoring, assignment help",
            "Event-based: photography, DJ, catering for parties"
        ]
    }
}

def get_opportunities_by_capital(max_capital):
    """Return opportunities within student's budget"""
    opportunities = []
    
    if max_capital == 0:
        # Return all service-based opportunities
        for category in SERVICES.values():
            opportunities.extend(category["opportunities"])
    elif max_capital <= 50000:
        # Services + low capital businesses
        for category in SERVICES.values():
            opportunities.extend(category["opportunities"])
        opportunities.extend(BUSINESSES["low_capital"]["opportunities"])
    else:
        # All opportunities
        for category in SERVICES.values():
            opportunities.extend(category["opportunities"])
        for category in BUSINESSES.values():
            opportunities.extend(category["opportunities"])
    
    return opportunities

def get_opportunities_by_skills(skill_keywords):
    """Return opportunities matching student's skills"""
    matched_opportunities = []
    skill_keywords_lower = [s.lower() for s in skill_keywords]
    
    # Search through all opportunities
    all_opportunities = []
    for category in SERVICES.values():
        all_opportunities.extend(category["opportunities"])
    for category in BUSINESSES.values():
        all_opportunities.extend(category["opportunities"])
    
    for opp in all_opportunities:
        # Check if any skill keyword matches
        skills_needed = " ".join(opp.get("skills_needed", [])).lower()
        if any(keyword in skills_needed for keyword in skill_keywords_lower):
            matched_opportunities.append(opp)
    
    return matched_opportunities