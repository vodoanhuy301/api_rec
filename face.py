from mtcnn import MTCNN
import cv2
from PIL import Image
from face_search import search_face
import os 
import requests
from imageio import imread
from io import BytesIO
import urllib.request as ur
import numpy as np
import json
import base64




def base64_pil(s):
    im_bytes = base64.b64decode(s)   # im_bytes is a binary image
    im_file = BytesIO(im_bytes)  # convert image to file-like object
    img = Image.open(im_file)
    return img

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = ur.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
	return image
#Resize Image  
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def url_to_img_file(path):
    response = requests.get(path)
    im = Image.open(BytesIO(response.content))
    im.save("images/test.jpg")

# Detect face, search face and display reuslts
detector = MTCNN()
def tagging_image(path):
    # response = requests.get(path)
    # imgdata = base64.b64decode(path)
    # im = Image.open(BytesIO(response.content))
    # im = Image.open(BytesIO(imgdata))
    im= base64_pil(str(path))
    # print (type(im))
    # image = url_to_image(path)
    image = np.asarray(im)
    # print (type(image))
    faces = detector.detect_faces(image)
    arr=[]
    if (len(faces)>0):
        for face in faces:
            bounding_box = face['box']
            cv2.rectangle(image,(bounding_box[0], bounding_box[1]),(bounding_box[0]+bounding_box[2], bounding_box[1]+bounding_box[3]),(0,204,0),2)
            crop_img = im.crop((bounding_box[0], bounding_box[1],bounding_box[0]+bounding_box[2], bounding_box[1]+bounding_box[3]))
            name = search_face(crop_img)
            arr.append(name)
        # cv2.putText(image,name, (bounding_box[0], bounding_box[1]),
        #         cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3)
    if (len(arr)>0):
        return arr[0]
    else:
        return "null"

    # img = ResizeWithAspectRatio(image, width=640)
    # cv2.imshow("Face Recognition", img)
    # cv2.waitKey(0)

# TEST
# Test with folder test
# image_folder_in = "./data/test/"
# for image_name in os.listdir(image_folder_in):
#             image_path = os.path.join(image_folder_in,image_name)
#             tagging_image(image_path)
        
# Test with one image 
# tagging_image("")
# https://media-cdn-v2.laodong.vn/Storage/NewsPortal/2020/5/14/805291/Messi-Ronaldo.jpg
# print (type(url_to_image("https://znews-stc.zdn.vn/static/topic/person/cristiano-ronaldo.jpg")))
# url_to_img_file("https://znews-stc.zdn.vn/static/topic/person/cristiano-ronaldo.jpg")