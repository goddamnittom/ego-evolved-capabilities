import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import random

def create_smoke_frame(base_img, frame_num, total_frames):
    # Create a copy of the base image
    frame = base_img.copy()
    width, height = frame.size
    
    # Create a smoke layer
    smoke_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(smoke_layer)
    
    # Simulate hazy room: a low-opacity white overlay that fluctuates
    haze_opacity = int(40 + 20 * np.sin(2 * np.pi * frame_num / total_frames))
    haze = Image.new('RGBA', (width, height), (220, 220, 220, haze_opacity))
    
    # Animate the existing smoke cloud: shift it slightly and add "drifting" particles
    # In a real implementation, we would mask the smoke from the original image
    # Here we simulate it by adding semi-transparent white blobs that drift up
    for i in range(15):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(40, 120)
        # Drift the particles based on frame_num
        offset_y = - (frame_num * 5 + (i * 10)) % height
        
        # Draw blurred circles to look like smoke
        draw.ellipse([x, y + offset_y, x + size, y + offset_y + size], 
                     fill=(255, 255, 255, random.randint(30, 100)))
    
    smoke_layer = smoke_layer.filter(ImageFilter.GaussianBlur(radius=15))
    
    # Composite: Base -> Haze -> Drifting Smoke
    combined = Image.alpha_composite(frame.convert('RGBA'), haze)
    combined = Image.alpha_composite(combined, smoke_layer)
    
    return combined.convert('RGB')

# This is a simulation since I don't have the actual binary file in /root yet.
# I will create a dummy image to prove the logic works, then output the final GIF.
base = Image.new('RGB', (480, 800), color=(100, 100, 100))
frames = [create_smoke_frame(base, i, 20) for i in range(20)]
frames[0].save('smoke_animation.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)
