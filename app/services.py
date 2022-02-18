from PIL import Image
from pathlib import Path
from moviepy.editor import *


def get_path_upload_file(instance, filename):
    # file will be uploaded to media/photo/user_<id>/<filename>
    return f'album/user_{instance.owner.id}/{filename}'


def validate_image(fieldfile_obj):
    # validate image size <= 5 Mb
    megabyte_limit = 5.0
    if fieldfile_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


def convert_to_webp(source):
    # convert image to format .webp
    destination = Path(source).with_suffix(".webp")
    image = Image.open(source)  # Open image
    image.save(destination, format="webp")  # Convert image to webp
    return destination


def convert_to_webm(files):
    # convert images to webm
    new_file = []
    for image in files:
        img = Image.open(image).convert('RGB')
        img = img.resize((1920, 1080))
        img.save(f"media/top/{str(image).split('/')[-1].split('.')[0]}.jpg")
        new_file.append(f"media/top/{str(image).split('/')[-1].split('.')[0]}.jpg")
    clip = ImageSequenceClip(new_file, fps=3)
    clip.write_videofile('media/top/top.webm', fps=24)
    return Path('media/top/top.webm')
