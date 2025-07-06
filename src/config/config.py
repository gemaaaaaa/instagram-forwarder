import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """
    Configuration manager for the Instagram Forwarder application.
    Handles loading and saving configuration from/to a JSON file.
    """
    def __init__(self, config_file: Path = Path("configs.json")):
        """
        Initialize the Config instance.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.config_data = self._load_config()
        
        # Environment variables
        self.instagram_username = os.getenv("INSTAGRAM_USERNAME")
        self.instagram_password = os.getenv("INSTAGRAM_PASSWORD")
        self.discord_webhook_url_1 = os.getenv("DISCORD_WEBHOOK_URL_1")
        self.discord_webhook_url_2 = os.getenv("DISCORD_WEBHOOK_URL_2")
        
        # Validate required environment variables
        if not all([self.instagram_username, self.instagram_password, self.discord_webhook_url_1]):
            raise EnvironmentError(
                "Please set INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, and DISCORD_WEBHOOK_URL_1 environment variables."
            )
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Dictionary containing configuration values
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON in config file: {self.config_file}")
                return {"webhook_counter": 0}
        return {"webhook_counter": 0}
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        with open(self.config_file, "w") as file:
            json.dump(self.config_data, file, indent=4)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value
        """
        return self.config_data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value by key.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config_data[key] = value
    
    def get_webhook_url(self) -> str:
        """
        Get the next webhook URL to use in a round-robin fashion.
        
        Returns:
            Discord webhook URL
        """
        webhook_counter = self.get("webhook_counter", 0)
        
        webhook_url = self.discord_webhook_url_1 if webhook_counter % 2 == 0 else self.discord_webhook_url_2
        
        # Update webhook counter for next use
        self.set("webhook_counter", webhook_counter + 1)
        self.save_config()
        
        return webhook_url 