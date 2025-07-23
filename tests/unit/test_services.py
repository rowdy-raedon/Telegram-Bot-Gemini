"""
Unit tests for services
"""

import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime

from src.services.mailsac import MailsacService, EmailMessage
from src.services.gemini import GeminiService, EmailCategory, SecurityLevel


class TestMailsacService:
    """Test Mailsac service."""
    
    @pytest.fixture
    def mailsac_service(self):
        """Create Mailsac service instance."""
        return MailsacService(api_key="test_key", base_url="https://test.mailsac.com/api")
    
    @pytest.mark.asyncio
    async def test_get_messages_success(self, mailsac_service):
        """Test successful message retrieval."""
        mock_response = [
            {
                "_id": "test123",
                "from": [{"address": "test@example.com"}],
                "subject": "Test Subject",
                "received": "2024-01-01T12:00:00Z"
            }
        ]
        
        with patch.object(mailsac_service, '_make_request', return_value=mock_response):
            messages = await mailsac_service.get_messages("user@mailsac.com")
            
            assert len(messages) == 1
            assert messages[0].id == "test123"
            assert messages[0].from_address == "test@example.com"
            assert messages[0].subject == "Test Subject"
    
    @pytest.mark.asyncio
    async def test_get_messages_empty(self, mailsac_service):
        """Test empty message list."""
        with patch.object(mailsac_service, '_make_request', return_value=[]):
            messages = await mailsac_service.get_messages("user@mailsac.com")
            assert len(messages) == 0
    
    @pytest.mark.asyncio
    async def test_delete_message_success(self, mailsac_service):
        """Test successful message deletion."""
        with patch.object(mailsac_service, '_make_request', return_value={}):
            result = await mailsac_service.delete_message("user@mailsac.com", "test123")
            assert result is True


class TestGeminiService:
    """Test Gemini AI service."""
    
    @pytest.fixture
    def gemini_service(self):
        """Create Gemini service instance."""
        with patch('google.generativeai.configure'):
            with patch('google.generativeai.GenerativeModel'):
                return GeminiService(api_key="test_key")
    
    @pytest.mark.asyncio
    async def test_summarize_email_success(self, gemini_service):
        """Test successful email summarization."""
        mock_summary = "This is a test email summary."
        
        with patch.object(gemini_service, '_generate_content', return_value=mock_summary):
            summary = await gemini_service.summarize_email("Test email content")
            assert summary == mock_summary
    
    @pytest.mark.asyncio
    async def test_summarize_email_failure(self, gemini_service):
        """Test email summarization failure."""
        with patch.object(gemini_service, '_generate_content', return_value=None):
            summary = await gemini_service.summarize_email("Test email content")
            assert "Unable to generate summary" in summary
    
    @pytest.mark.asyncio
    async def test_categorize_email_success(self, gemini_service):
        """Test successful email categorization."""
        with patch.object(gemini_service, '_generate_content', return_value="spam"):
            category = await gemini_service.categorize_email("Spam email content")
            assert category == EmailCategory.SPAM
    
    @pytest.mark.asyncio
    async def test_categorize_email_unknown(self, gemini_service):
        """Test email categorization with unknown result."""
        with patch.object(gemini_service, '_generate_content', return_value="invalid"):
            category = await gemini_service.categorize_email("Unknown email content")
            assert category == EmailCategory.UNKNOWN
    
    @pytest.mark.asyncio
    async def test_assess_email_security(self, gemini_service):
        """Test email security assessment."""
        mock_assessment = """
SECURITY_LEVEL: safe
CONFIDENCE: 95
THREATS: None detected
INDICATORS: No spam indicators
RECOMMENDATIONS: Email appears safe
        """
        
        with patch.object(gemini_service, '_generate_content', return_value=mock_assessment):
            result = await gemini_service.assess_email_security("Safe email content")
            
            assert result["security_level"] == SecurityLevel.SAFE
            assert result["confidence"] == 95