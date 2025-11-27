import streamlit as st
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from utils.security_tools import *
from utils.agent_logic import CyberSecurityAgent
from utils.chat_manager import ChatManager
from utils.business_advisor import BusinessAdvisor

# Load environment variables
load_dotenv()

# Initialize the AI agent, chat manager, and business advisor
@st.cache_resource
def load_agent():
    return CyberSecurityAgent()

@st.cache_resource
def load_chat_manager():
    return ChatManager()

@st.cache_resource
def load_business_advisor():
    return BusinessAdvisor()

# Configure the page
st.set_page_config(
    page_title="Echelon AI",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI with dark mode support
def load_custom_css(dark_mode=False):
    if dark_mode:
        # Dark mode colors
        bg_color = "#0e1117"
        text_color = "#fafafa"
        secondary_bg = "#262730"
        border_color = "#404040"
        gradient_start = "#4a5568"
        gradient_end = "#2d3748"
        input_bg = "#262730"
        input_text = "#fafafa"
    else:
        # Light mode colors
        bg_color = "#ffffff"
        text_color = "#31333f"
        secondary_bg = "#f0f2f6"
        border_color = "#e0e0e0"
        gradient_start = "#667eea"
        gradient_end = "#764ba2"
        input_bg = "#ffffff"
        input_text = "#31333f"
    
    st.markdown(f"""
        <style>
        /* Main app styling */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* All text elements */
        .stApp p, .stApp span, .stApp div, .stApp label {{
            color: {text_color} !important;
        }}
        
        /* Markdown text */
        .stMarkdown, .stMarkdown p, .stMarkdown span {{
            color: {text_color} !important;
        }}
        
        .main-header {{
            text-align: center;
            padding: 1rem 0;
            background: linear-gradient(90deg, {gradient_start} 0%, {gradient_end} 100%);
            color: white !important;
            border-radius: 10px;
            margin-bottom: 2rem;
        }}
        
        .main-header h1, .main-header p {{
            color: white !important;
        }}
        
        /* Chat message styling */
        .stChatMessage {{
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            background-color: {secondary_bg} !important;
        }}
        
        .stChatMessage p, .stChatMessage span, .stChatMessage div {{
            color: {text_color} !important;
        }}
        
        /* Timestamp styling */
        .timestamp {{
            font-size: 0.75rem;
            color: #888 !important;
            margin-top: 0.25rem;
        }}
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: {secondary_bg} !important;
        }}
        
        section[data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}
        
        /* Input fields */
        .stTextInput input, .stTextArea textarea {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {border_color} !important;
        }}
        
        .stChatInput input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
        }}
        
        /* Buttons */
        .stButton button {{
            color: {text_color} !important;
            border-color: {border_color} !important;
        }}
        
        /* Select boxes and dropdowns */
        .stSelectbox label, .stRadio label {{
            color: {text_color} !important;
        }}
        
        /* Info/Success/Warning boxes */
        .stAlert {{
            background-color: {secondary_bg} !important;
            color: {text_color} !important;
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
        }}
        
        /* Metrics and other elements */
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {text_color} !important;
        }}
        </style>
    """, unsafe_allow_html=True)

def export_chat_history():
    """Export chat history as text file"""
    if st.session_state.messages:
        chat_text = "CyberGuardian AI - Chat History\n"
        chat_text += "=" * 50 + "\n\n"
        
        for msg in st.session_state.messages:
            timestamp = msg.get('timestamp', 'N/A')
            role = msg['role'].upper()
            content = msg['content']
            chat_text += f"[{timestamp}] {role}:\n{content}\n\n"
        
        return chat_text
    return None

def main():
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "mode" not in st.session_state:
        st.session_state.mode = "Cybersecurity"
    
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    
    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize business advisor state (track conversation stage per session)
    if "business_stage" not in st.session_state:
        st.session_state.business_stage = "initial"
    
    if "student_profile" not in st.session_state:
        st.session_state.student_profile = {
            "path": None,
            "skills": [],
            "capital": 0,
            "time_available": None,
            "goals": {},
            "interests": []
        }
    
    # Load custom CSS based on dark mode
    load_custom_css(st.session_state.dark_mode)
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🔒 Echelon AI</h1>
            <p style="margin: 0;">Your Intelligent Cybersecurity & Business Consultant</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat manager
    chat_mgr = load_chat_manager()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings & Tools")
        
        # Dark Mode Toggle (at the top)
        st.subheader("🎨 Appearance")
        dark_mode_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
        if dark_mode_toggle != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode_toggle
            st.rerun()
        
        st.markdown("---")
        
        # Mode Selector
        st.subheader("🎯 Select Mode")
        mode_choice = st.radio(
            "Choose your consultation type:",
            ["🔒 Cybersecurity Help", "💼 Income Generation"],
            index=0 if st.session_state.mode == "Cybersecurity" else 1
        )
        
        # Update mode in session state
        if "Cybersecurity" in mode_choice:
            st.session_state.mode = "Cybersecurity"
        else:
            st.session_state.mode = "Income"
        
        st.markdown("---")
        
        # Quick Access Tools (Only for Cybersecurity mode)
        if st.session_state.mode == "Cybersecurity":
            st.subheader("🛠️ Security Tools")
            tool_choice = st.selectbox(
                "Quick Access:",
                ["Chat Consultation", "Password Checker", "Phishing Analyzer", "URL Safety Checker", "WiFi Advisor"]
            )
            
            if tool_choice == "Password Checker":
                st.markdown("### 🔐 Password Strength Checker")
                password = st.text_input("Enter password to check:", type="password", key="pwd_check")
                if password:
                    score, feedback = check_password_strength(password)
                    st.progress(score/100)
                    st.write(f"**Security Score:** {score}%")
                    for tip in feedback:
                        st.write(f"• {tip}")
            
            elif tool_choice == "Phishing Analyzer":
                st.markdown("### 📧 Phishing Email Analyzer")
                email_text = st.text_area("Paste suspicious email:", key="phish_check")
                if st.button("🔍 Analyze Email"):
                    if email_text:
                        with st.spinner("Scanning for phishing indicators..."):
                            result = analyze_phishing_email(email_text)
                            
                            risk_color = {
                                "HIGH": "🔴",
                                "MEDIUM": "🟡",
                                "LOW": "🟢"
                            }
                            st.markdown(f"### {risk_color[result['risk_level']]} Risk Level: {result['risk_level']}")
                            st.info(result['analysis'])
                    else:
                        st.warning("Please paste an email to analyze.")
            
            elif tool_choice == "URL Safety Checker":
                st.markdown("### 🌐 URL Safety Checker")
                st.caption("Powered by VirusTotal")
                url_to_check = st.text_input("Enter URL to check:", placeholder="https://example.com")
                
                if st.button("🔍 Check URL Safety"):
                    if url_to_check:
                        if not url_to_check.startswith(('http://', 'https://')):
                            st.warning("Please include http:// or https:// in the URL")
                        else:
                            with st.spinner("🔍 Scanning URL with VirusTotal..."):
                                result = check_url_safety(url_to_check)
                                
                                if result["status"] == "success":
                                    st.markdown(f"### {result['safety_color']} {result['safety_status']}")
                                    st.info(result['recommendation'])
                                    
                                    # Show scan statistics
                                    col1, col2, col3, col4 = st.columns(4)
                                    with col1:
                                        st.metric("Malicious", result['scan_results']['malicious'])
                                    with col2:
                                        st.metric("Suspicious", result['scan_results']['suspicious'])
                                    with col3:
                                        st.metric("Harmless", result['scan_results']['harmless'])
                                    with col4:
                                        st.metric("Total Scans", result['scan_results']['total_scans'])
                                
                                elif result["status"] == "scanning":
                                    st.info(result['message'])
                                
                                else:
                                    st.error(result['message'])
                    else:
                        st.warning("Please enter a URL to check.")
            
            elif tool_choice == "WiFi Advisor":
                st.markdown("### 🌐 WiFi Security Advisor")
                usage = st.selectbox(
                    "What will you do on this network?",
                    ["Banking", "Social Media", "Work", "General Browsing"]
                )
                if st.button("Get Recommendation"):
                    advice = wifi_security_recommendation(usage.lower())
                    st.success(advice)
        
        else:
            # Income generation mode info
            st.info("💼 **Income Generation Mode Active!**\n\nI can help you:\n- Start a business\n- Offer services\n- Make money as a student\n\nJust start chatting below! 👇")
        
        st.markdown("---")
        
        # Chat History Management
        st.subheader("💾 Chat History")
        
        # Show conversation history
        conversations = chat_mgr.get_conversation_summary()
        if conversations:
            st.write(f"**Saved Conversations:** {len(conversations)}")
            
            selected_conv = st.selectbox(
                "Load previous chat:",
                ["-- New Conversation --"] + [f"{conv['id']} ({conv['message_count']} msgs)" for conv in conversations]
            )
            
            if selected_conv != "-- New Conversation --":
                conv_id = selected_conv.split(" ")[0]
                if st.button("📂 Load Selected"):
                    loaded_messages = chat_mgr.load_conversation(conv_id)
                    if loaded_messages:
                        st.session_state.messages = loaded_messages
                        st.success("Chat loaded!")
                        st.rerun()
        else:
            st.info("No saved conversations yet")
        
        # Save current conversation
        if st.session_state.messages:
            if st.button("💾 Save Current Chat"):
                success = chat_mgr.save_conversation(
                    st.session_state.messages,
                    st.session_state.current_session_id
                )
                if success:
                    st.success("Chat saved!")
                else:
                    st.error("Failed to save chat")
        
        st.markdown("---")
        
        # Export Chat Button
        st.subheader("📥 Export")
        if st.button("📥 Export Current Chat"):
            chat_export = export_chat_history()
            if chat_export:
                st.download_button(
                    label="Download Chat (TXT)",
                    data=chat_export,
                    file_name=f"cyberguardian_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            else:
                st.warning("No chat history to export yet.")
        
        # Clear all history
        st.markdown("---")
        if st.button("⚠️ Delete All History", type="secondary"):
            if chat_mgr.clear_all_history():
                st.session_state.messages = []
                st.session_state.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.session_state.business_stage = "initial"
                st.session_state.student_profile = {
                    "path": None,
                    "skills": [],
                    "capital": 0,
                    "time_available": None,
                    "goals": {},
                    "interests": []
                }
                st.success("All history cleared!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Failed to clear history")
    
    # Main chat interface
    if st.session_state.mode == "Cybersecurity":
        st.header("💬 Cybersecurity Consultation")
        st.markdown("Ask me anything about cybersecurity, online safety, or digital protection.")
    else:
        st.header("💼 Income Generation Guidance")
        st.markdown("Get personalized advice on starting a business or offering services as a student.")
        st.info("💡 **Tip:** Tell me about your situation, and I'll guide you step-by-step!")
    
    # Display chat messages with timestamps
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "timestamp" in message:
                st.markdown(f'<p class="timestamp">{message["timestamp"]}</p>', unsafe_allow_html=True)
    
    # Chat input
    prompt = st.chat_input("Ask about cybersecurity..." if st.session_state.mode == "Cybersecurity" else "Tell me what you're interested in...")
    
    if prompt:
        # Get current timestamp
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": current_time
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
            st.markdown(f'<p class="timestamp">{current_time}</p>', unsafe_allow_html=True)
        
        # Get AI response with streaming and typing indicator
        with st.chat_message("assistant"):
            # Typing indicator
            with st.spinner("🤔 CyberGuardian is thinking..."):
                time.sleep(0.5)
            
            message_placeholder = st.empty()
            full_response = ""
            
            # Load appropriate agent based on mode
            if st.session_state.mode == "Cybersecurity":
                agent = load_agent()
                response_generator = agent.process_query(
                    prompt,
                    st.session_state.messages  # Pass full chat history
                )
                
                # Stream the response with typewriter effect
                for chunk in response_generator:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.01)
                
                message_placeholder.markdown(full_response)
            
            else:
                # Income generation mode - use business advisor
                business_advisor = load_business_advisor()
                
                # Update advisor's state from session state
                business_advisor.conversation_stage = st.session_state.business_stage
                business_advisor.student_profile = st.session_state.student_profile
                
                response_generator = business_advisor.process_income_query(
                    prompt, 
                    st.session_state.messages
                )
                
                # Stream the response
                for chunk in response_generator:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.01)
                
                message_placeholder.markdown(full_response)
                
                # Save updated state back to session
                st.session_state.business_stage = business_advisor.conversation_stage
                st.session_state.student_profile = business_advisor.student_profile
            
            # Add timestamp
            response_time = datetime.now().strftime("%H:%M:%S")
            st.markdown(f'<p class="timestamp">{response_time}</p>', unsafe_allow_html=True)
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "timestamp": response_time
        })

if __name__ == "__main__":

    main()

