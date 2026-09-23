# Local-to-Telegram Upload Bot

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge\&logo=telegram\&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-Supported-0078D4?style=for-the-badge\&logo=windows11\&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-Recommended-007ACC?style=for-the-badge\&logo=visualstudiocode\&logoColor=white)

![Status](https://img.shields.io/badge/Status-Development-F7DF1E?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-2EA44F?style=for-the-badge\&logo=opensourceinitiative\&logoColor=white)

</p>

A simple Python automation bot that monitors a local folder and automatically uploads images and videos to a private Telegram channel.

After Telegram confirms that the upload was successful, the local file is permanently deleted.

## Features

* Monitors a selected local folder
* Automatically detects images and videos
* Uploads media to a private Telegram channel
* Works with a Telegram bot added as a channel administrator
* Deletes local files only after a successful upload
* Keeps failed uploads on the computer
* Runs directly from the VS Code terminal
* Uses `.env` to keep configuration and bot tokens separate from the source code

## Project Structure

```text
Local-to-telegram-Upload-bot/
│
├── bot.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

* Windows
* Python 3.13 or newer
* Telegram account
* Telegram bot
* Private Telegram channel

Check Python:

```powershell
py --version
```

Example:

```text
Python 3.13.14
```

## 1. Create a Telegram Bot

Open Telegram and search for:

```text
@BotFather
```

Create a new bot using:

```text
/newbot
```

Follow the instructions and copy the generated bot token.

> Never share your bot token publicly or commit it to GitHub.

## 2. Add the Bot to Your Private Channel

1. Open your private Telegram channel.
2. Open the channel settings.
3. Go to **Administrators**.
4. Add your bot.
5. Allow the bot to **Post Messages**.

## 3. Get the Private Channel ID

Post a message in your private channel after adding the bot.

Then open this URL in your browser:

```text
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

Replace:

```text
YOUR_BOT_TOKEN
```

with your actual Telegram bot token.

Look for:

```json
"chat": {
    "id": -1001234567890,
    "title": "My Private Channel",
    "type": "channel"
}
```

Copy the channel ID beginning with:

```text
-100
```

## 4. Install Dependencies

Open the project in VS Code.

Open the terminal:

```text
Ctrl + `
```

Then run:

```powershell
py -m pip install requests python-dotenv
```

Or install everything from `requirements.txt`:

```powershell
py -m pip install -r requirements.txt
```

## 5. Configure `.env`

Create a file named:

```text
.env
```

Add:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
CHANNEL_ID=-1001234567890
WATCH_FOLDER=D:\TelegramUpload
```

Example:

```env
BOT_TOKEN=123456789:ABCDEF_EXAMPLE_TOKEN
CHANNEL_ID=-1009876543210
WATCH_FOLDER=D:\Media\TelegramUpload
```

Do not upload `.env` to GitHub.

## 6. Create `.gitignore`

Create:

```text
.gitignore
```

Add:

```gitignore
.env
__pycache__/
*.pyc
.venv/
venv/
```

## 7. Run the Bot

From the VS Code terminal:

```powershell
py bot.py
```

The bot should display something similar to:

```text
=======================================================
TELEGRAM AUTO MEDIA UPLOADER
=======================================================

Watching folder:
D:\TelegramUpload

Bot started.
Press CTRL+C to stop.
```

## How It Works

```text
Local Folder
     │
     ▼
Detect Image / Video
     │
     ▼
Upload to Telegram
     │
     ▼
Telegram confirms upload
     │
     ├── Failed → Keep local file
     │
     └── Successful
              │
              ▼
      Delete local file
```

Files are deleted only when Telegram confirms that the upload was successful.

## Supported Media

Examples:

```text
Images
.jpg
.jpeg
.png
.webp

Videos
.mp4
.mov
.mkv
.avi
.webm
```

Some media formats may be uploaded as Telegram documents instead of directly as photos or videos.

## Stop the Bot

Press:

```text
Ctrl + C
```

inside the terminal.

## Important

The normal Telegram Bot API has upload-size limitations.

Large videos may require using Telegram's local Bot API server instead of the standard hosted Bot API.

## Security

Never publish:

* Telegram bot tokens
* `.env` files
* Private channel information
* Sensitive local folder paths

Always keep your `.env` file inside `.gitignore`.

## Future Improvements

Possible additions:

* Automatic retry for failed uploads
* Upload progress display
* File logging
* Duplicate detection
* Telegram captions
* Recursive subfolder monitoring
* Start automatically with Windows
* Large-file support
* Upload queue
* Error notifications

## License

This project can be released under the MIT License.
