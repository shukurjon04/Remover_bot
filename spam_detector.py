"""
Spam detection module for identifying spam and promotional content
"""
import re
from telegram import Message, MessageOriginChannel, MessageOriginChat
from telegram.constants import ChatType
from config import SPAM_KEYWORDS, URL_PATTERNS, PHONE_PATTERNS, MAX_EMOJIS


class SpamDetector:
    """Detects spam and promotional content in messages"""
    
    def __init__(self):
        # Compile regex patterns for better performance
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            re.IGNORECASE
        )
        self.emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF'
            r'\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+',
            re.UNICODE
        )
    
    def is_spam(self, message: Message) -> tuple[bool, str]:
        """
        Check if a message is spam
        
        Args:
            message: Telegram message object
            
        Returns:
            Tuple of (is_spam, reason)
        """
        if not message.text and not message.caption:
            # Check for forwarded media from channels
            if message.forward_origin and isinstance(message.forward_origin, MessageOriginChannel):
                return True, "Kanaldan forward qilingan media"
            return False, ""
        
        text = (message.text or message.caption or "").lower()
        
        # Check for forwarded messages from channels
        if message.forward_origin and isinstance(message.forward_origin, MessageOriginChannel):
            return True, "Kanaldan forward qilingan xabar"
        
        # Check for URLs
        if self._contains_url(text):
            return True, "URL/link mavjud"
        
        # Check for phone numbers
        if self._contains_phone(text):
            return True, "Telefon raqami mavjud"
        
        # Check for excessive emojis
        if self._has_excessive_emojis(text):
            return True, f"Haddan tashqari emoji ({MAX_EMOJIS}+ ta)"
        
        # Check for promotional keywords
        if self._contains_spam_keywords(text):
            return True, "Reklama kalit so'zlari aniqlandi"
        
        return False, ""
    
    def _contains_url(self, text: str) -> bool:
        """Check if text contains URLs or usernames"""
        # Check with regex for http/https URLs
        if self.url_pattern.search(text):
            return True
        
        # Check for common URL patterns
        for pattern in URL_PATTERNS:
            if pattern in text.lower():
                return True
        
        # Check for @username mentions
        if '@' in text:
            # Simple check for words starting with @
            words = text.split()
            if any(word.startswith('@') and len(word) > 1 for word in words):
                return True
        
        return False
    
    def _contains_phone(self, text: str) -> bool:
        """Check if text contains phone numbers"""
        for pattern in PHONE_PATTERNS:
            if pattern in text:
                return True
        
        # Check for number patterns (simple detection)
        # Look for sequences like: 90 123 45 67 or 901234567
        if re.search(r'\d{2,3}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}', text):
            return True
        
        return False
    
    def _has_excessive_emojis(self, text: str) -> bool:
        """Check if text has too many emojis"""
        emojis = self.emoji_pattern.findall(text)
        total_emojis = sum(len(emoji) for emoji in emojis)
        return total_emojis > MAX_EMOJIS
    
    def _contains_spam_keywords(self, text: str) -> bool:
        """Check if text contains spam keywords"""
        # Count how many spam keywords are present
        keyword_count = sum(1 for keyword in SPAM_KEYWORDS if keyword in text)
        
        # If at least one spam keyword found, likely spam
        # We lowered threshold to 1 for more aggressive filtering
        return keyword_count >= 1
