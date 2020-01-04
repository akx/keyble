# -- encoding: UTF-8 --
import os

import cv2
import tqdm

import keyble.emcarden as emc
from keyble.image_utils import crop_image_only_outside


def extract_cards_from_video(input_video, dest_dir):
    cap = cv2.VideoCapture(input_video)
    n_frames = int(cap.get(int(cv2.CAP_PROP_FRAME_COUNT)))
    n_cards = 0
    with tqdm.tqdm(range(n_frames), unit='f', unit_scale=True) as prog:
        for fnum in prog:
            if not cap.isOpened():
                break
            ret, frame = cap.read()
            if not ret:
                break
            for cnum, card_image in enumerate(emc.find_cards(frame)):
                counter = f'{fnum:04d}_c{cnum:04d}'
                cv2.imwrite(os.path.join(dest_dir, f'card_{counter}.png'), card_image)
                text_image = crop_image_only_outside(
                    emc.extract_text_image_from_card(card_image)
                )
                cv2.imwrite(os.path.join(dest_dir, f'text_{counter}.png'), text_image)
                n_cards += 1
            prog.set_description('%d cards found' % n_cards)
