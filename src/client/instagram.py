import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple, Optional, Set, Dict, Any

from instagrapi import Client

from instagram_forwarder.storage.storage import Storage


class InstagramClient:
    """
    Instagram client manager for the Instagram Forwarder application.
    Handles Instagram API interactions through instagrapi.
    """
    
    def __init__(self, username: str, password: str, storage: Storage):
        """
        Initialize the InstagramClient instance.
        
        Args:
            username: Instagram username
            password: Instagram password
            storage: Storage instance for file operations
        """
        self.username = username
        self.password = password
        self.storage = storage
        self.client = Client()
        self._login()
    
    def _login(self) -> bool:
        """
        Login to Instagram.
        
        Returns:
            True if login was successful, False otherwise
        """
        try:
            self.client.load_settings("sessions.json")
            logging.info("Session loaded successfully.")
            return True
        except FileNotFoundError:
            logging.warning("Session file not found. Trying to login...")
            is_login = self.client.login(self.username, self.password)
            if is_login:
                logging.info("Successfully logged in.")
                self.client.dump_settings("sessions.json")
                return True
            else:
                logging.error("Failed to log in.")
                return False
    
    def get_user_id(self, username: str) -> int:
        """
        Get user ID from username.
        
        Args:
            username: Instagram username
            
        Returns:
            Instagram user ID
        """
        return self.client.user_id_from_username(username)
    
    def get_user_info(self, user_id: int) -> Any:
        """
        Get user information.
        
        Args:
            user_id: Instagram user ID
            
        Returns:
            User information object
        """
        return self.client.user_info(user_id)
    
    def get_user_media(self, user_id: int) -> List[Any]:
        """
        Get user media.
        
        Args:
            user_id: Instagram user ID
            
        Returns:
            List of media objects
        """
        return self.client.user_medias_paginated(user_id)[0]
    
    def get_user_stories(self, user_id: int) -> List[Any]:
        """
        Get user stories.
        
        Args:
            user_id: Instagram user ID
            
        Returns:
            List of story objects
        """
        return self.client.user_stories(user_id)
    
    def download_story(self, pk: str, folder: Path, filename: str) -> Path:
        """
        Download a story.
        
        Args:
            pk: Story ID
            folder: Folder to download to
            filename: Filename to save as
            
        Returns:
            Path to the downloaded file
        """
        return self.client.story_download(pk, folder=str(folder), filename=filename)
    
    def extract_new_story_ids(self, user_stories: List, target_username: str) -> List[Tuple[str, datetime]]:
        """
        Extract new story IDs.
        
        Args:
            user_stories: List of story objects
            target_username: Instagram username
            
        Returns:
            List of tuples containing story ID and timestamp
        """
        existing_ids = self.storage.load_existing_story_ids(target_username)
        new_stories = [
            (story.pk, story.taken_at)
            for story in user_stories
            if str(story.pk) not in existing_ids
        ]
        return new_stories
    
    def extract_new_post_ids(self, user_media: List, target_username: str) -> List[str]:
        """
        Extract new post IDs.
        
        Args:
            user_media: List of media objects
            target_username: Instagram username
            
        Returns:
            List of post IDs
        """
        existing_ids = self.storage.load_existing_post_ids(target_username)
        new_posts = [media for media in user_media if str(media.pk) not in existing_ids]
        return [media.pk for media in new_posts]
    
    def get_post_url(self, media_code: str) -> str:
        """
        Get post URL from media code.
        
        Args:
            media_code: Media code
            
        Returns:
            Post URL
        """
        return f"https://www.instagram.com/p/{media_code}/" 