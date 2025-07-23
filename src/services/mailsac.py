"""
Mailsac API client service with caching and improved error handling
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import aiohttp
from pydantic import BaseModel, ValidationError

from src.config.constants import APIConstants, LogConstants, StatusCode
from src.config.exceptions import APIError, EmailError, ErrorCode
from src.bot.utils.cache import (
    cached_email_messages, 
    cache_email_messages,
    cached_email_content,
    cache_email_content
)


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
    """Mailsac API service client with caching and connection pooling."""
    
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
        
        # Connection session for pooling
        self._session: Optional[aiohttp.ClientSession] = None
        
        # Timeout configuration
        self._timeout = aiohttp.ClientTimeout(
            total=APIConstants.API_TIMEOUT,
            connect=10
        )
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session with connection pooling."""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(
                limit=100,  # Total connection pool size
                limit_per_host=30,  # Per host connection limit
                ttl_dns_cache=300,  # DNS cache TTL
                use_dns_cache=True,
            )
            
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=self._timeout,
                headers=self.headers
            )
        
        return self._session
    
    async def close(self) -> None:
        """Close HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        retry_count: int = 0,
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request to Mailsac API with retry logic."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Log API request
        self.logger.debug(
            LogConstants.API_REQUEST.format(
                service="Mailsac", 
                method=method, 
                endpoint=endpoint
            )
        )
        
        session = await self._get_session()
        
        try:
            async with session.request(
                method=method,
                url=url,
                **kwargs
            ) as response:
                response_text = await response.text()
                
                if response.status == StatusCode.OK.value:
                    return await response.json() if response_text else {}
                
                elif response.status == StatusCode.NOT_FOUND.value:
                    return {}  # Empty response for not found
                
                elif response.status == StatusCode.UNAUTHORIZED.value:
                    self.logger.error("Mailsac API unauthorized - check API key")
                    raise APIError(
                        service="Mailsac",
                        status_code=response.status,
                        response_text=response_text,
                        error_code=ErrorCode.API_UNAUTHORIZED_ERROR
                    )
                
                elif response.status == StatusCode.TOO_MANY_REQUESTS.value:
                    # Retry with exponential backoff for rate limits
                    if retry_count < APIConstants.MAX_RETRIES:
                        import asyncio
                        delay = APIConstants.RETRY_BACKOFF ** retry_count
                        self.logger.warning(f"Rate limited, retrying in {delay}s")
                        await asyncio.sleep(delay)
                        return await self._make_request(method, endpoint, retry_count + 1, **kwargs)
                    
                    raise APIError(
                        service="Mailsac",
                        status_code=response.status,
                        response_text=response_text,
                        error_code=ErrorCode.API_RATE_LIMIT_ERROR
                    )
                
                elif response.status >= 500:
                    # Retry for server errors
                    if retry_count < APIConstants.MAX_RETRIES:
                        import asyncio
                        delay = APIConstants.RETRY_BACKOFF ** retry_count
                        self.logger.warning(f"Server error, retrying in {delay}s")
                        await asyncio.sleep(delay)
                        return await self._make_request(method, endpoint, retry_count + 1, **kwargs)
                    
                    raise APIError(
                        service="Mailsac",
                        status_code=response.status,
                        response_text=response_text,
                        error_code=ErrorCode.API_SERVER_ERROR
                    )
                
                else:
                    # Log and raise for other errors
                    self.logger.error(
                        LogConstants.API_ERROR.format(
                            service="Mailsac",
                            status_code=response.status,
                            error=response_text
                        )
                    )
                    raise APIError(
                        service="Mailsac",
                        status_code=response.status,
                        response_text=response_text,
                        error_code=ErrorCode.API_CONNECTION_ERROR
                    )
        
        except aiohttp.ClientTimeout:
            if retry_count < APIConstants.MAX_RETRIES:
                import asyncio
                delay = APIConstants.RETRY_BACKOFF ** retry_count
                self.logger.warning(f"Request timeout, retrying in {delay}s")
                await asyncio.sleep(delay)
                return await self._make_request(method, endpoint, retry_count + 1, **kwargs)
            
            raise APIError(
                service="Mailsac",
                status_code=None,
                response_text="Request timeout",
                error_code=ErrorCode.API_TIMEOUT_ERROR
            )
        
        except aiohttp.ClientError as e:
            self.logger.error(f"Mailsac API connection error: {e}")
            raise APIError(
                service="Mailsac",
                status_code=None,
                response_text=str(e),
                error_code=ErrorCode.API_CONNECTION_ERROR
            )
    
    async def get_messages(self, email_address: str) -> List[EmailMessage]:
        """Get messages for an email address with caching."""
        try:
            # Check cache first
            cached_messages = cached_email_messages(email_address)
            if cached_messages is not None:
                return cached_messages
            
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
            
            # Cache the results
            cache_email_messages(email_address, messages, ttl=60)
            
            return messages
            
        except APIError:
            # Re-raise API errors
            raise
        except Exception as e:
            self.logger.error(f"Error fetching messages for {email_address}: {e}")
            raise EmailError(
                operation="fetch",
                email_address=email_address,
                reason=str(e),
                error_code=ErrorCode.EMAIL_FETCH_FAILED
            )
    
    async def get_message_content(
        self, 
        email_address: str, 
        message_id: str
    ) -> Optional[EmailMessage]:
        """Get full message content including body with caching."""
        try:
            # Check cache first
            cached_content = cached_email_content(email_address, message_id)
            if cached_content is not None:
                return cached_content
            
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
            
            # Cache the message content for longer (5 minutes)
            cache_email_content(email_address, message_id, message, ttl=300)
            
            return message
            
        except APIError:
            # Re-raise API errors
            raise
        except Exception as e:
            self.logger.error(f"Error fetching message content: {e}")
            raise EmailError(
                operation="get content",
                email_address=email_address,
                reason=str(e),
                error_code=ErrorCode.EMAIL_FETCH_FAILED
            )
    
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