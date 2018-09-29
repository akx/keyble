# -- encoding: UTF-8 --
import cv2

from keyble.utils import birange


class CardError(Exception):
    pass


class NoExtents(CardError):
    pass


class NotDetected(CardError):
    pass


def find_corner(gray, y0, y1, y_up, x_left):
    """
    Find corner.
    The idea is that the corner has to be the first bright pixel
    in the given range of scanlines.

    To find a right corner, set x_left=True, so the rightmost bright pixel is found.
    Similarly, to find a lower corner, set y_up=True.
    """

    for y in birange(y0, y1, backwards=y_up):
        row = gray[y]
        for x in birange(0, len(row), backwards=x_left):
            if row[x] > 160:
                return (x, y)


TALL_RANGES = [(250, 300), (1270, 1400)]
SHORT_RANGES = [(680, 750), (1250, 1300)]
SHORT_ASPECT = 1.05892
TALL_ASPECT = 0.6121097


def find_card_corners(gray, ranges, all=True):
    (ny0, ny1), (sy0, sy1) = ranges
    corners = {}
    corners['nw'] = find_corner(gray, ny0, ny1, False, False)
    if all:
        corners['ne'] = find_corner(gray, ny0, ny1, False, True)
        corners['sw'] = find_corner(gray, sy0, sy1, True, False)
    corners['se'] = find_corner(gray, sy0, sy1, True, True)
    return corners


def find_card_extent(gray, ranges):
    corners = find_card_corners(gray, ranges, all=False)
    return (corners['nw'], corners['se'])


def detect_and_crop_card(img, gray, ranges):
    assert img.shape[:2] == (1920, 1080)
    p0, p1 = find_card_extent(gray, ranges)
    if not (p0 and p1):
        raise NoExtents("could not find card extent")
    x0, y0 = p0
    x1, y1 = p1
    cropped = img[y0:y1, x0:x1]
    return cropped


def get_aspect(img):
    h, w = img.shape[:2]
    return w / h


def crop_card(img):
    """
    Attempt to detect, then crop, a card from the given frame.

    :param img: Input frame. Should be BGR, 1080x1920 (but will be resized to that if not).
    :return: Cropped card.
    :raises CardError: if extraction fails
    """
    img = cv2.resize(img, (1080, 1920))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for ranges, expected_aspect in [
        (TALL_RANGES, TALL_ASPECT),
        (SHORT_RANGES, SHORT_ASPECT),
    ]:
        card_img = detect_and_crop_card(img, gray, ranges=ranges)
        aspect = get_aspect(card_img)
        aspect_delta = abs(aspect - expected_aspect)
        if aspect_delta < .008:
            return card_img
    raise NotDetected("no suitable card found")
