# author: Susliks
# e-mail: dishudishu@foxmail.com
# filename: generator.py

#生成单个字符

# -*- coding: utf-8 -*- #文件也为UTF-8

import sys
import os
import random
import re
from PIL import Image,ImageDraw,ImageFont

OUTPUT_AMOUNT = 1
IM_SIZE = 500
ROTATE_RANGE = (40, 45)
WIDTH_RANGE = (0, 5)
BACK_BLENDING_ALPHA = 0.1
FORE_BLENDING_ALPHA = 0.5
MIN_COLOR_DIFF = 60

MASK_SIZE = 2 * IM_SIZE
WORD_SIZE = (16, 32, 64, 128, 256)

def blending(im, alpha):
	dir_from = '..\\blending'
	blending_im_list = os.listdir(dir_from)
	while(True):
		blending_im_name = blending_im_list[random.randint(0, len(blending_im_list)-1)]
		if(blending_im_name.endswith('.db') == True):  #跳过缓存文件
			continue
		blending_im = Image.open(dir_from + '\\' + blending_im_name, mode = 'r')
		break
	
	if(min(blending_im.size) < IM_SIZE):
		blending_im = blending_im.crop((0, 0, min(blending_im.size), min(blending_im.size)))
		blending_im = blending_im.resize((IM_SIZE, IM_SIZE))
	else:
		horizontal_pos = random.randint(0, blending_im.size[0] - IM_SIZE - 1)
		vertical_pos = random.randint(0, blending_im.size[1] - IM_SIZE - 1)
		blending_im = blending_im.crop((horizontal_pos, vertical_pos, horizontal_pos + IM_SIZE, vertical_pos + IM_SIZE))

	im.save('tmp.png', "PNG")
	im2 = Image.open('tmp.png', mode = 'r')
	im2 = im2.convert("RGBA")
	blending_im = blending_im.convert("RGBA")
	im3 = Image.blend(im2, blending_im, alpha)

	return im3


def generator(content, amount):
	for i in range(0, amount):
		word_size = WORD_SIZE[4]
		dir_from = '..\\font'
		font_list = os.listdir(dir_from)
		font_name = font_list[random.randint(0, len(font_list)-1)]
		font = ImageFont.truetype(dir_from + '\\' + font_name, word_size)
		rotate_angle = random.randint(ROTATE_RANGE[0], ROTATE_RANGE[1])
		width = random.randint(WIDTH_RANGE[0], WIDTH_RANGE[1])
		back_im, back_color = back_layer()
		border_im, border_mask = border_layer(content, font, word_size, width, rotate_angle)
		im, fore_mask = fore_layer(content, font, word_size, rotate_angle, back_color)
		im.paste(border_im, (0, 0, IM_SIZE, IM_SIZE), fore_mask)
		im.paste(back_im, (0, 0, IM_SIZE, IM_SIZE), border_mask)
		#im.show()
		im.save('..\\output\\' + str(content) + '_' + str(i) + '.png', "PNG")
		im.show()


def back_layer():
	color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	im = Image.new("RGBA", (IM_SIZE, IM_SIZE), color)
	im = blending(im, BACK_BLENDING_ALPHA)
	return im, color


def border_layer(content, font, word_size, width, rotate_angle):
	color = (random.randint(150, 200), random.randint(150, 200), random.randint(150, 200))
	im = Image.new("RGBA", (IM_SIZE, IM_SIZE), color)
	mask = Image.new("RGBA", (MASK_SIZE, MASK_SIZE), (255, 255, 255))
	draw = ImageDraw.Draw(mask)
	word_width, word_height = font.getsize(content)
	word_width += font.getoffset(content)[0] 
	word_height += font.getoffset(content)[1]
	horizontal_pos = (IM_SIZE - word_width) / 2
	vertical_pos = (IM_SIZE - word_height) / 2
	for i in range(-1, 2):
		for j in range(-1, 2):
			draw.text((MASK_SIZE / 4 + horizontal_pos + width*i, MASK_SIZE / 4 + vertical_pos + width*j), str(content), font = font, fill = (255, 255, 255, 0))
	mask = mask.rotate(rotate_angle)
	crop_pos = int(0.25 * MASK_SIZE)
	mask = mask.crop((crop_pos, crop_pos, crop_pos + IM_SIZE, crop_pos + IM_SIZE))
	return im, mask


def fore_layer(content, font, word_size, rotate_angle, back_color):
	while(True):
		color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		dist = 0
		for i in range(0, 3):
			dist += abs(back_color[i] - color[i])
		if(dist > MIN_COLOR_DIFF):
			break
	im = Image.new("RGBA", (IM_SIZE, IM_SIZE), color)
	im = blending(im, FORE_BLENDING_ALPHA)
	mask = Image.new("RGBA", (MASK_SIZE, MASK_SIZE), (255, 255, 255))
	draw = ImageDraw.Draw(mask)
	word_width, word_height = font.getsize(content) 
	horizontal_pos = IM_SIZE / 2 - word_width / 2
	vertical_pos = IM_SIZE / 2 - word_height / 2
	draw.text((MASK_SIZE / 4 + horizontal_pos, MASK_SIZE / 4 + vertical_pos), str(content), font = font, fill = (0, 0, 0, 0))
	mask = mask.rotate(rotate_angle)
	crop_pos = int(0.25 * MASK_SIZE)
	mask = mask.crop((crop_pos, crop_pos, crop_pos + IM_SIZE, crop_pos + IM_SIZE))
	return im, mask


def main():
	dir_from = '..\\input'
	input_list = os.listdir(dir_from)
	for name in input_list:
		with open(dir_from + '\\' + name, 'rt') as f:
			for line in f:
				line = re.sub(r'\s', r'', line)
				line_len = len(line)
				for i in range(0, line_len):
					generator(line[i], OUTPUT_AMOUNT)
				

if __name__ == "__main__":
    main()


