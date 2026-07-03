import os
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def generate_daily_log_base64(log_date, status_intervals, total_trip_miles, origin_city, dest_city):
    # Target the high-resolution template verbatim
    asset_path = os.path.join(os.path.dirname(__file__), 'assets', 'Gemini_Generated_Image_8xvv4o8xvv4o8xvv.png')
    
    if not os.path.exists(asset_path):
        img = Image.new('RGB', (2000, 2000), color='white')
        img.save(asset_path)

    base_image = Image.open(asset_path).convert("RGB")
    draw = ImageDraw.Draw(base_image)
    
    # --- PIXEL-PERFECT ALIGNMENT CALIBRATION ---
    X_START = 260    
    X_END = 1820     
    PIXELS_PER_HOUR = (X_END - X_START) / 24.0
    
    # Stretched apart to perfectly bisect the taller grid cells
    Y_LINES = {
        "Off Duty": 800,
        "Sleeper Berth": 870,
        "Driving": 940,
        "On Duty": 1010
    }
    
    # --- STYLE SETTINGS ---
    LINE_COLOR = (10, 132, 255) 
    LINE_WIDTH = 6  
    
    totals = {
        "Off Duty": 0.0,
        "Sleeper Berth": 0.0,
        "Driving": 0.0,
        "On Duty": 0.0
    }
    
    # 1. Draw the Graph Lines and Aggregate Totals
    for idx, interval in enumerate(status_intervals):
        status = interval["status"]
        t_start = interval["start"]
        t_end = interval["end"]
        duration = t_end - t_start
        
        if status in totals:
            totals[status] += duration
        
        y = Y_LINES.get(status, 800)
        x1 = X_START + (t_start * PIXELS_PER_HOUR)
        x2 = X_START + (t_end * PIXELS_PER_HOUR)
        
        # Draw horizontal duration line
        draw.line([(x1, y), (x2, y)], fill=LINE_COLOR, width=LINE_WIDTH)
        
        # Draw vertical transition drop line
        if idx < len(status_intervals) - 1:
            next_status = status_intervals[idx + 1]["status"]
            next_y = Y_LINES.get(next_status, 800)
            draw.line([(x2, y), (x2, next_y)], fill=LINE_COLOR, width=LINE_WIDTH)
            
    # 2. Fill the Form Details with Pixel-Perfect Alignment
    try:
        # Load a scalable system font
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except IOError:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            except IOError:
                font = ImageFont.load_default()
        
        # --- Date & Routing ---
        draw.text((700, 40), f"{log_date}", fill=(0, 0, 0), font=font) 
        draw.text((360, 140), origin_city, fill=(0, 0, 0), font=font)
        draw.text((1100, 140), dest_city, fill=(0, 0, 0), font=font)
        
        # --- Mileage Information ---
        total_driving_miles = round(totals["Driving"] * 60) 
        draw.text((220, 285), f"{total_driving_miles} mi", fill=(0, 0, 0), font=font)        
        
        # --- Total Hours Column (Far Right) ---
        TOTALS_X = 1870
        
        # Decoupled from Y_LINES: Hardcoded to sit perfectly on the printed underlines
        draw.text((TOTALS_X, 765), f"{totals['Off Duty']:.1f}", fill=(0, 0, 0), font=font)
        draw.text((TOTALS_X, 835), f"{totals['Sleeper Berth']:.1f}", fill=(0, 0, 0), font=font)
        draw.text((TOTALS_X, 905), f"{totals['Driving']:.1f}", fill=(0, 0, 0), font=font)
        draw.text((TOTALS_X, 975), f"{totals['On Duty']:.1f}", fill=(0, 0, 0), font=font)
        
        # Shifted slightly down so the 24.0 sits securely on the final underline
        grand_total = sum(totals.values())
        draw.text((TOTALS_X, 1090), f"{grand_total:.1f}", fill=(0, 0, 0), font=font)
        
    except Exception as e:
        print(f"Font drawing error: {e}")
        pass 
        
    buffer = BytesIO()
    base_image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")