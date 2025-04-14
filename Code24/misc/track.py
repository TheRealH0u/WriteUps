import cv2
import numpy as np
from PIL import Image, ImageDraw

# Function to extract frames from a GIF
def extract_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []
    while True:
        frame = gif.copy()
        frames.append(frame)
        try:
            gif.seek(gif.tell() + 1)
        except EOFError:
            break
    return frames

# Function to detect the object in each frame
# Function to detect the object in each frame
def detect_object_position(frames):
    positions = []  # To store the positions (x, y) of the object
    prev_frame = None
    
    for frame in frames:
        # Ensure the frame is in RGB format (drop alpha channel if necessary)
        frame = frame.convert('RGB')
        frame_cv = np.array(frame)  # Convert PIL image to OpenCV format
        gray = cv2.cvtColor(frame_cv, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
        
        if prev_frame is None:
            prev_frame = gray
            continue
        
        # Find the difference between the current and previous frame
        diff = cv2.absdiff(gray, prev_frame)
        
        # Threshold the difference to find the moving object
        _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
        
        # Find contours to detect the object
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Assuming the largest contour is the object
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                positions.append((cx, cy))
        
        prev_frame = gray
    
    return positions

# Function to create a PNG image with the object's path
def draw_path_on_image(positions, output_path):
    # Create a blank white image (PNG)
    img_width = 800  # You can adjust this based on the size of the GIF
    img_height = 600
    path_image = Image.new("RGB", (img_width, img_height), (255, 255, 255))
    draw = ImageDraw.Draw(path_image)
    
    # Draw the path (as a red line connecting the positions)
    for i in range(1, len(positions)):
        draw.line([positions[i-1], positions[i]], fill="red", width=2)
    
    # Save the final image
    path_image.save(output_path)

# Example usage
gif_path = 'in.gif'  # Replace with the path to your GIF
output_path = 'object_path.png'    # The path where the PNG will be saved

frames = extract_frames(gif_path)        # Extract frames from the GIF
positions = detect_object_position(frames)  # Track the object and get positions
draw_path_on_image(positions, output_path)  # Draw the path and save as PNG
