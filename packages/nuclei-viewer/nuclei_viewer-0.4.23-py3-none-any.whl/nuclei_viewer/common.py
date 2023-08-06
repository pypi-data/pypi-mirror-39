import os
import re
import json
import base64
from datetime import datetime
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from flask import send_file, request
from PIL import Image
from skimage.io import imread
from skimage import img_as_ubyte
import warnings
warnings.filterwarnings("ignore")
from io import BytesIO
from . import app, page, cache
from . import helper
from .config import config

#####################################################
# backend callback functions
def list_group():
    # fire on page load
    return [
        {'label': f.name, 'value': f.name}
        for f in os.scandir(helper.dataset_path) if f.is_dir()
    ]

def list_samples(group):
    ''' update samples from selected group '''
    if not group:
        return []
    return sorted([
        {'label': f.name, 'value': f.name}
        for f in os.scandir(os.path.join(helper.dataset_path, group)) if f.is_dir()
    ], key=lambda x: x['value'])

def list_tile(group, sample, tile=None, count=None, color=None):
    ''' update items from selected dataset '''
    if not group or not sample:
        return [[]]
    sid = os.path.join(group, sample)
    data = helper.read_metadata(sid)
    if 'grid' not in data:
        # '.' imply current directory in unix
        return [[{'label': '', 'value': '.'}]]
    color = color if color != 'WhiteSmoke' else ''
    grid = data['grid']
    grid_color = data['color'] if 'color' in data else np.empty_like(grid, dtype=str).tolist()
    options = []
    for j, r in enumerate(grid):
        row = []
        for i, c in enumerate(r):
            tid = '{}_{}'.format(j, i)
            if tid == tile:
                if count is not None:
                    grid[j][i] = c = count
                if color is not None:
                    grid_color[j][i] = color
            cell = {'label': ' ', 'value': tid}
            if not helper.is_valid_sample(os.path.join(group, sample, tid)):
                cell['disabled'] = True
            else:
                if grid_color[j][i]:
                    cell['style'] = {'background-color': grid_color[j][i]}
                # cell['label'] = c
            row.append(cell)
        options.append(row)
    if tile:
        data['grid'] = grid
        data['color'] = grid_color
        helper.write_metadata(sid, data)
    return options

def select_default_tile(tiles, tile):
    if tile and any(tile == x['value'] for sub in tiles for x in sub):
        return tile
    if tiles and len(tiles[0]):
        return tiles[0][0]['value']
    return None

def fetch_info(uid, update=None):
    mask_csv = helper.csv_path(uid)
    df = pd.read_csv(mask_csv, index_col='ImageId', dtype={'Label': str})
    if 'Label' not in df.columns:
        df['Label'] = ''
    else:
        df.Label.fillna('', inplace=True)
    if update:
        label = update['label']
        mask = update['mask']
        df.at[mask, 'Label'] = '' if label == 'other' else label
        if 'contour' in update:
            rle = helper.contour_rle(update['contour'], image_size(uid)[::-1])
            df.at[mask, 'EncodedPixels'] = rle
        df.to_csv(mask_csv)
    return df

def gen_table(items):
    return [html.Tr([
        html.Td(d.upper() if i == 0 else d) for i, d in enumerate(r)
    ]) for r in items]

@app.route('/r/<path:uid>')
def serve_image(uid):
    # Refer: http://flask.pocoo.org/docs/1.0/quickstart/#the-request-object
    # ?key=value <=> value = request.args.get('key', '')
    channel = json.loads(config.get('UI', 'channel'))
    c = request.args.get('c', channel[0][0])
    e = request.args.get('e', 'true') == 'true'
    res = rawimg(uid, c, e)
    if not res:
        return ''
    buff, _, _ = res
    buff.seek(0)
    return send_file(buff, mimetype='image/jpeg', last_modified=datetime.now())

@cache.memoize()
def image_size(uid):
    ''' return (width, height) '''
    fp = helper.image_picker(uid, 'UV', 0)
    if not fp:
        return None
    im = Image.open(fp)
    return im.size

@cache.memoize()
def b64img(uid, channel, enhance):
    res = rawimg(uid, channel, enhance)
    if not res:
        return
    buff, w, h = res
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")
    return 'data:image/jpeg;base64, ' + encoded, w, h


def imopen(fp):
    # always return uint8 image array
    x = imread(fp)
    x = img_as_ubyte(x)
    if x.ndim == 3 and x.shape[-1] == 4:
        # drop alpha channel
        x = x[:,:,:3]
    return x

def rawimg(uid, channel, enhance=False, quality=75):
    fallback=0 if channel=='UV' else None # fallback to first file if DAPI channel
    fp = helper.image_picker(uid, channel, fallback)
    if not fp:
        return None
    if isinstance(fp, list):
        rgb = list(map(imopen, fp))
        if enhance:
            rgb = helper.enhance_contrast(rgb, channel)
        im = np.dstack(rgb)
    else:
        im = imopen(fp)
        if im.ndim == 2: # grayscale image
            if enhance:
                im = helper.enhance_contrast(im, channel)
            ch = config.getint('colorize', channel, fallback=-1)
            if ch != -1:
                # colorize grayscale image
                rgb = np.zeros((*im.shape, 3), dtype=np.uint8)
                rgb[:, :, ch] = im
                im = rgb
    # save as memory buffer
    im = Image.fromarray(im)
    w, h = im.size
    buff = BytesIO()
    im.save(buff, format='jpeg', quality=quality)
    return buff, w, h