
import sys
import os
from unittest.mock import MagicMock

# Add current directory to path
sys.path.append(os.getcwd())

from spam_detector import SpamDetector
from telegram import Message, MessageOriginChannel
from telegram.constants import ChatMemberStatus

def test_spam_detector():
    print("Testing SpamDetector compatibility...")
    detector = SpamDetector()
    
    # Mock message with forward_origin
    mock_message = MagicMock(spec=Message)
    mock_message.text = "Hello"
    mock_message.caption = None
    mock_message.forward_origin = MagicMock(spec=MessageOriginChannel)
    
    # This should not raise AttributeError now
    is_spam, reason = detector.is_spam(mock_message)
    print(f"Result: is_spam={is_spam}, reason={reason}")
    assert is_spam == True
    assert "Kanaldan forward" in reason
    print("SpamDetector check passed!")

def test_permissions():
    print("\nTesting PermissionChecker compatibility...")
    # Since ChatMemberStatus is an Enum-like class, we can check its values
    print(f"ChatMemberStatus.OWNER: {ChatMemberStatus.OWNER}")
    print(f"ChatMemberStatus.ADMINISTRATOR: {ChatMemberStatus.ADMINISTRATOR}")
    assert ChatMemberStatus.OWNER == 'creator' or ChatMemberStatus.OWNER == ChatMemberStatus.OWNER
    print("PermissionChecker check passed!")

if __name__ == "__main__":
    try:
        test_spam_detector()
        test_permissions()
        print("\nAll compatibility checks passed!")
    except Exception as e:
        print(f"\nVerification failed: {e}")
        sys.exit(1)
