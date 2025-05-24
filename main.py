from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import uuid
from pathlib import Path
import subprocess
import tempfile
from termcolor import colored

# Define constants
OUTPUT_DIR = Path("static/output")
TEMPLATES_DIR = Path("templates")

# Create directories if they don't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="NetworkX Playground")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    print(colored("Serving the landing page", "green"))
    # Check if index.html exists in the root directory
    if Path("index.html").exists():
        return FileResponse("index.html")
    else:
        return templates.TemplateResponse("networkx_playground.html", {"request": request})

@app.get("/playground", response_class=HTMLResponse)
async def read_playground(request: Request):
    print(colored("Serving the NetworkX playground page", "green"))
    return templates.TemplateResponse("networkx_playground.html", {"request": request})

@app.get("/gemini_doc.html", response_class=HTMLResponse)
async def read_gemini_doc(request: Request):
    print(colored("Serving the Gemini documentation page", "green"))
    if Path("templates/gemini_doc.html").exists():
        return templates.TemplateResponse("gemini_doc.html", {"request": request})
    else:
        raise HTTPException(status_code=404, detail="Gemini documentation page not found")

@app.get("/networkx_playground.html", response_class=HTMLResponse)
async def read_networkx_playground_direct(request: Request):
    print(colored("Serving the NetworkX playground page directly", "green"))
    if Path("templates/networkx_playground.html").exists():
        return templates.TemplateResponse("networkx_playground.html", {"request": request})
    elif Path("networkx_playground.html").exists():
        return FileResponse("networkx_playground.html")
    else:
        raise HTTPException(status_code=404, detail="NetworkX playground page not found")

@app.post("/run-code")
async def run_python_code(code: str = Form(...)):
    try:
        print(colored(f"Running Python code: {code[:100]}...", "cyan"))
        
        # Create a unique filename for this execution
        run_id = str(uuid.uuid4())
        output_img_path = OUTPUT_DIR / f"{run_id}.png"
        
        # Create a temporary Python file to execute
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False, encoding="utf-8") as temp_file:
            # Prepare the Python code with necessary imports and path setup
            complete_code = f"""
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import platform
import sys
from matplotlib import font_manager, rcParams
import glob

# Define global variables
global custom_font_prop
custom_font_prop = None

# Configure Korean font
def set_korean_font():
    global custom_font_prop
    # Try to find Nanum fonts in standard locations
    font_found = False
    korean_font_name = None
    
    # Common paths for the Nanum font
    nanum_paths = [
        # Linux standard paths
        "/usr/share/fonts/truetype/nanum/*.ttf",
        "/usr/share/fonts/opentype/nanum/*.otf",
        # Ubuntu specific
        "/usr/share/fonts/truetype/nanum/*",
        # User fonts
        os.path.expanduser("~/.fonts/NanumGothic.ttf"),
        os.path.expanduser("~/.local/share/fonts/NanumGothic.ttf"),
        # Add more potential paths here
    ]
    
    # Find Nanum fonts
    found_fonts = []
    for path_pattern in nanum_paths:
        found_fonts.extend(glob.glob(path_pattern))
    
    if found_fonts:
        print(f"Found Korean fonts: {{found_fonts}}")
        # Register the first font found
        for font_path in found_fonts:
            try:
                font_manager.fontManager.addfont(font_path)
                print(f"Registered font from: {{font_path}}")
                korean_font_name = font_manager.FontProperties(fname=font_path).get_name()
                
                # Explicitly set this font for all text elements
                plt.rcParams['font.family'] = korean_font_name
                plt.rcParams['axes.unicode_minus'] = False
                
                # Use the same font for all text elements
                font_prop = font_manager.FontProperties(family=korean_font_name)
                mpl.rc('font', family=korean_font_name)
                
                # Create a custom FontProperties object to use throughout
                custom_font_prop = font_manager.FontProperties(family=korean_font_name)
                
                print(f"Set font family to: {{korean_font_name}}")
                font_found = True
                break
            except Exception as e:
                print(f"Error registering font {{font_path}}: {{e}}")
    
    if not font_found:
        try:
            # Fallback to system font detection
            system = platform.system()
            if system == 'Windows':
                # Common Korean fonts on Windows
                font_candidates = ['Malgun Gothic', 'Gulim', 'Batang', 'Gungsuh']
            elif system == 'Darwin':  # macOS
                font_candidates = ['AppleGothic', 'Apple SD Gothic Neo', 'NanumGothic']
            else:  # Linux and others
                font_candidates = ['NanumGothic', 'NanumBarunGothic', 'UnDotum', 'Noto Sans CJK KR']
            
            # Check if any of the candidate fonts are available
            for font in font_candidates:
                try:
                    # Check if font exists in the system
                    if any(f.name == font for f in font_manager.fontManager.ttflist):
                        plt.rcParams['font.family'] = font
                        mpl.rc('font', family=font)
                        custom_font_prop = font_manager.FontProperties(family=font)
                        print(f"Using system font: {{font}}")
                        font_found = True
                        break
                except Exception as e:
                    print(f"Error checking font {{font}}: {{e}}")
        except Exception as e:
            print(f"Error in font detection: {{e}}")
    
    # If no Korean fonts found, try to use the Noto Sans font which is included in most systems
    if not font_found:
        try:
            # Use generic sans-serif with UTF-8 encoding
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = ['Noto Sans CJK KR', 'Noto Sans', 'DejaVu Sans', 'Malgun Gothic']
            mpl.rc('font', family='sans-serif')
            mpl.rc('axes', unicode_minus=False)
            custom_font_prop = font_manager.FontProperties(family='sans-serif')
            print("Using generic sans-serif fonts")
        except Exception as e:
            print(f"Error setting generic fonts: {{e}}")
    
    # Set encoding to UTF-8 to prevent unicode minus issues
    plt.rcParams['axes.unicode_minus'] = False
    
    # Print debug info for fonts
    print("Available fonts:")
    for font in sorted([f.name for f in font_manager.fontManager.ttflist])[:20]:  # Show first 20 fonts only
        print(f"  - {{font}}")
    print(f"Current font family: {{plt.rcParams['font.family']}}")
    
    # This modifier function will apply our Korean font to all labels in NetworkX
    def apply_korean_font(func):
        def wrapper(*args, **kwargs):
            # Different NetworkX drawing functions accept different font parameters
            if func.__name__ == 'draw_networkx_labels':
                # draw_networkx_labels accepts font_family but not fontproperties
                if 'font_family' not in kwargs and korean_font_name:
                    kwargs['font_family'] = korean_font_name
            elif func.__name__ == 'draw_networkx_edge_labels':
                # draw_networkx_edge_labels accepts font_family but not fontproperties
                if 'font_family' not in kwargs and korean_font_name:
                    kwargs['font_family'] = korean_font_name
            else:
                # For other functions that might accept fontproperties
                if 'fontproperties' not in kwargs and custom_font_prop:
                    kwargs['fontproperties'] = custom_font_prop
            return func(*args, **kwargs)
        return wrapper
    
    # Patch NetworkX drawing functions to use our Korean font
    nx.draw_networkx_labels = apply_korean_font(nx.draw_networkx_labels)
    nx.draw_networkx_edge_labels = apply_korean_font(nx.draw_networkx_edge_labels)
    
    # Return if we found a Korean font
    return font_found, korean_font_name

# Apply font settings before running code
font_found, korean_font_name = set_korean_font()

# Set output directory
output_path = r"{output_img_path}"

# Turn interactive mode off
plt.ioff()

# Monkey patch the title function to ensure Korean font is used
original_title = plt.title
def title_with_korean_font(*args, **kwargs):
    if 'fontproperties' not in kwargs and custom_font_prop:
        kwargs['fontproperties'] = custom_font_prop
    return original_title(*args, **kwargs)
plt.title = title_with_korean_font

# Now run the actual code
{code}

# Ensure plot is saved
plt.savefig(output_path, bbox_inches='tight', dpi=100)
plt.close()
"""
            temp_file.write(complete_code)
            temp_path = temp_file.name
        
        # Execute the Python code
        result = subprocess.run(
            ["python", temp_path], 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        # Print debugging info
        print(colored("Execution output:", "cyan"))
        print(colored(result.stdout, "blue"))
        if result.stderr:
            print(colored("Execution errors:", "yellow"))
            print(colored(result.stderr, "red"))
        
        # Clean up the temporary file
        os.unlink(temp_path)
        
        # Check if the execution was successful
        if result.returncode != 0:
            print(colored(f"Error running code: {result.stderr}", "red"))
            raise HTTPException(status_code=500, detail=f"Error executing code: {result.stderr}")
        
        # Check if the image was created
        if not output_img_path.exists():
            print(colored("Image was not created", "red"))
            raise HTTPException(status_code=500, detail="Failed to generate plot")
        
        # Return the path to the generated image
        return {"image_path": f"/static/output/{run_id}.png"}
    
    except Exception as e:
        print(colored(f"Exception: {str(e)}", "red"))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print(colored("Starting NetworkX Playground Server...", "green"))
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 