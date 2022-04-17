from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from const import * 
from elem import * 
import os 


def get_sidebar(LOGO, button_clicked, handle_placeholder): 

    if not handle_placeholder: 
        handle_placeholder = "IG Handle..."

    print(f"sender {handle_placeholder} | receiver {button_clicked}")

    sidebar = html.Div([
        get_sidebarTitle(), 
        html.Br(), 
        get_sidebarPlatform(), 
        html.Br(), 
        get_sidebarInput(handle_placeholder), 
        html.Br(), 
        html.Br(),
        html.H3("discover a whole new side to your messages", style=STYLE_SIDEBAR_TEXT_2),
        html.Br(), 
        get_sidebarOptions(button_clicked), 
        html.Br(), 
        get_sidebarClosing(LOGO), 
    ], style=STYLE_SIDEBAR)
    
    return sidebar 


def get_sidebarTitle(): 
    return html.H1("messages wrapped", style=STYLE_SIDEBAR_TITLE)


def get_sidebarPlatform(): 
    content = dbc.Card([
        html.Div([
            html.H5("select a platform", style=STYLE_SIDEBAR_TEXT),
            html.Br(), 
            dbc.RadioItems(
                options=[
                    {"label": "Instagram", "value": 1},
                    {"label": "iMessage", "value": 2, "disabled": True},
                    {"label": "Android", "value": 3, "disabled": True},
                ],
                value=1,
                id="radioitems-input",
                style=STYLE_SIDEBAR_PLATFORM
            ), 
        ], style={"background-color":"#000000", "padding":"1rem"}

        )
       
    ], outline=True, color="info")
    return content  


def get_sidebarInput(placeholder): 
    content = dbc.Card([
        html.Div([
            html.H5("enter your info", style=STYLE_SIDEBAR_TEXT),
            html.Br(), 
            dbc.Row([
                dbc.Col(dbc.Input(id="handle-text", placeholder=placeholder, type="text", style={"background-color":"#000000", "color":"#FFFFFF"}), width=8), 
                dbc.Col(dbc.Button("Go", id="go-button"), width=4)

            ])
        ], style={"background-color":"#000000", "padding":"1rem"}

        )
       
    ], outline=True, color="info")
    return content  


def get_sidebarOptions(button_clicked): 

    content = dbc.Card([
        html.Div([
            html.H5("choose a convo", style=STYLE_SIDEBAR_TEXT),
            html.Br(), 
            get_sidebarChecklist(button_clicked),
        ], style={"background-color":"#000000", "padding":"1rem", "color":WHITE, "font-family":"Quicksand"}

        )
       
    ], outline=True, color="info")
    return content  


def get_sidebarChecklist(button_clicked): 

    content = []
    selected = ""

    if not button_clicked: 
        content.append(dbc.Row(
                        dbc.Col(
                            dbc.Spinner(color="info", type="grow"), 
                            width="auto", style={"padding":"2rem"}
                        ),
                        align="center", 
                        justify="center",
                    )
                )
        
        

        options = []
    
    else: 

        names = []
        values = []
        for root, dirnames, filenames in os.walk(DATA_PATH):
            for filename in filenames:
                if filename.endswith(('.json')):
                    names.append(filename.split(".")[0].capitalize())
                    values.append(filename)

                    if filename == button_clicked: selected = filename

        options = []
        for i in range(len(names)): 
            options.append({"label": names[i], "value": values[i]})


    content.append(dbc.RadioItems(
            id="person-radio",
            options=options,
            value=selected,
            labelCheckedClassName="text-success",
            inputCheckedClassName="border border-success bg-success",
    ))
    return html.Div(content) 


def get_sidebarClosing(LOGO): 
    logo = "logo.png"
    content = html.Center(html.Img(src=LOGO, height="50px", style={"margin-top": "1rem"}))
    return content      
