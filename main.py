import sys
import time
from pathlib import Path
from src.browser import setup_browser
from src.styles_manager import inject_styles, clear_injected_styles
from selenium.webdriver.common.by import By

# CONFIGURATION: Set to 'DARK', 'LIGHT', or None
DEFAULT_THEME = 'DARK' 

def print_menu():
    print("\n--- YouTube Custom Theme Manager ---")
    print(f"Current Default: {DEFAULT_THEME}")
    print("1. Launch YouTube (Clean Browser)")
    print("2. Apply Custom Dark Mode")
    print("3. Apply Custom Light Mode")
    print("4. Clear Custom Styles")
    print("5. Switch Native Theme (Dark/Light)")
    print("6. Exit")
    print("------------------------------------")

def main():
    print("Initializing browser...")
    driver = setup_browser(headless=False)
    
    try:
        driver.get("https://www.youtube.com")
        print("YouTube loaded successfully.")

        # Auto-apply default theme
        if DEFAULT_THEME:
            print(f"Applying default theme: {DEFAULT_THEME}...")
            time.sleep(2) # Wait a bit for page to settle
            if DEFAULT_THEME.upper() == 'DARK':
                inject_styles(driver, Path("styles/dark_mode.css"))
            elif DEFAULT_THEME.upper() == 'LIGHT':
                inject_styles(driver, Path("styles/light_mode.css"))

        while True:
            # Re-focus on terminal for input
            print_menu()
            choice = input("Enter your choice (1-5): ").strip()

            if choice == '1':
                driver.get("https://www.youtube.com")
                print("Reloaded YouTube.")
            
            elif choice == '2':
                style_path = Path("styles/dark_mode.css")
                inject_styles(driver, style_path)
                print("Applied Dark Mode CSS.")

            elif choice == '3':
                style_path = Path("styles/light_mode.css")
                inject_styles(driver, style_path)
                print("Applied Light Mode CSS.")

            elif choice == '4':
                clear_injected_styles(driver)
                print("Cleared custom styles.")

            elif choice == '5':
                from src.youtube import YouTubePage
                yt = YouTubePage(driver)
                print("Attempting to toggle native theme (make sure you are logged in for this to work best)...")
                # Simple toggle logic - just switches to opposite of what user thinks, or cycle
                # Since we can't easily detect current state reliably without complex logic, we'll ask user
                target = input("Switch to (Dark/Light)? ").strip().capitalize()
                if target in ['Dark', 'Light']:
                    yt.toggle_native_theme(target)
                else:
                    print("Invalid theme choice.")

            elif choice == '6':
                print("Closing browser...")
                break
            
            else:
                print("Invalid choice. Please try again.")
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
