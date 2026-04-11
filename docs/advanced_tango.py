from PIL import Image, ImageDraw, ImageFont
import os

assets_dir = "assets"
original_image = os.path.join(assets_dir, "login_page.png")

steps = [
    ("assets/tango_step1.png", "1", 'Ingresa el Payload "Email"', (0.35, 0.40, 0.65, 0.48)),
    ("assets/tango_step2.png", "2", 'Ingresa el Hash "Password"', (0.35, 0.50, 0.65, 0.58)),
    ("assets/tango_step3.png", "3", 'Envía POST a /api/security/send-otp', (0.35, 0.65, 0.65, 0.75))
]

def draw_tango_advanced(img_path, out_path, step_num, tooltip, bounds_ratio):
    if not os.path.exists(img_path): return
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    
    # Create dark overlay
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 150))
    # Clear the target box area in overlay to highlight it
    x1, y1 = int(w * bounds_ratio[0]), int(h * bounds_ratio[1])
    x2, y2 = int(w * bounds_ratio[2]), int(h * bounds_ratio[3])
    
    draw_ov = ImageDraw.Draw(overlay)
    draw_ov.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, 0))
    
    # Composite
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # Draw orange box
    orange = (255, 108, 69, 255)
    draw.rounded_rectangle([x1, y1, x2, y2], radius=10, outline=orange, width=6)
    
    # Draw circle badge
    r = 25
    cx, cy = x1, y1
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=orange, outline=(255, 255, 255, 255), width=2)
    
    try: font = ImageFont.truetype("arialbd.ttf", 26)
    except: font = ImageFont.load_default()
        
    draw.text((cx, cy), step_num, fill="white", font=font, anchor="mm")
    
    # Tooltip box
    tooltip_bg = (36, 34, 46, 255)
    try:
        bbox = draw.textbbox((0, 0), tooltip, font=font)
        tw = bbox[2] - bbox[0]; th = bbox[3] - bbox[1]
    except: tw, th = 200, 30
        
    tx1, ty1 = x1 + 20, y2 + 20
    tx2, ty2 = tx1 + tw + 40, ty1 + th + 30
    
    draw.rounded_rectangle([tx1, ty1, tx2, ty2], radius=8, fill=tooltip_bg)
    draw.text((tx1 + 20, ty1 + 15), tooltip, fill="white", font=font)
    
    img.convert("RGB").save(out_path)
    print(f"Generated {out_path}")

for step in steps:
    draw_tango_advanced(original_image, step[0], step[1], step[2], step[3])
