from pylab import *
import numpy as np
#np.set_#printoptions(threshold=np.nan)
from os import listdir
from sklearn.svm import LinearSVC
import cv2
from PIL import Image
from sklearn import svm
import imagehash
from scipy.cluster.vq import *
from sklearn.preprocessing import StandardScaler
from sklearn import tree
from sklearn import linear_model
import pickle as pk

genuine_image_filenames = listdir("SRectF/")
if len(genuine_image_filenames)<1:
    print("No signature found!")
    exit()
genuine_image_paths = "SRectF/"
genuine_image_features = [[] for x in range(1)]
def preprocess_image(path, display=False):
    raw_image = cv2.imread(path)
    bw_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
    bw_image = 255 - bw_image 

    if display:
        cv2.imshow("RGB to Gray", bw_image)
        cv2.waitKey()

    _, threshold_image = cv2.threshold(bw_image, 30, 255, 0)

    if display:
        cv2.imshow("Threshold", threshold_image)
        cv2.waitKey()

    return threshold_image

def pr(path,tf, display=False):
    raw_image = cv2.imread(path)
    bw_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
    bw_image = 255 - bw_image 

    if display:
        cv2.imshow("RGB to Gray", bw_image)
        cv2.waitKey()

    _, threshold_image = cv2.threshold(bw_image, tf, 255, 0)

    if display:
        cv2.imshow("Threshold", threshold_image)
        cv2.waitKey()

    return threshold_image

def get_contour_features(im, display=False):
    '''
    :param im: input preprocessed image
    :param display: flag - if true display images
    :return:aspect ratio of bounding rectangle, area of : bounding rectangle, contours and convex hull
    '''

    rect = cv2.minAreaRect(cv2.findNonZero(im))
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    w = np.linalg.norm(box[0] - box[1])
    h = np.linalg.norm(box[1] - box[2])

    aspect_ratio = max(w, h) / min(w, h)
    bounding_rect_area = w * h

    if display:
        image1 = cv2.drawContours(im.copy(), [box], 0, (120, 120, 120), 2)
        cv2.imshow("a", cv2.resize(image1, (0, 0), fx=2.5, fy=2.5))
        cv2.waitKey()

    hull = cv2.convexHull(cv2.findNonZero(im))

    if display:
        convex_hull_image = cv2.drawContours(im.copy(), [hull], 0, (120, 120, 120), 2)
        cv2.imshow("a", cv2.resize(convex_hull_image, (0, 0), fx=2.5, fy=2.5))
        cv2.waitKey()

    im2, contours, hierarchy = cv2.findContours(im.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if display:
        contour_image = cv2.drawContours(im.copy(), contours, -1, (120, 120, 120), 3)
        cv2.imshow("a", cv2.resize(contour_image, (0, 0), fx=2.5, fy=2.5))
        cv2.waitKey()

    contour_area = 0
    for cnt in contours:
        contour_area += cv2.contourArea(cnt)
    hull_area = cv2.contourArea(hull)

    return aspect_ratio, bounding_rect_area, hull_area, contour_area

des_list = []

def sift(im, path, display=False):
    raw_image = cv2.imread(path)
    sift = cv2.xfeatures2d.SIFT_create()
    j=0
    while True:
        kp, des = sift.detectAndCompute(pr(path,j), None)
        if des is not None:
            break
        j+=1


    if display:
        cv2.drawKeypoints(im, kp, raw_image)
        cv2.imshow('sift_keypoints.jpg', cv2.resize(raw_image, (0, 0), fx=3, fy=3))
        cv2.waitKey()

    return (path, des)
for name in genuine_image_filenames:
    signature_id = int(name.split('_')[0][-3:])
    genuine_image_features[signature_id - 1].append({"name": name})
im_contour_features = []
for i in range(1):
    des_list = []
    for im in genuine_image_features[i]:
        image_path = genuine_image_paths + "/" + im['name']
        preprocessed_image = preprocess_image(image_path)
        hash = imagehash.phash(Image.open(image_path))

        aspect_ratio, bounding_rect_area, convex_hull_area, contours_area = \
            get_contour_features(preprocessed_image.copy(), display=False)

        hash = int(str(hash), 16)
        im['hash'] = hash
        im['aspect_ratio'] = aspect_ratio
        im['hull_area/bounding_area'] = convex_hull_area / bounding_rect_area
        im['contour_area/bounding_area'] = contours_area / bounding_rect_area

        im_contour_features.append([hash, aspect_ratio, convex_hull_area / bounding_rect_area, contours_area / bounding_rect_area])

        des_list.append(sift(preprocessed_image, image_path))
    descriptors = des_list[0][1]
    for image_path, descriptor in des_list[1:]:
        descriptors = np.vstack((descriptors, descriptor))
    k = 1
    while True:
    	try:
    		voc, variance = kmeans(descriptors, k, 1)
    		break
    	except:
    		k-=1

    im_features = np.zeros((len(genuine_image_features[i]), k+4), "float32")
    for i in range(len(genuine_image_features[i])):
        words, distance = vq(des_list[i][1], voc)
        for w in words:
            im_features[i][w] += 1

        for j in range(4):
            im_features[i][k+j] = im_contour_features[i][j]
    stdSlr = StandardScaler().fit(im_features)
    im_features = stdSlr.transform(im_features)
    train_genuine_features, test_genuine_features = im_features[0:3], im_features[3:5]
with open('my_dumped_classifier.pkl', 'rb') as fid:
    clf = pk.load(fid)

if clf!=None:

    genuine_res = clf.predict(im_features)
    scr=0

    for res in genuine_res:
        if int(res) == 2:
            scr+=1
    if(100*scr/len(genuine_res))>59:
        print("True")
    else:
        print("False")
            
