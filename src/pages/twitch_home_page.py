from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time


class TwitchHomePage:
    def __init__(self, driver):
        self.driver = driver
        self.search_icon = (
            By.XPATH, "//a[div/div[contains(text(), 'Browse')]]")
        self.search_input = (
            By.CSS_SELECTOR, "input[data-a-target='tw-input']")

    def open_home_page(self):
        self.driver.get("https://m.twitch.tv/")
        time.sleep(3)
        print('Open Twitch home page')

    def click_search_icon(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.search_icon)
        ).click()
        print('Click search icon')
        time.sleep(5)

    def search_for_game(self, game_name):
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.search_input)
        )
        search_box.click()
        time.sleep(1)
        print('Search game name')
        search_box.clear()
        actions = ActionChains(self.driver)
        actions.move_to_element(search_box).click().perform()
        search_box.clear()
        self.driver.execute_script(
            "arguments[0].value = arguments[1];", search_box, game_name[:-1])

        time.sleep(1)

        # 手動輸入最後一字元，trigger Twitch search event
        search_box.send_keys(game_name[-1])
        time.sleep(1)

        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

    def scroll_down(self, times=2):
        for _ in range(times):
            self.driver.execute_script(
                "window.scrollBy(0, window.innerHeight);")
            time.sleep(2)

    def select_streamer(self):
        """Choose the first streamer on Twitch live list"""
        streamer_xpath = "//a[contains(@href, '/videos/') or contains(@href, '/channel/')]"
        streamer = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, streamer_xpath))
        )
        streamer.click()

    def wait_for_stream_page_and_screenshot(self):
        """Wait for the streamer's page to load and take a screenshot"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "video"))  # Waiting for video loading
        )
        time.sleep(3)
        self.driver.save_screenshot("streamer_page.png")
        print("Screenshot saved!")
