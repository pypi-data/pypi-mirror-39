import numpy as np
import pandas as pd
import os
import argparse
import glob
import uuid
from PIL import Image
from tqdm import tqdm
from . import helper

def bbox(img):
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return rmin, rmax, cmin, cmax

def run(root, args):
    src = os.path.join(root, args.src)
    for mask_csv in tqdm(glob.iglob(os.path.join(src, '**', 'mask.csv'), recursive=True)):
        df = pd.read_csv(mask_csv, index_col='ImageId', dtype={'Label': str})
        if 'Label' not in df.columns:
            continue
        # filter out rows (a) labeled as ctc and (b) manual label
        dapi = helper.image_picker('', os.path.dirname(mask_csv), 'UV', 0)
        if not dapi:
            continue
        df_cad = df.filter(regex='^_n_|^[0-9a-z]+-[0-9a-z]+-', axis=0)
        df_cad[ df_cad['Label'] == 'ctc']
        if not len(df_cad):
            continue
        tqdm.write(f'{len(df_cad)} manual labeled CTC(s) found in {mask_csv} ... ')
        # construct mask array
        im = Image.open(dapi)
        shape = im.size[::-1] # w, h -> h, w
        masks = {}
        for row in df.itertuples():
            m = row.Index
            rle = row.EncodedPixels
            if not isinstance(rle, str):
                masks[m] = None
            else:
                masks[m] = helper.rle_decode(rle, shape)
        # for each missing nuclei, crop its target window upon DAPI channel and every mask inside target window
        w = args.crop // 2
        for row in df_cad.itertuples():
            m = row.Index
            if masks[m] is None:
                continue
            # create crop save folder, combine origin mask id and random string
            dest = os.path.join(root, args.dest, '{}__{}'.format(m, str(uuid.uuid4())[:8]))
            os.makedirs(dest)
            # get bounding box of missing nuclei
            y0, y1, x0, x1 = bbox(masks[m])
            # expand to target window, handle boundery case
            c = (int((y1+y0)/2), int((x1+x0)/2))
            y0, y1 = max(c[0]-w, 0), min(c[0]+w, shape[0])
            x0, x1 = max(c[1]-w, 0), min(c[1]+w, shape[1])
            # save crop as images, rect as (left, upper, right, lower)
            os.makedirs(os.path.join(dest, 'images'), exist_ok=True)
            if args.all:
                img_dir = os.path.join(os.path.dirname(mask_csv), 'images')
                for f in os.listdir(img_dir):
                    try:
                        t_im = Image.open(os.path.join(img_dir, f))
                        crop = t_im.crop((x0, y0, x1, y1))
                        crop.save(os.path.join(dest, 'images', f))
                    except IOError:
                        pass
            else:
                crop = im.crop((x0, y0, x1, y1))
                crop.save(os.path.join(dest, 'images', os.path.basename(dapi)))
            # save mask crop
            if args.rle:
                t_df = df.copy()
                t_df['EncodedPixels'] = ''
            for m in masks:
                if masks[m] is None:
                    continue
                arr = masks[m]
                if not np.any(arr[y0:y1, x0:x1]):
                    continue # bypass empty mask
                if args.rle:
                    crop = arr[y0:y1, x0:x1]
                    rle = helper.rle_encode(crop)
                    rle = ' '.join([str(i) for i in rle])
                    t_df.at[m, 'EncodedPixels'] = rle
                else:
                    arr = (255 * arr).astype(np.uint8)
                    crop = Image.fromarray(arr[y0:y1, x0:x1])
                    os.makedirs(os.path.join(dest, 'masks'), exist_ok=True)
                    crop.save(os.path.join(dest, 'masks', '{}.png'.format(m)))
            if args.rle:
                # remove empty masks
                t_df['EncodedPixels'].replace('', np.nan, inplace=True)
                t_df.dropna(subset=['EncodedPixels'], inplace=True)
                t_df.to_csv(os.path.join(dest, 'mask.csv'))
        # visit next mask_csv


def main(args=None):
    parser = argparse.ArgumentParser(
        prog='scan_miss'
    )
    parser.add_argument('--src', type=str, help='subfolder to process')
    parser.add_argument('--dest', type=str, help='subfolder to save crop data')
    parser.add_argument('--crop', type=int, help='crop region width')
    parser.add_argument('--all', action='store_true', help='crop all images not only DAPI')
    parser.add_argument('--rle', action='store_true', help='save as RLE instead of PNG')
    parser.set_defaults(src='test', crop=300, dest='train', all=False, rle=False)
    args = parser.parse_args(args)

    root = 'data'
    assert os.path.exists(root)
    assert os.path.exists(os.path.join(root, args.src))
    assert not os.path.exists(os.path.join(root, args.dest))
    run(root, args)

if __name__ == '__main__':
    main()