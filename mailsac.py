import requests
from typing import List, Dict, Optional
import json


class MailsacAPI:
    """Client for interacting with the Mailsac API."""
    
    def __init__(self, api_key: str):
        """Initialize the Mailsac API client.
        
        Args:
            api_key: Your Mailsac API key
        """
        self.api_key = api_key
        self.base_url = "https://mailsac.com/api"
        self.headers = {
            "Mailsac-Key": api_key,
            "Content-Type": "application/json"
        }
    
    def get_messages(self, email_address: str) -> List[Dict]:
        """Get all messages for a specific email address.
        
        Args:
            email_address: The email address to check
            
        Returns:
            List of message dictionaries
            
        Raises:
            requests.RequestException: If the API request fails
        """
        try:
            url = f"{self.base_url}/addresses/{email_address}/messages"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to get messages: {str(e)}")
    
    def get_message_body(self, email_address: str, message_id: str) -> Dict:
        """Get the body of a specific message.
        
        Args:
            email_address: The email address
            message_id: The ID of the message
            
        Returns:
            Message body dictionary
            
        Raises:
            requests.RequestException: If the API request fails
        """
        try:
            url = f"{self.base_url}/addresses/{email_address}/messages/{message_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to get message body: {str(e)}")
    
    def delete_message(self, email_address: str, message_id: str) -> bool:
        """Delete a specific message.
        
        Args:
            email_address: The email address
            message_id: The ID of the message to delete
            
        Returns:
            True if deletion was successful
            
        Raises:
            requests.RequestException: If the API request fails
        """
        try:
            url = f"{self.base_url}/addresses/{email_address}/messages/{message_id}"
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to delete message: {str(e)}")
    
    def check_address_availability(self, email_address: str) -> bool:
        """Check if an email address is available.
        
        Args:
            email_address: The email address to check
            
        Returns:
            True if address is available
        """
        try:
            url = f"{self.base_url}/addresses/{email_address}"
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except requests.RequestException:
            return False