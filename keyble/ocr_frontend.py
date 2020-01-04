# -- encoding: UTF-8 --
import glob
import os
from multiprocessing import Pool

import tqdm
from PIL import Image

from keyble.card_ocr import ocr_card


def wrap_ocr_card(filename):
    pil_image = Image.open(filename)
    res = ocr_card(pil_image)
    res['filename'] = filename
    return res


def ocr_card_image_directory(cards_dir):
    filenames = list(glob.glob(os.path.join(cards_dir, "text*.png")))
    results = []
    with Pool() as pool, tqdm.tqdm(
            pool.imap_unordered(wrap_ocr_card, filenames),
            total=len(filenames),
            unit='image',
    ) as prog:
        for result in prog:
            for line in result['lines']:
                line.pop(
                    'image', None
                )  # remove any images, we can't JSON serialize them anyway

            results.append(result)
            texts = ' '.join(
                line['text']
                for line in result['lines']
                if not line['text'].startswith('obtaining ')
            ).replace('\n', ' ')
            prog.set_description(texts[:40], False)

    results.sort(key=lambda r: r['filename'])
    return results
