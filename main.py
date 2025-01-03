import os
import logging
from dotenv import load_dotenv

from bot import TwitterBot
ENVIRONMENT = "DEMO"

if ENVIRONMENT == "DEMO":
    load_dotenv(".env.demo")
else:
    load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(filename)s - %(levelname)s - %(message)s - %(asctime)s")

TARGET_UP = "150"
TARGET_DOWN = "10"

def load_env_vars() -> dict[str, str]:

    vars_loaded: bool = True

    email: str = os.getenv("TWITTER_EMAIL")
    password: str = os.getenv("TWITTER_PASSWORD")

    env_vars: dict[str,str] = {
        "TWITTER_EMAIL":email,
        "TWITTER_PASSWORD":password,
    }

    for name,var in env_vars.items():
        if not var:
            logging.critical(f"Environment variable: {name} not found.")
            vars_loaded = False

    if not vars_loaded:
        raise Exception("Failed to load some environment variables.")

    return env_vars


def main(env_vars: dict[str, str]) -> None:

    email: str = env_vars["TWITTER_EMAIL"]
    password: str = env_vars["TWITTER_PASSWORD"]

    bot = TwitterBot(promised_up=TARGET_UP, promised_down=TARGET_DOWN)
    internet_speed_info = bot.get_internet_speeds()

    upload_speed: str = internet_speed_info["upload speed"]
    download_speed: str = internet_speed_info["download speed"]

    message: str =\
    f"Current internet speeds: {upload_speed}up/{download_speed}down. Promised internet speeds are {TARGET_UP}up/{TARGET_DOWN}/down"

    bot.tweet_info(email=email,password=password,message=message)


if __name__ == '__main__':
    environ_vars = load_env_vars()
    main(environ_vars)