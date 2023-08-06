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
color = {
    'centroid': 'MistyRose',
    'ctc': 'Gold',
    'other': 'LightSkyBlue',
    'immune': 'ForestGreen'
}

#####################################################
# frontend page layout

#### Critical! refer https://reactjs.org/docs/reconciliation.html
# div key attribute is essential to distinguish object instance,
# otherwise ReactDOM heuristics might mess up React Component lifecycle and upset nested component instance. 
####
layout = html.Div(key='pt_tab', className='row', children=[
    # menu and info
    html.Div(className='two columns', children=[
        # hidden variables
        html.Div(id='pt_uid', style={'display': 'none'}),
        html.Div(id='pt_info', style={'display': 'none'}),
        # Dataset info
        html.Div(className='card', children=[
            dashx.Dropdown(
                id='pt_group',
                className='dropdown',
                placeholder='Group ...',
            ),
            dashx.Dropdown(
                id='pt_sample',
                className='dropdown',
                placeholder='Samples ...',
                ellipsis=config.get('UI', 'ellipsis', fallback=None),
            ),
            dashx.RadioItemRows(id='pt_tile', className='tile'),
            dashx.RadioItemRows(
                id='pt_color',
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
                id='pt_channel',
                options=[
                    [{'label': i, 'value': i} for i in sub]
                    for sub in json.loads(config.get('UI', 'channel'))
                ],
            ),
            dashx.RadioItemRows(
                id='pt_enhance',
                style={'border-top': '1px solid #ddd'},
                options=[[
                    {'label': k, 'value': v}
                    for k, v in {'Enhanced': True, 'Origin': False}.items()
                ]],
            ),
            dashx.RadioItemRows(
                id='pt_lock',
                style={'border-top': '1px solid #ddd'},
                options=[[
                    {'label': k, 'value': v}
                    for k, v in {'Zoom lock': True, 'Refresh': False}.items()
                ]],
            ),
            dashx.RadioItemRows(
                id='pt_filter',
                style={'border-top': '1px solid #ddd'},
                options=[[
                    {'label': k, 'value': v}
                    for k, v in {'Adjacent': True, 'Generous': False}.items()
                ]]
            ),
        ]),
        # Nuclei info
        html.Table(id='pt_table')
    ]),
    # major content
    dashx.GraphObserver(id='pt_hook', cell='ctc', color=color, children=
        dcc.Graph(
            id='pt_graph',
            className='ten columns',
            style={'height': '80vh'},
        ),
    ),
])


#####################################################
# backend callback functions
@page.callback(
    Output('pt_group', 'options'),
    [Input('pt_uid', 'n_clicks')]
)
@cache.memoize()
def list_group(_):
    # fire on page load
    return common.list_group()

@page.callback(
    Output('pt_sample', 'options'),
    [Input('pt_group', 'value')]
)
@cache.memoize()
def list_samples(group):
    ''' update samples from selected group '''
    if isinstance(group, dict):
        group = group['value']
    return common.list_samples(group)

@page.callback(
    Output('pt_tile', 'options'),
    [Input('pt_sample', 'value'), Input('pt_color', 'value')],
    [State('pt_group', 'value'), State('pt_tile', 'value'), State('pt_uid', 'children')],
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
    Output('pt_tile', 'value'),
    [Input('pt_tile', 'options')],
    [State('pt_tile', 'value')]
)
def select_default_tile(tiles, tile):
    return common.select_default_tile(tiles, tile)

@page.callback(
    Output('pt_uid', 'children'),
    [Input('pt_tile', 'value')],
    [State('pt_group', 'value'), State('pt_sample', 'value')]
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
    Output('pt_hook', 'clickData'),
    [Input('pt_uid', 'children')],
)
def clear_select(uid):
    # clear click data when uid change
    return None

@page.callback(
    Output('pt_info', 'children'),
    [Input('pt_uid', 'children'), Input('pt_hook', 'clickData')],
)
def update_info(uid, update):
    if not uid:
        return
    df = common.fetch_info(uid, update)
    # return json object
    info = {}
    # parse centroid markers
    data = helper.read_metadata(uid)
    if 'centroid' in data and len(data['centroid']):
        info['centroid'] = len(data['centroid'])
    # count label
    for r in df.groupby(['Label']).count().itertuples():
        g = 'others' if r[0] == '' else r[0]
        info[g] = r[1]
    return json.dumps(info)

@page.callback(
    Output('pt_table', 'children'),
    [Input('pt_info', 'children')],
)
def update_table(info):
    if not info:
        return
    rows = []
    for k, v in json.loads(info).items():
        rows.append([k, v])
    return common.gen_table(rows)

@page.callback(
    Output('pt_graph', 'figure'),
    [Input('pt_uid', 'children'), Input('pt_channel', 'value'),
     Input('pt_filter', 'value'), Input('pt_enhance', 'value')],
    [State('pt_lock', 'value'), State('pt_graph', 'relayoutData')]
)
def update_graph(uid, channel, nearby, enhance, lock, relayout):
    if not uid:
        return {}
    res = common.b64img(uid, channel, enhance)
    if not res:
        return {'layout': {'title': 'Invalid image data'}}
    b64, w, h = res
    # figure images
    images = [dict(
        xref='x',
        yref='y',
        x=0,
        y=0,
        yanchor='top', # top-left is (0, 0)
        sizing='stretch',
        sizex=w,
        sizey=h,
        layer='below',
        #####
        # Bug at https://github.com/plotly/plotly.js/blob/edc166f62d0d958194c04d830501a741cf6c7175/src/components/images/draw.js#L77
        # Code: ``` if(this.img && this.img.src === d.source) { ```
        # which handle query path incorrectly, then always trigger image download, even it's same url
        # To workaround the issue, need a full url href.
        # However, the hack won't work inside docker or reverse proxy, alternaitve way is base64 encoded image
        #####
        # source='/r/{}'.format(uid)
        source=b64
    )] if channel else []
    # figure grid lines
    xaxis = dict(
        autorange=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        range=(0, w),
        scaleanchor='y',
        scaleratio=1,
    )
    yaxis = dict(
        autorange=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        range=(h, 0),
    )
    if relayout and lock:
        if 'xaxis.range[0]' in relayout:
            xaxis['range'] = (
                relayout['xaxis.range[0]'],
                relayout['xaxis.range[1]']
            )
        if 'yaxis.range[0]' in relayout:
            yaxis['range'] = (
                relayout['yaxis.range[0]'],
                relayout['yaxis.range[1]']
            )
    # configure legend
    legend = dict(
        x=0,
        y=1.01,
        orientation='h',
        bgcolor='rgba(255, 255, 255, 0.7)'
    )
    # annotation placeholder
    note = [dict(
        x=0.98,
        y=0.98,
        showarrow=False,
        text='Click to label: ctc',
        xref='paper',
        yref='paper',
        font=dict(color='silver'),
        align='right',
    )]
    # configure layout
    layout = dict(
        autosize=True,
        dragmode='pan',
        hovermode='closest',
        xaxis=xaxis,
        yaxis=yaxis,
        images=images,
        margin=dict(t=10, b=30, l=40, r=10, pad=4),
        legend=legend,
        annotations=note,
    )
    data = traces(uid, (h, w), nearby)
    return dict(data=data, layout=layout)

#####################################################
# utility functions
#@helper.timeit
def traces(uid, size, nearby):
    ''' parse json in syntax:
    {
       'centroid': [[y0, x0], [y1, x1], [y2, x2] ... ],
       'ctc': ['mask01', 'mask02' ...]
    }
    '''
    items = []
    data = helper.read_metadata(uid)
    # parse centroid markers
    centroid = None
    if 'centroid' in data and len(data['centroid']):
        centroid = np.array(data['centroid'], dtype=object)
        has_label = centroid.shape[1] == 3
        items.append(dict(
            showlegend = True,
            legendgroup = 'centroid',
            name = 'centroid',
            mode = 'markers',
            hoverinfo = 'text' if has_label else 'x+y',
            marker = {'color': color['centroid'], 'symbol': 'x', 'size': 10},
            x = centroid[:, 1],
            y = centroid[:, 0],
            text = centroid[:, 2] if has_label else ''
        ))
        centroid = centroid[:, :2].astype(int)
    # parse contours
    def trace(g, n, p, is_legend=False, visible=True, x=[0], y=[0]):
        sn = helper.shorten(n)
        sn = '{0}: {1:.0%}'.format(sn, p) if p > 0 else sn
        return dict(
            showlegend = is_legend,
            legendgroup = g,
            name = sn,
            customdata = [n],
            mode = 'lines',
            line = {'color': color[g]},
            x = x,
            y = y,
            fill = 'none' if is_legend else 'toself',
            fillcolor = color[g],
            opacity = 1.0 if is_legend else 0.7,
            hoverinfo = 'skip' if is_legend else 'name',
            visible = True if visible else 'legendonly',
        )
    # non-interactive legend placeholders
    hide_nuclei = config.getboolean('UI', 'hide_nuclei', fallback=False)
    for g in ['ctc', 'immune', 'other']:
        visible = g != 'other' if hide_nuclei else True
        items.append(trace(g, g, 0, True, visible))
    # iterate contours
    def _f(res):
        nonlocal centroid, nearby
        if centroid is None or res is None or not nearby:
            return True # no filter
        # filter by distance of centroid
        m, c, v, p = res
        x, y = np.mean(c, axis=0, dtype=int) # center of polygon
        dist = np.sqrt((centroid[:, 0] - y)**2 + (centroid[:, 1] - x)**2)
        return np.any(dist <= 150)
    for m, c, v, p in filter(_f, helper.iter_masks(uid, size)):
        if v == 'bad':
            continue
        g = v if v in ['ctc', 'immune'] else 'other'
        c = np.vstack((c, c[0])) # closure shape to first pixel
        visible = g != 'other' if hide_nuclei else True
        items.append(trace(g, m, p, False, visible, c[:, 0], c[:, 1]))
    return items
