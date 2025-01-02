class TwitterSiteInfo:
    URL: str = "https://x.com/"
    LOGIN_BUTTON: str = "a[data-testid='loginButton']"
    SITE_TITLE: str = "Home / X"
    COMPOSE_BUTTON_SELECTOR: str = "a[aria-label='Post']"
    TWEET_FORM_SELECTOR: str = "div[contenteditable='true']"
    POST_BUTTON_SELECTOR: str = "button[data-testid='tweetButton']"

class SpeedTestSiteInfo:
    URL: str = "https://www.speedtest.net/"
    START_BUTTON_CLASS: str = "js-start-test"
    RESULTS_CLASS: str = "result-data-large"