import sys
import os
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.browser import setup_browser

def extract_vars():
    driver = setup_browser(headless=True)
    try:
        print("Navigating to Video Page to capture full variable set...", file=sys.stderr)
        driver.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Use a real video to get watch-page vars
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "ytd-app")))
        time.sleep(8) # Wait for potential dynamic style injection

        print("Extracting ALL CSS variables...", file=sys.stderr)
        
        script = """
            const htmlStyles = getComputedStyle(document.documentElement);
            const allVars = {};
            
            // 1. Brute force iterate all styles to find custom properties
            // (Standard iteration might skip some, but it's the best we have without parsing stylesheets)
            for (let i = 0; i < htmlStyles.length; i++) {
                const prop = htmlStyles.item(i);
                if (prop.startsWith('--yt') || prop.startsWith('--paper')) {
                    allVars[prop] = htmlStyles.getPropertyValue(prop).trim();
                }
            }
            
            // 2. Inspect key structural elements for 'rogue' backgrounds
            const selectors = [
                'body', 'ytd-app', '#content', '#page-manager', '#columns', 
                '#primary', '#secondary', '#masthead-container', 
                'ytd-watch-flexy', '#cinematics', '#below'
            ];
            
            const structures = {};
            selectors.forEach(sel => {
                const el = document.querySelector(sel);
                if (el) {
                    const style = getComputedStyle(el);
                    structures[sel] = {
                        backgroundColor: style.backgroundColor,
                        color: style.color
                    };
                }
            });

            return {
                vars: allVars,
                structures: structures
            };
        """
        data = driver.execute_script(script)
        
        print("--- STRUCTURAL COLORS ---")
        print(json.dumps(data.get('structures'), indent=2))
        
        print("\n--- ALL CSS VARIABLES (Count: {}) ---".format(len(data.get('vars', {}))))
        # Print them all so we can parse them into the CSS file
        print(json.dumps(data.get('vars'), indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    extract_vars()
