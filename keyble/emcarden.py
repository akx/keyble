# -- encoding: UTF-8 --
import cv2


def find_cards(img):
    img = cv2.resize(img, (720, 1280))
    thresh = cv2.inRange(img, (120, 50, 0), (150, 100, 255))
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for idx, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if w < 300 or h < 100:
            continue
        aspect = w / h
        # Check this is a full enough card
        if not (1.9 < aspect < 1.95):
            continue
        yield img[y : y + h, x : x + w]


def extract_text_image_from_card(img):
    crop_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = crop_img.shape

    # The texts are in the lower part of the image, so crop to that lower half
    crop_img = crop_img[h // 2 : h, 0:w]

    # Extract white enough text
    crop_img = cv2.inRange(crop_img, 190, 255)
    return crop_img
