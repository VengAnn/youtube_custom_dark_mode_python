# YouTube Custom Dark & Light Mode Manager

A clean and structured Python project to customize YouTube's appearance using Selenium. This tool allows you to inject custom CSS for Dark and Light modes on the fly.

## Project Structure

- `main.py`: The entry point for the application. Interactive CLI menu.
- `src/`: Contains core logic.
  - `browser.py`: Handles Selenium WebDriver setup with best practices.
  - `styles_manager.py`: Logic to read and inject/remove CSS.
- `styles/`: Directory for your custom CSS files.
  - `dark_mode.css`: Custom overrides for Dark Mode.
  - `light_mode.css`: Custom overrides for Light Mode.
- `requirements.txt`: List of Python dependencies.

## Prerequisites

- Python 3.8+
- Google Chrome browser installed.

## Setup

1. **Create and Activate a Virtual Environment (Optional but Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script:

```bash
python3 main.py
```

Follow the on-screen menu to:
1. Launch YouTube.
2. Apply your custom Dark Mode or Light Mode CSS.
3. Clear styles to return to default.

## Customization

Edit the CSS files in the `styles/` directory to change the appearance.
- `styles/dark_mode.css`: Add your dark theme CSS here.
- `styles/light_mode.css`: Add your light theme CSS here.

The application automatically reloads the CSS content when you select the option in the menu, so you can edit the files while the script is running.


# run project 
- bash run.sh