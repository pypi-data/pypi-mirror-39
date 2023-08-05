import dash
import dash_core_components as dcc
import dash_html_components as html
from . import page
from . import __version__
from . import page_tile
from . import page_cell

#####################################################
# frontend page layout
page.title = 'Nuclei Viewer'
page.layout = html.Div([
    # Banner
    html.Div(className='banner', children=[
        html.Img(src="/assets/aixmed.png", className='logo'),
        html.H2('Nuclei Analysis App'),
        html.H6('© 2018 AIxMed, Inc. All Rights Reserved.'),
        html.Span(__version__),
        html.Img(src="/assets/logo.png")
    ]),
    # Body
    dcc.Tabs([
        dcc.Tab(label='Tile', children=[page_tile.layout]),
        dcc.Tab(label='Cell', children=[page_cell.layout]),
    ], parent_className='container', className='tabs')
])
