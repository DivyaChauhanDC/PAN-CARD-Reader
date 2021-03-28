from PIL import Image
import pytesseract
import argparse
import cv2
import os, re, csv
import json
import io
# construct the argument parse and parse the arguments

def read_pan_card(file_name):
    data = {}
    try:
        img = Image.open(file_name)
        img = img.convert('RGB')
        pix = img.load()

        for y in range(img.size[1]):
        	for x in range(img.size[0]):
        		if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
        			pix[x, y] = (0, 0, 0, 255)
        		else:
        			pix[x, y] = (255, 255, 255, 255)

        img.save('temp.jpg')

        text_in = pytesseract.image_to_string(Image.open('temp.jpg'))

        with open("output_data.txt","w") as file:
            file.write(text_in)
            print('text_in',text_in)

        with open("output_data.txt", "r") as file:
            text = file.read()
            # Searching for Values
            lines = text.split('\n')
            ind = 0
            while ind<len(lines):
                val = lines[ind].strip()
                if re.search("([0-9]{2}/[0-9]{2}/[0-9]{4})", val) is not None:
                    data['date_of_birth'] = val.strip()
                elif ind==2:
                    user_name = val.split(' ')
                    data['user_name'] = user_name[0]+' '+user_name[1]
                elif ind==3:
                    data['father_name'] = val.strip().replace("'", "")
                elif val.strip()=='Permanént Account Number':
                    data['pan'] = lines[ind+1].replace(" ", "")
                ind=ind+1

        os.remove('output_data.txt')
        print('d',data)
    except Exception as ex:
        print('error', str(ex))
    return data


if __name__ == '__main__':
    pass
