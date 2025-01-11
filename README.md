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
	<img src="https://img.shields.io/badge/Pydantic-E92063.svg?style=for-the-badge&logo=Pydantic&logoColor=white" alt="Pydantic">
</p>
<br>

##  Table of Contents

- [ Overview](#overview)
- [ Features](#features)
- [ Getting Started](#getting-started)
  - [ Installation](#installation)
  - [ Usage](#usage)


##  Overview


**Instagram Posts and Stories Forwarder**  is a Python script designed to automate the process of downloading Instagram stories and forwarding new posts to a Discord channel via webhooks powered by the `instagrapi` library. 


##  Features

-    **Discord Integration**: Sends posts and stories as files and post URLs as messages, complete with user information (profile picture and name).
     
-   **Session Management**: Saves Instagram login sessions to avoid frequent re-authentication.

##  Getting Started

###  Installation

Install instagram-forwarder using one of the following methods:

**Build from source:**

1. Clone the instagram-forwarder repository:
```sh
❯ git clone https://github.com/gemaaaaaa/instagram-forwarder
```

2. Navigate to the project directory:
```sh
❯ cd instagram-forwarder
```

3. Install the project dependencies:

```sh
❯ pip install -r requirements.txt
```




###  Usage
```sh
❯ python main.py
```
