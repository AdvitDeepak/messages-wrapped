# conda install -c conda-forge dash-renderer
# conda install -c conda-forge dash 
# conda install -c conda-forge dash-html-components 
# conda install -c conda-forge dash-core-components
# conda install -c conda-forge plotly
# conda install -c conda-forge dash-bootstrap-components
# conda install -c plotly plotly_express
# conda install pandas


from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from const import * 
from sbar import *
from elem import * 

import nltk 

nltk.download('punkt')
nltk.download("stopwords")
nltk.download("vader_lexicon")
nltk.download('words')


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, QUICKSAND])


# get_sidebar(LOGO, button_clicked, handle_placeholder)
# get_content(sender, receiver)

LOGO = app.get_asset_url ('logo.png')
content = html.Div([get_sidebar(LOGO, False, None), get_content(None, None)], id="page-content")
app.layout = html.Div(children=[content])

entered_handle = False # Will contain value
chose_receiver = False # Will contain value 

flags = [entered_handle, chose_receiver]


@app.callback(
    Output("page-content", "children"), 
    [Input("go-button", "n_clicks"), Input("person-radio", "value")], 
    [State("handle-text", "value")]
)
def on_button_click(n_clicks, radio_value, text_value):

    if not flags[0] and n_clicks and n_clicks >= 1: 
        flags[0] = text_value 
    
    if flags[0] and radio_value: 
        flags[1] = radio_value 

    print(f"n_clicks {n_clicks} | text_handle {text_value} | radio_value {radio_value} | flag_0 {flags[0]} | flag_1 {flags[1]}")


    ### Now, use the toggle flags to display the appropriate page ###

    if flags[0] and flags[1]: 
        return [get_sidebar(LOGO, flags[1], flags[0]), get_content(flags[0], flags[1])]

    elif flags[0]: 
        return [get_sidebar(LOGO, True, flags[0]), get_content(flags[0], None)]
    
    else: 
        return [get_sidebar(LOGO, False, None), get_content(None, None)]

    

if __name__ == '__main__':
    app.run_server(debug=True)
