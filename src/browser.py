from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional

def setup_browser(headless: bool = False, extension_paths: Optional[list[str]] = None) -> webdriver.Chrome:
    """Sets up the Chrome browser instance with clean options."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    
    # Standard clean options for stability
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    if extension_paths:
        for path in extension_paths:
            chrome_options.add_extension(path)

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver
