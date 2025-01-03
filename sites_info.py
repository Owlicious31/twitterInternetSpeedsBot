class TwitterSiteInfo:
    URL = "https://x.com/"
    LOGIN_BUTTON = "a[data-testid='loginButton']"
    SITE_TITLE = "Home / X"
    COMPOSE_BUTTON_SELECTOR = "a[aria-label='Post']"
    TWEET_FORM_SELECTOR = "div[contenteditable='true']"
    POST_BUTTON_SELECTOR = "button[data-testid='tweetButton']"

class SpeedTestSiteInfo:
    URL = "https://www.speedtest.net/"
    START_BUTTON_CLASS = "js-start-test"
    RESULTS_CLASS = "result-data-large"