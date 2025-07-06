import logging
import requests
from pathlib import Path
from typing import Dict, Any, Optional


class DiscordWebhook:
    """
    Discord webhook manager for the Instagram Forwarder application.
    Handles sending files and messages to Discord via webhooks.
    """
    
    def __init__(self, webhook_url: str):
        """
        Initialize the DiscordWebhook instance.
        
        Args:
            webhook_url: Discord webhook URL
        """
        self.webhook_url = webhook_url
    
    def send_file(self, file_path: Path, username: str, avatar_url: str) -> bool:
        """
        Send a file to Discord via webhook.
        
        Args:
            file_path: Path to the file to send
            username: Display name for the webhook
            avatar_url: URL for the webhook avatar
            
        Returns:
            True if the file was sent successfully, False otherwise
        """
        try:
            with open(file_path, "rb") as file:
                files = {"file": file}
                data = {
                    "username": username,
                    "avatar_url": avatar_url,
                }
                response = requests.post(self.webhook_url, files=files, data=data)
            
            if response.status_code == 200:
                logging.info(f"File {file_path} successfully sent to Discord.")
                return True
            else:
                logging.error(
                    f"Failed to send file {file_path} to Discord. Status code: {response.status_code}"
                )
                return False
        except Exception as e:
            logging.error(f"Error sending file {file_path} to Discord: {e}")
            return False
    
    def send_message(self, content: str, username: str, avatar_url: str) -> bool:
        """
        Send a message to Discord via webhook.
        
        Args:
            content: Message content
            username: Display name for the webhook
            avatar_url: URL for the webhook avatar
            
        Returns:
            True if the message was sent successfully, False otherwise
        """
        try:
            data = {
                "username": username,
                "avatar_url": avatar_url,
                "content": content,
            }
            response = requests.post(self.webhook_url, json=data)
            
            if response.status_code == 204:
                logging.info(f"Message successfully sent to Discord.")
                return True
            else:
                logging.error(
                    f"Failed to send message to Discord. Status code: {response.status_code}"
                )
                return False
        except Exception as e:
            logging.error(f"Error sending message to Discord: {e}")
            return False 