import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from src.pages.twitch_home_page import TwitchHomePage


@pytest.fixture(scope="function")
def browser():
    service = Service("/usr/bin/chromedriver")
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=375,812")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()


def test_twitch_search(browser):
    home_page = TwitchHomePage(browser)

    home_page.open_home_page()
    home_page.click_search_icon()
    home_page.search_for_game("StarCraft II")
    assert "StarCraft II" in browser.page_source, "Search result not found"
    home_page.scroll_down(2)
    home_page.select_streamer()
    assert "videos" in browser.current_url, "Streamer page not found"
    home_page.wait_for_stream_page_and_screenshot()
    print("Test passed!")
