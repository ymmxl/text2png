from PIL import Image,ImageFont,ImageDraw
from glob import glob
import os,sys,time,json
import ast

def import_config():
    try:
        with open("config.json","r") as f:
            return json.load(f)
    except Exception as e:
        print(e)
        sys.exit(1)
def dtop(data):
    dpi=300
    return int((dpi*data)/25.4)

def get_input(config):
    text = input(f"Enter Name (Max {config['TEXT_LENGTH']} Characters): ")
    if len(text) > config["TEXT_LENGTH"]:
        print(f"Max {config['TEXT_LENGTH']} only please!\n")
        return None
    else: return text

def check_font():
    if not os.path.isdir("font"):
        print("Font folder not found, please create a folder named\"font\" and restart program.")
        time.sleep(5)
        sys.exit(1)
    else:
        files = glob(os.path.join(os.getcwd(),"font/*.ttf"))
        if not files:
            print("font file not found, skipping..")
            return None
        elif len(files) > 1:
            print("More than one file found, please remove one and restart program.")
            time.sleep(5)
            sys.exit(1)
        else:
            return files[0]

def main(config):
    black = (0,0,0)
    white = (255,255,255)
    while True:
        image_width = dtop(config["CANVAS_WIDTH"])
        image_height = dtop(config["CANVAS_HEIGHT"])
        font_file = check_font()
        if font_file:
            font = ImageFont.truetype(font_file,size=config["TEXT_HEIGHT"])
        else:
            font = None

        for i in range(6):
            text = get_input(config)
            if text:
                break
            elif not text and i == 5:
                sys.exit(1)
        print(f"[{text}] Setting Image.")
        image = Image.new('RGBA',(image_width,image_height),(0,0,0,0))
        draw = ImageDraw.Draw(image)
        #get text width and height
        w = draw.textbbox((0,0),text,font=font)
        #(x1,y1,x2,y2)
        print(f"[{text}] Adding Text.")
        if config["DIST_FROM_TOP"] > config["CANVAS_HEIGHT"]:
            print(f"[{text}] Top Out of Bounds! Check settings.")
            time.sleep(10)
            continue
        if config["DIST_FROM_LEFT"] > config["CANVAS_WIDTH"]:
            print(f"[{text}] Left Out of Bounds! Check settings.")
            time.sleep(10)
            continue
        draw.text(((dtop(config["DIST_FROM_LEFT"])),(dtop(config["DIST_FROM_TOP"]))),text,fill=ast.literal_eval(config["FONT_COLOR"]),font=font,anchor="lm")
        filename = f"{text}.png"
        try:
            image.save(f"images/{filename}",dpi=(300,300))
            print(f"[{text}] Image saved.")
        except:
            print("Images folder not found, please create a folder named\"images\" and restart program.")
            time.sleep(5)
            sys.exit(1)
        time.sleep(1)

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
        sys.path.append(app_path)
    else:
        app_path = os.path.dirname(os.path.abspath(__file__))
    config=import_config()
    main(config)
