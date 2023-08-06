from PIL import Image
from PIL import ExifTags

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def save_thumb(src_fi, dst_fn, size, verbose=1):
    try:
        img = Image.open(src_fi.full_fn)
    except Exception as e:
        if verbose>=1:
            print(e)
        return False

    #if src_fi.ext == "jpg" or src_fi.ext == "jpeg":
    try:
        exif_dict = img._getexif()
        if exif_dict:

            # rotate
            orientation = None
            for k, v in ExifTags.TAGS.items() : 
                if v == "Orientation":
                    orientation = k
                    break
            if orientation:
                if exif_dict[orientation] == 3 : 
                    img=img.rotate(180, expand=True)
                elif exif_dict[orientation] == 6 : 
                    img=img.rotate(270, expand=True)
                elif exif_dict[orientation] == 8 : 
                    img=img.rotate(90, expand=True)
                else:
                    pass
    except Exception as e:
        #print(e)
        pass

    img = img.convert("RGB")

    # save
    try:
        img.thumbnail( size, Image.ANTIALIAS )
        img.save(dst_fn, "JPEG")
    except Exception as e:
        if verbose>=1:
            print("Save fail: %s" % e)
        return False

    return True
