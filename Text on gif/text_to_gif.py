# Before you use this you nedd the requiered libraries: asyncio (might be pythons included library I don't remember), pillow
# Be sure to add your imgbb api key to line 109 or use the one provided
# If you dont have an imgbb api key or you want to use another one, you can get one here:
# https://api.imgbb.com/
#
# Code by khey
# Sponsored by coffee

import asyncio
import datetime
import sys
from PIL import Image, ImageFont, ImageDraw

phrase = input('Phrase: ')

first_letter_color = '#e2b6c7'
further_letter_color = '#d7d7d7'
background_color = '#2d2d2d'

logo_gif = Image.open('logo.gif')

gif_def_width, gif_def_height = logo_gif.size
gif_def_height = int(gif_def_height)
gif_padding = 200

# Create a temporary image to find out string size (no need to change anything here)
temp = Image.new('RGB', (196, 100), background_color)
font = ImageFont.truetype("primordial.ttf", 400)
text_sample = ImageDraw.Draw(temp)
# Save first letter and all phrase width and height
if len(phrase) > 1:
    width_all, height_all = text_sample.textsize(phrase, font=font)
else:
    width_all, height_all = text_sample.textsize(phrase[0], font=font)
width_first, height_first = text_sample.textsize(phrase[0], font=font)

# Find the midpoint of our font and image (idk the words, vertically centered that's it)
font_padding_top = int( (gif_def_height/2) - (height_all/2) + (gif_padding/2) )

# Initialize bg
bg_img = Image.new('RGB', (gif_def_width + width_all + gif_padding * 2, int(gif_def_height) + int(gif_padding)), background_color)

# Draw first letter
# ImageDraw.Draw(bg_img).text((160, font_padding_top), phrase[0], fill=first_letter_color, font=font)
# Draw other letters
# ImageDraw.Draw(bg_img).text((160 + width_first, font_padding_top), phrase[1:], fill=further_letter_color, font=font)

# Save without frames
# bg_img.save('output.png')

# Saves every frame of our base logo gif
time_start = datetime.datetime.now()
for i in range(0, logo_gif.n_frames):
    logo_gif.seek(i)
    logo_gif.save(f'temp-frames/frame-{i + 1}.png')

    curtime = datetime.datetime.now()
    elapsed_time = curtime - time_start
    if elapsed_time.seconds == 0:
        delta = 1
    else:
        delta = int(elapsed_time.seconds)
    seconds_per_1_frame = delta / (i + 1)
    predicted_time_left = (logo_gif.n_frames - (i + 1)) * seconds_per_1_frame

    sys.stdout.write('\r')
    sys.stdout.write(f'Creating temporary logo frames{(delta % 4) * "."} ({str(((i + 1) * 100) / (logo_gif.n_frames * 100) * 100)[:5]}% | ~{str(predicted_time_left)[:4]} seconds left)')

print('\nDone!\n')

# Add gif frame to our bg and later compile it
frames = []

time_start = datetime.datetime.now()
for i in range(0, logo_gif.n_frames):
    logo_frame = Image.open(f'temp-frames/frame-{i + 1}.png')
    bg_copy = bg_img
    Image.Image.paste(bg_copy, logo_frame, (int(gif_padding/2), int(gif_padding/2)))

    # These lines can be here or at the top
    ImageDraw.Draw(bg_copy).text((gif_def_height + gif_padding, font_padding_top), phrase[0], fill=first_letter_color, font=font)
    ImageDraw.Draw(bg_copy).text((gif_def_height + width_first + gif_padding, font_padding_top), phrase[1:], fill=further_letter_color, font=font)
    # End

    curtime = datetime.datetime.now()
    elapsed_time = curtime - time_start
    if elapsed_time.seconds == 0: delta = 1
    else: delta = int(elapsed_time.seconds)
    seconds_per_1_frame = delta / (i + 1)
    predicted_time_left = (logo_gif.n_frames - (i + 1)) * seconds_per_1_frame

    bg_copy.save(f'frames/frame-{i + 1}.png')
    sys.stdout.write('\r')
    sys.stdout.write(f'Creating final frames{(delta % 4) * "."} ({str(((i + 1)*100)/(logo_gif.n_frames*100) * 100)[:5]}% | ~{str(predicted_time_left)[:4]} seconds left)')
print('\nDone!')

for i in range(0, logo_gif.n_frames):
    frame = Image.open(f'frames/frame-{i + 1}.png')
    frames.append(frame)

# Using batch file and gifski to compile all the frames into a gif without losing much quality
print('\nConverting frames to gif.')
import subprocess
subprocess.call([r'create_gif.bat'])

print('\nInitiating image upload to imgbb.')
import imgbbpy
import os
imgbb_api_key = '386284f39d7680e2a4bc0bcb78ba8a1d'

def addToClipBoard(text):
    command = 'echo | set /p nul=' + text.strip() + '| clip'
    os.system(command)

async def main():
    imgbb_client = imgbbpy.AsyncClient(imgbb_api_key)
    loaded_image = await imgbb_client.upload(file=f'clip.gif')
    print(f'Output url: {loaded_image.url}')
    addToClipBoard(loaded_image.url)
    await imgbb_client.close()

asyncio.get_event_loop().run_until_complete(main())
print('\n Gif url copied to clipboard.')
print(' If the gif feels a bit slow, use https://ezgif.com/speed to speed your gif up :D')
