import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_password_strength(password):
    """Analyze password strength and provide feedback"""
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 12:
        score += 25
        feedback.append("✅ Good length (12+ characters)")
    elif len(password) >= 8:
        score += 15
        feedback.append("⚠️ Consider longer password (12+ characters recommended)")
    else:
        feedback.append("❌ Password too short (minimum 8 characters)")
    
    # Complexity checks
    if re.search(r"[A-Z]", password):
        score += 15
        feedback.append("✅ Contains uppercase letters")
    else:
        feedback.append("❌ Add uppercase letters")
    
    if re.search(r"[a-z]", password):
        score += 15
        feedback.append("✅ Contains lowercase letters")
    else:
        feedback.append("❌ Add lowercase letters")
    
    if re.search(r"\d", password):
        score += 15
        feedback.append("✅ Contains numbers")
    else:
        feedback.append("❌ Add numbers")
    
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 20
        feedback.append("✅ Contains special characters")
    else:
        feedback.append("❌ Add special characters")
    
    # Common password check
    common_passwords = ["password", "123456", "qwerty", "letmein"]
    if password.lower() in common_passwords:
        score = 0
        feedback.append("❌ This is a commonly used password - choose something unique")
    
    # Sequential check
    if re.search(r"(.)\1{2,}", password):
        score -= 10
        feedback.append("❌ Avoid repeated characters")
    
    return min(score, 100), feedback

def analyze_phishing_email(email_text):
    """Analyze email for phishing indicators"""
    indicators = {
        "urgent_language": len(re.findall(r'urgent|immediately|quick|action required', email_text.lower())),
        "suspicious_links": len(re.findall(r'http://|https?://[^\s]+', email_text)),
        "grammar_errors": len(re.findall(r"\b(?:their|there|you're|your)\b", email_text.lower())),
        "request_personal_info": len(re.findall(r'password|account|login|verify|confirm', email_text.lower()))
    }
    
    risk_score = sum(indicators.values())
    
    if risk_score >= 5:
        risk_level = "HIGH"
        analysis = "Multiple phishing indicators detected. Do not click links or provide information."
    elif risk_score >= 3:
        risk_level = "MEDIUM"
        analysis = "Several suspicious elements found. Proceed with caution."
    else:
        risk_level = "LOW"
        analysis = "Few indicators detected, but always verify sender authenticity."
    
    return {
        "risk_level": risk_level,
        "analysis": analysis,
        "indicators_found": indicators
    }

def wifi_security_recommendation(usage_type):
    """Provide WiFi security recommendations based on usage"""
    recommendations = {
        "banking": "Use VPN and avoid public WiFi for banking. If essential, use mobile data.",
        "social": "Public WiFi acceptable, but avoid logging into sensitive accounts.",
        "work": "Use company VPN. Avoid accessing confidential documents on public networks.",
        "browsing": "Public WiFi acceptable for general browsing. Use HTTPS sites only."
    }
    return recommendations.get(usage_type.lower(), "Use VPN for all activities on public WiFi.")

def check_url_safety(url):
    """
    Check URL safety using VirusTotal API
    Returns: dict with safety status and details
    """
    api_key = os.getenv("VIRUSTOTAL_API_KEY")
    
    if not api_key:
        return {
            "status": "error",
            "message": "VirusTotal API key not configured. Please add VIRUSTOTAL_API_KEY to your .env file."
        }
    
    try:
        # VirusTotal API v3 endpoint
        headers = {
            "x-apikey": api_key
        }
        
        # Step 1: Submit URL for scanning
        scan_url = "https://www.virustotal.com/api/v3/urls"
        
        # Encode the URL
        import base64
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        
        # Step 2: Get analysis results
        analysis_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        
        response = requests.get(analysis_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            stats = data['data']['attributes']['last_analysis_stats']
            
            malicious = stats.get('malicious', 0)
            suspicious = stats.get('suspicious', 0)
            harmless = stats.get('harmless', 0)
            undetected = stats.get('undetected', 0)
            
            total_scans = malicious + suspicious + harmless + undetected
            
            # Determine safety level
            if malicious > 0 or suspicious > 2:
                safety_status = "DANGEROUS"
                safety_color = "🔴"
                recommendation = "DO NOT VISIT - This URL has been flagged as malicious by security vendors."
            elif suspicious > 0:
                safety_status = "SUSPICIOUS"
                safety_color = "🟡"
                recommendation = "Exercise caution - Some vendors flagged this URL as suspicious."
            else:
                safety_status = "SAFE"
                safety_color = "🟢"
                recommendation = "This URL appears safe based on current analysis."
            
            return {
                "status": "success",
                "url": url,
                "safety_status": safety_status,
                "safety_color": safety_color,
                "recommendation": recommendation,
                "scan_results": {
                    "malicious": malicious,
                    "suspicious": suspicious,
                    "harmless": harmless,
                    "undetected": undetected,
                    "total_scans": total_scans
                }
            }
        
        elif response.status_code == 404:
            # URL not in database, submit for scanning
            submit_response = requests.post(
                scan_url,
                headers=headers,
                data={"url": url},
                timeout=10
            )
            
            if submit_response.status_code == 200:
                return {
                    "status": "scanning",
                    "message": "URL submitted for analysis. This may take a few moments. Please try again in 30 seconds."
                }
        
        return {
            "status": "error",
            "message": f"Unable to check URL. API returned status code: {response.status_code}"
        }
    
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "Request timed out. Please try again."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error checking URL: {str(e)}"
        }