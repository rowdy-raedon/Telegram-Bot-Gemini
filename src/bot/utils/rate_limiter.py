"""
Rate limiting utilities for API protection
"""

import time
import logging
from typing import Dict, Tuple, Optional
from collections import defaultdict, deque

from src.config.constants import APIConstants, SecurityConstants
from src.config.exceptions import RateLimitError

logger = logging.getLogger(__name__)


class TokenBucket:
    """Token bucket rate limiter implementation."""
    
    def __init__(self, capacity: int, refill_rate: float):
        """Initialize token bucket.
        
        Args:
            capacity: Maximum number of tokens
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
    
    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens.
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens were consumed, False otherwise
        """
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        
        return False
    
    def available_tokens(self) -> int:
        """Get number of available tokens."""
        self._refill()
        return int(self.tokens)
    
    def time_until_available(self, tokens: int = 1) -> float:
        """Get time until specified tokens are available."""
        self._refill()
        
        if self.tokens >= tokens:
            return 0.0
        
        needed_tokens = tokens - self.tokens
        return needed_tokens / self.refill_rate


class SlidingWindowRateLimiter:
    """Sliding window rate limiter."""
    
    def __init__(self, max_requests: int, window_seconds: int):
        """Initialize sliding window rate limiter."""
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, deque] = defaultdict(deque)
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed."""
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        request_times = self.requests[key]
        while request_times and request_times[0] < window_start:
            request_times.popleft()
        
        # Check if under limit
        if len(request_times) < self.max_requests:
            request_times.append(now)
            return True
        
        return False
    
    def get_remaining_requests(self, key: str) -> int:
        """Get remaining requests in window."""
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        request_times = self.requests[key]
        while request_times and request_times[0] < window_start:
            request_times.popleft()
        
        return max(0, self.max_requests - len(request_times))
    
    def get_reset_time(self, key: str) -> float:
        """Get time when window resets."""
        request_times = self.requests[key]
        if not request_times:
            return 0.0
        
        return request_times[0] + self.window_seconds


class RateLimiter:
    """Main rate limiter with multiple strategies."""
    
    def __init__(self):
        """Initialize rate limiter."""
        # User rate limiting (per minute)
        self.user_limiter = SlidingWindowRateLimiter(
            max_requests=SecurityConstants.USER_RATE_LIMIT,
            window_seconds=60
        )
        
        # Global rate limiting (per minute)
        self.global_limiter = SlidingWindowRateLimiter(
            max_requests=SecurityConstants.GLOBAL_RATE_LIMIT,
            window_seconds=60
        )
        
        # API rate limiting (per minute)
        self.api_limiter = SlidingWindowRateLimiter(
            max_requests=APIConstants.MAX_REQUESTS_PER_MINUTE,
            window_seconds=60
        )
        
        # Token buckets for burst protection
        self.user_buckets: Dict[str, TokenBucket] = {}
    
    def _get_user_bucket(self, user_id: str) -> TokenBucket:
        """Get or create token bucket for user."""
        if user_id not in self.user_buckets:
            self.user_buckets[user_id] = TokenBucket(
                capacity=10,  # Allow burst of 10 requests
                refill_rate=0.5  # Refill 0.5 tokens per second (30 per minute)
            )
        return self.user_buckets[user_id]
    
    def check_user_rate_limit(self, user_id: str) -> None:
        """Check user rate limit."""
        user_key = f"user:{user_id}"
        
        # Check sliding window
        if not self.user_limiter.is_allowed(user_key):
            reset_time = self.user_limiter.get_reset_time(user_key)
            retry_after = int(reset_time - time.time())
            
            logger.warning(f"User {user_id} hit rate limit")
            raise RateLimitError("user", retry_after)
        
        # Check token bucket for burst protection
        bucket = self._get_user_bucket(user_id)
        if not bucket.consume():
            retry_after = int(bucket.time_until_available())
            
            logger.warning(f"User {user_id} hit burst limit")
            raise RateLimitError("burst", retry_after)
    
    def check_global_rate_limit(self) -> None:
        """Check global rate limit."""
        if not self.global_limiter.is_allowed("global"):
            reset_time = self.global_limiter.get_reset_time("global")
            retry_after = int(reset_time - time.time())
            
            logger.warning("Global rate limit exceeded")
            raise RateLimitError("global", retry_after)
    
    def check_api_rate_limit(self, service: str) -> None:
        """Check API rate limit."""
        api_key = f"api:{service}"
        
        if not self.api_limiter.is_allowed(api_key):
            reset_time = self.api_limiter.get_reset_time(api_key)
            retry_after = int(reset_time - time.time())
            
            logger.warning(f"API rate limit exceeded for {service}")
            raise RateLimitError(f"api:{service}", retry_after)
    
    def get_user_stats(self, user_id: str) -> Dict[str, int]:
        """Get rate limit stats for user."""
        user_key = f"user:{user_id}"
        bucket = self._get_user_bucket(user_id)
        
        return {
            "remaining_requests": self.user_limiter.get_remaining_requests(user_key),
            "available_tokens": bucket.available_tokens(),
            "window_reset": int(self.user_limiter.get_reset_time(user_key))
        }
    
    def get_global_stats(self) -> Dict[str, int]:
        """Get global rate limit stats."""
        return {
            "remaining_requests": self.global_limiter.get_remaining_requests("global"),
            "window_reset": int(self.global_limiter.get_reset_time("global"))
        }


# Global rate limiter instance
_rate_limiter = RateLimiter()


def check_rate_limits(user_id: str, service: Optional[str] = None) -> None:
    """Check all applicable rate limits."""
    try:
        # Check global rate limit first
        _rate_limiter.check_global_rate_limit()
        
        # Check user rate limit
        _rate_limiter.check_user_rate_limit(str(user_id))
        
        # Check API rate limit if service specified
        if service:
            _rate_limiter.check_api_rate_limit(service)
            
    except RateLimitError:
        # Re-raise rate limit errors
        raise
    except Exception as e:
        logger.error(f"Error checking rate limits: {e}")
        # Don't block on rate limiter errors


def get_user_rate_limit_stats(user_id: str) -> Dict[str, int]:
    """Get rate limit statistics for user."""
    return _rate_limiter.get_user_stats(str(user_id))


def get_global_rate_limit_stats() -> Dict[str, int]:
    """Get global rate limit statistics."""
    return _rate_limiter.get_global_stats()


def rate_limit_middleware(service: str = "bot"):
    """Decorator for rate limiting functions."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract user_id from message or callback
            user_id = None
            for arg in args:
                if hasattr(arg, 'from_user') and hasattr(arg.from_user, 'id'):
                    user_id = arg.from_user.id
                    break
            
            if user_id:
                check_rate_limits(user_id, service)
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator