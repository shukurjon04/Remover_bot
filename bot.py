"""
Telegram Spam Removal Bot
Automatically removes spam and advertisements from groups
while preserving messages from admins and group owners
"""
import logging
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
)
from config import BOT_TOKEN
from spam_detector import SpamDetector
from permissions import PermissionChecker

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize spam detector and permission checker
spam_detector = SpamDetector()
permission_checker = PermissionChecker()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle incoming messages and check for spam
    """
    message = update.message
    
    # Ignore messages from private chats
    if message.chat.type == 'private':
        return
    
    # Ignore messages without a user (system messages, etc.)
    if not message.from_user:
        return
    
    try:
        # Check if user is admin or owner
        is_admin = await permission_checker.is_admin_or_owner(
            message.chat,
            message.from_user,
            context
        )
        
        # If user is admin or owner, don't check for spam
        if is_admin:
            logger.info(
                f"Skipping spam check for admin/owner {message.from_user.id} "
                f"(@{message.from_user.username}) in chat {message.chat.id}"
            )
            return
        
        # Check if message is spam
        is_spam, reason = spam_detector.is_spam(message)
        
        if is_spam:
            # Try to delete the spam message
            try:
                await message.delete()
                logger.info(
                    f"Deleted spam message from user {message.from_user.id} "
                    f"(@{message.from_user.username}) in chat {message.chat.id}. "
                    f"Reason: {reason}"
                )
                
                # Optional: Send a notification to the chat (can be commented out)
                # notification = await message.chat.send_message(
                #     f"⚠️ Spam xabar o'chirildi.\nSabab: {reason}"
                # )
                # # Delete notification after 5 seconds
                # await asyncio.sleep(5)
                # await notification.delete()
                
            except Exception as e:
                logger.error(f"Failed to delete spam message: {e}")
                # Check if bot has permission
                can_delete = await permission_checker.bot_can_delete_messages(
                    message.chat,
                    context
                )
                if not can_delete:
                    logger.error(
                        f"Bot does not have delete permission in chat {message.chat.id}. "
                        f"Please grant admin rights with 'Delete messages' permission."
                    )
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")


async def post_init(application: Application) -> None:
    """
    Post initialization callback
    """
    logger.info("Bot initialized successfully!")
    logger.info(f"Bot username: @{(await application.bot.get_me()).username}")


def main() -> None:
    """
    Main function to run the bot
    """
    logger.info("Starting Spam Removal Bot...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    # Add message handler for all text and media messages in groups
    application.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND & (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP),
            handle_message
        )
    )
    
    logger.info("Bot is running. Press Ctrl+C to stop.")
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
