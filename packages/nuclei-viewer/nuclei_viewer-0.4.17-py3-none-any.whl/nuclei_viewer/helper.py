import os
import csv
import time
import unittest
import json
import glob
from functools import lru_cache
import numpy as np
from PIL import Image
import pandas as pd
from skimage import img_as_ubyte
from skimage.measure import find_contours, approximate_polygon
from skimage.exposure import equalize_adapthist
from skimage.draw import polygon
import warnings
warnings.filterwarnings('ignore')
from .config import config

dataset_path = 'data'

def timeit(method):
    ''' as decorator '''
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed

def timef(method, *args, **kw):
    ''' as helper function '''
    ts = time.time()
    result = method(*args, **kw)
    te = time.time()
    print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
    return result

def json_path(uid):
    return os.path.join(dataset_path, uid, 'meta.json')

def mask_path(uid):
    return os.path.join(dataset_path, uid, 'masks')

def csv_path(uid):
    return os.path.join(dataset_path, uid, 'mask.csv')

def img_path(uid):
    return os.path.join(dataset_path, uid, 'images')

def con_path(uid):
    return os.path.join(dataset_path, uid, 'contour.json')

def read_metadata(path):
    fp = json_path(path)
    if not os.path.exists(fp):
        return {}
    with open(fp) as f:
        data = json.load(f)
        return data

def write_metadata(path, data):
    fp = json_path(path)
    with open(fp, 'w') as f:
        json.dump(data, f)

def is_valid_sample(uid):
    return os.path.exists(img_path(uid))

def rle_encode(x):
    '''
    x: numpy array of shape (height, width), 1 - mask, 0 - background
    Returns run length as list
    '''
    dots = np.where(x.T.flatten()==1)[0] # .T sets Fortran order down-then-right
    run_lengths = []
    prev = -2
    for b in dots:
        if (b>prev+1): run_lengths.extend((b+1, 0))
        run_lengths[-1] += 1
        prev = b
    return ' '.join([str(i) for i in run_lengths])

def rle_decode(mask_rle, shape, fill=True):
    '''
    mask_rle: run-length as string formated (start length)
    shape: (height,width) of array to return
    Returns numpy array, 1 - mask, 0 - background
    '''
    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths
    img = np.zeros(shape[0]*shape[1], dtype=bool) #np.uint8)
    for lo, hi in zip(starts, ends):
        if fill:
            img[lo:hi] = 1
        else:
            img[lo] = img[hi-1] = 1
    return img.reshape(shape, order='F')

@lru_cache(maxsize=40960)
def rle_contour(mask_rle, shape):
    if not isinstance(mask_rle, str):
        return []
    s = mask_rle.split()
    starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
    starts -= 1
    ends = starts + lengths - 1
    pix = set()
    for p in np.append(starts, ends):
        y = p % shape[0]
        x = p // shape[0]
        pix.add((y, x))
    return np.array(list(polygon_sort(pix)))

def save_rle(uid):
    mask_dir = mask_path(uid)
    if not os.path.exists(mask_dir):
        return False
    masks = [f for f in os.listdir(mask_dir) if f.endswith('.png')]
    masks.sort()
    mask_csv = csv_path(uid)
    with open(mask_csv, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(['ImageId', 'EncodedPixels'])
        for m in masks:
            img = Image.open(os.path.join(mask_dir, m))
            # = np.array(img.getdata(), dtype=np.uint8).reshape(img.size[::-1])
            x = np.asarray(img, dtype=bool)
            #x = x // 255
            rle = rle_encode(x)
            writer.writerow([os.path.splitext(m)[0], rle])
    return True

def load_rle_contour(uid, shape, centroid=None):
    return [c for m, c, _, _ in iter_contour(uid, shape, centroid)]

def iter_contour(uid, shape, centroid=None):
    ''' return name, contour pixels, label and probability '''
    mask_csv = csv_path(uid)
    if not os.path.exists(mask_csv):
        if not save_rle(uid):
            return
    df = pd.read_csv(mask_csv, dtype={'Label': str})
    if 'TumorProb' in df.columns:
        df.sort_values(by=['TumorProb'], ascending=False, inplace=True)
    for row in df.itertuples():
        m = row.ImageId
        rle = row.EncodedPixels
        v = getattr(row, 'Label', '')
        p = getattr(row, 'TumorProb', 0)
        c = rle_contour(rle, shape)
        if len(c) == 0:
            continue
        y, x = np.mean(c, axis=0, dtype=int) # center of polygon
        dist = 0
        if centroid is not None:
            centroid = np.asarray(centroid)
            dist = np.sqrt((centroid[:, 0] - y)**2 + (centroid[:, 1] - x)**2)
        if np.any(dist <= 150):
            yield m, c, v, p
        else:
            continue

def create_circular_mask(h, w, center=None, radius=None):
    if center is None: # use the middle of the image
        center = [int(w/2), int(h/2)]
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)
    mask = dist_from_center <= radius
    return mask

def centroid_mask(shape, centroid):
    if centroid is None:
        return np.full(shape, True)
    mask = np.full(shape, False)
    h, w = shape
    for c in centroid:
        c = c[::-1] # reverse order
        m = create_circular_mask(h, w, c, 150) # limit scope
        mask = np.logical_or(mask, m)
    return mask

def skimage_contour(uid):
    mask_dir = mask_path(uid)
    masks = [f for f in os.listdir(mask_dir) if f.endswith('.png')]
    masks.sort()
    for m in masks:
        img = Image.open(os.path.join(mask_dir, m))
        x = np.asarray(img, dtype=bool)
        contour = find_contours(x, 0.9)[0]

def contour_rle(contour, shape):
    '''
    contour: list of x, y vertices
    shape: image shape (h, w)
    '''
    y, x = polygon(contour[1], contour[0], shape)
    img = np.zeros(shape, dtype=np.bool)
    img[y, x] = 1
    return rle_encode(img)

def cv2_contour(uid):
    import cv2
    mask_dir = mask_path(uid)
    masks = [f for f in os.listdir(mask_dir) if f.endswith('.png')]
    masks.sort()
    for m in masks:
        img = cv2.imread(os.path.join(mask_dir, m), cv2.IMREAD_GRAYSCALE)
        _, thresh = cv2.threshold(img,127,255,0)
        _, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

def polygon_sort(corners):
    n = len(corners)
    cx = float(sum(x for x, y in corners)) / n
    cy = float(sum(y for x, y in corners)) / n
    cornersWithAngles = []
    for x, y in corners:
        an = (np.arctan2(y - cy, x - cx) + 2.0 * np.pi) % (2.0 * np.pi)
        cornersWithAngles.append((x, y, an))
    cornersWithAngles.sort(key = lambda tup: tup[2])
    return map(lambda p: (p[0], p[1]), cornersWithAngles)

def image_picker(uid, channel='UV', failback=None):
    ext = ['jpg', 'jpeg', 'png', 'tif', 'tiff']
    ext += [x.upper() for x in ext]
    ext = tuple(ext)
    img_dir = img_path(uid)
    if not os.path.exists(img_dir):
        return
    files = [f for f in os.listdir(img_dir) if f.endswith(ext)]
    files.sort()
    def _isin(sub, default=None):
        assert isinstance(sub, list)
        for fn in files:
            if any(s in fn for s in sub):
                return fn
        return default
    def _r(fn):
        if not fn:
            return
        if isinstance(fn, list):
            return [os.path.join(img_dir, f) for f in fn]
        return os.path.join(img_dir, fn)
    rule = json.loads(config.get('channels', channel))
    assert isinstance(rule, list)
    if isinstance(rule[0], list):
        # nested rule
        fn = []
        for x in rule:
            fn.append(_isin(x))
        if not fn.count(None):
            return _r(fn)
    else:
        fn = _isin(rule)
        if fn is not None:
            return _r(fn)
    # no matched filename, check failback
    if isinstance(failback, str):
        return image_picker(uid, failback)
    elif isinstance(failback, int):
        return _r(files[failback])
    return

def clahe(x):
    '''
    return PIL image or numpy array
    '''
    is_pil = isinstance(x, Image.Image)
    if is_pil:
        x = np.asarray(x, dtype=np.uint8)
    x = equalize_adapthist(x, clip_limit=0.02)
    x = img_as_ubyte(x)
    if is_pil:
        x = Image.fromarray(x)
    return x

def correct_gamma(img, gamma=1.):
    '''
    gamma correction of an intensity image, where
    gamma = 1. : no effect
    gamma > 1. : image will darken
    gamma < 1. : image will brighten
    '''
    return 255. *(img/255.)**gamma

# threshold contrast histogram equalization
def thche(x, bounds=(0, 255)):
    is_pil = isinstance(x, Image.Image)
    npx = np.array(x) if is_pil else x.copy()
    lb, ub = bounds
    scale = 2 * 255 / (ub - lb)
    npx = npx.astype(np.int16)
    npx -= lb
    npx[npx<0] = 0
    npx = npx.astype(np.uint16)
    npx = scale * npx
    npx[npx > 255] = 255
    npx = npx.astype(np.uint8)
    if is_pil:
        return Image.fromarray(npx)
    else:
        return npx

def ptche(x):
    percentile = config['UI'].getfloat('ptche_percentile', 0.85)
    is_pil = isinstance(x, Image.Image)
    # get pixel value of max and enhance percentile
    ix, it = np.max(x), np.nanquantile(x, percentile)
    if it > 15:
        # bypass image bright enough
        return x
    # enhance contract as tanh(2x) if pixel value exceed 85% percentile
    if is_pil:
        return x.point(lambda i: 255 * np.tanh(2*(i/ix)) if i > it else i)
    else:
        x[x>it] = 255 * np.tanh(2*(x[x>it]/ix))
        return x

def shorten(s, n=10, suffix=False):
    # truncate a string to at most n characters
    if suffix:
        return '...' + s[-n:] if len(s) > n else s
        # n = n-5
        # return s[:n] + (s[n:] and '...' + s[-5:])
    else:
        return s[:n] + (s[n:] and '...')

def move_ctc_to_csv(root):
    for fp in glob.iglob(os.path.join(root, '**', 'meta.json'), recursive=True):
        # check meta.json first
        with open(fp) as f:
            data = json.load(f)
        if 'ctc' not in data:
            continue
        ctc = data['ctc']
        del data['ctc']
        with open(fp, 'w') as f:
            json.dump(data, f)
        # read mask.csv
        fp = os.path.join(os.path.dirname(fp), 'mask.csv')
        df = pd.read_csv(fp, index_col='ImageId')
        if 'Label' not in df.columns:
            df['Label'] = ''
        # assign value to dataframe
        for id in ctc:
            if id == 'ctc':
                continue
            df.at[id, 'Label'] = 'ctc'
        # overwrite mask.csv
        df.to_csv(fp)

class FunctionTest(unittest.TestCase):
    def test_rle_convert(self):
        def random_test():
            data = np.random.randint(0,2,(100,100))
            seq = rle_encode(data)
            data_ = rle_decode(seq, data.shape)
            np.testing.assert_allclose(data, data_)
        random_test()

    def test_polygon_sort(self):
        a = np.array([
            [0, 1, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ])
        c = [(2, 2), (1, 3), (0, 2), (0, 1), (1, 1), (2, 1)]
        b = list(polygon_sort(list(zip(*np.nonzero(a)))))
        np.testing.assert_allclose(b, c)

class BenchmarkTest(unittest.TestCase):
    def test(self):
        uid = 'nina/2018-01-30/1_3'
        image_path = 'data/{}/images/1_3_DAPI.png'.format(uid)
        centroid = [[6, 1459], [617, 364], [634, 2040], [767, 1411], [1804, 589], [1893, 523], [2109, 1967]]
        img = Image.open(image_path)
        shape = img.size[::-1]
        print('Image shape is', shape)
        #timef(save_rle, mask_path)
        timef(save_contour, uid, shape)
        timef(load_rle_contour, uid, shape, centroid)
        #timef(cv2_contour, mask_path)
        #timef(skimage_contour, mask_path)

if __name__ == '__main__':
    unittest.main()
