from PIL import Image
import os


img_dir = 'solive/static/img/cate'
imgs = os.listdir(img_dir)
for img in imgs:
    img_path = os.path.join(img_dir, img)
    im = Image.open(img_path)
    # im.resize((147,203), Image.ANTIALIAS).save(img_path)
    im.resize((200, 276), Image.ANTIALIAS).save(img_path)