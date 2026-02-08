import json
import os

def generate_css():
    try:
        with open('extracted_vars.json', 'r') as f:
            # Skip the first line "--- STRUCTURAL COLORS ---"
            lines = f.readlines()
            
        # Parse the structures part manually or splitty
        content = "".join(lines)
        
        # Split into structures and vars
        parts = content.split('--- ALL CSS VARIABLES')
        structural_json_str = parts[0].replace('--- STRUCTURAL COLORS ---', '').strip()
        vars_json_str = parts[1].split('---')[1].strip() # Get the JSON part after the header
        
        structures = json.loads(structural_json_str)
        variables = json.loads(vars_json_str)
        
        css_lines = []
        css_lines.append("/* === NUCLEAR OPTION LIGHT MODE v8 (Generated from Native Values) === */")
        css_lines.append("/* This file is auto-generated based on real YouTube Light Mode variables */")
        css_lines.append("")
        
        # 1. Structural Overrides
        css_lines.append("/* --- 1. Structural Backgrounds --- */")
        for selector, styles in structures.items():
            bg = styles.get('backgroundColor')
            # If transparent or black/dark in a light theme, force white
            # But the extraction showed transparency for many, which means they rely on underlying body/app color
            if bg == 'rgba(0, 0, 0, 0)':
                 pass # Don't force transparent things to white necessarily, unless they are overlaying
            
        # Force Body/App/Columns to White
        css_lines.append("body, html, ytd-app, #page-manager, #columns, #primary, #secondary, #content {")
        css_lines.append("    background-color: #ffffff !important;")
        css_lines.append("    color: #0f0f0f !important;")
        css_lines.append("}")
        css_lines.append("")

        # 2. Variable Overrides
        css_lines.append("/* --- 2. Global Variable Enforcement --- */")
        css_lines.append(":root, html, html[dark], body, [dark] {")
        
        # Sort variables for cleanliness
        for prop in sorted(variables.keys()):
            val = variables[prop]
            # Clean up value if needed
            if val:
                css_lines.append(f"    {prop}: {val} !important;")
        
        # Add some manual overrides that might not be in the extraction or need reinforcement
        css_lines.append("    /* Manual Reinforcements */")
        css_lines.append("    --yt-spec-base-background: #ffffff !important;")
        css_lines.append("    --yt-spec-raised-background: #f9f9f9 !important;")
        css_lines.append("    --yt-spec-text-primary: #0f0f0f !important;")
        css_lines.append("    --yt-spec-text-secondary: #606060 !important;")
        css_lines.append("    --yt-spec-inverted-background: #0f0f0f !important;")
        css_lines.append("}")
        css_lines.append("")
        
        # 3. Component Specifics (Search Bar, Chips)
        css_lines.append("/* --- 3. Component Fixes --- */")
        
        # Search Bar
        css_lines.append("ytd-searchbox, yt-searchbox, #container.ytd-searchbox, .ytSearchboxComponentInputContainer {")
        css_lines.append("    --ytd-searchbox-background: #ffffff !important;")
        css_lines.append("    background-color: #ffffff !important;")
        css_lines.append("    color: #0f0f0f !important;")
        css_lines.append("}")
        
        css_lines.append("input#search, input.ytSearchboxComponentInput {")
        css_lines.append("    color: #0f0f0f !important;")
        css_lines.append("    -webkit-text-fill-color: #0f0f0f !important;")
        css_lines.append("}")

        # Chips
        css_lines.append("yt-chip-cloud-chip-renderer {")
        css_lines.append("    background-color: #f2f2f2 !important;")
        css_lines.append("    color: #0f0f0f !important;")
        css_lines.append("}")
        css_lines.append("yt-chip-cloud-chip-renderer[selected] {")
        css_lines.append("    background-color: #0f0f0f !important;")
        css_lines.append("    color: #ffffff !important;")
        css_lines.append("}")
        
        # Video Titles & text
        css_lines.append("#video-title, h3, h1, span {")
        css_lines.append("    color: inherit;") # Inherit from our global force, but...
        css_lines.append("}")
        css_lines.append("#video-title { color: #0f0f0f !important; }")
        
        # Logo Fix
        css_lines.append("/* Logo Fix */")
        css_lines.append("ytd-topbar-logo-renderer path { fill: #000 !important; }")
        css_lines.append("ytd-topbar-logo-renderer path[fill*='FF00'] { fill: #FF0000 !important; }")
        css_lines.append("ytd-topbar-logo-renderer path[fill*='fff'], ytd-topbar-logo-renderer path[fill*='FFF'] { fill: #FFF !important; }")

        
        with open('styles/light_mode.css', 'w') as f:
            f.write("\n".join(css_lines))
            
        print("Successfully generated styles/light_mode.css")
        
    except Exception as e:
        print(f"Error generating CSS: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_css()
