###
# ╭╴detect_and_dive.py
# ╰--> detect a qr code, and given an url, dive to end url
# ╭╴Oportunitas (Taib Izzat Samawi); 15/Jul/2023
# ╰-@Barunastra_ITS
###

import cv2
import numpy
import glob
from pyzbar.pyzbar import decode
from my_functions import dive, hasKeyword
import os
## import all dependencies

### define essential constants and variables BELOW this line
dataset_path = "./datasets/barunastra-oa-search/"
file_type = "png"
keyword = "barunastra"
### define essential constants and variables ABOVE this line

file_pattern = dataset_path + f"/*.{file_type}"
dataset = glob.glob(file_pattern)
## get dataset of files of a certain type, in a certain folder

url_map = {}
url_keyword_state = {}
no_keyword = []

for file in dataset:
    image = cv2.imread(file) # read current image
    gray_image = cv2.cvtColor(image, 0) # change image to grayscale
    qr_code = decode(gray_image) # decode qr code in image

    for detection in qr_code:
        file_name = os.path.basename(file)
        qr_data = str(detection.data.decode("utf-8"))

        if qr_data in url_map:
            if (not url_keyword_state[qr_data]):
                no_keyword.append(file_name)
            qr_data = url_map[qr_data]
        ## if code has dove url previouslt, print past finding
        else:
            ori_qr_data = qr_data
            while True:
                qr_data_temp = qr_data
                qr_data = dive(qr_data)
                if (qr_data_temp == qr_data):
                    break
            ## dive to end url
            url_map[ori_qr_data] = qr_data

            if (hasKeyword(qr_data, keyword)):
                url_keyword_state[ori_qr_data] = True
            else:
                url_keyword_state[ori_qr_data] = False
                no_keyword.append(file_name)
        ## if found novel url, dive until end url

        print(f"{file_name}\t: {qr_data}")
    ## iterate through every detected qr in image
## iterate through every image in given dataset
        
print(f"keyword: {keyword} is not found in:")
for file in no_keyword:
    print(file)
## tell which files does not contain the keyword