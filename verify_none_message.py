
import sys
import os
import asyncio
from unittest.mock import MagicMock

# Add current directory to path
sys.path.append(os.getcwd())

from bot import handle_message
from telegram import Update

async def test_none_message():
    print("Testing handle_message with None message...")
    mock_update = MagicMock(spec=Update)
    mock_update.message = None
    mock_context = MagicMock()
    
    # This should not raise AttributeError
    try:
        await handle_message(mock_update, mock_context)
        print("Test passed: No error raised for None message.")
    except AttributeError as e:
        print(f"Test failed: Caught AttributeError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Test failed: Caught unexpected exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_none_message())
