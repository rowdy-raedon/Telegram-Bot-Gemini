import google.generativeai as genai
from typing import Optional


class GeminiClient:
    """Client for interacting with the Gemini API."""
    
    def __init__(self, api_key: str):
        """Initialize the Gemini client.
        
        Args:
            api_key: Your Gemini API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_response(self, prompt: str) -> str:
        """Generate a response from Gemini based on the given prompt.
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Generated response text
            
        Raises:
            Exception: If the API request fails
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def summarize_email(self, email_content: str) -> str:
        """Summarize email content using Gemini.
        
        Args:
            email_content: The email content to summarize
            
        Returns:
            Summary of the email
        """
        prompt = f"""
        Please provide a concise summary of the following email content:
        
        {email_content}
        
        Focus on the main points, key information, and any action items mentioned.
        """
        return self.generate_response(prompt)
    
    def answer_question_about_email(self, email_content: str, question: str) -> str:
        """Answer a specific question about email content.
        
        Args:
            email_content: The email content
            question: The question to answer
            
        Returns:
            Answer to the question
        """
        prompt = f"""
        Based on the following email content, please answer this question: {question}
        
        Email content:
        {email_content}
        
        Please provide a clear and accurate answer based on the information in the email.
        """
        return self.generate_response(prompt)