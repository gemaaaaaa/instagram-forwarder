import logging
from pathlib import Path
from dotenv import load_dotenv

from instagram_forwarder.client.instagram import InstagramClient
from instagram_forwarder.config.config import Config
from instagram_forwarder.storage.storage import Storage
from instagram_forwarder.utils.forwarder import Forwarder


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def main():
    """Main entry point for the Instagram Forwarder application."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Setup logging
    setup_logging()
    
    try:
        # Initialize configuration
        config = Config()
        
        # Initialize storage
        storage = Storage()
        
        # Initialize Instagram client
        instagram_client = InstagramClient(
            config.instagram_username,
            config.instagram_password,
            storage
        )
        
        # Initialize forwarder
        forwarder = Forwarder(instagram_client, config, storage)
        
        # Get target username from user input
        target_username = input("Enter Instagram username target: ")
        
        # Run the forwarder
        forwarder.run(target_username)
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    main() 