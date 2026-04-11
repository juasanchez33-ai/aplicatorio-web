from PIL import Image, ImageDraw, ImageFont
import os
import glob

assets_dir = "assets"

def get_tooltip_for_file(filename):
    name = filename.lower()
    if 'login' in name: return "1", "Ingresa tus credenciales aquí"
    if 'register' in name: return "2", "Completa el formulario de registro"
    if 'dashboard' in name: return "3", "Revisa tus gráficas interactivas"
    if 'movement' in name: return "4", "Registra un nuevo ingreso/gasto"
    if 'debt' in name: return "5", "Control de pasivos y saldo adeudado"
    if 'payment' in name: return "6", "Pestaña de pagos pre-programados"
    if 'news' in name: return "7", "Indicadores de la macroeconomía mundial"
    if 'profile' in name: return "8", "Edita tu información personal"
    if 'settings' in name: return "9", "Ajusta la interfaz de usuario y MFA"
    if 'study' in name: return "10", "Balancea tu capital: 50% - 30% - 20%"
    if 'recover' in name: return "11", "Recuperación de contraseña vía SMTP"
    return "*", "Interacción y vista de usuario"

def draw_tango(img_path):
    filename = os.path.basename(img_path)
    if "_tango.png" in filename: return
    
    out_path = img_path.replace(".png", "_tango.png")
    
    try:
        img = Image.open(img_path).convert("RGBA")
    except Exception as e:
        print(f"Error opening {img_path}: {e}")
        return
        
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    number, tooltip = get_tooltip_for_file(filename)
    
    # Generic center-bottom or general highlight
    # Let's highlight a section in the middle of the screen
    x1, y1 = int(w * 0.1), int(h * 0.15)
    x2, y2 = int(w * 0.9), int(h * 0.85)

    # Some screens are small. Adjust.
    if w > 800:
        x1, y1 = int(w * 0.2), int(h * 0.2)
        x2, y2 = int(w * 0.8), int(h * 0.8)
    
    orange = (255, 108, 69, 255)
    draw.rounded_rectangle([x1, y1, x2, y2], radius=15, outline=orange, width=5)
    
    r = 25
    cx, cy = x1, y1
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=orange)
    
    try:
        font = ImageFont.truetype("arialbd.ttf", 26)
    except:
        font = ImageFont.load_default()
        
    draw.text((cx, cy), number, fill="white", font=font, anchor="mm")
    
    tooltip_bg = (36, 34, 46, 255)
    try:
        bbox = draw.textbbox((0, 0), tooltip, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    except AttributeError:
        tw, th = 200, 30
        
    box_w = tw + 40
    box_h = th + 30
    
    tx1 = x1 + 30
    ty1 = y2 + 15
    tx2 = tx1 + box_w
    ty2 = ty1 + box_h
    
    draw.rounded_rectangle([tx1, ty1, tx2, ty2], radius=8, fill=tooltip_bg)
    draw.text((tx1 + 20, ty1 + 15), tooltip, fill="white", font=font)
    
    img.convert("RGB").save(out_path)
    print(f"Annotated: {out_path}")

for f in glob.glob(os.path.join(assets_dir, "*.png")):
    draw_tango(f)
