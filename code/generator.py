# author: Susliks
# e-mail: dishudishu@foxmail.com
# filename: generator.py

#生成单个字符

# -*- coding: utf-8 -*- #文件也为UTF-8

from PIL import Image,ImageDraw,ImageFont
import sys
import os
import random
import re
import math

global output_img_cnt
global maxnum
global color_list, color_list_len, flag
maxnum = 0
 
OUTPUT_AMOUNT = 200
CHAR_PER_IMG = 4
IM_SIZE = 832
#IM_SIZE = (70, 160, 250, 500, 850)
#IM_SIZE = (52, 104, 208, 416, 832)
ROTATE_RANGE = (-15, 15)
WIDTH_RANGE = (0, 0)
BACK_BLENDING_ALPHA = 0.2
FORE_BLENDING_ALPHA = 0.3
MIN_COLOR_DIFF = 150

WORD_SIZE = 256
WORD_SIZE2 = (16, 32, 64, 128, 256)
output_img_cnt = 0


def init():
	path = '..\\output'
	for i in range(0, 5):
		new_path = path + '\\' + str(WORD_SIZE2[i])
		if not os.path.isdir(new_path):
			os.makedirs(new_path)
		new_path2 = new_path + '\\' + 'info'
		if not os.path.isdir(new_path2):
			os.makedirs(new_path2)
		new_path2 = new_path + '\\' + 'crop'
		if not os.path.isdir(new_path2):
			os.makedirs(new_path2)


def get_color():
	global color_list, color_list_len
	color_list = list()
	fin = open('..\\input\\color\\picture.txt', "r")
	for line in fin:
		line = re.split('\s*', line)
		color_list.append(line)
	color_list_len = len(color_list)
	#print(len(color_list))


def blending(im, alpha, im_size):
	dir_from = '..\\blending'
	blending_im_list = os.listdir(dir_from)
	while(True):
		blending_im_name = blending_im_list[random.randint(0, len(blending_im_list)-1)]
		if(blending_im_name.endswith('.db') == True):  #跳过缓存文件
			continue
		blending_im = Image.open(dir_from + '\\' + blending_im_name, mode = 'r')
		break
	
	'''
	if(min(blending_im.size) < im_size):
		blending_im = blending_im.crop((0, 0, min(blending_im.size), min(blending_im.size)))
		blending_im = blending_im.resize((im_size, im_size / 2))
	else:
		horizontal_pos = random.randint(0, blending_im.size[0] - im_size - 1)
		vertical_pos = random.randint(0, blending_im.size[1] - im_size / 2 - 1)
		blending_im = blending_im.crop((horizontal_pos, vertical_pos, horizontal_pos + im_size, vertical_pos + im_size))
	'''
	blending_im = blending_im.resize((im_size, int(im_size / 2)))

	im.save('tmp.png', "PNG")
	im2 = Image.open('tmp.png', mode = 'r')
	im2 = im2.convert("RGBA")
	blending_im = blending_im.convert("RGBA")
	im3 = Image.blend(im2, blending_im, alpha)

	return im3



def get_info(content, font, word_size, im_size, rotate_angle, img_cnt, im):
	content_len = len(content)
	pre_width, pre_height = font.getsize(content)
	#print(font.getsize(content))

	offset = 0
	f1 = open('..\\output\\' + str(word_size) + '\\info\\' + str(word_size) + '_' + str(img_cnt) + '_info.txt', 'wt')
	crop_path = '..\\output\\' + str(word_size) + '\\crop'
	print(content_len, content, file = f1)
	for i in range(0, content_len):
		pre_x = -0.5 * pre_width + offset
		pre_y = -0.5 * pre_height
		#print(pre_x, pre_y)
		rho = math.sqrt(pre_x*pre_x + pre_y*pre_y)
		#print(rho)
		theta = math.acos(pre_x / rho) + math.radians(rotate_angle)
		#print(theta)
		x1 = rho * math.cos(theta)
		y1 = -rho * math.sin(theta)
		#print(x1, y1)
		#print(rotate_angle, math.sin(math.radians(rotate_angle)))
		single_width = font.getsize(content[i])[0] - font.getoffset(content[i])[0]
		single_height = font.getsize(content[i])[1] - font.getoffset(content[i])[1]
		if(rotate_angle > 0):
			x2 = x1
			y2 = y1 - font.getsize(content[i])[0] * math.sin(math.radians(abs(rotate_angle)))
		else:
			x2 = x1 - pre_height * math.sin(math.radians(abs(rotate_angle)))
			y2 = y1
		x = math.floor(0.5 * im_size + x2 + \
			(font.getoffset(content[i])[1]) * math.sin(math.radians(abs(rotate_angle))))
		y = math.floor(0.5 * im_size / 2 + y2 + font.getoffset(content)[1] * math.cos(math.radians(abs(rotate_angle))) / 2\
				+ font.getoffset(content[i])[1] - font.getoffset(content)[1])
		#print(font.getoffset(content[i])[0])
		
		
		#print(type(math.sin(math.radians(rotate_angle))))
		width = single_height * math.sin(math.radians(abs(rotate_angle))) + single_width * math.cos(math.radians(abs(rotate_angle)))\
				- (font.getoffset(content[i])[1]) * math.sin(math.radians(abs(rotate_angle)))
		#print(content[i], single_width, width)
		height = single_height * math.cos(math.radians(abs(rotate_angle))) + single_width * math.sin(math.radians(abs(rotate_angle)))
		offset = offset + single_width
		
		x = x - 10
		y = y - 10
		'''
		if(word_size <= 32):
			x = x-1
			y = y-1
			width = width + 6 * (word_size / 16)
			height = height + 3
		'''
		print(x, y, int(width+15), int(height+15), file = f1)
		crop_im = im.crop((x, y, int(x + width+15), int(y + height + 15)))
		crop_im.save(crop_path + '\\' + str(word_size) + '_' + str(img_cnt) + '_crop_' + str(i+1) + '_' + content[i] + '.png', "PNG")


def generator(content):
	global output_img_cnt
	global maxnum
	output_img_cnt = output_img_cnt + 1
	
	word_size = WORD_SIZE
	dir_from = '..\\font'
	font_list = os.listdir(dir_from)
	font_name = font_list[random.randint(0, len(font_list)-1)]
	font = ImageFont.truetype(dir_from + '\\' + font_name, word_size)
	#print(font.getsize(content))
	maxnum = max(maxnum, font.getsize(content)[0])
	rotate_angle = random.randint(ROTATE_RANGE[0], ROTATE_RANGE[1])
	width = random.randint(WIDTH_RANGE[0], WIDTH_RANGE[1])

	back_im, back_color = back_layer(IM_SIZE)
	border_im, border_mask = border_layer(content, font, word_size, width, rotate_angle, IM_SIZE)
	im, fore_mask = fore_layer(content, font, word_size, rotate_angle, back_color, IM_SIZE)
	#print(fore_mask.size)
	im.paste(border_im, (0, 0, IM_SIZE, int(IM_SIZE / 2)), fore_mask)
	im.paste(back_im, (0, 0, IM_SIZE, int(IM_SIZE / 2)), border_mask)
	#im.show()
	im.save('..\\output\\' + str(WORD_SIZE) + '\\' + str(WORD_SIZE) + '_' + str(output_img_cnt) + '.png', "PNG")
	get_info(content, font, word_size, IM_SIZE, rotate_angle, output_img_cnt, im)
	#im.show()


def back_layer(im_size):
	global color_list, color_list_len
	index = random.randint(0, color_list_len-1)
	color = (int(color_list[index][0]), int(color_list[index][1]), int(color_list[index][2]))
	#color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	im = Image.new("RGBA", (im_size, int(im_size / 2)), color)
	im = blending(im, BACK_BLENDING_ALPHA, im_size)
	return im, color


def border_layer(content, font, word_size, width, rotate_angle, im_size):
	mask_size = 2 * im_size
	global color_list, color_list_len
	index = random.randint(0, color_list_len-1)
	color = (int(color_list[index][0]), int(color_list[index][1]), int(color_list[index][2]))
	#color = (random.randint(150, 200), random.randint(150, 200), random.randint(150, 200))
	im = Image.new("RGBA", (im_size, int(im_size / 2)), color)
	mask_size = 2 * im_size
	mask = Image.new("RGBA", (mask_size, int(mask_size / 2)), color)
	draw = ImageDraw.Draw(mask)
	word_width, word_height = font.getsize(content)
	word_width += font.getoffset(content)[0] 
	word_height += font.getoffset(content)[1]
	horizontal_pos = (im_size - word_width) / 2
	vertical_pos = (im_size / 2 - word_height) / 2
	for i in range(-1, 2):
		for j in range(-1, 2):
			draw.text((mask_size / 4 + horizontal_pos + width*i, mask_size / 2 / 4 + vertical_pos + width*j), str(content), font = font, fill = (color[0], color[1], color[2], 0))
	mask = mask.rotate(rotate_angle)
	crop_pos = int(0.25 * mask_size)
	mask = mask.crop((crop_pos, int(crop_pos / 2), crop_pos + im_size, int(crop_pos / 2 + im_size / 2)))
	return im, mask


def fore_layer(content, font, word_size, rotate_angle, back_color, im_size):
	global color_list, color_list_len, flag
	mask_size = 2 * im_size
	while(True):
		index = random.randint(0, color_list_len-1)
		color = (int(color_list[index][0]), int(color_list[index][1]), int(color_list[index][2]))
		#color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		dist = 0
		for i in range(0, 3):
			dist += abs(back_color[i] - color[i])
		if(dist > MIN_COLOR_DIFF):
			break
	im = Image.new("RGBA", (im_size, int(im_size / 2)), color)
	im = blending(im, FORE_BLENDING_ALPHA, im_size)
	mask = Image.new("RGBA", (mask_size, int(mask_size / 2)), color)
	draw = ImageDraw.Draw(mask)
	word_width, word_height = font.getsize(content) 
	word_width += font.getoffset(content)[0] 
	word_height += font.getoffset(content)[1]
	horizontal_pos = (im_size - word_width) / 2
	vertical_pos = (im_size / 2 - word_height) / 2
	draw.text((mask_size / 4 + horizontal_pos, mask_size / 2 / 4 + vertical_pos), str(content), font = font, fill = (color[0], color[1], color[2], 0))
	if(word_size == 256 and flag):
		flag = False
		mask.save('tmp11.png', "PNG")
	mask = mask.rotate(rotate_angle)
	crop_pos = int(0.25 * mask_size)
	mask = mask.crop((crop_pos, int(crop_pos / 2), crop_pos + im_size, int(crop_pos / 2 + im_size / 2)))
	return im, mask


def image_resize():
	dir_from = '..\\output\\256'
	im_list = os.listdir(dir_from)
	im_amount = len(im_list)
	times = 32
	info_dir_from = '..\\output\\256\\info'
	for i in range(4):
		info_dir_to = '..\\output\\' + str(WORD_SIZE2[i]) + '\\info'
		crop_dir_to = '..\\output\\' + str(WORD_SIZE2[i]) + '\\crop' 
		times = int(times / 2)
		for j in range(im_amount):
			path = dir_from + '\\' + im_list[j]
			#print(path)
			if(path.endswith('.png') == False):
				continue
			#print(path)
			im = Image.open(path)
			width = int(im.size[0] / times)
			height = int(im.size[1] / times)
			im = im.resize((width, height), Image.ANTIALIAS)
			#im.show()
			im.save('..\\output\\' + str(WORD_SIZE2[i]) + '\\' + str(WORD_SIZE2[i]) + str(im_list[j])[3:], "PNG")

			fin = open(info_dir_from + '\\' + re.sub(r'.png', r'_info.txt', im_list[j]), 'r')
			fout = open(info_dir_to + '\\' + re.sub(r'.png', r'_info.txt', str(WORD_SIZE2[i]) + str(im_list[j])[3:]), 'wt')
			line_cnt = 0
			content = str('')
			for line in fin:
				if(line_cnt == 0):
					line = re.sub(r'\n', r'', line)
					print(line, file = fout)
					line = re.split(r'\s', line)
					content = line[1]
					#print('!!' + content)
				else:
					#print(line)
					line = re.split(r'\s', line)
					print(math.floor(float(line[0]) / times), math.floor(float(line[1]) / times), \
						math.ceil(math.ceil(float(line[2])) / times), math.ceil(math.ceil(float(line[3])) / times), file = fout)
					crop_im = im.crop((math.floor(float(line[0]) / times), math.floor(float(line[1]) / times), \
						math.floor(float(line[0]) / times) + math.ceil(math.ceil(float(line[2])) / times), \
							math.floor(float(line[1]) / times) + math.ceil(math.ceil(float(line[3])) / times)))
					#im.show()
					#crop_im.show()
					crop_im.save(crop_dir_to + '\\' + re.sub(r'.png', r'_crop_', str(WORD_SIZE2[i]) + str(im_list[j])[3:]) + str(line_cnt) + '_' + content[line_cnt - 1] + '.png', "PNG")
				line_cnt += 1

	'''
	dir_from = '..\\output\\256\\info'
	info_list = os.listdir(dir_from)
	info_amount = len(info_list)
	times = 32
	for i in range(4):
		im_dir_from = '..\\output\\' + str(WORD_SIZE2[i])
		crop_dir_to = '..\\output\\' + str(WORD_SIZE2[i]) + '\\crop' 
		times = int(times / 2)
		dir_to = '..\\output\\' + str(WORD_SIZE2[i]) + '\\info'
		cnt = 0
		for j in range(im_amount):
			path = dir_from + '\\' + info_list[j]
			if(path.endswith('.txt') == False):
				continue
			im_path = im_dir_from + '\\' + re.sub(r'_info.txt', r'.png', info_list[j])
			cnt += 1
			fin = open(dir_from + '\\' + info_list[j], 'r')
			fout = open(dir_to + '\\' + str(WORD_SIZE2[i]) + '_' + str(cnt) + '_info.txt', 'wt')
			line_cnt = 0
			content = str('')
			for line in fin:
				if(line_cnt == 0):
					print(line, file = fout)
				else:
					print(line)
					print(math.floor(float(line[0]) / times), math.floor(float(line[1]) / times), \
						math.floor(math.ceil(float(line[2])) / times), math.floor(math.ceil(float(line[3])) / times), file = fout)
					crop_im = im.crop((math.floor(float(line[0]) / times), math.floor(float(line[1]) / times), \
						math.floor(math.ceil(float(line[2])) / times), math.floor(math.ceil(float(line[3])) / times)))
					crop_im.save(crop_dir_to + '\\' + str(WORD_SIZE2[i]) + '_' + str(cnt) + '_' + str(line_cnt) + '_' + content[line_cnt - 1] + '.png', "PNG")
				line_cnt += 1
	'''




	'''
	im = Image.open('..\\output\\256\\256_45.png')
	width = int(im.size[0] / 16)
	height = int(im.size[1] / 16)
	#im = im.resize((width, height), Image.ANTIALIAS)
	im = im.resize((width, height))
	im.show()
	'''

def main():
	global flag
	flag = True

	get_color()
	init()
	
	global maxnum
	dir_from = '..\\input\\text'
	input_list = os.listdir(dir_from)
	for name in input_list:
		with open(dir_from + '\\' + name, 'rt') as f:
			for line in f:
				line = re.sub(r'\s', r'', line)
				tmp_line = line
				for j in range(0, OUTPUT_AMOUNT-1):
					line += tmp_line

				line = list(line)
				random.shuffle(line)
				line = ''.join(line)

				line_len = len(line)
				loop_cnt = math.floor(line_len / CHAR_PER_IMG)
				for i in range(0, loop_cnt):
					generator(line[i*CHAR_PER_IMG: (i+1)*CHAR_PER_IMG])
				if (line_len % CHAR_PER_IMG != 0):
					generator(line[loop_cnt*CHAR_PER_IMG: ])

	#print(maxnum)
	image_resize()
	

if __name__ == "__main__":
    main()


