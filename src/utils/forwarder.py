import logging
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple, Any

from instagram_forwarder.client.instagram import InstagramClient
from instagram_forwarder.discord.webhook import DiscordWebhook
from instagram_forwarder.config.config import Config
from instagram_forwarder.storage.storage import Storage


class Forwarder:
    """
    Content forwarder for the Instagram Forwarder application.
    Handles forwarding Instagram content to Discord.
    """
    
    def __init__(self, instagram_client: InstagramClient, config: Config, storage: Storage):
        """
        Initialize the Forwarder instance.
        
        Args:
            instagram_client: Instagram client instance
            config: Configuration instance
            storage: Storage instance
        """
        self.instagram_client = instagram_client
        self.config = config
        self.storage = storage
    
    def download_and_forward_stories(
        self, story_data: List[Tuple[str, datetime]], target_username: str, user_info: Any, delay: int = 2
    ) -> None:
        """
        Download and forward stories to Discord.
        
        Args:
            story_data: List of story IDs and timestamps
            target_username: Instagram username
            user_info: User information
            delay: Delay between requests in seconds
        """
        user_folder = self.storage.get_user_stories_folder(target_username)
        
        for pk, taken_at in story_data:
            try:
                taken_at_utc7 = taken_at + timedelta(hours=7)
                filename = f"{target_username}_stories_{taken_at_utc7.strftime('%d%m%y')}_{taken_at_utc7.strftime('%H%M%S')}"
                file_path = self.instagram_client.download_story(
                    pk, folder=user_folder, filename=filename
                )
                logging.info(f"Downloaded story with pk: {pk} to {file_path}")
                
                webhook_url = self.config.get_webhook_url()
                discord = DiscordWebhook(webhook_url)
                
                if discord.send_file(file_path, user_info.full_name, str(user_info.profile_pic_url_hd)):
                    self.storage.delete_file(file_path)
                else:
                    logging.warning(f"File {file_path} was not deleted due to failed Discord upload.")
                
                self.storage.save_story_id(pk, target_username)
                time.sleep(delay)
            except Exception as e:
                logging.error(f"Failed to process story with pk: {pk}. Error: {e}")
    
    def forward_posts(
        self, media_list: List[Any], target_username: str, user_info: Any, delay: int = 1
    ) -> None:
        """
        Forward posts to Discord.
        
        Args:
            media_list: List of media objects
            target_username: Instagram username
            user_info: User information
            delay: Delay between requests in seconds
        """
        existing_ids = self.storage.load_existing_post_ids(target_username)
        new_posts = [media for media in media_list if str(media.pk) not in existing_ids]
        
        if not new_posts:
            logging.info("No new posts found.")
            return
        
        logging.info(f"Found {len(new_posts)} new posts. Processing...")
        
        # Reverse the list to process from oldest to newest
        reversed_new_posts = reversed(new_posts)
        
        for media in reversed_new_posts:
            try:
                post_url = self.instagram_client.get_post_url(media.code)
                
                webhook_url = self.config.get_webhook_url()
                discord = DiscordWebhook(webhook_url)
                
                if discord.send_message(post_url, user_info.full_name, str(user_info.profile_pic_url_hd)):
                    self.storage.save_post_id(media.pk, target_username)
                    logging.info(f"Forwarded post URL: {post_url}")
                else:
                    logging.warning(f"Failed to forward post URL: {post_url}")
                
                time.sleep(delay)
            except Exception as e:
                logging.error(f"Failed to process post with pk: {media.pk}. Error: {e}")
    
    def run(self, target_username: str) -> None:
        """
        Run the forwarder continuously.
        
        Args:
            target_username: Instagram username to monitor
        """
        while True:
            logging.info(f"Fetching data for user: {target_username}")
            
            try:
                user_id = self.instagram_client.get_user_id(target_username)
                user_info = self.instagram_client.get_user_info(user_id)
                
                # Fetch user media
                user_media = self.instagram_client.get_user_media(user_id)
                
                # Extract and forward new posts
                new_post_ids = self.instagram_client.extract_new_post_ids(user_media, target_username)
                if new_post_ids:
                    logging.info(f"Found {len(new_post_ids)} new posts. Processing...")
                    self.forward_posts(user_media, target_username, user_info)
                else:
                    logging.info("No new posts found.")
                
                # Fetch and forward new stories
                user_stories = self.instagram_client.get_user_stories(user_id)
                new_story_data = self.instagram_client.extract_new_story_ids(user_stories, target_username)
                if new_story_data:
                    logging.info(f"Found {len(new_story_data)} new stories. Processing...")
                    self.download_and_forward_stories(new_story_data, target_username, user_info)
                else:
                    logging.info("No new stories found.")
                
                # Wait before the next check
                delay = random.randint(550, 600)
                logging.info(f"Waiting for {delay} seconds before the next check...")
                time.sleep(delay)
            except Exception as e:
                logging.error(f"Error during forwarding: {e}")
                time.sleep(60)  # Wait a minute before retrying 