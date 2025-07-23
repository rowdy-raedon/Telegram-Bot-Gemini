"""
Caching utilities for improved performance
"""

import time
import hashlib
import logging
from typing import Any, Optional, Dict, Tuple
from datetime import datetime, timedelta

from src.config.constants import APIConstants, LogConstants

logger = logging.getLogger(__name__)


class MemoryCache:
    """Simple in-memory cache with TTL support."""
    
    def __init__(self, max_size: int = APIConstants.MAX_CACHE_SIZE):
        """Initialize memory cache."""
        self.max_size = max_size
        self.cache: Dict[str, Tuple[Any, float]] = {}  # key -> (value, expiry_time)
        self._access_times: Dict[str, float] = {}  # For LRU eviction
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        key_data = f"{args}{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_expired(self, expiry_time: float) -> bool:
        """Check if cache entry is expired."""
        return time.time() > expiry_time
    
    def _evict_expired(self) -> None:
        """Remove expired entries."""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.cache.items()
            if current_time > expiry
        ]
        
        for key in expired_keys:
            self.cache.pop(key, None)
            self._access_times.pop(key, None)
    
    def _evict_lru(self) -> None:
        """Remove least recently used entries if cache is full."""
        while len(self.cache) >= self.max_size:
            # Find least recently used key
            lru_key = min(self._access_times.keys(), key=lambda k: self._access_times[k])
            self.cache.pop(lru_key, None)
            self._access_times.pop(lru_key, None)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self.cache:
            logger.debug(LogConstants.CACHE_MISS.format(key=key))
            return None
        
        value, expiry_time = self.cache[key]
        
        if self._is_expired(expiry_time):
            self.cache.pop(key, None)
            self._access_times.pop(key, None)
            logger.debug(LogConstants.CACHE_MISS.format(key=key))
            return None
        
        # Update access time for LRU
        self._access_times[key] = time.time()
        logger.debug(LogConstants.CACHE_HIT.format(key=key))
        return value
    
    def set(self, key: str, value: Any, ttl: int = APIConstants.CACHE_TTL_SECONDS) -> None:
        """Set value in cache with TTL."""
        # Clean up expired entries
        self._evict_expired()
        
        # Evict LRU entries if needed
        self._evict_lru()
        
        expiry_time = time.time() + ttl
        self.cache[key] = (value, expiry_time)
        self._access_times[key] = time.time()
        
        logger.debug(f"Cached value for key: {key} (TTL: {ttl}s)")
    
    def delete(self, key: str) -> None:
        """Delete key from cache."""
        self.cache.pop(key, None)
        self._access_times.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        self._access_times.clear()
        logger.info("Cache cleared")
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        current_time = time.time()
        active_entries = sum(
            1 for _, expiry in self.cache.values()
            if current_time <= expiry
        )
        
        return {
            "total_entries": len(self.cache),
            "active_entries": active_entries,
            "max_size": self.max_size,
            "utilization": len(self.cache) / self.max_size if self.max_size > 0 else 0
        }


# Global cache instance
_cache = MemoryCache()


def cache_result(ttl: int = APIConstants.CACHE_TTL_SECONDS, key_prefix: str = ""):
    """Decorator to cache function results."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{_cache._generate_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_result = _cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            _cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator


def get_cache_stats() -> Dict[str, Any]:
    """Get global cache statistics."""
    return _cache.stats()


def clear_cache() -> None:
    """Clear global cache."""
    _cache.clear()


def cached_email_messages(email_address: str, ttl: int = 60) -> Optional[Any]:
    """Get cached email messages."""
    key = f"messages:{email_address}"
    return _cache.get(key)


def cache_email_messages(email_address: str, messages: Any, ttl: int = 60) -> None:
    """Cache email messages."""
    key = f"messages:{email_address}"
    _cache.set(key, messages, ttl)


def cached_email_content(email_address: str, message_id: str, ttl: int = 300) -> Optional[Any]:
    """Get cached email content."""
    key = f"content:{email_address}:{message_id}"
    return _cache.get(key)


def cache_email_content(email_address: str, message_id: str, content: Any, ttl: int = 300) -> None:
    """Cache email content."""
    key = f"content:{email_address}:{message_id}"
    _cache.set(key, content, ttl)


def cached_ai_response(content_hash: str, operation: str, ttl: int = 1800) -> Optional[Any]:
    """Get cached AI response."""
    key = f"ai:{operation}:{content_hash}"
    return _cache.get(key)


def cache_ai_response(content_hash: str, operation: str, response: Any, ttl: int = 1800) -> None:
    """Cache AI response."""
    key = f"ai:{operation}:{content_hash}"
    _cache.set(key, response, ttl)


def generate_content_hash(content: str) -> str:
    """Generate hash for content caching."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]