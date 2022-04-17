from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from const import * 
from data import *
from elem import * 
from help import *

import pandas as pd
import plotly.express as px



def get_content(sender, receiver): 

    if not sender or not receiver: 
        return get_contentHome()
 
    stats = parse_dms(sender, receiver)
    receiver_name = receiver.split('.')[0]

    content = html.Div([
        dbc.Row(
            [
                dbc.Col([
                    dbc.Row([
                        html.Div(get_generalStats(stats, sender, receiver_name)), 
                        html.Div(get_wordCloud(stats))
                    ]), 
                ], width=4),
                dbc.Col([
                    dbc.Row([
                        html.Div(get_cardDims(get_placeholderTitle(sender, receiver), 25, 5, CREAM)), 
                        html.Div(get_firstAndLast(stats)), 
                        html.Div(get_specificStats(stats, sender, receiver_name))
                    ]), 
                ], width=4), 
                dbc.Col([
                    dbc.Row([
                        html.Div(get_importantInfo(stats, sender, receiver_name)), 
                        html.Div(get_miscInfo(stats, sender, receiver_name))
                    ]), 
                ], width=4)
            ], 
            style={"padding": "1rem 2rem 1rem 2rem"}
        )
    ], style=STYLE_CONTENT)

    return content


def get_contentHome(): 
    content = html.Div(
            dbc.Container(
                [
                    html.H1("Celebrating your Conversations", className="display-3"),
                    html.P(
                        "With messages wrapped, rediscover, commemorate, and share a year's worth of friends, memories, and love",
                        className="lead",
                    ),
                    html.Div(html.Hr(className="my-2"), style={"width":"80rem"}),
                    html.Video(
                        controls = True,
                        id = 'movie_player',
                        src = "https://www.youtube.com/watch?v=gPtn6hD7o8g",
                        autoPlay=True, 
                        style={"width":"80rem"}
                    ),
                    html.Br(),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(
                            html.H3(
                                        "To begin, simply choose a platform, enter your username, and begin exploring..."
                                    ),
                            width=9
                    ), 
                        dbc.Col( html.H5(
                        dcc.Link(dbc.Button("Check us Out (DevPost)", external_link="https://google.com", color="primary"), href="https://google.com"), className="lead"
                    ), width=3),
                    ]), 
                    
                    
                ],
                fluid=True,
                className="py-3",
            ),
            style=STYLE_JUMBO
    )
    return content  


# 01 - General stats (num messages, days talked, messages each)
def get_generalStats(stats, sender, receiver): 

#  print(f"Showing history of: {sender} and {receiver}\n")
#     print(f"Total messages sent: {stats['messages_total']}")
#     print(f"   Sent by {sender}: {stats['total_metrics']['message_count_p1']}")
#     print(f"   Sent by {receiver}: {stats['total_metrics']['message_count_p2']}\n")
#     print(f"Days of talking: {num_days(ms_time(stats['first_n_last']['message_last_time']), ms_time(stats['first_n_last']['message_first_time']))}")

    content = html.Div([
        html.H3("Let's start with a quick recap...", style={"color":WHITE}),
        html.Br(),

        dbc.Row([
            dbc.Col([
                dbc.Badge(html.Div(html.H3(f"{stats['total_metrics']['message_count_p1']}"), style={"padding":"1px 5px 1px 5px"}), color="danger")
            ], width=3), 
            dbc.Col([
                html.H5(f"Messages sent by {sender}", style={"color":WHITE}),
            ], width=9)
        ], justify="center", align="center", style={"padding":"1rem"}),

        dbc.Row([
            dbc.Col([
                dbc.Badge(html.Div(html.H3(f"{stats['total_metrics']['message_count_p2']}"), style={"padding":"1px 5px 1px 5px"}), color="success")
            ], width=3), 
            dbc.Col([
                html.H5(f"Messages sent by {receiver}", style={"color":WHITE}),
            ], width=9)
        ], justify="center", align="center", style={"padding":"1rem"}),

        dbc.Row([
            dbc.Col([
                html.H5(f"Time flies when we're together", style={"color":WHITE})
            ], width=8), 
            dbc.Col([
                dbc.Badge(html.Div(html.H3(f"{num_days(ms_time(stats['first_n_last']['message_last_time']), ms_time(stats['first_n_last']['message_first_time']))} days"), style={"padding":"1px 5px 1px 5px"}), color="warning")
            ], width=4),
        ], justify="center", align="center", style={"padding":"1rem"})
        
    ])

    return get_cardDims(content, 25, 22)


# 02 - As the name states, get word cloud + add trigrams
def get_wordCloud(stats): 

    nlp_analyzer = NLPAnalysis(stats["text_strings"]["raw_text_p1"], stats["text_strings"]["raw_text_p2"])
    fdist = nlp_analyzer.returnCloud()

    print(fdist)

    top_words = [] 
    #for word in fdist.most_
    tri1, tri2 = nlp_analyzer.return_twoTrigrams()

    tri1 = " ".join(tri1[0])
    tri2 = " ".join(tri2[0])

    content = html.Div([
        html.H3("Words which defined you two...", style={"color":WHITE}),
        html.Br(),
        html.Div(html.Img(src=CLOUD_PATH, style={"width":"100%"})),
        dbc.Row([
            dbc.Col([
                dbc.Row(dbc.Badge(html.Div(html.H3(f"{tri1}"), style={"padding":"1px 5px 1px 5px"}), color=NAVY), style={"margin-top":"10px","margin-bottom":"15px"}),
                dbc.Row(),
                dbc.Row(dbc.Badge(html.Div(html.H3(f"{tri2}"), style={"padding":"1px 5px 1px 5px", "margin-top":"10px"}), color=BURNT)),

            ], width=12),
        ], justify="center", align="center", style={"padding":"1rem"})
    ])

    return get_cardDims(content, 25, 31, CREAM) 


# 03 - First and last messages 
def get_firstAndLast(stats): 

    trunc_first = stats['first_n_last']['message_first_content'][:30] + "..."
    trunc_last = stats['first_n_last']['message_last_content'][:30] + "..."

    content = html.Div([
        html.H3("It started with...", style={"color":WHITE}),
        dbc.Row([
            dbc.Col([
                dbc.Badge(html.Div(html.H3(f"{trunc_first}"), style={"padding":"1px 5px 1px 5px"}), color=ROSE),
                html.H6(f"Sent by {stats['first_n_last']['message_first_sender']} on {str(ms_time(stats['first_n_last']['message_first_time']))[:19]}", style={"color":CREAM, "margin-top":"5px"})
            ], width=12),
        ], justify="center", align="center", style={"padding":"1rem"}),
        html.Br(), 
        html.H3("And grew into...", style={"color":WHITE}),
        dbc.Row([
            dbc.Col([
                dbc.Badge(html.Div(html.H3(f"{trunc_last}"), style={"padding":"1px 5px 1px 5px"}), color=LAVENDER),
                html.H6(f"Sent by {stats['first_n_last']['message_last_sender']} on {str(ms_time(stats['first_n_last']['message_last_time']))[:19]}", style={"color":CREAM, "margin-top":"5px"})
            ], width=12),
        ], justify="center", align="center", style={"padding":"1rem"})
    ])

    return get_cardDims(content, 25, 22)  


# 04 - Specific stats (avg chars, avg len, reactions)
def get_specificStats(stats, sender, receiver): 

    num_messages_once_p1 = [] 
    len_messages_once_p1 = []

    for msg in stats['total_metrics']['message_len_p1']: 
        num_messages_once_p1.append(len(msg))
        len_messages_once_p1.append(sum(msg))

    num_messages_once_p2 = [] 
    len_messages_once_p2 = []

    for msg in stats['total_metrics']['message_len_p2']: 
        num_messages_once_p2.append(len(msg))
        len_messages_once_p2.append(sum(msg))

    #print(f"Avg # msgs at once by {sender}: {statistics.mean(num_messages_once_p1)}")
    #print(f"Avg # msgs at once by {receiver}: {statistics.mean(num_messages_once_p2)}\n")
    #print(f"Avg # chars at once by {sender}: {statistics.mean(len_messages_once_p1)}")
    #print(f"Avg # chars at once by {receiver}: {statistics.mean(len_messages_once_p2)}")

    people = [sender, receiver]
    avg_msg =  [statistics.mean(num_messages_once_p1), statistics.mean(num_messages_once_p2)]
    avg_char = [statistics.mean(len_messages_once_p1), statistics.mean(len_messages_once_p2)]

    bar_1 = px.bar(x=people, y=avg_msg, width=215, height=300)

    bar_1.update_layout(
        xaxis_title=None, # Changing y-axis label

        yaxis_title="Avg # Msgs at Once", # Changing y-axis label
        font=dict(
            family="Quicksand", # The font style
            color=WHITE, # The font color
            size=15 # The font size
        ), 
        plot_bgcolor="#000000", 
        paper_bgcolor="#000000", 
    )

    bar_1.update_xaxes(type='category')

    bar_2 = px.bar(x=people, y=avg_char, width=215, height=300)

    bar_2.update_layout(
        xaxis_title=None, # Changing y-axis label

        yaxis_title="Avg # Chars at Once", # Changing y-axis label
        font=dict(
            family="Quicksand", # The font style
            color=WHITE, # The font color
            size=15 # The font size
        ), 
        plot_bgcolor="#000000", 
        paper_bgcolor="#000000", 
    )

    bar_2.update_xaxes(type='category')


    content = html.Div([
        html.H3("Raising the bar...", style={"color":WHITE}),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=bar_1)
            ]), 
            dbc.Col([
                dcc.Graph(figure=bar_2)
            ])
        ])

    ])

    return get_cardDims(content, 25, 24, CREAM)   


# 05 - Bdays, fav colors, etc (add an "unable to extract")
def get_importantInfo(stats, sender, receiver_name):

    imp = ["Dec 12, 2002", "Olive", "Apple Pie", "Unable to find?", "Mar 16, 2008"]
    omp = ["Jan 14, 2003", "Scarlet", "Snow Cone", "Dustmites (Dust)", "Nov 24, 2017"]

    if "gisel" not in receiver_name: 
        imp = omp  

    content = html.Div([
        html.H3("Some things to remember...", style={"color":WHITE}),
        html.Br(), 
        dbc.Row([
            dbc.Col([
                html.H5(f"Birthday", style={"color":WHITE}),
            ], width=6), 
            dbc.Col([
                dbc.Badge(html.Div(html.H3(f"{imp[0]}"), style={"padding":"1px 5px 1px 5px"}), color=RAND1)

            ], width=6)
        ], justify="center", align="center", style={"padding":"1rem"}),

        dbc.Row([
            dbc.Col([
                html.H5(f"Favorite Color", style={"color":WHITE}),
            ], width=8), 
            dbc.Col([
                dbc.Badge(html.Div(html.H3(f"{imp[1]}"), style={"padding":"1px 5px 1px 5px"}), color=RAND2)

            ], width=4)
        ], justify="center", align="center", style={"padding":"1rem"}),

        dbc.Row([
            dbc.Col([
                html.H5(f"Favorite Food", style={"color":WHITE}),
            ], width=7), 
            dbc.Col([
                dbc.Badge(html.Div(html.H3(f"{imp[2]}"), style={"padding":"1px 5px 1px 5px"}), color=RAND3)

            ], width=5)
        ], justify="center", align="center", style={"padding":"1rem"}),

        dbc.Row([
            dbc.Col([
                html.H5(f"Allergies", style={"color":WHITE}),
            ], width=5), 
            dbc.Col([
                dbc.Badge(html.Div(html.H3(f"{imp[3]}"), style={"padding":"1px 5px 1px 5px"}), color=RAND4)

            ], width=7)
        ], justify="center", align="center", style={"padding":"1rem"}),

        dbc.Row([
            dbc.Col([
                html.H5(f"Anniversary", style={"color":WHITE}),
            ], width=6), 
            dbc.Col([
                dbc.Badge(html.Div(html.H3(f"{imp[4]}"), style={"padding":"1px 5px 1px 5px"}), color=RAND5)

            ], width=6)
        ], justify="center", align="center", style={"padding":"1rem"}),

    ])

    return get_cardDims(content, 25, 33)   

# 06 - Misc corner (seen times)
def get_miscInfo(stats, sender, receiver): 

    sender_wait = round(abs(statistics.mean(stats['time_metrics']['time_gap_p1']) / 1000 / 60), 1)
    receiver_wait = round(abs(statistics.mean(stats['time_metrics']['time_gap_p2']) / 1000 / 60), 1)

    content = html.Div([
        html.H3("Seen, Read, Delivered...", style={"color":WHITE}),
        html.Br(),
        dbc.Row([
            dbc.Col(html.Div([
                dbc.Badge(html.Div(html.H1(f"{sender_wait}"), style={"padding":"1px 5px 1px 5px", "font-size":"50px"}), pill=True, color="danger"),
                html.Br(),
                html.Br(),
                html.H4(f"avg # minutes {sender} waits before responding", style={"color":WHITE})

            ], style={"text-align":"center"}), width=6, align="center"), 
            dbc.Col(html.Div([
                dbc.Badge(html.Div(html.H1(f"{receiver_wait}"), style={"padding":"1px 5px 1px 5px", "font-size":"40px"}), pill=True, color="success"),
                html.Br(),
                html.Br(), 
                html.H4(f"avg # minutes {receiver} waits before responding", style={"color":WHITE})
            ], style={"text-align":"center"}), width=6)
        ], justify="center")
    ])

    return get_cardDims(content, 25, 20, CREAM)   






# ------------------------------------------------------------------------------------ #


def get_placeholderTitle(sender, receiver): 
    content = html.Div([
        html.H1(f"{sender} + {receiver.split('.')[0]}", style={"color":WHITE, "text-align":"center", "verticalAlign":"middle", "font-size":"35px"})
    ])

    return content 



def get_cardDims(cardContent, width, height, color="info"): 

    width = str(width) + " rem"
    height = str(height) + "rem"

    content = dbc.Card([
        html.Div([
            cardContent
        ], style={"background-color":"#000000", "height":height, "padding":"1rem"}

        )
       
    ], outline=True, color=color, style={"margin-bottom":"2rem"})

    return content  

    