import os
import json
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from . import app, page, cache
from . import helper
from .config import config
from . import common
from . import dashx

#####################################################
# global variables

#####################################################
# frontend page layout

#### Critical! refer https://reactjs.org/docs/reconciliation.html
# div key attribute is essential to distinguish object instance,
# otherwise ReactDOM heuristics might mess up React Component lifecycle and upset nested component instance. 
####
layout = html.Div(key='pc_tab', className='row', children=[
    # menu and info
    html.Div(className='two columns', children=[
        # hidden variables
        html.Div(id='pc_uid', style={'display': 'none'}),
        html.Div(id='pc_info', style={'display': 'none'}),
        # Dataset info
        html.Div(className='card', children=[
            dashx.Dropdown(
                id='pc_group',
                className='dropdown',
                placeholder='Group ...',
            ),
            dashx.Dropdown(
                id='pc_sample',
                className='dropdown',
                placeholder='Samples ...',
                ellipsis=config.get('UI', 'ellipsis', fallback=None),
            ),
            dashx.RadioItemRows(id='pc_tile', className='tile'),
            dashx.RadioItemRows(
                id='pc_color',
                style={'font-size': '6px', 'margin-top': '3px'},
                options=[[
                    {
                        'label': ' ',
                        'value': c,
                        'style': {
                            'background-color': c,
                            'white-space': 'pre',
                            'border-radius': '0px',
                        }
                    }
                    for c in ['WhiteSmoke', 'Red', 'Orange', 'Gold', 'LimeGreen', 'RoyalBlue', 'BlueViolet']
                ]],
            ),
        ]),
        # Toolbar
        html.Div(className='card', children=[
            dashx.RadioItemRows(
                id='pc_filter',
                style={'border-bottom': '1px solid #ddd', 'margin-bottom': '10px'},
                options=[[
                    {'label': k, 'value': v}
                    for k, v in {'All': False, 'Labeled': True}.items()
                ]],
                value = False,
            ),
            html.Div(style={'height': '35px'}, children=[
                dcc.Slider(
                    id='pc_prob',
                    min=0,
                    max=1,
                    step=0.05,
                    value=0.7,
                    included=False,
                    marks= {p: {'label': '{:.0%}'.format(p)} for p in [0.4, 0.7]}
                ),
            ]),
        ]),
        # Nuclei info
        html.Table(id='pc_table')
    ]),
    html.Div(className='ten columns', style={'min-height': '80vh'}, children=[
        dashx.ImageBox(
            id='pc_box',
            className='card',
            coordinate=config.getboolean('UI', 'coordinate'),
            channel=[
                [{'label': i, 'value': i} for i in sub]
                for sub in json.loads(config.get('UI', 'channel'))
            ],
            enhance=[[
                {'label': k, 'value': v}
                for k, v in {'Enhanced': True, 'Origin': False}.items()
            ]],
            cell=[[
                {'label': k, 'value': v}
                for k, v in {'Others': 'other', 'Tumor': 'ctc', 'Immune': 'immune'}.items()
            ]],
        ),
    ]),
])

#####################################################
# backend callback functions
@page.callback(
    Output('pc_group', 'options'),
    [Input('pc_uid', 'n_clicks')]
)
@cache.memoize()
def list_group(_):
    # fire on page load
    return common.list_group()

@page.callback(
    Output('pc_sample', 'options'),
    [Input('pc_group', 'value')]
)
@cache.memoize()
def list_samples(group):
    if isinstance(group, dict):
        group = group['value']
    ''' update samples from selected group '''
    return common.list_samples(group)

@page.callback(
    Output('pc_tile', 'options'),
    [Input('pc_sample', 'value'), Input('pc_color', 'value')],
    [State('pc_group', 'value'), State('pc_tile', 'value'), State('pc_uid', 'children')]
)
def list_tile(sample, color, group, tile, uid):
    ''' update tiles from selected sample '''
    if not group or not sample:
        return [[]]
    if isinstance(group, dict):
        group = group['value']
    if isinstance(sample, dict):
        sample = sample['value']
    # detect if sample selection changed or not
    if tile and uid == os.path.join(group, sample, tile):
        return common.list_tile(group, sample, tile, color=color)
    return common.list_tile(group, sample)

@page.callback(
    Output('pc_tile', 'value'),
    [Input('pc_tile', 'options')],
    [State('pc_tile', 'value')]
)
def select_default_tile(tiles, tile):
    return common.select_default_tile(tiles, tile)

@page.callback(
    Output('pc_uid', 'children'),
    [Input('pc_tile', 'value')],
    [State('pc_group', 'value'), State('pc_sample', 'value')]
)
def update_uid(tile, group, sample):
    if not group or not sample or tile is None:
        return
    if isinstance(group, dict):
        group = group['value']
    if isinstance(sample, dict):
        sample = sample['value']
    uid = os.path.join(group, sample, tile)
    if helper.is_valid_sample(uid):
        return uid

@page.callback(
    Output('pc_box', 'prob'),
    [Input('pc_prob', 'value')]
)
def update_prob(prob):
    return prob

@page.callback(
    Output('pc_box', 'filter'),
    [Input('pc_filter', 'value')]
)
def update_filter(fil):
    return fil

@page.callback(
    Output('pc_box', 'clickData'),
    [Input('pc_uid', 'children')],
)
def clear_select(uid):
    # clear click data when uid change
    return None

@page.callback(
    Output('pc_info', 'children'),
    [Input('pc_uid', 'children'), Input('pc_prob', 'value'), Input('pc_box', 'clickData')],
)
def update_info(uid, prob, update):
    if not uid:
        return
    df = common.fetch_info(uid, update)
    if 'TumorProb' not in df.columns:
        df['TumorProb'] = 0.
    else:
        df.TumorProb.fillna(0, inplace=True)
    # calculate statitics
    df1 = df.groupby(['Label']).count()
    df2 = df[ df['TumorProb'] >= prob ].groupby(['Label']).count()
    df3 = df1.join(df2, rsuffix='_', sort=True).fillna(0)
    # return json object
    info = {}
    for r in df3.itertuples():
        g = 'others' if r[0] == '' else r[0]
        info[g] = {'total': r[1], 'sub': int(r[3])}
    return json.dumps(info)

@page.callback(
    Output('pc_table', 'children'),
    [Input('pc_info', 'children')],
    [State('pc_prob', 'value')],
)
def update_table(info, prob):
    if not info:
        return
    rows = [['probability', '{:.0%}'.format(prob)]]
    for k, v in json.loads(info).items():
        rows.append([k, '{} / {}'.format(v['sub'], v['total'])])
    return common.gen_table(rows)

@page.callback(
    Output('pc_box', 'data'),
    [Input('pc_uid', 'children')],
)
def update_mask(uid):
    if not uid:
        return {}
    res = common.image_size(uid)
    if not res:
        return {}
    w, h = res
    return {
        'src': '/r/{}'.format(uid),
        'masks': masks(uid, (h, w)),
    }

#####################################################
# utility functions
def masks(uid, size):
    items = []
    for m, c, v, p in helper.iter_masks(uid, size, only_bbox=True):
        if v == 'bad':
            continue
        g = v if v in ['ctc', 'immune'] else 'other'
        y0, y1, x0, x1 = c
        items.append({
            'mask': m,
            'label': g,
            'rect': [x0, y0, x1, y1],
            'prob': p,
        })
    return items
