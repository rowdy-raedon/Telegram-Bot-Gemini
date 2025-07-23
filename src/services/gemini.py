"""
Google Gemini AI service integration
"""

import logging
from typing import Optional, List, Dict, Any
from enum import Enum

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


class EmailCategory(Enum):
    """Email category classifications."""
    SPAM = "spam"
    PROMOTIONAL = "promotional"
    PERSONAL = "personal"
    BUSINESS = "business"
    VERIFICATION = "verification"
    NEWSLETTER = "newsletter"
    SECURITY = "security"
    UNKNOWN = "unknown"


class SecurityLevel(Enum):
    """Email security assessment levels."""
    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    DANGEROUS = "dangerous"
    UNKNOWN = "unknown"


class GeminiService:
    """Google Gemini AI service client."""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        """Initialize Gemini service."""
        self.api_key = api_key
        self.model_name = model
        self.logger = logging.getLogger(__name__)
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize model with safety settings
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
        )
        
        self.logger.info(f"✅ Gemini service initialized with model: {self.model_name}")
    
    async def _generate_content(self, prompt: str, **kwargs) -> Optional[str]:
        """Generate content using Gemini model."""
        try:
            response = self.model.generate_content(prompt, **kwargs)
            
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text.strip()
            else:
                self.logger.warning("No valid response from Gemini")
                return None
                
        except Exception as e:
            self.logger.error(f"Gemini generation error: {e}")
            return None
    
    async def summarize_email(self, email_content: str, max_length: int = 150) -> str:
        """Generate a concise summary of an email."""
        prompt = f"""
Please provide a concise summary of the following email in {max_length} characters or less.
Focus on the main points, key information, and any action items.

Email content:
{email_content}

Summary:
        """
        
        try:
            summary = await self._generate_content(prompt)
            return summary or "Unable to generate summary for this email."
        except Exception as e:
            self.logger.error(f"Error summarizing email: {e}")
            return "Error occurred while generating summary."
    
    async def answer_question_about_email(
        self, 
        email_content: str, 
        question: str
    ) -> str:
        """Answer a specific question about email content."""
        prompt = f"""
Based on the following email content, please answer this question: "{question}"

Provide a clear, accurate, and helpful response. If the information is not available in the email, please state that clearly.

Email content:
{email_content}

Question: {question}

Answer:
        """
        
        try:
            answer = await self._generate_content(prompt)
            return answer or "I couldn't find enough information in the email to answer your question."
        except Exception as e:
            self.logger.error(f"Error answering question: {e}")
            return "Error occurred while processing your question."
    
    async def categorize_email(self, email_content: str) -> EmailCategory:
        """Categorize email into predefined categories."""
        prompt = f"""
Analyze the following email and categorize it into one of these categories:
- spam: Unwanted promotional or malicious emails
- promotional: Marketing emails from legitimate businesses
- personal: Personal communication from individuals
- business: Professional/work-related emails
- verification: Account verification, password resets, confirmations
- newsletter: Subscribed newsletters and updates
- security: Security alerts, warnings, notifications
- unknown: Cannot be clearly categorized

Email content:
{email_content}

Respond with only the category name (lowercase).
        """
        
        try:
            result = await self._generate_content(prompt)
            if result:
                category_str = result.lower().strip()
                try:
                    return EmailCategory(category_str)
                except ValueError:
                    pass
            
            return EmailCategory.UNKNOWN
        except Exception as e:
            self.logger.error(f"Error categorizing email: {e}")
            return EmailCategory.UNKNOWN
    
    async def assess_email_security(self, email_content: str) -> Dict[str, Any]:
        """Assess email for security threats and spam indicators."""
        prompt = f"""
Analyze this email for security threats and spam indicators. Provide assessment in this format:

SECURITY_LEVEL: [safe/suspicious/dangerous]
CONFIDENCE: [0-100]
THREATS: [list any threats found]
INDICATORS: [list spam/phishing indicators]
RECOMMENDATIONS: [safety recommendations]

Email content:
{email_content}

Assessment:
        """
        
        try:
            assessment = await self._generate_content(prompt)
            if not assessment:
                return {
                    "security_level": SecurityLevel.UNKNOWN,
                    "confidence": 0,
                    "threats": [],
                    "indicators": [],
                    "recommendations": ["Unable to assess email security"]
                }
            
            # Parse assessment (simplified parsing)
            lines = assessment.split('\n')
            result = {
                "security_level": SecurityLevel.UNKNOWN,
                "confidence": 0,
                "threats": [],
                "indicators": [],
                "recommendations": []
            }
            
            for line in lines:
                line = line.strip()
                if line.startswith('SECURITY_LEVEL:'):
                    level_str = line.split(':', 1)[1].strip().lower()
                    try:
                        result["security_level"] = SecurityLevel(level_str)
                    except ValueError:
                        pass
                elif line.startswith('CONFIDENCE:'):
                    try:
                        result["confidence"] = int(line.split(':', 1)[1].strip())
                    except ValueError:
                        pass
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error assessing email security: {e}")
            return {
                "security_level": SecurityLevel.UNKNOWN,
                "confidence": 0,
                "threats": ["Error during security assessment"],
                "indicators": [],
                "recommendations": ["Manual review recommended"]
            }
    
    async def translate_email(
        self, 
        email_content: str, 
        target_language: str = "en"
    ) -> str:
        """Translate email content to specified language."""
        prompt = f"""
Translate the following email content to {target_language}. 
Maintain the original formatting and tone as much as possible.

Email content:
{email_content}

Translation:
        """
        
        try:
            translation = await self._generate_content(prompt)
            return translation or "Translation failed."
        except Exception as e:
            self.logger.error(f"Error translating email: {e}")
            return "Error occurred during translation."
    
    async def extract_key_information(self, email_content: str) -> Dict[str, List[str]]:
        """Extract key information like dates, phone numbers, links, etc."""
        prompt = f"""
Extract key information from this email and organize it into categories:

DATES: [any dates mentioned]
PHONE_NUMBERS: [any phone numbers]
EMAIL_ADDRESSES: [any email addresses]
LINKS: [any URLs or links]
MONEY_AMOUNTS: [any monetary amounts]
IMPORTANT_INFO: [any other important information]

Email content:
{email_content}

Extracted information:
        """
        
        try:
            extraction = await self._generate_content(prompt)
            # Simplified parsing - in production, you'd want more robust parsing
            return {
                "dates": [],
                "phone_numbers": [],
                "email_addresses": [],
                "links": [],
                "money_amounts": [],
                "important_info": [extraction or "No key information extracted"]
            }
        except Exception as e:
            self.logger.error(f"Error extracting information: {e}")
            return {
                "dates": [],
                "phone_numbers": [],
                "email_addresses": [],
                "links": [],
                "money_amounts": [],
                "important_info": ["Error during information extraction"]
            }