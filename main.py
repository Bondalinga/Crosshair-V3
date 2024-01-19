# Stop outputting to console
import os
import sys
sys.stdout = open(os.devnull, 'w')

Installing = True
while Installing:
    try:
        import config
        import subprocess
        import threading
        import tkinter as tk
        from tkinter import ttk
        import keyboard
        import pygame
        import time
        import pyautogui
        import sys
        import colorama
        import win32gui
        import win32con
        import time
        import shutil
        import ctypes
        import json
        Installing = False  # All modules are successfully imported, exit the loop
    except ImportError as e:
        print(f"Installing missing module: {e.name}")
        subprocess.check_call(["python", "-m", "pip", "install", e.name])


import threading
import tkinter as tk
from tkinter import ttk
import keyboard
import pygame
import time
from colorama import *
from crosshair import CrosshairOverlay
import ctypes
import config
import subprocess
import shutil
import json
if not pygame.get_init():
    pygame.init()

# Initialize pygame for sound
sound_path = "Bin/click.mp3"
pygame.mixer.init()
click_sound = pygame.mixer.Sound(sound_path)

app = None  # Initialize the global variable
visible = True  # Initialize the 'visible' variable
crosshair_visible = True

# Declare global variables for GUI elements
size_var = None
width_var = None
distance_var = None
color_r_var = None
color_g_var = None
color_b_var = None
draggable_area = None
root = None

# Initialize previous values
prev_size = None
prev_width = None
prev_distance = None
prev_color_r = None
prev_color_g = None
prev_color_b = None


def update_crosshair():
    global app  # Declare app as a global variable

    # Update values in config.py
    update_config_values()

    click_sound.play()

    # Destroy the existing overlay, if any
    destroy_existing_overlay()

    # Create a new instance of CrosshairOverlay with the updated values
    create_crosshair_overlay()

def update_config_values():
    config.size = size_var.get()
    config.width = width_var.get()
    config.distance = distance_var.get()
    config.color_r = color_r_var.get()
    config.color_g = color_g_var.get()
    config.color_b = color_b_var.get()

def destroy_existing_overlay():
    global app
    if app:
        app.after(150, app.destroy)  # Destroy the existing overlay, if any 
#                                                                                                                                                                                                                                                                                                                                                                                       # Sigma Doodle Bird
def create_crosshair_overlay():
    global app
    app = CrosshairOverlay(config.size, config.width, config.distance,
                           config.color_r, config.color_g, config.color_b, config.crosshair_visible)
    app.after(0, app._update_crosshair)  # Call the update function periodically
    app.lift()  # Make the window always on top

def update_draggable_area_color():
    draggable_area.config(bg=f'#{config.color_r:02X}{config.color_g:02X}{config.color_b:02X}')

def on_close():
    click_sound.play()
    os.kill(os.getpid(), 9)

SW_HIDE = 0
SW_SHOW = 5

def toggle_console():
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')

    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        if user32.IsWindowVisible(hWnd):
            user32.ShowWindow(hWnd, SW_HIDE)
        else:
            user32.ShowWindow(hWnd, SW_SHOW)

def toggle_visibility():
    global visible
    if visible:
        root.withdraw()
    else:
        root.deiconify()
        click_sound.play()
    visible = not visible
    time.sleep(0.1)

def check_insert_key():
    if keyboard.is_pressed('insert'):
        toggle_visibility()
        time.sleep(0.1)
    root.after(100, check_insert_key)  # Check every 100 milliseconds

def check_f2_key():
    if keyboard.is_pressed('f2'):
        update_crosshair()
        app.toggle_visibility()
        time.sleep(0.1)
    root.after(100, check_f2_key)  # Check every 100 milliseconds

def check_f3_key():
    if keyboard.is_pressed('f3'):
        toggle_console()
        time.sleep(0.1)
    root.after(100, check_f3_key)  # Check every 100 milliseconds

def start_drag(event):
    global win_x, win_y, mouse_x, mouse_y, dragging
    win_x = root.winfo_x()
    win_y = root.winfo_y()
    mouse_x = event.x_root
    mouse_y = event.y_root
    dragging = True

def stop_drag(event):
    global dragging
    dragging = False

def drag(event):
    global win_x, win_y, mouse_x, mouse_y, dragging
    if dragging:
        new_x = win_x + (event.x_root - mouse_x)
        new_y = win_y + (event.y_root - mouse_y)
        root.geometry(f"+{new_x}+{new_y}")

def run_gui():
    # Create main window
    global root
    root = tk.Tk()
    root.title("Crosshair Customizer")
    root.configure(bg='#222222')  # Set a black and gray background color
    root.overrideredirect(True)  # Remove the top bar
    root.wm_attributes("-topmost", True)

    # Draggable area with RGB color
    global draggable_area
    draggable_area = tk.Canvas(root, bg=f'#{config.color_r:02X}{config.color_g:02X}{config.color_b:02X}', height=20, width=root.winfo_reqwidth())
    draggable_area.grid(row=0, column=0, columnspan=4, sticky=tk.W + tk.E)
    draggable_area.bind("<Button-1>", start_drag)
    draggable_area.bind("<B1-Motion>", drag)
    draggable_area.bind("<ButtonRelease-1>", stop_drag)

    # Set a bold font with a white color
    bold_font = ('Helvetica', 10, 'bold')  # Using Helvetica font for a modern look

    # Title with a white color
    title_text = "Crosshair V3"
    title_label = draggable_area.create_text(10, 10, text=title_text, anchor=tk.W, font=bold_font, fill='white')  # White text color

    # Crosshair size
    global size_var
    size_label = tk.Label(root, text="Size", bg='#222222', fg='white', font=bold_font)  # Set label color and background
    size_var = tk.Scale(root, from_=1, to=25, orient=tk.HORIZONTAL, bg='#222222', fg='white', font=bold_font)
    size_var.set(config.size)
    size_label.grid(row=1, column=0)
    size_var.grid(row=1, column=1)

    # Crosshair width
    global width_var
    width_label = tk.Label(root, text="Width", bg='#222222', fg='white', font=bold_font)
    width_var = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, bg='#222222', fg='white', font=bold_font)
    width_var.set(config.width)
    width_label.grid(row=2, column=0)
    width_var.grid(row=2, column=1)

    # Crosshair distance
    global distance_var
    distance_label = tk.Label(root, text="Distance", bg='#222222', fg='white', font=bold_font)
    distance_var = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, bg='#222222', fg='white', font=bold_font)
    distance_var.set(config.distance)
    distance_label.grid(row=3, column=0)
    distance_var.grid(row=3, column=1)

    # Function to update color in real-time
    def update_color_realtime(event=None):
        draggable_area.config(bg=f'#{color_r_var.get():02X}{color_g_var.get():02X}{color_b_var.get():02X}')


    # Draw Functions
    def draw_top():
        config.draw_top = not config.draw_top
        update_button_color()
        click_sound.play()
        update_crosshair()

    def draw_bottom():
        config.draw_bottom = not config.draw_bottom
        update_button_color()
        click_sound.play()
        update_crosshair()

    def draw_right():
        config.draw_right = not config.draw_right
        update_button_color()
        click_sound.play()
        update_crosshair()

    def draw_left():
        config.draw_left = not config.draw_left
        update_button_color()
        click_sound.play()
        update_crosshair()

    def update_button_color():
        top_text.config(fg='Lime' if config.draw_top else 'red')
        bottom_text.config(fg='Lime' if config.draw_bottom else 'red')
        right_text.config(fg='Lime' if config.draw_right else 'red')
        left_text.config(fg='Lime' if config.draw_left else 'red')

    # Initialize buttons with default color
    top_text = tk.Button(root, text="Draw Top", bg='#222222', fg='red', font=bold_font, command=draw_top)
    top_text.grid(row=4, column=0, sticky=tk.E)

    bottom_text = tk.Button(root, text="Draw Bottom", bg='#222222', fg='red', font=bold_font, command=draw_bottom)
    bottom_text.grid(row=4, column=2, sticky=tk.W)

    right_text = tk.Button(root, text="Draw Right", bg='#222222', fg='red', font=bold_font, command=draw_right)
    right_text.grid(row=5, column=0, sticky=tk.E)

    left_text = tk.Button(root, text="Draw Left", bg='#222222', fg='red', font=bold_font, command=draw_left)
    left_text.grid(row=5, column=2, sticky=tk.W)

    # Update button colors based on config values
    update_button_color()

    # Color Text
    color_text = tk.Label(root, text="Colour (RGB)", bg='#222222', fg='white', font=bold_font)
    color_text.grid(row=7, column=1)

    # Red component
    global color_r_var
    color_r_var = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, bg='#222222', fg='white', font=bold_font, command=update_color_realtime)
    color_r_var.set(config.color_r)
    color_r_var.grid(row=8, column=0, sticky=tk.W)

    # Green component
    global color_g_var
    color_g_var = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, bg='#222222', fg='white', font=bold_font, command=update_color_realtime)
    color_g_var.set(config.color_g)
    color_g_var.grid(row=8, column=1, sticky=tk.W)

    # Blue component
    global color_b_var
    color_b_var = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, bg='#222222', fg='white', font=bold_font, command=update_color_realtime)
    color_b_var.set(config.color_b)
    color_b_var.grid(row=8, column=2, sticky=tk.W)

    # Save Config
    def save_config():
        update_config_values()
        config_content = f"# config.py\n# Default configuration values\nsize = {config.size}\nwidth = {config.width}\ndistance = {config.distance}\ncolor_r = {config.color_r}\ncolor_g = {config.color_g}\ncolor_b = {config.color_b}\ncrosshair_visible = {config.crosshair_visible}\ndraw_top = {config.draw_top}\ndraw_bottom = {config.draw_bottom}\ndraw_right = {config.draw_right}\ndraw_left = {config.draw_left}\noutline_width = 0"
        with open('Bin/config.txt', 'w') as f:
            f.write(config_content)
        with open('config.py', 'w') as f:
            f.write(config_content)
        print(Fore.GREEN + "Saved Config!" + Fore.RESET)

    save_button = tk.Button(root, text="Save Config", bg='#222222', fg='white', font=bold_font, command=save_config)
    save_button.grid(row=9, column=0)

    # Update button
    update_button = tk.Button(root, text="Update", bg='#222222', fg='white', font=bold_font, command=update_crosshair)
    update_button.grid(row=9, column=1)

    # Close Button
    close_button = tk.Button(root, text="Close", bg='#222222', fg='white', font=bold_font, command=on_close)
    close_button.grid(row=9, column=2)

    # Start checking for 'insert' key
    root.after(100, check_insert_key)
    root.after(100, check_f2_key)
    root.after(100, check_f3_key)

    # Run the GUI
    root.mainloop()

version = None
def version_text():
    with open('Bin/version.txt', 'r') as f:
        return f.read()

def on_start():
    print(Fore.RED + """------------------------------------------------------------
 _____                   _           _        _   _  _____ 
/  __ \                 | |         (_)      | | | ||____ |
| /  \/_ __ ___  ___ ___| |__   __ _ _ _ __  | | | |    / /
| |   | '__/ _ \/ __/ __| '_ \ / _` | | '__| | | | |    \ \\
| \__/\ | | (_) \__ \__ \ | | | (_| | | |    \ \_/ /.___/ /
 \____/_|  \___/|___/___/_| |_|\__,_|_|_|     \___/ \____/ 
""", "\n------------------------------------------------------------\n"+Fore.GREEN+"Version: "+version_text()+Fore.LIGHTRED_EX+"\nCredits To: bondalinga, On Discord\n\n"+Fore.CYAN+"Controls:\nInsert: Toggle Gui\nF2: Toggle Crosshair\nF3: Toggle Console\n\n"+Fore.LIGHTMAGENTA_EX+"Note: If Crosshair Doesnt Appear Click The Update Button.\n"+colorama.Style.RESET_ALL)

if __name__ == "__main__":
    # Start output to console
    sys.stdout = sys.__stdout__
    colorama.init(convert=True)
    gui_thread = threading.Thread(target=run_gui)
    gui_thread.start()
    on_start()