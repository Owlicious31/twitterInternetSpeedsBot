import time
import logging

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

#For type annotations
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException

logging.basicConfig(level=logging.INFO, format="%(filename)s - %(levelname)s - %(message)s - %(asctime)s")

class TwitterBot:
    timeout: int = 1800

    def __init__(self, target_up: str, target_down: str) -> None:

        self.chrome_options: webdriver.ChromeOptions = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option(name="detach",value=True)

        self.driver: WebDriver = webdriver.Chrome(options=self.chrome_options)

        self.target_up: str = target_up
        self.target_down: str = target_down

        logging.info(f"Target upload speed: {target_up}, Target download speed: {target_down}")


    def get_internet_speeds(self) -> dict[str,str]:
        """
        Get your current internet speeds from speedtest.net.
        :return: Your upload and download speeds in a dictionary, keys: "download speed", "upload speed"
        """

        self.driver.get(url="https://www.speedtest.net/")
        logging.info("Getting internet speeds")

        try:
            start_button: WebElement = self.driver.find_element(By.CLASS_NAME,"js-start-test")
            start_button.click()

        except NoSuchElementException:
            logging.critical("Unable to locate start button.")
            raise

        except StaleElementReferenceException:
            logging.error("Unable to click on start button, page might have dynamically changed.")
            raise

        while True:
            wait: WebDriverWait[WebDriver] = WebDriverWait(driver=self.driver,timeout=10)
            wait.until(ec.presence_of_element_located((By.CLASS_NAME, "result-data-large")))

            result_data: list[WebElement] = self.driver.find_elements(By.CLASS_NAME,"result-data-large")

            if not result_data:
                logging.critical("Was unable to find result data containers, the CSS selector might have changed.")
                raise Exception("Could not find data result divs.")

            download_mbps: str = result_data[0].text
            upload_mbps: str = result_data[1].text

            if upload_mbps != "" and upload_mbps != "—":
                logging.info("Got internet speeds")
                break

            elif self.timeout == 0:
                self.driver.quit()
                logging.error("Could not get internet speeds, maximum wait time exceeded")
                raise Exception("Could not find Internet speeds maximum wait time has been exceeded.")

            else:
                self.timeout -= 1

        return {"download speed":download_mbps, "upload speed":upload_mbps}


    def tweet_info(self, email: str, password: str, message: str) -> None:
        """
        Send a tweet.
        :param email: You email connected to your Twitter account
        :param password: Your Twitter account password.
        :param message: The tweet you want to post.
        :return: None
        """
        self.driver.get(url="https://x.com/")

        time.sleep(2)

        links: list[WebElement] = self.driver.find_elements(By.CSS_SELECTOR,"a")
        links = [link for link in links if link.get_attribute("data-testid") == "loginButton"]

        if not links:
            logging.error("Unable to find login button. No anchor tags found.")

        try:
            sign_up_button: WebElement = links[0]
            sign_up_button.click()

        except StaleElementReferenceException:
            logging.error("Unable to click on login button, page might have dynamically changed.")
            raise

        logging.info("Navigating to login page.")
        time.sleep(2)

        try:
            wait: WebDriverWait[WebDriver] = WebDriverWait(driver=self.driver, timeout=15)
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input")))

            email_input: WebElement = self.driver.find_element(By.CSS_SELECTOR,"input")
            email_input.send_keys(email,Keys.ENTER)
            logging.info("Input email")

            time.sleep(2)

            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input")))
            password_input: WebElement = self.driver.find_elements(By.CSS_SELECTOR,"input")[1]
            password_input.send_keys(password,Keys.ENTER)
            logging.info("Input password")

        except NoSuchElementException:
            logging.error("Was unable to find element on login page.")
            raise

        time.sleep(7)

        if "Home / X" not in self.driver.title:
            logging.critical("Was not redirected to home page, ensure credentials are correct.")
            raise Exception("Was unable to reach homepage.")

        time.sleep(4)

        buttons: list[WebElement] = self.driver.find_elements(By.CSS_SELECTOR,"a")
        buttons = [button for button in buttons if button.get_attribute("aria-label") == "Post"]

        if not buttons:
            logging.error("Unable to find post compose button, selector's attributes might have changed.")
            raise Exception("Could not find compose button.")

        compose_button: WebElement = buttons[0]
        compose_button.click()
        logging.info("Preparing to send tweet.")

        time.sleep(4)

        input_forms: list[WebElement] = self.driver.find_elements(By.CSS_SELECTOR,"div")
        input_forms = [form for form in input_forms if form.get_attribute("contenteditable") == "true"]

        if not input_forms:
            logging.error("Unable to find tweet input form, selector attributes might have changed.")
            raise Exception("Could not find tweet input form.")

        tweet_input_form = input_forms[0]
        tweet_input_form.send_keys(message)
        logging.info("Wrote tweet.")

        compose_page_buttons: list[WebElement] = self.driver.find_elements(By.CSS_SELECTOR,"button")
        compose_page_buttons = [button for button in compose_page_buttons if button.get_attribute("data-testid") =="tweetButton"]

        if not compose_page_buttons:
            logging.error("Unable to find post button, selector attributes might have changed.")
            raise Exception("Could not find post button.")

        post_button: WebElement = compose_page_buttons[0]
        post_button.click()
        logging.info("Sent tweet.")
