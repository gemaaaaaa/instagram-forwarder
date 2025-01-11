import datetime
import json
import logging
import os
import random
import time
from datetime import timedelta
from pathlib import Path
from typing import List, Set, Tuple

import requests
from dotenv import load_dotenv

from instagrapi import Client

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

STORIES_FOLDER = Path("stories")
MARKED_STORIES_DATA_FOLDER = Path("marked_stories_data")
MARKED_POSTS_DATA_FOLDER = Path("marked_posts_data")
WEBHOOK_URL_1 = os.getenv("DISCORD_WEBHOOK_URL_1")
WEBHOOK_URL_2 = os.getenv("DISCORD_WEBHOOK_URL_2")
CONFIG_FILE = Path("configs.json")

ACCOUNT_USERNAME = os.getenv("INSTAGRAM_USERNAME")
ACCOUNT_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

if not all([ACCOUNT_USERNAME, ACCOUNT_PASSWORD, WEBHOOK_URL_1, WEBHOOK_URL_2]):
    raise EnvironmentError(
        "Please set INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, and DISCORD_WEBHOOK_URL_1 environment variables."
    )

cl = Client()


def load_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {"webhook_counter": 0}


def save_config(config: dict) -> None:
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


def get_webhook_url() -> str:
    config = load_config()
    webhook_counter = config.get("webhook_counter", 0)

    if webhook_counter > 1:
        webhook_counter = 0

    webhook_url = WEBHOOK_URL_1 if webhook_counter % 2 == 0 else WEBHOOK_URL_2
    config["webhook_counter"] = webhook_counter + 1
    save_config(config)
    return webhook_url


def ensure_folder(folder: Path) -> None:
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created folder: {folder}")


def save_story_id(story_id: str, target_username: str) -> None:
    ensure_folder(MARKED_STORIES_DATA_FOLDER)
    file_path = MARKED_STORIES_DATA_FOLDER / f"marked_stories_{target_username}.txt"
    with open(file_path, "a") as file:
        file.write(f"{story_id}\n")
    logging.info(f"Saved story ID: {story_id}")


def save_post_id(post_id: str, target_username: str) -> None:
    ensure_folder(MARKED_POSTS_DATA_FOLDER)
    file_path = MARKED_POSTS_DATA_FOLDER / f"marked_posts_{target_username}.txt"
    with open(file_path, "a") as file:
        file.write(f"{post_id}\n")
    logging.info(f"Saved post ID: {post_id}")


def load_existing_story_ids(target_username: str) -> Set[str]:
    ensure_folder(MARKED_STORIES_DATA_FOLDER)
    file_path = MARKED_STORIES_DATA_FOLDER / f"marked_stories_{target_username}.txt"
    if file_path.exists():
        with open(file_path, "r") as file:
            return set(file.read().splitlines())
    return set()


def load_existing_post_ids(target_username: str) -> Set[str]:
    ensure_folder(MARKED_POSTS_DATA_FOLDER)
    file_path = MARKED_POSTS_DATA_FOLDER / f"marked_posts_{target_username}.txt"
    if file_path.exists():
        with open(file_path, "r") as file:
            return set(file.read().splitlines())
    return set()


def extract_new_story_ids(
    user_stories: List, target_username: str
) -> List[Tuple[str, datetime.datetime]]:
    existing_ids = load_existing_story_ids(target_username)
    new_stories = [
        (story.pk, story.taken_at)
        for story in user_stories
        if str(story.pk) not in existing_ids
    ]
    return new_stories


def extract_new_post_ids(user_medias: tuple, target_username: str) -> List[str]:
    existing_ids = load_existing_post_ids(target_username)
    new_posts = [media for media in user_medias if str(media.pk) not in existing_ids]
    return [media.pk for media in new_posts]


def send_to_discord(file_path: Path, user_info) -> bool:
    webhook_url = get_webhook_url()
    try:
        with open(file_path, "rb") as file:
            files = {"file": file}
            data = {
                "username": user_info.full_name,
                "avatar_url": str(user_info.profile_pic_url_hd),
            }
            response = requests.post(webhook_url, files=files, data=data)
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


def send_post_url_to_discord(post_url: str, user_info) -> bool:
    webhook_url = get_webhook_url()
    try:
        data = {
            "username": user_info.full_name,
            "avatar_url": str(user_info.profile_pic_url_hd),
            "content": post_url,
        }
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            logging.info(f"Post URL {post_url} successfully sent to Discord.")
            return True
        else:
            logging.error(
                f"Failed to send post URL {post_url} to Discord. Status code: {response.status_code}"
            )
            return False
    except Exception as e:
        logging.error(f"Error sending post URL {post_url} to Discord: {e}")
        return False


def download_and_forward_stories(
    story_data: List[Tuple[str, datetime.datetime]],
    target_username: str,
    user_info,
    delay: int = 2,
) -> None:
    user_folder = STORIES_FOLDER / target_username
    ensure_folder(user_folder)

    for pk, taken_at in story_data:
        try:
            taken_at_utc7 = taken_at + timedelta(hours=7)
            filename = f"{target_username}_stories_{taken_at_utc7.strftime('%d%m%y')}_{taken_at_utc7.strftime('%H%M%S')}"
            file_path = cl.story_download(
                pk, folder=str(user_folder), filename=filename
            )
            logging.info(f"Downloaded story with pk: {pk} to {file_path}")

            if send_to_discord(file_path, user_info):
                os.remove(file_path)
                logging.info(f"Deleted file: {file_path}")
            else:
                logging.warning(
                    f"File {file_path} was not deleted due to failed Discord upload."
                )
            save_story_id(pk, target_username)
            time.sleep(delay)
        except Exception as e:
            logging.error(f"Failed to process story with pk: {pk}. Error: {e}")


def forward_posts(
    media_list: tuple, target_username: str, user_info, delay: int = 1
) -> None:
    existing_ids = load_existing_post_ids(target_username)
    new_posts = [media for media in media_list if str(media.pk) not in existing_ids]

    if not new_posts:
        logging.info("No new posts found.")
        return

    logging.info(f"Found {len(new_posts)} new posts. Processing...")

    # Reverse the list to process from oldest to newest
    reversed_new_posts = reversed(new_posts)

    for media in reversed_new_posts:
        try:
            post_url = f"https://www.instagram.com/p/{media.code}/"
            if send_post_url_to_discord(post_url, user_info):
                save_post_id(media.pk, target_username)
                logging.info(f"Forwarded post URL: {post_url}")
            else:
                logging.warning(f"Failed to forward post URL: {post_url}")
            time.sleep(delay)
        except Exception as e:
            logging.error(f"Failed to process post with pk: {media.pk}. Error: {e}")


def main(target_username: str) -> None:
    while True:
        logging.info(f"Fetching data for user: {target_username}")
        user_id = cl.user_id_from_username(target_username)
        user_info = cl.user_info(user_id)

        # Fetch user media
        user_medias = cl.user_medias_paginated(user_id)[0]

        # Extract and forward new posts
        new_post_pks = extract_new_post_ids(user_medias, target_username)
        if new_post_pks:
            logging.info(f"Found {len(new_post_pks)} new posts. Processing...")
            forward_posts(user_medias, target_username, user_info)
        else:
            logging.info("No new posts found.")

        # Fetch and forward new stories
        user_stories = cl.user_stories(user_id)
        new_story_data = extract_new_story_ids(user_stories, target_username)
        if new_story_data:
            logging.info(f"Found {len(new_story_data)} new stories. Processing...")
            download_and_forward_stories(new_story_data, target_username, user_info)
        else:
            logging.info("No new stories found.")

        # Wait before the next check
        delay = random.randint(550, 600)
        logging.info(f"Waiting for {delay} seconds before the next check...")
        time.sleep(delay)


if __name__ == "__main__":
    ensure_folder(STORIES_FOLDER)
    ensure_folder(MARKED_STORIES_DATA_FOLDER)
    ensure_folder(MARKED_POSTS_DATA_FOLDER)
    try:
        cl.load_settings("sessions.json")
        logging.info("Session loaded successfully.")
    except FileNotFoundError:
        logging.warning("Session file not found. Trying to login...")
        is_login = cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
        if is_login:
            logging.info("Successfully logged in.")
            cl.dump_settings("sessions.json")
        else:
            logging.error("Failed to log in.")
            exit(1)

    target_username = input("Enter Instagram username target: ")
    main(target_username)
