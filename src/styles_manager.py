from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
import time

def inject_styles(driver: WebDriver, style_path: Path):
    """
    Injects custom CSS from a file into the current YouTube page.
    This creates a <style> tag on the page to override existing styles.
    """
    if not style_path.exists():
        print(f"Error: Style file not found at {style_path}")
        return

    try:
        css_content = style_path.read_text(encoding="utf-8")
        # Ensure we escape quotes or create the style element safely
        # Standard approach: Create style element, set innerHTML, wait for it
        script = f"""
            var style = document.createElement('style');
            style.type = 'text/css';
            style.id = 'custom-theme-injector';
            style.textContent = `{css_content}`; // Use textContent to bypass TrustedHTML checks
            document.head.appendChild(style);
        """
        driver.execute_script(script)
        print(f"Successfully injected custom styles from {style_path.name}")
    except Exception as e:
        print(f"Failed to inject styles: {e}")

def clear_injected_styles(driver: WebDriver):
    """Removes the injected style tag."""
    script = """
        var style = document.getElementById('custom-theme-injector');
        if (style) {
            style.remove();
        }
    """
    driver.execute_script(script)
    print("cleared custom styles")
