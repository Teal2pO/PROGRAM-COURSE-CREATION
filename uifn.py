from globals import *
import base64
import io

from dash import dash_table
from dash import dcc, callback_context
from dash import html
import dash_daq as daq
from collections import OrderedDict
import dash_bootstrap_components as dbc

import re

# PDF to data table


def UI_PDFtoTable(data_df, height='300px'):
    div = dash_table.DataTable(
        data=data_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in data_df.columns],
        style_cell={'textAlign': 'left',
                    'height': 'auto', 'whiteSpace': 'normal'},
        style_header={
            'backgroundColor': '#8febb5',
            'fontWeight': 'bold'
        },
        # page_size=2,
        style_table={'height': height, 'overflowY': 'auto'},  # enable scroll
        # style_table={'height': '300px'},#enable scroll
        # style_table={
        #     'minHeight': '600px', 'height': '600px', 'maxHeight': '600px',
        #     'minWidth': '900px', 'width': '900px', 'maxWidth': '900px'
        # },
        # fixed_rows={'headers': True}
    )
    return div


def UI_dropdown(dropdown_id, option_list, styleDict={}, defaultValue=''):
    div = dcc.Dropdown(
        id=dropdown_id,
        options=[
            {'label': i, 'value': i} for i in option_list
        ],
        value=defaultValue,
        style=styleDict)

    return div


def UI_multidropdown(dropdown_id, option_list, styleDict={}):
    div = dcc.Dropdown(
        id=dropdown_id,
        options=[
            {'label': i, 'value': i} for i in option_list
        ],
        style=styleDict,
        multi=True,
        value=option_list,
    )

    return div


def UI_multidropdown_empty(dropdown_id, option_list, styleDict={}):
    div = dcc.Dropdown(
        id=dropdown_id,
        options=[
            {'label': i, 'value': i} for i in option_list
        ],
        style=styleDict,
        multi=True,
        value=[],
    )

    return div


# template download
html.Div([
    html.A('Download template', id='btn-template1',
           style={'font-style': 'italic', 'textAlign': 'center'}),
    dcc.Download(id='download-template1')
]),


def UI_fileUpload(upload_id):
    # upload file
    div = html.Div([
        html.P('Please upload csv file below to start',
               style={'font-style': 'italic'}),
        dcc.Upload(
            id=upload_id,
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select File')
            ]),
            style={
                'width': '98%',
                'height': '80px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ),
    ])
    return div

# pdf to CSV


def UI_fileDownload(button_id, download_id, user_msg):
    div = html.Div([
        html.A(user_msg, id=button_id, style={
               'font-style': 'italic', 'textAlign': 'left'}),
        dcc.Download(id=download_id)
    ])
    return div
# @app.callback(
#     Output("download-dataframe-csv", "data"),
#     Input("btn_csv", "n_clicks"),
#     prevent_initial_call=True,
# )
# def func(n_clicks):
#     return dcc.send_data_frame(df.to_csv, "mydf.csv")


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        df = pd.DataFrame()

    return df


def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression and the string into the fullmatch() method
    if (re.fullmatch(regex, email)):
        valid_email = True
    else:
        valid_email = False
    return valid_email


# 04 sections after login
# Changing course code
def section1Div_change_course_code(List):
    div = html.Div([
        # html.H5('Change course code',style={'font-weight': 'bold'}),

        html.H5([
            html.H5("Change course code", style={
                    "font-weight": "bold", "display": "inline"}),
            UI_toolTipIcon("changeCourseCodeMain"),
            html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                   href="https://youtu.be/o1iwwRMh06Q", target='_blank', style={"text-decoration": "none"}),
        ], style={'textAlign': 'center'}),

        UI_toolTip("changeCourseCodeMain", "Use this section to change the course code of a course created by you. When you change the course code existing course will not be updated, instead a new course will be created with the same course information. You can provide a new course code and a new course name."),


        html.P('Pick course code to change'),
        UI_dropdown('course2bChangedCode', List, {'width': '50%'}, None),
        html.Button(
            'Proceed', id='proceed_after_pick_course_code-btn', n_clicks=0),
        html.Div(id='proceed_after_pick_course_code-output'),

    ])
    return div

# changing course name - dropdown


def section2Div_change_course_name(List):
    div = html.Div([
        # html.H5('Change course name',style={'font-weight': 'bold'}),

        html.H5([
            html.H5("Change course name", style={
                    "font-weight": "bold", "display": "inline"}),
            UI_toolTipIcon("changeCourseNameMain"),
            html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                   href="https://youtu.be/IHckaI1X3MA", target='_blank', style={"text-decoration": "none"}),
        ], style={'textAlign': 'center'}),

        UI_toolTip("changeCourseNameMain", "Use this section to change a course name of a course created by you. When changing the course name, you will have to enter a comment for the version controlling system."),


        html.P('Pick course code to change'),
        UI_dropdown('course2bChangedCode2', List, {'width': '50%'}, None),
        html.Button(
            'Proceed', id='proceed_after_pick_course_code_Cname-btn', n_clicks=0),
        html.Div(id='proceed_after_pick_course_code_Cname-output'),
    ])
    return div


# delete course
def section3Div_delete_course_from_program(List):
    div = html.Div([
        # html.H5('Delete course from a program',style={'font-weight': 'bold'}),

        html.H5([
            html.H5("Delete course from a program", style={
                    "font-weight": "bold", "display": "inline"}),
            UI_toolTipIcon("deleteCourseFromAprogram"),
            html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                   href="https://youtu.be/n6CPziS3mhU", target='_blank', style={"text-decoration": "none"}),
        ], style={'textAlign': 'center'}),

        UI_toolTip("deleteCourseFromAprogram",
                   "Use this section to delete courses from the programs where you're the program lead."),



        html.P('Pick program'),
        UI_dropdown('program_deleteCourse', List, {'width': '50%'}, None),
        html.Button(
            'Proceed', id='proceed_after_programSelect-btn', n_clicks=0),
        html.Div(id='proceed_after_programSelect-output'),

    ])

    return div


# DataTable with Per-Row Dropdowns
# def UI_table_dropdown(table_id,data):
def UI_table_dropdown(table_id, data):
    # table_id='test'
    # data={'Cname1':['1','2','3'],'Cname2':['11','22','33']}
    column_name_list = data.keys()

    L = []
    for name in data:
        option_list = data[name]
        dict = {'if': {'column_id': 'Value', 'filter_query': '{Column_name} eq '+name},
                'options': [{'label': str(i), 'value': str(i)}for i in option_list]}
        L.append(dict)

    df_per_row_dropdown = pd.DataFrame(OrderedDict([
        ('Column_name', column_name_list),
        # ('Value', ['213', '3213', '1232']),
    ]))

    div = html.Div([

        dash_table.DataTable(
            id=table_id,
            data=df_per_row_dropdown.to_dict('records'),
            columns=[
                {'id': 'Column_name', 'name': 'Column name'},
                {'id': 'Value', 'name': 'Value', 'presentation': 'dropdown'},
            ],
            editable=True,
            dropdown_conditional=L
        ),
    ])

    return div


# ==================From course creation app=================================

def div_skillSelectionCourseCreation(programDomains, CAH3_skill_txt, num):
    # course skill selection for course creation
    div = html.Div([
        # html.H6('Search by course skills',style={'textAlign': 'center','font-weight': 'bold'}),
        html.Div([
            html.P('Domain', style={'font-weight': 'bold',
                   'textAlign': 'left', 'marginLeft': 20}),
            html.P('Sub domain', style={
                   'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20}),
            html.P('CAH3 skill classification', style={
                   'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20}),
        ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div([
            UI_dropdown('program_domainCC'+str(num), programDomains),
            UI_dropdown('program_subdomainCC'+str(num), []),
            UI_dropdown('program_skillCC'+str(num),
                        [CAH3_skill_txt], defaultValue=CAH3_skill_txt),
        ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    ])
    return div


# User Inputs for defining the course information
def UI_ILOx(ILO_num, ILOx_verb, ILOx_txt, ILOx_Cval, num):
    # ILO_num=1
    # num=1 for update
    # num=2 for create

    ILO_name = 'ILO-'+str(ILO_num)
    solo_level_dropdown_id = 'solo_level_ILO' + \
        str(ILO_num)+str(num)  # Ex: solo_level_ILO1
    verb_dropdown_id = 'verb_ILO' + \
        str(ILO_num)+str(num)  # Ex:verb_ILO11,verb_ILO12
    textbox_id = 'text_ILO'+str(ILO_num)+str(num)
    credit_slider_id = 'creditSlider'+str(ILO_num)+str(num)

    # ILO1
    div = html.Div([
        html.Div([
            html.P(ILO_name, style={'font-weight': 'bold',
                   'textAlign': 'left', 'marginLeft': 20}),
            html.Div([  # left side - solo level and action verb pick
                html.P('Pick solo level', style={
                       'font-weight': 'bold', 'textAlign': 'left'}),
                dcc.Dropdown(
                    id=solo_level_dropdown_id,
                    options=[
                        {'label': 'SOLO-01-UNISTRUCTURAL',
                         'value': 'SOLO_01_UNISTRUCTURAL'},
                        {'label': 'SOLO-02-MULTISTRUCTURAL',
                         'value': 'SOLO_02_MULTISTRUCTURAL'},
                        {'label': 'SOLO-03-RELATIONAL',
                            'value': 'SOLO_03_RELATIONAL'},
                        {'label': 'SOLO-04-EXTENDED ABSTRACT',
                         'value': 'SOLO_04_EXTENDED_ABSTRACT'},
                    ], style={'width': '95%'}),
                html.Br(),
                html.P('to do (pick action verb)', style={
                       'font-weight': 'bold', 'textAlign': 'left'}),
                # html.Div(id='app-output-verbs-ILO1'),#verb selection drop down appear here


                dcc.Dropdown(  # dropdown with action verbs
                    id=verb_dropdown_id,
                    # options=[ILOx_verb],
                    options=[] if ILOx_verb == None else [ILOx_verb],
                    value=ILOx_verb,
                    style={'width': '95%'}),

                html.Br(),
                html.P('Select ILO credits', style={
                       'font-weight': 'bold', 'textAlign': 'left'}),
                html.Br(),
                html.Br(),
                daq.Slider(
                    id=credit_slider_id,
                    min=0.1,
                    max=6,
                    # value=0.5,
                    value=ILOx_Cval,
                    # handleLabel={"showCurrentValue": True,"label": "VALUE"},
                    handleLabel={"showCurrentValue": True,
                                 "label": "Credits", "color": "black"},
                    step=0.05,
                ),

            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': 20}),

            html.Div([  # right side of the div
                html.P('what? (statement)', style={
                       'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20}),
                dcc.Textarea(
                    id=textbox_id,
                    value=ILOx_txt,
                    style={'width': '100%', 'height': 240, 'marginLeft': 20},
                ),
            ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top'}),








        ], style={'height': 350, 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '10px', }),

        html.Br()
    ])

    return div


# course skill selection for course search
def div_skillSelectionCourseSearch(programDomains):
    div = html.Div([
        html.H6('Search by course skills', style={
                'textAlign': 'center', 'font-weight': 'bold'}),
        html.Div([
            html.P('Domain', style={'font-weight': 'bold',
                   'textAlign': 'left', 'marginLeft': 20}),
            html.P('Sub domain', style={
                   'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20}),
            html.P('CAH3 skill classification', style={
                   'font-weight': 'bold', 'textAlign': 'left', 'marginLeft': 20}),
        ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top'}),


        html.Div([
            UI_dropdown('program_domain', programDomains),
            UI_dropdown('program_subdomain', []),
            UI_dropdown('program_skill', []),
        ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Button('Search', id='search-btn4', n_clicks=0),
        html.Div(id='search-output4'),
    ])
    return div


# application specific user interfaces===============================
# ILO to PO mapping depending on ILO count
def UIapp_POmappingBox(ILO_count, POList):
    # selectedPO_ILO1,selectedPO_ILO2 = dropdown id
    mappingBoxDivList = []
    for ILO_num in range(1, ILO_count+1):
        label = 'Map PO to ILO'+str(ILO_num)
        dropDownID = 'selectedPO_ILO'+str(ILO_num)
        mappingBoxDivList.append(html.P(label))
        # mappingBoxDivList.append(UI_dropdown(dropDownID,POList))
        mappingBoxDivList.append(
            html.Div([dcc.Dropdown(options=POList, id=dropDownID)]))
        mappingBoxDivList.append(html.Br())

    # for not availale ILOs generate empty dropdowns to keep callback errorless
    # ILO_num=6
    toDisableILOnos = list(range(ILO_num+1, 6+1))
    for ILO_num in toDisableILOnos:
        label = 'Map PO to ILO'+str(ILO_num)
        dropDownID = 'selectedPO_ILO'+str(ILO_num)
        mappingBoxDivList.append(html.P(label))
        mappingBoxDivList.append(html.Div([dcc.Dropdown(
            [{'label': 'ILO not specified', 'value': ':sampletext'}], ':sampletext', id=dropDownID, disabled=True)]))
        mappingBoxDivList.append(html.Br())

    return html.Div(mappingBoxDivList)


# Dash bootstrap for tool tips

def UI_toolTipIcon(idOfIcon):
    div = html.Sup(html.A(
        html.P("🛈",style={"display": "inline" ,"color" :"#007bff"} ,id=idOfIcon)))
    return div


def UI_toolTip(idOfIcon, textTip):
    div = dbc.Tooltip(
        html.Div([
            html.H6(textTip),
        ]),
        target=idOfIcon,
        placement="auto-start",
        # trigger="click"
        trigger="legacy"
    )

    return div
