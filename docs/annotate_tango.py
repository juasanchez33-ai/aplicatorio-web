from PIL import Image, ImageDraw, ImageFont
import os

assets_dir = "assets"
original_images = [
    ("login_page.png", "1", "Click into the Login Box", (0.3, 0.4, 0.7, 0.6)),
    ("add_movement_modal.png", "2", "Type the expense amount", (0.2, 0.3, 0.8, 0.6)),
    ("dashboard_main.png", "3", "Review your Total Balance", (0.1, 0.1, 0.9, 0.4))
]

def draw_tango(img_path, number, tooltip, bounds_ratio):
    if not os.path.exists(img_path):
        print(f"File not found: {img_path}")
        return
        
    img = Image.open(img_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # Calculate box coordinates
    x1 = int(w * bounds_ratio[0])
    y1 = int(h * bounds_ratio[1])
    x2 = int(w * bounds_ratio[2])
    y2 = int(h * bounds_ratio[3])
    
    # Draw orange box (rounded if possible, standard rect otherwise)
    orange = (255, 108, 69, 255) # #ff6c45
    radius = 10
    
    # Fake rounded rectangle for PIL
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, outline=orange, width=6)
    
    # Draw circle badge at top left
    r = 25
    cx, cy = x1, y1
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=orange, outline=(255, 255, 255), width=2)
    
    # Fast substitute for font
    try:
        font = ImageFont.truetype("arialbd.ttf", 26)
    except:
        font = ImageFont.load_default()
        
    # Text in circle
    draw.text((cx, cy), number, fill="white", font=font, anchor="mm")
    
    # Tooltip box
    tooltip_bg = (36, 34, 46, 255) # #24222e
    try:
        tw, th = draw.textsize(tooltip, font=font)
    except AttributeError:
        # PIL >= 10.0
        bbox = draw.textbbox((0, 0), tooltip, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
    box_w = tw + 40
    box_h = th + 30
    
    tx1 = x1
    ty1 = y2 + 15
    tx2 = tx1 + box_w
    ty2 = ty1 + box_h
    
    draw.rounded_rectangle([tx1, ty1, tx2, ty2], radius=8, fill=tooltip_bg)
    draw.text((tx1 + 20, ty1 + 15), tooltip, fill="white", font=font)
    
    out_path = img_path.replace(".png", "_tango.png")
    img.convert("RGB").save(out_path)
    print(f"Saved {out_path}")

for args in original_images:
    path = os.path.join(assets_dir, args[0])
    draw_tango(path, args[1], args[2], args[3])
