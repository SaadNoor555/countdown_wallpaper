from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import time
import ctypes
from datetime import datetime


########## Change values to configure layout ############
TARGET_TIME = '2023-09-28 00:00:00'         # Finishing date
IMG_PATH = r'pic\bgPic.png'             # base pic directory
FONT_PATHS = ['fonts\Poppins-Bold.ttf', 'fonts\SpaceMono-Regular.ttf']  #fonts
OUT_DIR = 'pic'                 # output folder
OUTPUT_FILE_NAME = 'wallpaper.png'  #output file name


# Batch name
BATCH_TEXT = {
    'value': 'BSSE 11',
    'coords': (830, 100),   # (x, y) of left top corner
    'font': FONT_PATHS[0],
    'font-size': 100,
    'fill': (0, 0, 0)
}
# Batch slogan
BATCH_SLOGAN = {
    'value': 'The Last Binaries of The Century',
    'coords': (570, 230),   # (x, y) of left top corner
    'font': FONT_PATHS[1],
    'font-size': 48,
    'fill': (0, 0, 0)
}
# Time 
TIME_TEXT = {
    'coords': (625, 780),   # (x, y) of left top corner
    'font': FONT_PATHS[1],
    'font-size': 110,
    'fill': (255, 255, 255)
}

# days, hours, minutes text
MISC_COORDS = [(650, 925), (985, 925), (1300, 925)]
MISC_FILL = (255, 255, 255)

# Rectangle in which time is kept
RECTANGLE = {
    'coords' : [550, 790, 1500, 990],   # (x1, y1, x2, y2) left top and right bottom corners
    'color': '#000000',
    'radius': 30
}

# Text to show after timer runs out
FINAL_TEXT = {
    'value': 'BSSE 11 Was Here',
    'coords': (625, 820),
    'font': FONT_PATHS[1],
    'font-size': 80,
    'fill': (255, 255, 255)
}

CREDITS_TEXT = {
    'value': '*designed by Tasmia, developed by Saad',
    'coords': (1300, 1000),
    'font': FONT_PATHS[1],
    'font-size': 20,
    'fill': (0, 0, 0)
}


########## Preferred not to touch code below ############
def set_wallpaper(output_name):
    SPI_SETDESKWALLPAPER = 20 
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, output_name , 3)

def minutes_until(target_time_str):
    try:
        target_time = datetime.strptime(target_time_str, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        time_difference = target_time - current_time
        minutes_remaining = int(time_difference.total_seconds() / 60)

        if minutes_remaining < 0:
            return 0  # If the target time is in the past, return 0 minutes
        else:
            return minutes_remaining

    except ValueError:
        return "Invalid time format. Please use 'YYYY-MM-DD HH:MM:SS'."


if __name__=='__main__':
    OUTPUT_RELATIVE_PATH = os.path.join(OUT_DIR, OUTPUT_FILE_NAME)
    OUTPUT_ABS_PATH = os.path.join(os.getcwd(), OUTPUT_RELATIVE_PATH)
    try:
        batch_text_font = ImageFont.truetype(BATCH_TEXT['font'], size=BATCH_TEXT['font-size'])
        batch_slogan_font = ImageFont.truetype(BATCH_SLOGAN['font'], size=BATCH_SLOGAN['font-size'])
        time_text_font = ImageFont.truetype(TIME_TEXT['font'], size=TIME_TEXT['font-size'])
        misc_font =  ImageFont.truetype(FONT_PATHS[1], size=30)
        final_text_font = ImageFont.truetype(FINAL_TEXT['font'], size=FINAL_TEXT['font-size'])
        credits_text_font = ImageFont.truetype(CREDITS_TEXT['font'], CREDITS_TEXT['font-size'])

        img = Image.open(IMG_PATH)
        Im = ImageDraw.Draw(img)

        Im.text(BATCH_TEXT['coords'], BATCH_TEXT['value'],\
                fill=BATCH_TEXT['fill'], font=batch_text_font)
        Im.text(BATCH_SLOGAN['coords'], BATCH_SLOGAN['value'],\
                fill=BATCH_SLOGAN['fill'], font=batch_slogan_font)
        Im.text(BATCH_SLOGAN['coords'], BATCH_SLOGAN['value'],\
                fill=BATCH_SLOGAN['fill'], font=batch_slogan_font)
        Im.text(CREDITS_TEXT['coords'], CREDITS_TEXT['value'],\
                fill=CREDITS_TEXT['fill'], font=credits_text_font)
        Im.rounded_rectangle(RECTANGLE['coords'], fill=RECTANGLE['color'], radius=RECTANGLE['radius'])

        remaining = minutes_until(TARGET_TIME)
        while(remaining>0):
            img_clone = img.copy()
            ImC = ImageDraw.Draw(img_clone)
            days = remaining//1440
            remaining -= days*1440
            hours = remaining//60
            remaining -= hours*60
            ImC.text(TIME_TEXT['coords'], \
                    '%02d : %02d : %02d' % (days, hours, remaining),\
                    fill=TIME_TEXT['fill'], font=time_text_font)
            ImC.text(MISC_COORDS[0], "days",fill=MISC_FILL, font=misc_font)
            ImC.text(MISC_COORDS[1], "hours",fill=MISC_FILL, font=misc_font)
            ImC.text(MISC_COORDS[2], "minutes",fill=MISC_FILL, font=misc_font)
            
            img_clone.save(OUTPUT_RELATIVE_PATH)
            set_wallpaper(OUTPUT_ABS_PATH)
            time.sleep(60)
            remaining = minutes_until(TARGET_TIME)

        Im.text(FINAL_TEXT['coords'], FINAL_TEXT['value'], fill=FINAL_TEXT['fill'], font=final_text_font)
        img.save(OUTPUT_RELATIVE_PATH)
        set_wallpaper(OUTPUT_ABS_PATH)
    except:
        print('Unexpected Error Occured')
