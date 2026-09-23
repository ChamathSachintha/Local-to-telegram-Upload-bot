import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


# -------------------------------------------------
# LOAD SETTINGS
# -------------------------------------------------

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
WATCH_FOLDER = os.getenv("WATCH_FOLDER")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing from .env")

if not CHANNEL_ID:
    raise ValueError("CHANNEL_ID is missing from .env")

if not WATCH_FOLDER:
    raise ValueError("WATCH_FOLDER is missing from .env")


WATCH_PATH = Path(WATCH_FOLDER)

if not WATCH_PATH.exists():
    raise FileNotFoundError(
        f"Watch folder does not exist: {WATCH_PATH}"
    )


# -------------------------------------------------
# SETTINGS
# -------------------------------------------------

CHECK_INTERVAL = 3

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".webm"
}


# Telegram normal Bot API limits
PHOTO_LIMIT = 10 * 1024 * 1024
BOT_FILE_LIMIT = 50 * 1024 * 1024


# -------------------------------------------------
# CHECK FILE
# -------------------------------------------------

def is_supported_media(file_path):
    extension = file_path.suffix.lower()

    return (
        extension in IMAGE_EXTENSIONS
        or extension in VIDEO_EXTENSIONS
    )


# -------------------------------------------------
# WAIT UNTIL FILE FINISHES COPYING
# -------------------------------------------------

def wait_until_file_ready(file_path):
    print(f"Checking file: {file_path.name}")

    previous_size = -1

    for _ in range(10):

        try:
            current_size = file_path.stat().st_size
        except FileNotFoundError:
            return False

        if current_size == previous_size and current_size > 0:
            return True

        previous_size = current_size

        time.sleep(2)

    return False


# -------------------------------------------------
# TELEGRAM REQUEST
# -------------------------------------------------

def send_to_telegram(file_path):

    extension = file_path.suffix.lower()
    file_size = file_path.stat().st_size

    if file_size > BOT_FILE_LIMIT:
        print(
            f"SKIPPED: {file_path.name} is larger than 50 MB."
        )
        return False

    # ---------------------------------------------
    # IMAGE
    # ---------------------------------------------

    if extension in IMAGE_EXTENSIONS:

        # Large images are sent as documents
        if file_size > PHOTO_LIMIT:

            api_method = "sendDocument"
            file_parameter = "document"

        else:

            api_method = "sendPhoto"
            file_parameter = "photo"

    # ---------------------------------------------
    # VIDEO
    # ---------------------------------------------

    elif extension == ".mp4":

        api_method = "sendVideo"
        file_parameter = "video"

    else:

        # MOV, MKV, AVI, WEBM etc.
        # Send as Telegram document
        api_method = "sendDocument"
        file_parameter = "document"

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/{api_method}"
    )

    print(f"Uploading: {file_path.name}")

    try:

        with open(file_path, "rb") as media_file:

            files = {
                file_parameter: (
                    file_path.name,
                    media_file
                )
            }

            data = {
                "chat_id": CHANNEL_ID,
                "caption": file_path.name
            }

            response = requests.post(
                url,
                data=data,
                files=files,
                timeout=300
            )

        result = response.json()

        if response.ok and result.get("ok"):

            print(
                f"UPLOAD SUCCESSFUL: {file_path.name}"
            )

            return True

        else:

            print(
                f"UPLOAD FAILED: {file_path.name}"
            )

            print(result)

            return False

    except Exception as error:

        print(
            f"ERROR uploading {file_path.name}: {error}"
        )

        return False


# -------------------------------------------------
# DELETE FILE
# -------------------------------------------------

def delete_local_file(file_path):

    try:

        file_path.unlink()

        print(
            f"LOCAL FILE DELETED: {file_path.name}"
        )

    except Exception as error:

        print(
            f"Could not delete {file_path.name}: {error}"
        )


# -------------------------------------------------
# PROCESS FILE
# -------------------------------------------------

def process_file(file_path):

    if not file_path.is_file():
        return

    if not is_supported_media(file_path):
        return

    if not wait_until_file_ready(file_path):

        print(
            f"File is still being written: {file_path.name}"
        )

        return

    upload_successful = send_to_telegram(file_path)

    # VERY IMPORTANT:
    # Delete ONLY after Telegram confirms success.
    if upload_successful:

        delete_local_file(file_path)

    else:

        print(
            f"Keeping local file because upload failed: "
            f"{file_path.name}"
        )


# -------------------------------------------------
# SCAN FOLDER
# -------------------------------------------------

def scan_folder():

    for file_path in WATCH_PATH.iterdir():

        process_file(file_path)


# -------------------------------------------------
# MAIN
# -------------------------------------------------

def main():

    print("=" * 55)
    print("TELEGRAM AUTO MEDIA UPLOADER")
    print("=" * 55)

    print(f"Watching folder:")
    print(WATCH_PATH)

    print()
    print("Bot started.")
    print("Press CTRL+C to stop.")
    print()

    # Upload anything already inside the folder
    scan_folder()

    # Keep watching folder
    while True:

        try:

            scan_folder()

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:

            print("\nBot stopped.")
            break

        except Exception as error:

            print(f"Unexpected error: {error}")

            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()