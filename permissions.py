"""
Permission checking utilities for admin and owner verification
"""
from telegram import Chat, ChatMember, User
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


class PermissionChecker:
    """Checks user permissions in groups"""
    
    def __init__(self):
        # Cache for admin lists per chat (expires after some time)
        self.admin_cache = {}
        self.cache_ttl = 60  # seconds
    
    async def is_admin_or_owner(
        self, 
        chat: Chat, 
        user: User,
        context: ContextTypes.DEFAULT_TYPE,
        message: Message = None
    ) -> bool:
        """
        Check if user is admin or owner of the chat
        
        Args:
            chat: Telegram chat object
            user: Telegram user object
            context: Bot context
            message: Optional Telegram message object for additional checks
            
        Returns:
            True if user is admin or owner, False otherwise
        """
        # 1. Check for Telegram Service account (ID: 777000)
        # This user represents the Telegram system and is used for 
        # automatic forwards from linked channels.
        if user and user.id == 777000:
            logger.info(f"User {user.id} is Telegram Service account (Admin/System)")
            return True

        # 2. Check for Anonymous Admin (ID: 1087968824)
        if user and user.id == 1087968824:
            logger.info(f"User {user.id} is Anonymous Admin")
            return True

        # 3. Check if message is sent on behalf of a chat (e.g. the group itself)
        if message and message.sender_chat:
            if message.sender_chat.id == chat.id:
                logger.info(f"Message sent on behalf of the group {chat.id} (Anonymous Admin)")
                return True
            
            # Check if it's a linked channel (sender_chat is a channel)
            if message.sender_chat.type == 'channel':
                logger.info(f"Message sent from a channel {message.sender_chat.id} (likely linked)")
                return True

        # 4. Standard admin check via get_chat_member
        try:
            # Get chat member info
            member = await context.bot.get_chat_member(chat.id, user.id)
            
            # Check if user is creator (owner) or administrator
            if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                logger.info(f"User {user.id} (@{user.username}) is {member.status} in chat {chat.id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking permissions for user {user.id} in chat {chat.id}: {e}")
            # In case of error, assume not admin to be safe
            return False
    
    async def bot_can_delete_messages(
        self,
        chat: Chat,
        context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        """
        Check if bot has permission to delete messages
        
        Args:
            chat: Telegram chat object
            context: Bot context
            
        Returns:
            True if bot can delete messages, False otherwise
        """
        try:
            # Get bot's member info
            bot_member = await context.bot.get_chat_member(chat.id, context.bot.id)
            
            # Check if bot is admin and has delete permission
            if bot_member.status == ChatMemberStatus.ADMINISTRATOR:
                # Check if bot has can_delete_messages permission
                if hasattr(bot_member, 'can_delete_messages') and bot_member.can_delete_messages:
                    return True
            
            logger.warning(f"Bot does not have delete permission in chat {chat.id}")
            return False
            
        except Exception as e:
            logger.error(f"Error checking bot permissions in chat {chat.id}: {e}")
            return False
