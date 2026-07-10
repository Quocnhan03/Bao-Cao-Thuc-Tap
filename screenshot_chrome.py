import sys
import pygetwindow as gw
import pyautogui
import time

def capture_chrome(output_path):
    windows = gw.getWindowsWithTitle('Chrome')
    if not windows:
        windows = gw.getWindowsWithTitle('Google Chrome')
    
    if not windows:
        print("Could not find Chrome window")
        sys.exit(1)
        
    win = windows[0]
    
    if win.isMinimized:
        win.restore()
    win.activate()
    time.sleep(1)
    
    bbox = (win.left, win.top, win.width, win.height)
    print(f"Capturing bounds: {bbox}")
    
    screenshot = pyautogui.screenshot(region=bbox)
    screenshot.save(output_path)
    print(f"Saved to {output_path}")

if __name__ == '__main__':
    output = sys.argv[1] if len(sys.argv) > 1 else 'screenshot.png'
    capture_chrome(output)
