
import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock

# Add current directory to path
sys.path.append(os.getcwd())

from permissions import PermissionChecker
from telegram import User, Chat, Message, ChatMember
from telegram.constants import ChatMemberStatus

async def test_admin_logic():
    print("Testing improved PermissionChecker logic...")
    checker = PermissionChecker()
    
    mock_chat = MagicMock(spec=Chat)
    mock_chat.id = 12345
    
    mock_context = MagicMock()
    mock_context.bot.get_chat_member = AsyncMock()
    
    # 1. Test Telegram Service account
    service_user = MagicMock(spec=User)
    service_user.id = 777000
    is_admin = await checker.is_admin_or_owner(mock_chat, service_user, mock_context)
    print(f"Service account check (ID 777000): {is_admin}")
    assert is_admin == True

    # 2. Test Anonymous Admin ID
    anon_user = MagicMock(spec=User)
    anon_user.id = 1087968824
    is_admin = await checker.is_admin_or_owner(mock_chat, anon_user, mock_context)
    print(f"Anonymous Admin ID check (ID 1087968824): {is_admin}")
    assert is_admin == True

    # 3. Test sender_chat (Anonymous admin via group)
    regular_user = MagicMock(spec=User)
    regular_user.id = 999
    
    mock_message_group = MagicMock(spec=Message)
    mock_message_group.sender_chat = mock_chat
    
    is_admin = await checker.is_admin_or_owner(mock_chat, regular_user, mock_context, message=mock_message_group)
    print(f"sender_chat group check: {is_admin}")
    assert is_admin == True

    # 4. Test sender_chat (Linked channel)
    mock_channel = MagicMock(spec=Chat)
    mock_channel.id = -100123
    mock_channel.type = 'channel'
    
    mock_message_channel = MagicMock(spec=Message)
    mock_message_channel.sender_chat = mock_channel
    
    is_admin = await checker.is_admin_or_owner(mock_chat, regular_user, mock_context, message=mock_message_channel)
    print(f"sender_chat channel check: {is_admin}")
    assert is_admin == True

    # 5. Test regular admin
    mock_member = MagicMock(spec=ChatMember)
    mock_member.status = ChatMemberStatus.ADMINISTRATOR
    mock_context.bot.get_chat_member.return_value = mock_member
    
    is_admin = await checker.is_admin_or_owner(mock_chat, regular_user, mock_context)
    print(f"Regular admin check: {is_admin}")
    assert is_admin == True

    # 6. Test regular user (not admin)
    mock_member_user = MagicMock(spec=ChatMember)
    mock_member_user.status = ChatMemberStatus.MEMBER
    mock_context.bot.get_chat_member.return_value = mock_member_user
    
    is_admin = await checker.is_admin_or_owner(mock_chat, regular_user, mock_context)
    print(f"Regular user check: {is_admin}")
    assert is_admin == False

    print("\nAll PermissionChecker logic tests passed!")

if __name__ == "__main__":
    asyncio.run(test_admin_logic())
