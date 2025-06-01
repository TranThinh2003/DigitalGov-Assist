import cv2 
import matplotlib.pyplot as plt
import numpy as np
import os
import time

start = time.time()

def im_show(img, figsize=(6, 6)):
    _, ax = plt.subplots(1, 1, figsize=(figsize))
    ax.axis('off')
    ax.imshow(img)
    plt.show()


def list_template(start_path='.'):
    for root, _, files in os.walk(start_path):
        for file in files:
            print(os.path.join(root, file))


def reading_image(img_src):#'./dang_ky_thuong_tru.jpeg'
    img_rgb = cv2.imread(img_src)
    assert img_rgb is not None, "file could not be read, check with os.path.exists()"
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    return img_rgb, img_gray


def reading_template(template_src):
    template = cv2.imread(template_src, cv2.IMREAD_GRAYSCALE)
    assert template is not None, "file could not be read, check with os.path.exists()"
    # print(template)
    return template

template = reading_template('./templates/to_khai_dk_thuongtru/ho_ten/ho_ten_template.jpeg')



def extract_templates(img_src, template_src):
    template = reading_template(template_src)
    img_rgb, img_gray = reading_image(img_src)

    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
    #     hoten_image = img_rgb[pt[1]:pt[1] + h, pt[0]:pt[0] + w] 
        
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        cv2.putText(img_rgb, 'ngay_thang_nam_sinh', (pt[0], pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    #     cv2.imwrite(f'./templates/to_khai_dk_thuongtru/ngay_thang_nam_sinh/{pt[0]}_{pt[1]}_ngay_thang_nam_sinh.png', hoten_image)
    cv2.imwrite('./templates/to_khai_dk_thuongtru/ngay_thang_nam_sinh/ngay_thang_nam_sinh_extracted.png', img_rgb)
    
    im_show(img_rgb, figsize=(10, 10))


extract_templates('./dang_ky_thuong_tru.jpeg', './templates/to_khai_dk_thuongtru/ngay_thang_nam_sinh/ngay_thang_nam_sinh_template.jpeg')



end = time.time()
print(end - start)
