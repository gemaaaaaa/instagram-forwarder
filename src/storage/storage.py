import os
import logging
from pathlib import Path
from typing import Set, Dict, Any, List, Optional


class Storage:
    """
    Storage manager for the Instagram Forwarder application.
    Handles file operations and data persistence.
    """
    
    def __init__(self, base_path: Path = Path(".")):
        """
        Initialize the Storage instance.
        
        Args:
            base_path: Base path for all storage operations
        """
        self.base_path = base_path
        self.stories_folder = base_path / "stories"
        self.marked_stories_data_folder = base_path / "marked_stories_data"
        self.marked_posts_data_folder = base_path / "marked_posts_data"
        
        # Ensure required folders exist
        self.ensure_folder(self.stories_folder)
        self.ensure_folder(self.marked_stories_data_folder)
        self.ensure_folder(self.marked_posts_data_folder)
    
    def ensure_folder(self, folder: Path) -> None:
        """
        Ensure a folder exists, creating it if necessary.
        
        Args:
            folder: Path to the folder
        """
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created folder: {folder}")
    
    def get_user_stories_folder(self, username: str) -> Path:
        """
        Get the folder path for a user's stories.
        
        Args:
            username: Instagram username
            
        Returns:
            Path to the user's stories folder
        """
        folder = self.stories_folder / username
        self.ensure_folder(folder)
        return folder
    
    def save_story_id(self, story_id: str, target_username: str) -> None:
        """
        Save a story ID to the marked stories file.
        
        Args:
            story_id: Instagram story ID
            target_username: Instagram username
        """
        file_path = self.marked_stories_data_folder / f"marked_stories_{target_username}.txt"
        with open(file_path, "a") as file:
            file.write(f"{story_id}\n")
        logging.info(f"Saved story ID: {story_id}")
    
    def save_post_id(self, post_id: str, target_username: str) -> None:
        """
        Save a post ID to the marked posts file.
        
        Args:
            post_id: Instagram post ID
            target_username: Instagram username
        """
        file_path = self.marked_posts_data_folder / f"marked_posts_{target_username}.txt"
        with open(file_path, "a") as file:
            file.write(f"{post_id}\n")
        logging.info(f"Saved post ID: {post_id}")
    
    def load_existing_story_ids(self, target_username: str) -> Set[str]:
        """
        Load existing story IDs for a user.
        
        Args:
            target_username: Instagram username
            
        Returns:
            Set of story IDs
        """
        file_path = self.marked_stories_data_folder / f"marked_stories_{target_username}.txt"
        if file_path.exists():
            with open(file_path, "r") as file:
                return set(file.read().splitlines())
        return set()
    
    def load_existing_post_ids(self, target_username: str) -> Set[str]:
        """
        Load existing post IDs for a user.
        
        Args:
            target_username: Instagram username
            
        Returns:
            Set of post IDs
        """
        file_path = self.marked_posts_data_folder / f"marked_posts_{target_username}.txt"
        if file_path.exists():
            with open(file_path, "r") as file:
                return set(file.read().splitlines())
        return set()
    
    def delete_file(self, file_path: Path) -> bool:
        """
        Delete a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if the file was deleted, False otherwise
        """
        try:
            os.remove(file_path)
            logging.info(f"Deleted file: {file_path}")
            return True
        except Exception as e:
            logging.error(f"Error deleting file {file_path}: {e}")
            return False 