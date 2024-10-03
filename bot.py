import cv2
import numpy as np
from pynput.mouse import Controller, Button, Listener
import keyboard
import time
import mss

# Variable to keep track of whether the bot is enabled or not
enabled = False
frame1 = None  # Initialize frame1

# Function to handle mouse events (toggle on right click)
def on_click(x, y, button, pressed):
    global enabled, frame1
    if button == Button.right and pressed:
        time.sleep(0.3)  # Wait for 0.3 seconds after right-click
        enabled = not enabled  # Toggle the enabled state
        if enabled:
            print('Right-click detected, bot activated')
            frame1 = None  # Reset frame1 when the bot is activated
        else:
            print('Right-click detected, bot deactivated')

# Start of the actual script
if __name__ == '__main__':
    print('Starting...')

    # Setting up the mouse controller
    mouse = Controller()
    tm = int(round(time.time() * 1000))
    fps = 1
    fps1 = 0

    # Define the monitor region for screenshot (e.g., at position 955, 535 with 10x10 pixels)
    monitor = {"top": 535, "left": 955, "width": 10, "height": 10}

    # Create an instance of mss for fast screenshot capture
    with mss.mss() as sct:
        # Start a mouse listener in a separate thread
        with Listener(on_click=on_click) as listener:
            # Start a while loop to loop infinitely and as fast as possible
            while True:
                # Capture the screen in the defined region
                img = np.array(sct.grab(monitor))
                # Calculate the sum of all pixel values in the captured region
                frame = img.sum()

                # Checks if the bot is active (right-click toggles activation)
                if enabled:
                    # If frame1 is None, initialize it with the current frame value
                    if frame1 is None:
                        frame1 = frame

                    # If the picture value is different, the bot will shoot and deactivate itself
                    if frame1 > (frame + 200) or frame1 < (frame - 200):  # Adjust threshold based on sensitivity
                        keyboard.press('u')  # Press 'u' instead of clicking the mouse
                        time.sleep(0.2)
                        keyboard.release('u')  # Release 'u'
                        enabled = False  # Deactivate the bot after shooting
                        print('Shot')
                        print('Click')  # Print "Click" when the bot triggers the action

                    # If frame1 is not None and the picture value is not changing too much -> update it
                    if frame1 is not None and (frame1 > (frame + 50) or frame1 < (frame - 50)):  # Update based on a smaller threshold
                        frame1 = frame

                # Calculate FPS
                if int(round(time.time() * 1000)) - tm > 1000:
                    fps1 = fps
                    tm = int(round(time.time() * 1000))
                    fps = 0
                fps += 1

                # Show FPS and color values for debugging
                print(f'colorValue: {frame} FPS: {fps1}')

                # Press 'i' to quit
                if keyboard.is_pressed('i'):
                    break

            listener.join()  # Ensure the listener thread ends when the loop exits
