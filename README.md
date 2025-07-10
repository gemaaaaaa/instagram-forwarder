<p align="center"><h1 align="center">INSTAGRAM-FORWARDER</h1></p>

<p align="center">
	<img src="https://img.shields.io/github/license/gemaaaaaa/instagram-forwarder?style=for-the-badge&logo=opensourceinitiative&logoColor=white&color=dd2a7b" alt="license">
	<img src="https://img.shields.io/github/last-commit/gemaaaaaa/instagram-forwarder?style=for-the-badge&logo=git&logoColor=white&color=dd2a7b" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/gemaaaaaa/instagram-forwarder?style=for-the-badge&color=dd2a7b" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/gemaaaaaa/instagram-forwarder?style=for-the-badge&color=dd2a7b" alt="repo-language-count">
</p>
<p align="center">Built with the tools and technologies:</p>
<p align="center">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="Python">
</p>
<br>


##  Overview

**Instagram Posts and Stories Forwarder** is a Python script designed to automate the process of downloading Instagram stories and forwarding new posts to a Discord channel via webhooks powered by the `instagrapi` library. 


##  Features

- **Discord Integration**: Sends posts and stories as files and post URLs as messages, complete with user information (profile picture and name).
     
- **Session Management**: Saves Instagram login sessions to avoid frequent re-authentication.

- **Configurable**: Easy to configure via environment variables or .env file.

##  Architecture

The application follows a modular architecture:

- **client**: Handles Instagram API interactions.
  
- **config**: Manages configuration loading and environment variables.
  
- **discord**: Handles Discord webhook operations.
  
- **storage**: Manages file operations and data persistence.
  
- **utils**: Contains utility functions and the main forwarder logic.

##  Getting Started

###  Installation

Install instagram-forwarder using one of the following methods:

**Build from source:**

1. Clone the instagram-forwarder repository:
```sh
git clone https://github.com/gemaaaaaa/instagram-forwarder
```

2. Navigate to the project directory:
```sh
cd instagram-forwarder
```

3. (Recommended) Create and activate a virtual environment:

On Unix/Mac:
```sh
python3 -m venv venv
source venv/bin/activate
```
On Windows:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

4. Install the project dependencies:

```sh
pip install -r requirements.txt
```

5. Copy the example environment file:

On Unix/Mac:
```sh
cp .env.example .env
```
On Windows:
```powershell
copy .env.example .env
```

###  Usage
```sh
python main.py
```

When prompted, enter the Instagram username you want to monitor, and the application will start forwarding their posts and stories to Discord.
