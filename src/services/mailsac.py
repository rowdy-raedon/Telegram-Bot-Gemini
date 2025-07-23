"""
Mailsac API client service
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import aiohttp
from pydantic import BaseModel, ValidationError


class EmailMessage(BaseModel):
    """Email message model."""
    id: str
    from_address: str
    to_address: str
    subject: str
    received: datetime
    body: Optional[str] = None
    attachments: List[Dict[str, Any]] = []


class MailsacService:
    """Mailsac API service client."""
    
    def __init__(self, api_key: str, base_url: str = "https://mailsac.com/api"):
        """Initialize Mailsac service."""
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.logger = logging.getLogger(__name__)
        
        # Headers for API requests
        self.headers = {
            'Mailsac-Key': self.api_key,
            'Content-Type': 'application/json'
        }
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request to Mailsac API."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    **kwargs
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 404:
                        return {}  # Empty response for not found
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Mailsac API error {response.status}: {error_text}")
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=error_text
                        )
            except aiohttp.ClientError as e:
                self.logger.error(f"Mailsac API request failed: {e}")
                raise
    
    async def get_messages(self, email_address: str) -> List[EmailMessage]:
        """Get messages for an email address."""
        try:
            # Extract local part of email (before @)
            local_part = email_address.split('@')[0]
            
            # Get messages from API
            response = await self._make_request(
                'GET', 
                f'/addresses/{local_part}/messages'
            )
            
            messages = []
            for msg_data in response:
                try:
                    # Parse message data
                    message = EmailMessage(
                        id=msg_data.get('_id', ''),
                        from_address=msg_data.get('from', [{}])[0].get('address', ''),
                        to_address=email_address,
                        subject=msg_data.get('subject', 'No Subject'),
                        received=datetime.fromisoformat(
                            msg_data.get('received', '').replace('Z', '+00:00')
                        )
                    )
                    messages.append(message)
                except (ValidationError, ValueError) as e:
                    self.logger.warning(f"Failed to parse message: {e}")
                    continue
            
            return messages
            
        except Exception as e:
            self.logger.error(f"Error fetching messages for {email_address}: {e}")
            raise
    
    async def get_message_content(
        self, 
        email_address: str, 
        message_id: str
    ) -> Optional[EmailMessage]:
        """Get full message content including body."""
        try:
            local_part = email_address.split('@')[0]
            
            # Get message body
            response = await self._make_request(
                'GET',
                f'/text/{local_part}/{message_id}'
            )
            
            if not response:
                return None
            
            # Parse full message
            message = EmailMessage(
                id=message_id,
                from_address=response.get('from', [{}])[0].get('address', ''),
                to_address=email_address,
                subject=response.get('subject', 'No Subject'),
                received=datetime.fromisoformat(
                    response.get('received', '').replace('Z', '+00:00')
                ),
                body=response.get('body', '')
            )
            
            return message
            
        except Exception as e:
            self.logger.error(f"Error fetching message content: {e}")
            raise
    
    async def delete_message(self, email_address: str, message_id: str) -> bool:
        """Delete a specific message."""
        try:
            local_part = email_address.split('@')[0]
            
            await self._make_request(
                'DELETE',
                f'/addresses/{local_part}/messages/{message_id}'
            )
            
            self.logger.info(f"Deleted message {message_id} from {email_address}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting message: {e}")
            return False
    
    async def delete_all_messages(self, email_address: str) -> bool:
        """Delete all messages for an email address."""
        try:
            local_part = email_address.split('@')[0]
            
            await self._make_request(
                'DELETE',
                f'/addresses/{local_part}/messages'
            )
            
            self.logger.info(f"Deleted all messages for {email_address}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting all messages: {e}")
            return False
    
    async def check_email_availability(self, email_address: str) -> bool:
        """Check if an email address is available."""
        try:
            messages = await self.get_messages(email_address)
            return True  # If no error, email is accessible
        except Exception:
            return False