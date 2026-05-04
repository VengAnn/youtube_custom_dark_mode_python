import webview
from pathlib import Path
import threading
import time

# CONFIGURATION
DEFAULT_THEME = 'DARK'

def inject_css(window, css_file):
    try:
        css_content = Path(css_file).read_text(encoding="utf-8")
        script = f"""
            var old_style = document.getElementById('custom-theme-injector');
            if (old_style) old_style.remove();
            var style = document.createElement('style');
            style.type = 'text/css';
            style.id = 'custom-theme-injector';
            style.textContent = `{css_content}`;
            document.head.appendChild(style);
        """
        window.evaluate_js(script)
    except Exception as e:
        print(f"Error injecting CSS: {e}")

def clear_css(window):
    script = """
        var style = document.getElementById('custom-theme-injector');
        if (style) style.remove();
    """
    window.evaluate_js(script)

class Api:
    def __init__(self):
        self.window = None

    def log_action(self, message):
        print(f"✅ [AdBlocker] {message}")

    def set_theme(self, theme_name):
        print(f"Applying theme: {theme_name}")
        if theme_name.upper() == 'DARK':
            js = """
            localStorage.setItem('custom_theme', 'DARK');
            document.cookie = "PREF=f6=400; expires=Thu, 31 Dec 2030 23:59:59 UTC; domain=.youtube.com; path=/";
            if (!document.documentElement.hasAttribute('dark')) {
                window.location.reload();
            }
            """
            try: self.window.evaluate_js(js)
            except: pass
            inject_css(self.window, "styles/dark_mode.css")
            
        elif theme_name.upper() == 'LIGHT':
            js = """
            localStorage.setItem('custom_theme', 'LIGHT');
            document.cookie = "PREF=f6=4; expires=Thu, 31 Dec 2030 23:59:59 UTC; domain=.youtube.com; path=/";
            if (document.documentElement.hasAttribute('dark')) {
                window.location.reload();
            }
            """
            try: self.window.evaluate_js(js)
            except: pass
            inject_css(self.window, "styles/light_mode.css")
            
        elif theme_name.upper() == 'CLEAR':
            try: self.window.evaluate_js("localStorage.removeItem('custom_theme');")
            except: pass
            clear_css(self.window)

def inject_control_panel(window):
    # Wait for the DOM to be fully ready
    time.sleep(2)
    
    # Inject a clean, floating UI panel to switch themes
    ui_script = """
    if (!document.getElementById('theme-control-panel')) {
        var panel = document.createElement('div');
        panel.id = 'theme-control-panel';
        panel.style.position = 'fixed';
        panel.style.bottom = '20px';
        panel.style.right = '20px';
        panel.style.zIndex = '999999';
        panel.style.background = 'rgba(20, 20, 20, 0.85)';
        panel.style.backdropFilter = 'blur(10px)';
        panel.style.padding = '12px';
        panel.style.borderRadius = '12px';
        panel.style.boxShadow = '0 4px 15px rgba(0,0,0,0.3)';
        panel.style.display = 'flex';
        panel.style.gap = '8px';
        panel.style.fontFamily = 'system-ui, -apple-system, sans-serif';
        
        function createBtn(text, theme) {
            var btn = document.createElement('button');
            btn.innerText = text;
            btn.style.background = '#333';
            btn.style.color = '#fff';
            btn.style.border = 'none';
            btn.style.padding = '8px 16px';
            btn.style.borderRadius = '6px';
            btn.style.cursor = 'pointer';
            btn.style.fontWeight = '500';
            btn.style.transition = 'background 0.2s';
            btn.onmouseover = () => btn.style.background = '#555';
            btn.onmouseout = () => btn.style.background = '#333';
            btn.onclick = () => pywebview.api.set_theme(theme);
            return btn;
        }
        
        panel.appendChild(createBtn('Dark Mode', 'DARK'));
        panel.appendChild(createBtn('Light Mode', 'LIGHT'));
        panel.appendChild(createBtn('Reset', 'CLEAR'));
        
        document.body.appendChild(panel);
    }
    """
    window.evaluate_js(ui_script)
    
    # Apply theme based on localStorage, or fallback to DEFAULT_THEME
    init_script = f"""
    var theme = localStorage.getItem('custom_theme') || '{DEFAULT_THEME}';
    if (theme === 'DARK') {{
        pywebview.api.set_theme('DARK');
    }} else if (theme === 'LIGHT') {{
        pywebview.api.set_theme('LIGHT');
    }}
    """
    window.evaluate_js(init_script)

def inject_adblock(window):
    adblock_script = """
    // YouTube Ad Auto-Skipper & Remover
    setInterval(() => {
        // 1. Auto-click 'Skip Ad' buttons
        const skipBtn = document.querySelector('.ytp-skip-ad-button') || document.querySelector('.ytp-ad-skip-button');
        if (skipBtn) {
            skipBtn.click();
            if (window.pywebview && window.pywebview.api) {
                window.pywebview.api.log_action('Skipped ad via button click!');
            }
        }
        
        // 2. Fast-forward video ads
        const adShowing = document.querySelector('.ad-showing') || document.querySelector('.ytp-ad-player-overlay');
        if (adShowing) {
            const video = document.querySelector('video');
            if (video && isFinite(video.duration) && video.currentTime < video.duration) {
                video.currentTime = video.duration;
                if (window.pywebview && window.pywebview.api) {
                    window.pywebview.api.log_action('Fast-forwarded unskippable ad!');
                }
            }
        }
        
        // 3. Remove popup ads and banners
        const adSelectors = [
            '.ytp-ad-overlay-container', 
            'ytd-ad-slot-renderer', 
            'ytd-banner-promo-renderer', 
            'ytd-promoted-sparkles-web-renderer',
            'ytd-in-feed-ad-layout-renderer',
            '#masthead-ad'
        ];
        let removedAds = false;
        adSelectors.forEach(selector => {
            const ads = document.querySelectorAll(selector);
            ads.forEach(ad => {
                ad.remove();
                removedAds = true;
            });
        });
        
        // Only log banner removals occasionally so we don't spam the console too much
        // but for testing, it's good to see it.
        // We will just silently remove banners to keep the terminal clean for video skips.
    }, 500); // Check every 500ms for ads
    """
    try:
        window.evaluate_js(adblock_script)
        print("Adblock script injected.")
    except Exception as e:
        print(f"Error injecting adblock: {e}")

def inject_custom_logo(window):
    try:
        import base64
        logo_path = Path("assets/tube_pro_logo.png")
        if logo_path.exists():
            encoded = base64.b64encode(logo_path.read_bytes()).decode('utf-8')
            b64_src = f"data:image/png;base64,{encoded}"
            logo_script = f"""
            setInterval(() => {{
                const logoContainer = document.querySelector('ytd-topbar-logo-renderer #logo');
                if (logoContainer && !logoContainer.hasAttribute('data-custom-logo')) {{
                    logoContainer.setAttribute('data-custom-logo', 'true');
                    logoContainer.innerHTML = `<div style="display: flex; align-items: center; padding-left: 16px;">
                        <img src="{b64_src}" style="height: 28px; width: 28px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.5);">
                        <span style="font-size: 20px; font-weight: 700; margin-left: 10px; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; letter-spacing: -0.5px; color: var(--yt-spec-text-primary, white);">Tube Pro</span>
                    </div>`;
                    
                    // Hide the country code if it exists next to the logo
                    const countryCode = document.querySelector('#country-code');
                    if(countryCode) countryCode.style.display = 'none';
                }}
            }}, 1000);
            """
            window.evaluate_js(logo_script)
            print("Custom logo injected.")
    except Exception as e:
        print(f"Error injecting custom logo: {e}")

def main():
    api = Api()
    
    # Create native window using pywebview
    window = webview.create_window(
        'YouTube (Native Webview)', 
        'https://www.youtube.com', 
        js_api=api, 
        width=1200, 
        height=800
    )
    api.window = window
    
    # When the page loads, inject our controls, CSS, and Adblock
    def on_loaded():
        try:
            current_url = window.get_current_url()
            if current_url and "youtube.com" in current_url:
                threading.Thread(target=inject_control_panel, args=(window,)).start()
                threading.Thread(target=inject_adblock, args=(window,)).start()
                threading.Thread(target=inject_custom_logo, args=(window,)).start()
        except Exception as e:
            print(f"Error in on_loaded: {e}")
        
    window.events.loaded += on_loaded
    
    # Start the app (private_mode=False allows saving cookies/login state)
    print("Starting native webview...")
    webview.start(private_mode=False)

if __name__ == '__main__':
    main()
