from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import time

class YouTubePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        self.driver.get("https://www.youtube.com")
        print("Loaded YouTube")

    def toggle_native_theme(self, target_theme: str = "Dark"):
        """
        Attempts to toggle YouTube's native theme via the settings menu.
        This is complex due to dynamic IDs, so it relies on text content.
        """
        try:
            # Click Avatar/Settings button
            print("Opening settings menu...")
            avatar_btn = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button#avatar-btn")
            ))
            avatar_btn.click()
            time.sleep(1) # Wait for animation

            # Click Appearance menu item
            print("Clicking Appearance...")
            # This selector is tricky as it changes. Looking for 'Appearance' text in menu items.
            appearance_item = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//ytd-compact-link-renderer[.//div[contains(text(), 'Appearance')]]")
            ))
            appearance_item.click()
            time.sleep(1)

            # Select the theme
            print(f"Selecting {target_theme} theme...")
            theme_option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//ytd-compact-link-renderer[.//div[contains(text(), '{target_theme}')]]")
            ))
            theme_option.click()
            print(f"Switched to {target_theme} theme")
            
            # Close menu by clicking outside (optional, usually it closes)
            time.sleep(1)
            # Click body to close if open
            self.driver.execute_script("document.body.click()")

        except Exception as e:
            print(f"Could not toggle native theme: {e}")
