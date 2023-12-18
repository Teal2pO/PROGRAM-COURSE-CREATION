from fns import *
from fns_webservice import *
from globals import *
from uifn import *

import dash
import dash_auth
from dash import html
from dash import dcc, callback_context
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from dash import Dash, dcc, html, Input, Output, callback
import re


app = dash.Dash(__name__, suppress_callback_exceptions=True, url_base_pathname='/{}-program-course/'.format(
    'teal'), external_stylesheets=[dbc.themes.BOOTSTRAP])  # added DBC 4Jul2023


server = app.server
app.title = '{} Program Structure and Course Creation Tool'.format(
    appPrefixNAME)
app.layout = html.Div([

    html.Div([  # logos here

        html.Div([
            html.Img(src=('assets/erasmus_logo.png'),
                     style={'height': '50%', 'width': '50%'}),
        ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top', 'textAlign': 'left'}),

        html.Div(id='institute_logo-output', children=[
            # html.Img(src=('assets/logo.png'),style={'height':'50%', 'width':'50%'}),
        ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top', 'textAlign': 'center'}),

        html.Div([
            html.Img(src=('assets/teal_logo.jpeg'),
                     style={'height': '50%', 'width': '50%'}),
        ], style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'top', 'textAlign': 'right'}),

        html.Hr(),
    ]),

    html.H3('{} Program Structure and Course Creation Tool'.format(
        appPrefixNAME), style={'textAlign': 'center', 'font-weight': 'bold'}),
    html.Hr(),

    # html.P('Please provide your e-mail'),

    # dcc.Input(id="userEmail", type="email", debounce=True),

    # now get from moodle user email
    html.Button('Proceed to program and course',
                id='emailConfirm-btn', n_clicks=0),
    # html.A(html.Button('View/Edit content'),href="{}/{}-lrm".format(serverURL,appPrefixname)),
    html.A(html.Button('Home'), href="{}/teal-lrm/".format(serverURL)),

    html.Br(),
    html.Div(id='contentAfterEmail-output'),

    # Footer=============
    html.Hr(),

    dcc.Loading(id="loading-1", type="dot", fullscreen=True,
                children=html.Div(id="loading-output-1",
                                  style={'display': 'none'})
                ),
    dcc.Loading(id="loading-2", type="dot", fullscreen=True,
                children=html.Div(id="loading-output-2",
                                  style={'display': 'none'})
                ),
    dcc.Loading(id="loading-3", type="dot", fullscreen=True,
                children=html.Div(id="loading-output-3",
                                  style={'display': 'none'})
                ),
    dcc.Loading(id="loading-4", type="dot", fullscreen=True,
                children=html.Div(id="loading-output-4",
                                  style={'display': 'none'})
                ),
    dcc.Loading(id="loading-5", type="dot", fullscreen=True,
                children=html.Div(id="loading-output-5",
                                  style={'display': 'none'})
                ),
    dcc.Loading(id="loading-6", type="dot", fullscreen=True,
                children=html.Div(id="loading-output-6",
                                  style={'display': 'none'})
                ),
    dcc.Loading(id="loading-7", type="dot", fullscreen=True,
                children=html.Div(id="loading-output-7",
                                  style={'display': 'none'})
                ),
    dcc.Loading(id="loading-8", type="dot", fullscreen=True,
                children=html.Div(id="loading-output-8",
                                  style={'display': 'none'})
                ),
    dcc.Loading(id="loading-9", type="dot", fullscreen=True,
                children=html.Div(id="loading-output-9",
                                  style={'display': 'none'})
                ),


    dcc.Store(id='store_propsedCourse'),
    dcc.Store(id='store_FilteredColumnsfromTablePDF'),
    dcc.Store(id='store_FilteredColumnsfromTablePDF_CSV'),
    dcc.Store(id='store_email_list'),
    dcc.Store(id='store_uploadedCSVPDF'),
    dcc.Store(id='store_uploadedCSVPDFInsertRecords'),
    dcc.Store(id='store_uploadedCSVPDFDeleteRecords'),
    dcc.Store(id='store_CSVmodeBulkcourseactions'),
    dcc.Store(id='store_CSVmodeBulkUserCreate'),
    dcc.Store(id='store_courseCodes'),
    dcc.Store(id='store_moduleNameUrlList'),
    dcc.Store(id='store_secnHVPModules'),
    dcc.Store(id='store_githubPullModDict'),

    # user emailed passed here from moodle
    dcc.Store(id='session1Type', storage_type='local'),




], style={'margin': '10px'})


# Enter email and press continue - show section navgation radio buttons
@app.callback(
    Output('contentAfterEmail-output', 'children'),
    Output('institute_logo-output', 'children'),
    Input('emailConfirm-btn', 'n_clicks'),
    # State('userEmail','value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, userEmail):
    try:
        valid_email = check_email(userEmail)
    except:
        return html.P('User not logged in!'), html.Div([])

    if (valid_email == True):
        msg = 'User: '+userEmail

        institute_logo_src = 'assets/{}.png'.format(userEmail.split("@")[-1])

        radio1Style = {'background-color': '#FFE5B4', 'color': 'black', 'font-size': 15,
                       'border': '2px solid #21b3db', 'border-radius': '10px', 'margin': '10px', 'padding': '10px'}

        radio2Style = {'background-color': '#D5F5E3', 'color': 'black', 'font-size': 15,
                       'border': '2px solid #21b3db', 'border-radius': '10px', 'margin': '10px', 'padding': '10px'}

        radio3Style = {'background-color': '#C9F0FF', 'color': 'black', 'font-size': 15,
                       'border': '2px solid #21b3db', 'border-radius': '10px', 'margin': '10px', 'padding': '10px'}

        radio4Style = {'background-color': '#E6E6FA', 'color': 'black', 'font-size': 15,
                       'border': '2px solid #21b3db', 'border-radius': '10px', 'margin': '10px', 'padding': '10px'}

        radio5Style = {'background-color': '#FFE5ED', 'color': 'black', 'font-size': 15,
                       'border': '2px solid #21b3db', 'border-radius': '10px', 'margin': '10px', 'padding': '10px'}

        div = html.Div([
            html.P(msg),
            # html.P(institute),

            html.Div([
                # dcc.RadioItems(
                # #External program mapping temporary removed
                # ['View Program Structure','View Courses' ,'Create/Edit Courses','ILO to PO Mapping','Create/Update Classrooms','Admin'], 'View Program Structure',
                # #hidden classroom radio button 07 Feb 2023 Enabled again 28 Mar 2023
                # # ['View Program Structure','View Courses' ,'Create/Edit Courses','ILO to PO Mapping','Admin'], 'View Program Structure',
                # inline=True,
                # id='radio-items'),

                dcc.RadioItems([
                    {"label": html.Div([
                        html.P('View Program'),
                        html.P('Structure'),
                    ], style=radio1Style),
                        "value": "View Program Structure"},

                    {"label": html.Div([
                        html.P('View'),
                        html.P('Courses'),
                    ], style=radio2Style),
                        "value": "View Courses"},

                    {"label": html.Div([
                        html.P('Create/Edit'),
                        html.P('Courses'),
                    ], style=radio2Style),
                        "value": "Create/Edit Courses"},

                    {"label": html.Div([
                        html.P('Change'),
                        html.P('course code'),
                    ], style=radio2Style),
                        "value": 'Change course code'},


                    {"label": html.Div([
                        html.P('Change'),
                        html.P('course name'),
                    ], style=radio2Style),
                        "value": 'Change course name'},


                    {"label": html.Div([
                        html.P('Add course'),
                        html.P('to program'),
                    ], style=radio3Style),
                        "value": 'Add course to program'},

                    {"label": html.Div([
                        html.P('Delete course'),
                        html.P('from program'),
                    ], style=radio3Style),
                        "value": 'Delete course from program'},

                    {"label": html.Div([
                        html.P('Edit'),
                        html.P('delivery plan'),
                    ], style=radio3Style),
                        "value": 'Edit delivery plan'},

                    {"label": html.Div([
                        html.P('ILO to PO'),
                        html.P('Mapping'),
                    ], style=radio3Style),
                        "value": 'ILO to PO Mapping'},

                    {"label": html.Div([
                        html.P('Create/Update'),
                        html.P('Classrooms'),
                    ], style=radio4Style),
                        "value": 'Create/Update Classrooms'},

                    {"label": html.Div([
                        html.P('Admin'),
                        html.P('Panel'),
                    ], style=radio5Style),
                        "value": 'Admin'},


                ], value='View Program Structure',
                    inline=True,
                    id='radio-items'),

            ], style={'text-align': 'center'}),
            html.Br(),
            html.Div(id='after-pick radiobtn-output')
        ]),

        div2 = html.Div([
            html.Img(src=institute_logo_src, style={
                     'height': '50%', 'width': '50%'}),
        ])
    else:
        div = html.P('Invalid user!')
        div2 = html.Div([])

    return div, div2

# user selects radio button - show relevant section


@app.callback(
    Output('after-pick radiobtn-output', 'children'),
    Input('radio-items', 'value'),
    State('session1Type', 'data')
    # prevent_initial_call=True,
)
def func(value, userEmail):
    if (value == 'View Program Structure'):
        # programList=pd.read_sql('SELECT program_code FROM program',engineCourseApp)['program_code'].to_list()
        # programList.sort()

        # added 13 Aug 2022
        programListPDF = pd.read_sql(
            'SELECT program_code, program_name FROM program WHERE program_active=1', engineCourseApp)
        programListPDF.to_dict(orient='records')
        programListMenu = [
            tmp['program_code']+' ('+tmp['program_name']+')' for tmp in programListPDF.to_dict(orient='records')]

        div = html.Div([
            # Section1 - program structure view/creation
            # User input - drop down menu

            html.H4([
                    html.H4("Program Structure view", style={
                            "font-weight": "bold", "display": "inline"}),
                    UI_toolTipIcon("programStructureview"),
                    html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                           href="https://youtu.be/o7BKxGM4nIU", target='_blank', style={"text-decoration": "none"}),
                    ], style={'textAlign': 'center'}),

            UI_toolTip("programStructureview",
                       "Use this section to view program structure information."),


            html.P('Pick the program'),
            html.Div([
                html.Div([
                    UI_dropdown('selectedProgram', programListMenu),
                ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'}),

                html.Div([
                    html.Button('Display program',
                                id='display-program-btn', n_clicks=0),
                ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            ]),


            html.Div(id='display-program-output'),

        ]),

    elif (value == 'View Courses'):
        div = html.Div([

            html.H4([
                html.H4("View Courses", style={
                        "font-weight": "bold", "display": "inline"}),
                UI_toolTipIcon("viewCourses"),
                html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                       href="https://youtu.be/7rZWKTt0k0o", target='_blank', style={"text-decoration": "none"}),
            ], style={'textAlign': 'center'}),

            UI_toolTip("viewCourses", "Use this section to view all the courses arranged according to the CAH3 classification. If you want to search for a course, go to 'All courses' > 'Course search'. Also you can use advanced search options in the 'Create/Edit Courses' section."),


            html.Div(id="output-create-content", children=html.Iframe(id="myframe1",
                     src='{}/{}_course'.format(serverURL, appPrefixname), style={"height": "1067px", "width": "100%"})),

        ])

    elif (value == 'Create/Edit Courses'):
        # courseSummaryPDF=pd.read_sql('SELECT * FROM course',engineCourseApp)
        # userCourseListPDF=pd.read_sql('SELECT * FROM course WHERE course_updated_by="{}"'.format(userEmail),engineCourseApp)
        # userCourseList=userCourseListPDF['course_code'].to_list()
        programDomains = list(set(pd.read_sql(
            'SELECT Domain From HECoS_CAH', engineCourseApp)['Domain'].to_list()))
        programDomains.sort()

        if userEmail != "":  # only allow if username is not empty
            # adminEmails = are coming from static globals.
            if userEmail not in adminEmails:  # normal user
                # userCourseListPDF=pd.read_sql('SELECT * FROM course WHERE course_updated_by="{}"'.format(userEmail),engineCourseApp)
                userCourseListPDF = pd.read_sql('SELECT * FROM course WHERE course_updated_by LIKE "%{}%"'.format(
                    userEmail), engineCourseApp)  # multiple users added
                userCourseList = userCourseListPDF['course_code'].str.cat(
                    ['-'+zz for zz in userCourseListPDF['course_name'].to_list()])
            else:  # admin user
                userCourseListPDF = pd.read_sql(
                    'SELECT * FROM course', engineCourseApp)
                userCourseList = userCourseListPDF['course_code'].str.cat(
                    ['-'+zz for zz in userCourseListPDF['course_name'].to_list()])
        else:
            userCourseList = []

        div = html.Div([

            html.H4([
                html.H4("Create/Edit Courses",
                        style={"font-weight": "bold", "display": "inline"}),
                UI_toolTipIcon("createEditCourses"),
            ], style={'textAlign': 'center'}),

            UI_toolTip("createEditCourses",
                       "Use this section to create and edit courses."),




            # Search box
            html.Div([
                html.Div([

                    html.H5([
                        html.H5("Search for course", style={
                                "font-weight": "bold", "display": "inline"}),
                        UI_toolTipIcon("searchForCourse"),
                        html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                               href="https://youtu.be/ejrYrpOzgg8", target='_blank', style={"text-decoration": "none"}),
                    ], style={'textAlign': 'center'}),
                    UI_toolTip(
                        "searchForCourse", "Use this section to search and view course information. Use provided different search modes to perform an advanced search."),

                    html.P('Please select search mode', style={
                           'textAlign': 'left', 'font-weight': 'bold'}),
                    UI_dropdown('courseSearchMode',
                                searchModes, {'width': '50%'}),
                    html.Div(id='search-options'),
                ], style={'margin': '10px'}),
            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px'}),

            html.Hr(),

            # Update box
            html.Div([
                html.Div([
                    html.A(id="CCtop"),

                    # html.H5(children='Update course',style={'textAlign': 'center','font-weight': 'bold'}),

                    html.H5([
                        html.H5("Update course", style={
                                "font-weight": "bold", "display": "inline"}),
                        UI_toolTipIcon("updateCourseMain"),
                        html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                               href="https://youtu.be/XxuZ2Uo2TUI", target='_blank', style={"text-decoration": "none"}),
                    ], style={'textAlign': 'center'}),

                    UI_toolTip(
                        "updateCourseMain", "Use this section to edit/update the existing course information for the courses where you're the author."),


                    html.P('Select course to update', style={
                           'textAlign': 'left', 'font-weight': 'bold'}),

                    UI_dropdown('course_code', userCourseList,
                                {'width': '60%'}),

                    html.Button(
                        'Proceed', id='after_select_course_to_update-btn', n_clicks=0),
                    html.Div(id='after_select_course_to_update-output'),


                ], style={'margin': '10px'}),
            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px'}),

            html.Hr(),

            # Create box
            html.Div([
                html.Div([

                     html.Div([
                         # html.H5(children='Create course',style={'textAlign': 'center','font-weight': 'bold'}),

                         html.H5([
                             html.H5("Create course", style={
                                 "font-weight": "bold", "display": "inline"}),
                             UI_toolTipIcon("createCourseMain"),
                             html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                                    href="https://youtu.be/ymEaHx4YUJs", target='_blank', style={"text-decoration": "none"}),
                         ], style={'textAlign': 'center'}),

                         UI_toolTip("createCourseMain",
                                    "Use this section to create a new course."),


                         html.Div([
                             html.P('Enter course code to create', style={
                                 'textAlign': 'left', 'font-weight': 'bold'}),
                             dcc.Input(id="newCourseCodeCreate",
                                       type="text", value=""),
                             html.P('Enter course name to create', style={
                                 'textAlign': 'left', 'font-weight': 'bold'}),
                             dcc.Input(id="newCourseNameCreate", type="text"),

                         ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),

                         html.Div([
                             html.Div([
                                 html.Br(),
                                 html.P(
                                     "Course code should not contain any special characters or spaces."),
                                 html.P("Only allowed A-Z, a-z, 0-9."),
                                 # html.Div('Example course code: ',style={'display': 'inline-block'}),
                                 # html.Strong('CAH3'),
                                 # html.Div('abcd',style={'display': 'inline-block'}),
                                 # html.Strong('CR'),
                                 # html.Div('n',style={'display': 'inline-block'}),
                                 # html.Strong('X'),
                                 # html.Div('pqrs',style={'display': 'inline-block'}),
                                 # CAH3 abcd CRnXpqrs
                             ], style={'display': 'inline-block', 'verticalAlign': 'top', 'color': 'red'}),

                             # html.Ul([
                             #     html.Li('abcd=CAH3 classification number'),
                             #     html.Li('n=number of credits'),
                             #     html.Li('pqrs=four random integers'),
                             # ])
                         ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                     ]),







                     html.P('Select classification', style={
                            'textAlign': 'left', 'font-weight': 'bold'}),
                     div_skillSelectionCourseCreation(programDomains, '', 2),

                     html.Button(
                         'Create', id='after_select_course_to_create-btn', n_clicks=0),
                     html.Div(id='after_select_course_to_create-output'),


                     ], style={'margin': '10px'}),
            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px'}),


            # course creation new 20 Dec 2022
        ], style={'margin': '10px'}),

    elif (value == 'ILO to PO Mapping'):
        if userEmail != "":
            # adminEmails = are coming from static globals.
            if userEmail not in adminEmails:  # normal user #added 04 May 2023
                programListPDF = pd.read_sql(
                    'SELECT program_code, program_name FROM program WHERE program_active=1 AND program_lead LIKE "%{}%"'.format(userEmail), engineCourseApp)
                programListPDF.to_dict(orient='records')
                programListMenu = [
                    tmp['program_code']+' ('+tmp['program_name']+')' for tmp in programListPDF.to_dict(orient='records')]
            else:  # faculty head/admin user
                # added 13 Aug 2022
                programListPDF = pd.read_sql(
                    'SELECT program_code, program_name FROM program WHERE program_active=1', engineCourseApp)
                programListPDF.to_dict(orient='records')
                programListMenu = [
                    tmp['program_code']+' ('+tmp['program_name']+')' for tmp in programListPDF.to_dict(orient='records')]
        else:
            programListMenu = []

        programListMenu.sort()

        div = html.Div([
            # html.H5('ILO to PO Mapping',style={'font-weight': 'bold','textAlign':'center'}),

            html.H5([
                html.H5("ILO to PO Mapping", style={
                        "font-weight": "bold", "display": "inline"}),
                UI_toolTipIcon("IloToPoMapping"),
                html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                       href="https://youtu.be/LE-0FrTF9sY", target='_blank', style={"text-decoration": "none"}),
            ], style={'textAlign': 'center'}),

            UI_toolTip("IloToPoMapping", "Use this section to map the course Intended Learning Outcomes (ILOs) to the Program Outcomes (POs). Only the program lead is allowed to do the mapping."),



            html.P('Pick the program'),
            html.Div([
                html.Div([
                    UI_dropdown(
                        'selectedProgram_ILOtoPOmapping', programListMenu),
                ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}),

                html.Div([
                    html.Button(
                        'Proceed', id='selectProgram_ILOtoPOmapping-btn', n_clicks=0),
                ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            ]),


            html.Div(id='selectProgram_ILOtoPOmapping-output'),

        ]),

    elif (value == 'Create/Update Classrooms'):
        programDomains = list(set(pd.read_sql(
            'SELECT Domain From HECoS_CAH', engineCourseApp)['Domain'].to_list()))
        programDomains.sort()
    # Create classroom box
        div = html.Div([

            html.Div([

                html.Div([

                    # html.H5(children='Create classroom',style={'textAlign': 'center','font-weight': 'bold'}),

                    html.H5([
                        html.H5("Create classroom", style={
                                "font-weight": "bold", "display": "inline"}),
                        UI_toolTipIcon("createClassroomMain"),
                        html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                               href="https://youtu.be/ZqtljqGH4l4", target='_blank', style={"text-decoration": "none"}),
                    ], style={'textAlign': 'center'}),

                    UI_toolTip("createClassroomMain", "With this section you can create a classroom for a course you have already created. This classroom will be created inside your institute classroom LMS (If implemented)."),



                    html.P('Select classification', style={
                           'textAlign': 'left', 'font-weight': 'bold'}),
                    div_skillSelectionCourseCreation(programDomains, '', 3),

                    html.Button(
                        'Proceed', id='after_select_classificationClassroom-btn', n_clicks=0),
                    html.Div(id='after_select_classificationClassroom-output'),


                ], style={'margin': '10px'}),

            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px'}),


            html.Br(),
            html.Br(),



            # Add content block

            html.Div([

                html.Div([

                    # html.H5(children='Choose content to add',style={'textAlign': 'center','font-weight': 'bold'}),

                    html.H5([
                        html.H5("Choose content to add", style={
                                "font-weight": "bold", "display": "inline"}),
                        UI_toolTipIcon("chooseContenttoAdd"),
                        html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                               href="https://youtu.be/jttClGchSuE", target='_blank', style={"text-decoration": "none"}),
                    ], style={'textAlign': 'center'}),

                    UI_toolTip(
                        "chooseContenttoAdd", "Use this section to copy the created content to the classrooms. Please note currently only some content types are supported."),



                    html.P('Select classification', style={
                           'textAlign': 'left', 'font-weight': 'bold'}),
                    div_skillSelectionCourseCreation(programDomains, '', 4),

                    html.Button(
                        'Proceed', id='after_select_classificationAddContent-btn', n_clicks=0),
                    html.Div(id='after_select_classificationAddContent-output'),


                ], style={'margin': '10px'}),

            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px'}),


        ]),

    elif (value == 'Admin'):
        div = html.Div([
            html.H3('Admin use only', style={
                    'font-weight': 'bold', 'textAlign': 'center'}),
            html.P('Please login to continue', style={'textAlign': 'left'}),
            dcc.Input(id="passwordText", type="password",
                      placeholder="Password", debounce=True),
            html.Button('Login', id='password-btn', n_clicks=0),
            html.Div(id='afterpasswordDiv'),
        ]),

    elif (value == 'External Program Mapping'):
        # programListPDF=pd.read_sql('SELECT program_code FROM external_program_mapping',engineCourseApp)
        # extProgramCodeList=list(set(programListPDF['program_code'].to_list()))

        # Note : to be solved when more external programs are added

        programListPDF = pd.read_sql(
            'SELECT program_code, program_name FROM program WHERE program_active=1 AND program_code IN ("{}")'.format('TEAL'), engineCourseApp)
        programListPDF.to_dict(orient='records')
        programListMenu = [
            tmp['program_code']+' ('+tmp['program_name']+')' for tmp in programListPDF.to_dict(orient='records')]

        div = html.Div([
            html.H4('External Program Mapping', style={
                    'font-weight': 'bold', 'textAlign': 'center'}),
            html.P('Pick the program'),
            html.Div([
                html.Div([
                    UI_dropdown('selectedProgramExt', programListMenu),
                ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top'}),

                html.Div([
                    html.Button('Display program',
                                id='display-ext-program-btn', n_clicks=0),
                ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            ]),


            html.Div(id='display-ext-program-output'),
        ]),

    elif (value == 'Change course code'):

        if userEmail != "":
            if userEmail not in adminEmails:  # normal user
                # userCourseListPDF=pd.read_sql('SELECT * FROM course WHERE course_updated_by LIKE "%{}%"'.format(userEmail),engineCourseApp)#multiple users added
                loadedCourseList = pd.read_sql('SELECT course_code FROM course WHERE course_updated_by LIKE "%{}%"'.format(
                    userEmail), engineCourseApp)['course_code'].dropna().to_list()  # multiple users added
            else:  # admin user
                loadedCourseList = pd.read_sql('SELECT course_code FROM course', engineCourseApp)[
                    'course_code'].dropna().to_list()
        else:
            loadedCourseList = []

        loadedCourseList.sort()
        div = section1Div_change_course_code(loadedCourseList)
    elif (value == 'Change course name'):
        if userEmail != "":

            if userEmail not in adminEmails:  # normal user
                loadedCourseList = pd.read_sql('SELECT course_code FROM course WHERE course_updated_by LIKE "%{}%"'.format(
                    userEmail), engineCourseApp)['course_code'].dropna().to_list()  # multiple users added
            else:  # admin user
                loadedCourseList = pd.read_sql('SELECT course_code FROM course', engineCourseApp)[
                    'course_code'].dropna().to_list()
        else:
            loadedCourseList = []

        loadedCourseList.sort()
        div = section2Div_change_course_name(loadedCourseList)

    elif (value == 'Delete course from program'):
        if userEmail != "":

            if userEmail not in adminEmails:  # normal user
                programList = pd.read_sql('SELECT program_code FROM program WHERE program_active=1 AND program_lead LIKE "%{}%"'.format(
                    userEmail), engineCourseApp)['program_code'].dropna().to_list()  # multiple users added

            else:  # admin user
                programList = pd.read_sql('SELECT program_code FROM program WHERE program_active=1', engineCourseApp)[
                    'program_code'].to_list()
        else:
            programList = []

        programList.sort()

        div = section3Div_delete_course_from_program(programList)

    elif (value == 'Add course to program'):
        if userEmail != "":

            if userEmail not in adminEmails:  # normal user
                programList = pd.read_sql('SELECT program_code FROM program WHERE program_active=1 AND program_lead LIKE "%{}%"'.format(
                    userEmail), engineCourseApp)['program_code'].dropna().to_list()  # multiple users added

            else:  # admin user
                programList = pd.read_sql('SELECT program_code FROM program WHERE program_active=1', engineCourseApp)[
                    'program_code'].to_list()
        else:
            programList = []

        programList.sort()

        div = html.Div([
            # html.H5('Add Course to a program',style={'font-weight': 'bold'}),

            html.H5([
                html.H5("Add course to a program", style={
                        "font-weight": "bold", "display": "inline"}),
                    UI_toolTipIcon("addCourse2aProgram"),
                    html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                           href="https://youtu.be/PDrmLs_cWBw", target='_blank', style={"text-decoration": "none"}),
                    ], style={'textAlign': 'center'}),

            UI_toolTip("addCourse2aProgram",
                       "Use this section to add courses to the programs where you're the program lead."),


            html.P('Pick program'),
            UI_dropdown('program_addCourse', programList,
                        {'width': '50%'}, None),
            html.Button(
                'Proceed', id='proceed_after_programSelect_addCourse-btn', n_clicks=0),
            html.Div(id='proceed_after_programSelect_addCourse-output'),
        ])
    elif (value == 'Edit delivery plan'):
        if userEmail != "":

            if userEmail not in adminEmails:  # normal user
                programList = pd.read_sql('SELECT program_code FROM program WHERE program_active=1 AND program_lead LIKE "%{}%"'.format(
                    userEmail), engineCourseApp)['program_code'].dropna().to_list()  # multiple users added

            else:  # admin user
                programList = pd.read_sql('SELECT program_code FROM program WHERE program_active=1', engineCourseApp)[
                    'program_code'].to_list()
        else:
            programList = []
        programList.sort()

        div = html.Div([
            # html.H5('Edit delivery plan',style={'font-weight': 'bold'}),

            html.H5([
                html.H5("Edit delivery plan", style={
                        "font-weight": "bold", "display": "inline"}),
                UI_toolTipIcon("editDeliveryPlan"),
                html.A(html.Sup(html.H5("▶️", style={"font-weight": "bold", "display": "inline", "color": "blue"})),
                       href="https://youtu.be/xwXA4LgdtF0", target='_blank', style={"text-decoration": "none"}),
            ], style={'textAlign': 'center'}),

            UI_toolTip(
                "editDeliveryPlan", "Use this section to edit the course delivery plan for the programs where you're the program lead."),



            html.P('Pick program'),
            UI_dropdown('program_editDeliveryplan',
                        programList, {'width': '50%'}),
            html.Button(
                'Proceed', id='proceed_program_select_deliveryplan-btn', n_clicks=0),
            html.Div(id='proceed_program_select_deliveryplan-output'),
        ])

    return div

# all other callbacks=======

# 1 Program Structure - User clicks display program button


@app.callback(
    Output('display-program-output', 'children'),
    Input('display-program-btn', 'n_clicks'),
    State('selectedProgram', 'value'),
    prevent_initial_call=True,)
def func(n_clicks, selectedProgram):
    if (n_clicks != 0 and selectedProgram != None):

        selectedProgram = selectedProgram.split(' (')[0]
        [selectedProgramCreditDistFig, figProgramDeliveryPlan, selectedPrgCourseInfoTables, selectedProgramStructurePDF] = get_program_data(
            engineCourseApp, mgDB, 'program_structure', 'semester_label', 'course_type_color_map', 'course_types', selectedProgram)  # New 30/06/2022
        selectedProgramCreditDistFig = dcc.Graph(
            figure=selectedProgramCreditDistFig, config={'displaylogo': False})
        figProgramDeliveryPlan = dcc.Graph(
            figure=figProgramDeliveryPlan, config={'displaylogo': False})

        # print table1 -
        crstyp = [*selectedPrgCourseInfoTables][0]
        selectedProgramIC_label = (
            crstyp+' courses - total credits = '+selectedPrgCourseInfoTables[crstyp]['total_credits'])
        selectedProgramIC_PDF = selectedPrgCourseInfoTables[crstyp]['course_information'][[
            'course_code',	'course_name',		'course_credits', 'program_course_pre_requisites',	'program_course_semester',	'program_structure_updated_on',	'program_structure_updated_by']]

        # print table2
        crstyp = [*selectedPrgCourseInfoTables][1]
        selectedProgramSC_label = (
            crstyp+' courses - total credits = '+selectedPrgCourseInfoTables[crstyp]['total_credits'])
        selectedProgramSC_PDF = selectedPrgCourseInfoTables[crstyp]['course_information'][[
            'course_code',	'course_name',		'course_credits', 'program_course_pre_requisites',	'program_course_semester',	'program_structure_updated_on',	'program_structure_updated_by']]

        # print table3
        crstyp = [*selectedPrgCourseInfoTables][2]
        selectedProgramPC_label = (
            crstyp+' courses - total credits = '+selectedPrgCourseInfoTables[crstyp]['total_credits'])
        selectedProgramPC_PDF = selectedPrgCourseInfoTables[crstyp]['course_information'][[
            'course_code',	'course_name',		'course_credits', 'program_course_pre_requisites',	'program_course_semester',	'program_structure_updated_on',	'program_structure_updated_by']]

        # print table4
        crstyp = [*selectedPrgCourseInfoTables][3]
        selectedProgramPE_label = (
            crstyp+' courses - total credits = '+selectedPrgCourseInfoTables[crstyp]['total_credits'])
        selectedProgramPE_PDF = selectedPrgCourseInfoTables[crstyp]['course_information'][[
            'course_code',	'course_name',		'course_credits', 'program_course_pre_requisites',	'program_course_semester',	'program_structure_updated_on',	'program_structure_updated_by']]

        # Show and allow download program course list
        programCoursesList = pd.read_sql('SELECT course_code FROM program_structure WHERE program_code="{}"'.format(
            selectedProgram), engineCourseApp)['course_code'].to_list()
        sqlQ = 'SELECT * FROM course WHERE course_code IN ({})'.format(
            '", "'.join(['"']+programCoursesList+['"']))
        programCoursesPDF = pd.read_sql(
            sqlQ, engineCourseApp).drop(columns='course_id')

        # added 13 Aug 2022
        programListPDF = pd.read_sql(
            'SELECT program_code, program_name FROM program WHERE program_active=1', engineCourseApp)
        programListPDF.to_dict(orient='records')
        programListMenu = [
            tmp['program_code']+' ('+tmp['program_name']+')' for tmp in programListPDF.to_dict(orient='records')]

        # added on 22 Aug 2022
        programInfo = pd.read_sql('SELECT PO1,PO2,PO3,PO4,PO5,PO6,PO7,PO8,PO9,PO10,PO11,PO12,PO13,PO14,PO15 FROM program WHERE program_code="{}" AND program_active="{}"'.format(
            selectedProgram, 1), engineCourseApp)
        POsdict = programInfo.to_dict(orient='records')[0]
        nonEmptyPOsdict = {PO: POsdict[PO]
                           for PO in [*POsdict] if POsdict[PO] != ''}
        nonEmptyPOsPDF = pd.DataFrame(nonEmptyPOsdict, index=[0])

        dbfig = program_PO_depth_breadth_graph(
            engineCourseApp, selectedProgram)
        dbfig = dcc.Graph(figure=dbfig, config={'displaylogo': False})

        try:
            competencyFig = program_competency_depth_breadth_graph(
                engineCourseApp, selectedProgram, 'CAH3_skill_classification', 'SOLO_level', '')  # 23/08/2022
            competencyFig = dcc.Graph(figure=competencyFig, config={
                                      'displaylogo': False})
        except:
            competencyFig = 0

        div = html.Div([
            html.Br(),
            html.P("Program credit distribution", style={
                   'fontWeight': 'bold', 'textAlign': 'center'}),
            selectedProgramCreditDistFig,
            html.Br(),
            html.Br(),
            # html.P("Program credit distribution",style={'fontWeight':'bold','textAlign':'center'}),

            html.P('Program outcomes', style={
                   'fontWeight': 'bold', 'textAlign': 'center'}),
            UI_PDFtoTable(nonEmptyPOsPDF),
            html.P('Program Depth vs Breadth Matrix', style={
                   'fontWeight': 'bold', 'textAlign': 'center'}),
            dbfig,


            html.P('Competency Depth and Breadth Map', style={
                   'fontWeight': 'bold', 'textAlign': 'center'}),
            competencyFig,

            html.Br(),
            html.Br(),
            html.P("Program delivery plan", style={
                   'fontWeight': 'bold', 'textAlign': 'center'}),
            figProgramDeliveryPlan,

            html.Hr(),
            html.P("Program structure", style={
                   'fontWeight': 'bold', 'textAlign': 'center'}),
            html.Br(),
            html.P(selectedProgramIC_label),
            UI_PDFtoTable(selectedProgramIC_PDF),
            html.Br(),
            html.P(selectedProgramSC_label),
            UI_PDFtoTable(selectedProgramSC_PDF),
            html.Br(),
            html.P(selectedProgramPC_label),
            UI_PDFtoTable(selectedProgramPC_PDF),
            html.Br(),
            html.P(selectedProgramPE_label),
            UI_PDFtoTable(selectedProgramPE_PDF),
            html.Br(),
            UI_fileDownload('program_structure_download-btn',
                            'program_structure_download-download', "Download program structure"),
            html.Br(),
            html.Br(),
            html.Hr(),
            html.P("Program course list", style={
                   'fontWeight': 'bold', 'textAlign': 'center'}),
            html.Br(),
            UI_PDFtoTable(programCoursesPDF),
            UI_fileDownload('downloadProgramwisecourselist2-btn',
                            'downloadProgramwisecourselist2-dwn', 'Download program course list')

        ])

        return div
    else:
        raise PreventUpdate


# 1 Program Structure view/creation - Download Programwise course list
@app.callback(
    Output("downloadProgramwisecourselist2-dwn", "data"),
    Input("downloadProgramwisecourselist2-btn", "n_clicks"),
    State('selectedProgram', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, selectedProgram):
    selectedProgram = selectedProgram.split(' (')[0]
    programCoursesList = pd.read_sql('SELECT course_code FROM program_structure WHERE program_code="{}"'.format(
        selectedProgram), engineCourseApp)['course_code'].to_list()
    sqlQ = 'SELECT * FROM course WHERE course_code IN ({})'.format(
        '", "'.join(['"']+programCoursesList+['"']))
    programCoursesPDF = pd.read_sql(
        sqlQ, engineCourseApp).drop(columns='course_id')

    filename = selectedProgram+'-' + \
        datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")+'.csv'

    return dcc.send_data_frame(programCoursesPDF.to_csv, filename, index=False)

# 4 Admin - login button click


@app.callback(
    Output("afterpasswordDiv", "children"),
    Input("password-btn", "n_clicks"),
    State("passwordText", "value"),
    # State('store_selectedProgramCourseList', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, passwordText):
    # passwordText='admin@2330' #auto login for testing purposes
    if (passwordText == 'admin@2330'):

        div = html.Div([
            html.Div([
                html.Div([
                    html.Br(),
                    html.Br(),
                    dcc.RadioItems(
                        # ['Change course code', 'Change course name','Delete course from program','Add course','Edit delivery plan','Insert Records (CSV upload)','Delete Records (CSV upload)','Table update (CSV upload)','Generate reports','Send email','Generate Taxonomy level'], 'Change course code',
                        # ['Change course code', 'Change course name','Add course to program','Delete course from program','Edit delivery plan','Insert Records (CSV upload)','Delete Records (CSV upload)','Table update (CSV upload)','Generate reports','Generate Taxonomy level','Bulk course actions'], 'Change course code',

                        # moved some stuff to main radio button panel 04Mar2023
                        ['Generate reports', 'Insert Records (CSV upload)', 'Delete Records (CSV upload)', 'Table update (CSV upload)',
                         'Generate Taxonomy level', 'Bulk course actions'], 'Generate reports',


                        inline=True,
                        id='radio-items-adminPanel'),

                ], style={'text-align': 'center'}),

                html.Div(id='after-admin-pick-radiobtn-output'),
            ]),




        ])

    else:
        div = html.Div([
            html.P('Invalid password!')
        ])
    return div

# 4 Admin - admin selects radio button for course modification - show relevant section default Change course code


@app.callback(
    Output('after-admin-pick-radiobtn-output', 'children'),
    Input('radio-items-adminPanel', 'value'),
    # prevent_initial_call=True,
)
def func(value):

    if (value == 'Insert Records (CSV upload)'):
        div = html.Div([

            html.Div([
                html.H5('CSV Upload to Insert Records',
                        style={'font-weight': 'bold'}),
                html.P('**Note: Insert CSV should not have updated on column'),
                UI_fileUpload('CSVmodeInsertRecords-upload'),
                html.Div(id='output-afterCSVuploadInsertRecords'),
            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px'}),


        ])

    elif (value == 'Delete Records (CSV upload)'):
        div = html.Div([
            html.Div([
                html.H5('CSV Upload to Delete Records',
                        style={'font-weight': 'bold'}),
                UI_fileUpload('CSVmodeDeleteRecords-upload'),
                html.Div(id='output-afterCSVuploadDeleteRecords'),
            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px'}),
        ])

    elif (value == 'Table update (CSV upload)'):

        div = html.Div([
            html.Div([
                html.H5('CSV Upload', style={'font-weight': 'bold'}),
                UI_fileUpload('CSVmode-upload'),
                html.Div(id='output-afterCSVupload'),
            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px'}),


        ])

    elif (value == 'Generate reports'):
        tableNamesList = ['SOLO_BLOOMS_Taxonomy', 'course', 'program', 'program_structure',
                          'course_update_history', 'program_update_history', 'program_structure_update_history']

        programList = pd.read_sql('SELECT program_code FROM program', engineCourseApp)[
            'program_code'].to_list()
        programList.sort()

        div = html.Div([
            html.Div([
                html.H5('Download Columns From Tables',
                        style={'font-weight': 'bold'}),
                html.P('Select table'),
                UI_dropdown('tableName', tableNamesList),
                html.Button('Select table', id='select_table-btn', n_clicks=0),
                html.Div(id='select_table-output'),
            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px'}),
            html.Br(),

            html.Div([
                html.H5('Download Filtered Data from Table',
                        style={'font-weight': 'bold'}),
                html.P('Select table'),
                UI_dropdown('tableName2', tableNamesList),
                html.Button('Select table',
                            id='select_table2-btn', n_clicks=0),
                html.Div(id='select_table2-output'),
            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px'}),
            html.Br(),


            html.Div([
                html.H5('Download Programwise course list',
                        style={'font-weight': 'bold'}),
                UI_dropdown('selectedProgram_programwise', programList),
                html.Button(
                    'Procced', id='select_program_programwise-btn', n_clicks=0),
                html.Div(id='select_program_programwise-output'),
            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px'}),

            html.Br(),

            html.Div([
                html.H5('Download report - SQL',
                        style={'font-weight': 'bold'}),

                # dcc.Input(id='Download_report_SQL_text',type='text'),
                dcc.Textarea(id="Download_report_SQL_text", style={
                             'width': '100%', 'height': 90}),

                html.Button('Generate reports',
                            id='Download_report_SQL-btn', n_clicks=0),
                html.Div(id='Download_report_SQL-output'),

            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px'}),




        ])

    elif (value == 'Send email'):
        tableNamesList = ['SOLO_BLOOMS_Taxonomy',
                          'course', 'program', 'program_structure']
        div = html.Div([
            html.H5('Send email', style={'font-weight': 'bold'}),

            html.Div([
                html.H5('Download Filtered Data from Table',
                        style={'font-weight': 'bold'}),
                html.P('Select table'),
                UI_dropdown('send_email_tableName2', tableNamesList),
                html.Button('Select table',
                            id='send_email_select_table2-btn', n_clicks=0),
                html.Div(id='send_email_select_table2-output'),
            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px'}),



        ])

    elif (value == 'Generate Taxonomy level'):  # 24/11/2022

        div = html.Div([
            html.H5('Generate Taxonomy level', style={'font-weight': 'bold'}),


            html.Div([
                html.P('This section is to calculate blooms/solo level. If there are any courses in course table without blooms level you can use this section to calculate and add those values. Usually blooms levels are not calculated when you do bulk updates through CSV upload option.'),
                html.P(
                    'If no blooms level found, blooms and solo levels are calculated. Need at least ILO1 filled.'),
                html.Button('Process course table',
                            id='process_course_table-btn', n_clicks=0),
                html.Div(id='process_course_table-output'),

            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px'}),



        ])

    elif (value == 'Bulk course actions'):  # 24/11/2022

        div = html.Div([


            html.H5('Bulk course actions', style={'font-weight': 'bold'}),
            html.Div([
                html.H5('CSV Upload Course List (Moved to backend)',
                        style={'font-weight': 'bold'}),
                html.P(
                    'Use the backend script to complete this task due to timeout issue.'),
                html.P(
                    "This section let's you bulk update the course information UI and version control."),
                UI_fileUpload('CSVmodeBulkcourseactions-upload'),
                html.Div(id='CSVmodeBulkcourseactions-output'),

            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px'}),

            html.Br(),
            html.Br(),

            html.Div([
                html.H5('CSV Upload User List', style={'font-weight': 'bold'}),
                html.P(
                    "This section let's you bulk create users. Headers should be username,email,firstname,lastname,password"),
                html.P("Password Policy: Password length - 8,Digits - 1, Lowercase letters - 1, Uppercase letters - 1, Non-alphanumeric characters - 1"),
                UI_fileUpload('CSVmodeBulkUserCreate-upload'),
                html.Div(id='CSVmodeBulkUserCreate-output'),

            ], style={'borderWidth': '2px', 'borderStyle': 'solid', 'borderRadius': '10px', 'padding': '20px'}),


        ])

    return div

# 3.1course code change - proceed button after pick course code clicked


@app.callback(
    Output("proceed_after_pick_course_code-output", "children"),
    Input("proceed_after_pick_course_code-btn", "n_clicks"),
    State('course2bChangedCode', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, course2bChangedCode):
    if (course2bChangedCode != None):
        courseInfoPDF = pd.read_sql('SELECT * FROM  course_update_history WHERE course_code="{}"'.format(
            course2bChangedCode), engineCourseApp).drop(columns=['course_update_history_id'])  # New 30/06/2022
        div = html.Div([
            UI_PDFtoTable(courseInfoPDF),
            html.P('Enter new course code*'),
            dcc.Input(id="newCourseCode", value="",
                      type="text", debounce=True),
            html.P('Enter new course name*'),
            dcc.Input(id="newCourseName_courseCode", value="",
                      style={'width': '100%', 'height': 50}),
            html.Button('Proceed', id='change_course_code-btn', n_clicks=0),
            html.Div(id='change_course_code-output'),
        ])
    else:
        div = html.Div([
            html.P('Please pick course code', style={'color': 'red'})
        ])

    return div

# 3.1course code change button click


@app.callback(
    Output("change_course_code-output", "children"),
    Output('loading-output-1', 'children'),
    Output("course2bChangedCode", "options"),
    Input("change_course_code-btn", "n_clicks"),
    State("course2bChangedCode", "value"),
    State("newCourseCode", "value"),
    State("newCourseName_courseCode", "value"),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, course2bChangedCode, newCourseCode, newCourseName_courseCode, userEmail):
    if (n_clicks != 0 and newCourseCode.replace(" ", "") != "" and newCourseName_courseCode.replace(" ", "") != ""):
        newCourseName = newCourseName_courseCode
        msg, createdCrsPDF = create_course_4m_old_course(
            engineCourseApp, mgDB, course2bChangedCode, newCourseCode, newCourseName, userEmail)

        loadedCourseList = pd.read_sql('SELECT course_code FROM course', engineCourseApp)[
            'course_code'].to_list()  # New 30/06/2022
        loadedCourseList.sort()
        # loadedCourseList=['a','b','c']
        options = [{'label': i, 'value': i} for i in loadedCourseList]

        div = html.Div([
            html.P(msg),
            UI_PDFtoTable(createdCrsPDF),
        ])

        return div, 1, options

    elif (n_clicks != 0):
        loadedCourseList = pd.read_sql('SELECT course_code FROM course', engineCourseApp)[
            'course_code'].to_list()  # New 30/06/2022
        loadedCourseList.sort()
        options = [{'label': i, 'value': i} for i in loadedCourseList]
        div = html.Div([
            html.P("Please complete all required fields",
                   style={'color': 'red'}),
        ])
        return div, 1, options
    else:
        raise PreventUpdate

# 3.2course name change - click proceed after course code select


@app.callback(
    Output("proceed_after_pick_course_code_Cname-output", "children"),
    Input("proceed_after_pick_course_code_Cname-btn", "n_clicks"),
    State("course2bChangedCode2", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, course2bChangedCode2):
    if (course2bChangedCode2 != None):
        tempCrsPDF = pd.read_sql('SELECT * FROM course_update_history WHERE course_code="{}"'.format(course2bChangedCode2),
                                 engineCourseApp).drop(columns=['course_update_history_id'])  

        div = html.Div([
            html.P('Course Update History'),



            UI_PDFtoTable(tempCrsPDF),

            html.P('Enter new course name*'),
            dcc.Input(id="newCourseName", value="",
                      type="text", debounce=True),
            html.P('Enter comment*'),
            dcc.Textarea(id="courseNameUpdateComment", value="",
                         style={'width': '100%', 'height': 50}),
            html.Button('Proceed', id='change_course_name-btn', n_clicks=0),
            html.Div(id='change_course_name-output'),
        ])
    else:
        div = html.Div([
            html.P('Please pick course code', style={'color': 'red'})
        ])

    return div

# 3.2change course name proceed btn click


@app.callback(
    Output("change_course_name-output", "children"),
    Output('loading-output-2', 'children'),
    Input("change_course_name-btn", "n_clicks"),
    State("course2bChangedCode2", "value"),
    State("newCourseName", "value"),
    State("courseNameUpdateComment", "value"),
    # State("userEmail", "value"),
    # now user email taken reading local variable
    State('session1Type', 'data'),

    prevent_initial_call=True,
)
def func(n_clicks, course2bChangedCode2, newCourseName, courseNameUpdateComment, userEmail):
    print(newCourseName)
    print(courseNameUpdateComment)
    if (n_clicks != 0 and newCourseName.replace(" ", "") != "" and courseNameUpdateComment.replace(" ", "") != ""):
        courseUpdateDict = {'course_name': newCourseName}
        msg, updatedCrsPDF = update_course_data(
            engineCourseApp, mgDB, course2bChangedCode2, courseUpdateDict, courseNameUpdateComment, userEmail)
        updatedCrsPDF = updatedCrsPDF.drop(columns=['course_id'])
        div = html.Div([
            html.P(msg),
            UI_PDFtoTable(updatedCrsPDF),
        ])
        return div, 1

    elif (n_clicks != 0):
        div = html.Div([
            html.P('Please complete all required fields',
                   style={'color': 'red'}),
        ])

        return div, 1
    else:
        raise PreventUpdate


# 3.3delete course - proceed click after program select
@app.callback(
    Output('proceed_after_programSelect-output', 'children'),
    Input('proceed_after_programSelect-btn', 'n_clicks'),
    State('program_deleteCourse', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, program_deleteCourse):
    if (program_deleteCourse != None):
        selectedProgram = program_deleteCourse
        courseList2Delete = pd.read_sql('SELECT course_code FROM program_structure WHERE program_code="{}"'.format(
            selectedProgram), engineCourseApp)['course_code'].to_list()
        courseList2Delete.sort()

        div = html.Div([
            html.P('Pick course code to delete'),
            UI_dropdown('course2bDeletedCode', courseList2Delete,
                        {'width': '50%'}, None),
            html.Button(
                'Proceed', id='proceed_after_ccode_selecttoDelete-btn', n_clicks=0),
            html.Div(id='proceed_after_ccode_selecttoDelete-output'),
        ])
    else:
        div = html.Div([
            html.P('Please pick a program', style={'color': 'red'}),
        ])

    return div

# 3.3delete course - click proceed after course code select


@app.callback(
    Output('proceed_after_ccode_selecttoDelete-output', 'children'),
    Input('proceed_after_ccode_selecttoDelete-btn', 'n_clicks'),
    State('program_deleteCourse', 'value'),
    State('course2bDeletedCode', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, program_deleteCourse, course2bDeletedCode):
    if (course2bDeletedCode != None and program_deleteCourse != None):
        selectedProgram = program_deleteCourse

        courseInfoPDF = pd.read_sql('SELECT * FROM course WHERE course_code="{}"'.format(
            course2bDeletedCode), engineCourseApp).drop(columns=['course_id'])

        div = html.Div([
            UI_PDFtoTable(courseInfoPDF),
            html.P('Enter comment*'),
            dcc.Textarea(id="programUpdateComment_delete", value="",
                         style={'width': '100%', 'height': 50}),
            html.Button('Delete', id='delete_course-btn', n_clicks=0),
            html.Div(id='delete_course-output'),
        ])
    else:
        div = html.Div([
            html.P('Please fill all required information',
                   style={'color': 'red'}),
        ])
    return div

# 3.3delete course - User click delete course button


@app.callback(
    Output("delete_course-output", "children"),
    Output('loading-output-3', 'children'),
    Input("delete_course-btn", "n_clicks"),
    State("course2bDeletedCode", "value"),
    State("programUpdateComment_delete", "value"),
    State("program_deleteCourse", "value"),
    # State("userEmail", "value"),
    # now user email taken reading local variable
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, course2bDeletedCode, programUpdateComment_delete, program_deleteCourse, userEmail):
    print(n_clicks)
    print("delete button activated")
    if (n_clicks != 0 and programUpdateComment_delete.replace(" ", "") != "" and course2bDeletedCode != None and program_deleteCourse != None):
        selectedProgram = program_deleteCourse
        programUpdateComment = programUpdateComment_delete
        msg = delete_course_from_program(
            engineCourseApp, mgDB, course2bDeletedCode, selectedProgram, programUpdateComment, userEmail)
        updatedPrgStrPDF = pd.read_sql(
            'SELECT * FROM program_structure WHERE program_code="{}"'.format(selectedProgram), engineCourseApp)

        div = html.Div([
            html.P(msg),
            UI_PDFtoTable(updatedPrgStrPDF),
        ])
        return div, 1

    elif (n_clicks != 0):
        div = html.Div([
            html.P('Please fill all required information',
                   style={'color': 'red'}),
        ])

        return div, 1
    else:
        raise PreventUpdate

# 3.4add course - proceed after program select button clicked


@app.callback(
    Output("proceed_after_programSelect_addCourse-output", "children"),
    Input("proceed_after_programSelect_addCourse-btn", "n_clicks"),
    State("program_addCourse", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, program_addCourse):
    if (program_addCourse != None):
        selectedProgram = program_addCourse
        courseSummaryInfoPDFdisplay = pd.read_sql(
            'SELECT * FROM program_structure WHERE program_code="{}"'.format(selectedProgram), engineCourseApp)
        courseSummaryInfoPDFdisplay = courseSummaryInfoPDFdisplay[[
            'course_code', 'program_course_semester', 'program_course_pre_requisites']]
        courseList2Add = pd.read_sql('SELECT course_code FROM course', engineCourseApp)[
            'course_code'].to_list()
        courseList2Add.sort()

        div = html.Div([
            UI_PDFtoTable(courseSummaryInfoPDFdisplay),
            html.P('Pick course code to be added'),
            UI_multidropdown_empty('course2bAddedCodes',
                                   courseList2Add, {'width': '100%'}),
            html.Button(
                'Proceed', id='proceed_course_select_addCourse-btn', n_clicks=0),
            html.Div(id='proceed_course_select_addCourse-output'),
        ])

    else:
        div = html.Div([
            html.P('Please pick program', style={'color': 'red'}),
        ])
    return div


# 3.4Course add - click proceed after course code selection from dropdown
@app.callback(
    Output('proceed_course_select_addCourse-output', 'children'),
    Input('proceed_course_select_addCourse-btn', 'n_clicks'),
    State("course2bAddedCodes", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, course2bAddedCodes):
    if (course2bAddedCodes != []):
        courseTypesList0 = [
            *pd.read_sql("SELECT * FROM course_types", engineCourseApp)]
        courseTypesList0.remove("course_types_id")

        div = html.Div([
            html.P('Pick courseType*'),
            UI_dropdown('courseType', courseTypesList0,
                        {'width': '50%'}, None),
            html.P('Enter comment'),
            dcc.Textarea(id="programUpdateComment_addCourse",
                         value="", style={'width': '100%', 'height': 50}),
            html.Button('Add course', id='add_final_course-btn', n_clicks=0),
            html.Div(id='add_course_output'),
        ])
    else:
        div = html.Div([
            html.P('Please pick at least one course code',
                   style={'color': 'red'}),
        ])

    return div

# 3.4add course -"Add course" button clicked


@app.callback(
    Output("add_course_output", "children"),
    Output('loading-output-4', 'children'),
    Input("add_final_course-btn", "n_clicks"),
    State("course2bAddedCodes", "value"),
    State("courseType", "value"),
    State("program_addCourse", "value"),
    State("programUpdateComment_addCourse", "value"),
    # State("userEmail", "value"),
    # now user email taken reading local variable
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, course2bAddedCodes, courseType, program_addCourse, programUpdateComment_addCourse, userEmail):
    if (n_clicks != 0 and courseType != None):
        selectedProgram = program_addCourse
        programUpdateComment = programUpdateComment_addCourse
        msg = ''
        print(course2bAddedCodes)
        for course2bAddedCode in course2bAddedCodes:
            print(course2bAddedCode)
            msg0, updatePrgStrPDF = add_course_to_a_program(
                engineCourseApp, mgDB, course2bAddedCode, courseType, selectedProgram, programUpdateComment, userEmail)
            updatePrgStrPDF = updatePrgStrPDF.drop(
                columns=['program_structure_id'])
            msg += msg0+', '

        div = html.Div([
            html.P(msg),
            UI_PDFtoTable(updatePrgStrPDF),
        ])
        return div, 1

    elif (n_clicks != 0):  # store element triggers event automatically
        div = html.Div([
            html.P("Please complete all required fields",
                   style={'color': 'red'}),
        ])
        return div, 1

    else:
        raise PreventUpdate

# 3.5edit delivery plan -  proceed clicked after slecting a program


@app.callback(
    Output("proceed_program_select_deliveryplan-output", "children"),
    Input("proceed_program_select_deliveryplan-btn", "n_clicks"),
    State("program_editDeliveryplan", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, selectedProgram):
    [selectedProgramCreditDistFig, figProgramDeliveryPlan, selectedPrgCourseInfoTables, selected_program_info_PDF] = get_program_data(
        engineCourseApp, mgDB, 'program_structure', 'semester_label', 'course_type_color_map', 'course_types', selectedProgram)
    semester_label_PDF = mgDB.read_table_2_PDF(
        engineCourseApp, 'semester_label')
    semsterLabelsList = semester_label_PDF.loc[semester_label_PDF.index.values[-1], :].to_list()[
        :8]
    selectedProgramCourseList = selected_program_info_PDF['course_code'].to_list(
    )

    figProgramDeliveryPlan = dcc.Graph(
        figure=figProgramDeliveryPlan, config={'displaylogo': False})

    semester_list = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']

    div = html.Div([
        html.P('Existing Program Delivery Plan'),
        html.Div(html.P('Beginner'), style={
                 'background-color': 'rgb(255, 155, 227)', 'display': 'inline-block', 'margin': '1px', 'padding': '1px'}),
        html.Div(html.P('Intermediate'), style={
                 'background-color': 'rgb(255, 255, 100)', 'display': 'inline-block', 'margin': '1px', 'padding': '1px'}),
        html.Div(html.P('Advanced'), style={
                 'background-color': 'rgb(46, 131, 255)', 'display': 'inline-block', 'margin': '1px', 'padding': '1px'}),
        html.Div(html.P('Elective'), style={
                 'background-color': 'rgb(0, 255, 162)', 'display': 'inline-block', 'margin': '1px', 'padding': '1px'}),


        figProgramDeliveryPlan,
        html.P('Pick semester to update'),
        UI_dropdown('updateSemester', semester_list, {'width': '50%'}),
        html.P('Select courses to add'),
        UI_multidropdown_empty('chosenSemesterCourses',
                               selectedProgramCourseList),
        html.P('Update comment'),
        dcc.Textarea(id="updateCommentEditDeliveryPlan",
                     style={'width': '100%', 'height': 50}),
        html.Button('Update', id='update_program_delivery-btn', n_clicks=0),
        html.Div(id='after_update_program_delivery-output'),

    ])

    return div

# 3.5edit delivery plan - user click update button


@app.callback(
    Output("after_update_program_delivery-output", "children"),
    Output('loading-output-5', 'children'),
    Input("update_program_delivery-btn", "n_clicks"),
    State("updateSemester", "value"),
    State("chosenSemesterCourses", "value"),
    State("program_editDeliveryplan", "value"),
    State("updateCommentEditDeliveryPlan", "value"),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, updateSemester, chosenSemesterCourses, selectedProgram, updateComment, userEmail):
    if (n_clicks != 0):
        dpUpdatedfig = update_delivery_plan(engineCourseApp, mgDB, 'program_structure', 'semester_label', 'course_type_color_map',
                                            'course_types', selectedProgram, chosenSemesterCourses, updateSemester, updateComment, userEmail)
        dpUpdatedfig = dcc.Graph(figure=dpUpdatedfig, config={
                                 'displaylogo': False})

        div = html.Div([
            html.P('Updated Program Delivery Plan'),
            dpUpdatedfig,

        ])

        return div, 1

    else:
        raise PreventUpdate

# 3.6.1 generate reports - user click select table button after picking table name from the dropdown


@app.callback(
    Output("select_table-output", "children"),
    Input("select_table-btn", "n_clicks"),
    State('tableName', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, tableName):
    temp000x = pd.read_sql('SELECT * FROM {}'.format(tableName),
                           engineCourseApp).drop(columns=[tableName+'_id'])
    colList = [*temp000x]
    colList.sort()

    div = html.Div([
        html.P('Pick filter columns'),
        UI_multidropdown('selectedColList', colList),
        html.Button('Show data', id='select_columns-btn', n_clicks=0),
        html.Div(id='select_columns-output'),
    ])

    return div

# 3.6.1 generate reports -user click Select filter values btn to show table and allow download


@app.callback(
    Output("select_columns-output", "children"),
    Input("select_columns-btn", "n_clicks"),
    State('tableName', 'value'),
    State('selectedColList', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, tableName, selectedColList):
    selectedTablePDF = pd.read_sql('SELECT {} FROM {}'.format(
        ', '.join(selectedColList), tableName), engineCourseApp)

    div = html.Div([
        UI_PDFtoTable(selectedTablePDF),
        UI_fileDownload('columnsfromtablesdownload-btn',
                        'columnsfromtablesdownload-dwn', 'Download data')
    ])

    return div

# 3.6.1 generate reports -Download Columns From Tables


@app.callback(
    Output("columnsfromtablesdownload-dwn", "data"),
    Input("columnsfromtablesdownload-btn", "n_clicks"),
    State('tableName', 'value'),
    State('selectedColList', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, tableName, selectedColList):
    selectedTablePDF = pd.read_sql('SELECT {} FROM {}'.format(
        ', '.join(selectedColList), tableName), engineCourseApp)
    filename = tableName+'-'+datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")+'.csv'
    return dcc.send_data_frame(selectedTablePDF.to_csv, filename, index=False)


# Insert records - new section 13 Aug 2022 - User uploads CSV
@app.callback(
    Output('output-afterCSVuploadInsertRecords', 'children'),
    Output('store_uploadedCSVPDFInsertRecords', 'data'),
    Input('CSVmodeInsertRecords-upload', 'contents'),
    State('CSVmodeInsertRecords-upload', 'filename'),
    State('CSVmodeInsertRecords-upload', 'last_modified'),
    # State('tableName2_CSV','value'),
    prevent_initial_call=True,
)
def func(contents, filename, last_modified):
    if contents is None:
        raise PreventUpdate
        div = html.Div()

    else:  # read CSV data
        updateDataPDF = parse_contents(contents, filename, last_modified)
        updateDataPDF = updateDataPDF.fillna('')
        updateCols = [*updateDataPDF]

        updateDataPDF_JSON = updateDataPDF.to_json()
        # temp000x=updateDataPDF
        # colList=[*temp000x]

        tableNamesList = ['course', 'program',
                          'program_structure', 'external_program_mapping']

        div = html.Div([
            UI_PDFtoTable(updateDataPDF),

            html.Div([

                html.P('Select table name', style={'font-weight': 'bold'}),
                UI_dropdown('tableName_CSVInsertRecords', tableNamesList),

                # html.P('Select filter column',style={'font-weight': 'bold'}),
                # UI_multidropdown_empty('selectedColList2_CSVInsertRecords',colList),
                html.P('Enter update comment'),
                dcc.Textarea(
                    id='CSV_updateCommentInsertRecords',
                    value='Updated by academic affairs',
                    style={'width': '100%', 'height': 50},
                ),
                html.Br(),
                html.Button(
                    'Add data', id='finalize_csv_dataInsertRecords-btn', n_clicks=0),
                html.Div(id='finalize_csv_dataInsertRecords-output'),
            ]),

        ])

        return div, updateDataPDF_JSON


# Insert records - new section 13 Aug 2022 - add data to table once user click add data
'''
**Note: Insert CSV should not have updated on column
'''


@app.callback(
    Output("finalize_csv_dataInsertRecords-output", "children"),
    Input("finalize_csv_dataInsertRecords-btn", "n_clicks"),
    State("store_uploadedCSVPDFInsertRecords", 'data'),
    State("CSV_updateCommentInsertRecords", 'value'),
    State('tableName_CSVInsertRecords', 'value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, store_uploadedCSVPDFInsertRecords, CSV_updateCommentInsertRecords, tableName_CSVInsertRecords, userEmail):
    if (n_clicks != 0):
        updateDataPDF = pd.read_json(store_uploadedCSVPDFInsertRecords)
        updateDataPDF = updateDataPDF.fillna('')
        updateComment = CSV_updateCommentInsertRecords
        tableName = tableName_CSVInsertRecords

        updateCols = [*updateDataPDF]
        tableCols = [
            *pd.read_sql('SELECT * FROM {}'.format(tableName), engineCourseApp)]
        misMatchList = list(set(updateCols).difference(set(tableCols)))

        if len(misMatchList) != 0:
            msg = 'Update table {} columns do not contain the columns: {}'.format(
                tableName, ', '.join(misMatchList))
            div = html.Div([
                html.P(msg)
            ])

        else:
            # msg=update_table(engineCourseApp,mgDB,tableName,selectedColList,updateDataPDF,updateComment,userEmail)
            msg1, msg2 = insert_records(
                engineCourseApp, mgDB, tableName, updateDataPDF, updateComment, userEmail)
            div = html.Div([
                html.P(msg1),
                html.P(msg2),
            ])

    else:
        raise PreventUpdate

    return div

# Delete records - new section 14 Aug 2022 - user uploads CSV


@app.callback(
    Output('output-afterCSVuploadDeleteRecords', 'children'),
    Output('store_uploadedCSVPDFDeleteRecords', 'data'),
    Input('CSVmodeDeleteRecords-upload', 'contents'),
    State('CSVmodeDeleteRecords-upload', 'filename'),
    State('CSVmodeDeleteRecords-upload', 'last_modified'),
    # State('tableName2_CSV','value'),
    prevent_initial_call=True,
)
def func(contents, filename, last_modified):
    if contents is None:
        raise PreventUpdate
        div = html.Div()

    else:  # read CSV data
        updateDataPDF = parse_contents(contents, filename, last_modified)
        updateDataPDF = updateDataPDF.fillna('')
        updateCols = [*updateDataPDF]

        updateDataPDF_JSON = updateDataPDF.to_json()
        temp000x = updateDataPDF
        colList = [*temp000x]

        tableNamesList = ['course', 'program', 'program_structure']

        div = html.Div([
            UI_PDFtoTable(updateDataPDF),

            html.Div([

                html.P('Select table name', style={'font-weight': 'bold'}),
                UI_dropdown('tableName_CSVDeleteRecords', tableNamesList),

                html.P('Select filter column', style={'font-weight': 'bold'}),
                UI_multidropdown_empty(
                    'selectedColList2_CSVDeleteRecords', colList),
                html.P('Enter update comment'),
                dcc.Textarea(
                    id='CSV_updateCommentDeleteRecords',
                    value='Updated by academic affairs',
                    style={'width': '100%', 'height': 50},
                ),
                html.Br(),
                html.Button('Delete data', id='finalize_csv_dataDeleteRecords-btn',
                            n_clicks=0, style={'color': 'red'}),
                html.Div(id='finalize_csv_dataDeleteRecords-output'),
            ]),

        ])

        return div, updateDataPDF_JSON

# Delete records - new section 14 Aug 2022 - user click button to delete data


@app.callback(
    Output("finalize_csv_dataDeleteRecords-output", "children"),
    Input("finalize_csv_dataDeleteRecords-btn", "n_clicks"),
    State("store_uploadedCSVPDFDeleteRecords", 'data'),
    State("CSV_updateCommentDeleteRecords", 'value'),
    State('selectedColList2_CSVDeleteRecords', 'value'),
    State('tableName_CSVDeleteRecords', 'value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, store_uploadedCSVPDFDeleteRecords, CSV_updateCommentDeleteRecords, selectedColList2_CSVDeleteRecords, tableName_CSVDeleteRecords, userEmail):
    if (n_clicks != 0):
        updateDataPDF = pd.read_json(store_uploadedCSVPDFDeleteRecords)
        updateDataPDF = updateDataPDF.fillna('')
        updateComment = CSV_updateCommentDeleteRecords
        selectedColList = selectedColList2_CSVDeleteRecords
        tableName = tableName_CSVDeleteRecords

        updateCols = [*updateDataPDF]

        tableCols = [
            *pd.read_sql('SELECT * FROM {}'.format(tableName), engineCourseApp)]
        misMatchList = list(set(updateCols).difference(set(tableCols)))

        if len(misMatchList) != 0:
            msg = 'Update table {} columns do not contain the columns: {}'.format(
                tableName, ', '.join(misMatchList))
            div = html.Div([
                html.P(msg)
            ])

        else:
            msg = delete_records(engineCourseApp, mgDB, tableName,
                                 selectedColList, updateDataPDF, updateComment, userEmail)
            div = html.Div([
                html.P(msg)
            ])

    else:
        raise PreventUpdate

    return div


# 3.6.2a - new section 7 Aug 2022 - User uploads csv
@app.callback(
    Output('output-afterCSVupload', 'children'),
    Output('store_uploadedCSVPDF', 'data'),
    Input('CSVmode-upload', 'contents'),
    State('CSVmode-upload', 'filename'),
    State('CSVmode-upload', 'last_modified'),
    # State('tableName2_CSV','value'),
    prevent_initial_call=True,
)
def func(contents, filename, last_modified):
    if contents is None:
        raise PreventUpdate
        div = html.Div()

    else:  # read CSV data
        updateDataPDF = parse_contents(contents, filename, last_modified)
        updateDataPDF = updateDataPDF.fillna('')
        updateCols = [*updateDataPDF]

        updateDataPDF_JSON = updateDataPDF.to_json()
        temp000x = updateDataPDF
        colList = [*temp000x]

        tableNamesList = ['course', 'program', 'program_structure']

        div = html.Div([
            UI_PDFtoTable(updateDataPDF),

            html.Div([

                html.P('Select table name', style={'font-weight': 'bold'}),
                UI_dropdown('tableName_CSV', tableNamesList),

                html.P('Select filter column', style={'font-weight': 'bold'}),
                UI_multidropdown_empty('selectedColList2_CSV', colList),
                html.P('Enter update comment'),
                dcc.Textarea(
                    id='CSV_updateComment',
                    value='Updated by academic affairs',
                    style={'width': '100%', 'height': 50},
                ),
                html.Br(),
                html.Button('Overwrite data', id='finalize_csv_data-btn',
                            n_clicks=0, style={'color': 'red'}),
                html.Div(id='finalize_csv_data-output'),
            ]),

        ])

        return div, updateDataPDF_JSON

# 3.6.2a - new section 7 Aug 2022 - Overwrite CSV data to database


@app.callback(
    Output("finalize_csv_data-output", "children"),
    Input("finalize_csv_data-btn", "n_clicks"),
    State("store_uploadedCSVPDF", 'data'),
    State("CSV_updateComment", 'value'),
    State('selectedColList2_CSV', 'value'),
    State('tableName_CSV', 'value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, store_uploadedCSVPDF, CSV_updateComment, selectedColList2_CSV, tableName_CSV, userEmail):
    if (n_clicks != 0):
        updateDataPDF = pd.read_json(store_uploadedCSVPDF)
        updateDataPDF = updateDataPDF.fillna('')
        updateComment = CSV_updateComment
        selectedColList = selectedColList2_CSV
        tableName = tableName_CSV

        updateCols = [*updateDataPDF]

        tableCols = [
            *pd.read_sql('SELECT * FROM {}'.format(tableName), engineCourseApp)]
        misMatchList = list(set(updateCols).difference(set(tableCols)))

        if len(misMatchList) != 0:
            msg = 'Update table {} columns do not contain the columns: {}'.format(
                tableName, ', '.join(misMatchList))
            div = html.Div([
                html.P(msg)
            ])

        else:
            msg = update_table(engineCourseApp, mgDB, tableName,
                               selectedColList, updateDataPDF, updateComment, userEmail)
            div = html.Div([
                html.P(msg)
            ])

    else:
        raise PreventUpdate

    return div

# 3.6.2 generate reports -user click select table2 button after picking table2 name from the dropdown


@app.callback(
    Output("select_table2-output", "children"),
    Input("select_table2-btn", "n_clicks"),
    State('tableName2', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, tableName2):
    temp000x = pd.read_sql('SELECT * FROM {}'.format(tableName2),
                           engineCourseApp).drop(columns=[tableName2+'_id'])
    colList = [*temp000x]

    div = html.Div([
        html.P('Pick filter columns'),
        UI_multidropdown('selectedColList2', colList),
        html.Button('Select filter values',
                    id='select_columns2-btn', n_clicks=0),
        html.Div(id='select_columns2-output'),
    ])

    return div

# 3.6.2 generate reports -user click Select filter values2 btn


@app.callback(
    Output("select_columns2-output", "children"),
    Input("select_columns2-btn", "n_clicks"),
    State('tableName2', 'value'),
    State('selectedColList2', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, tableName2, selectedColList2):
    slectedTableDataPDF = pd.read_sql('SELECT {} FROM {}'.format(
        ', '.join(selectedColList2), tableName2), engineCourseApp).fillna('')
    filterLists = {}
    for col in selectedColList2:
        filterLists[col] = list(set(slectedTableDataPDF[col].to_list()))

    temp000x = pd.read_sql('SELECT * FROM {}'.format(tableName2),
                           engineCourseApp).drop(columns=[tableName2+'_id'])
    colList = [*temp000x]

    div = html.Div([
        html.P('Enter filter values'),
        UI_table_dropdown('filtered_data_table1', filterLists),
        html.P('Select display columns'),
        UI_multidropdown('selectedColList2b', colList),
        html.Button('Get filtered data',
                    id='get_filtered_data-btn', n_clicks=0),
        html.Div(id='get_filtered_data-output'),
    ])

    return div

# 3.6.2 generate reports -User clicks get filtered data button - show table and allow download


@app.callback(
    Output("get_filtered_data-output", "children"),
    Output("store_FilteredColumnsfromTablePDF", "data"),
    Input("get_filtered_data-btn", "n_clicks"),
    State('tableName2', 'value'),
    State('filtered_data_table1', 'data'),
    State('selectedColList2b', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, tableName2, filtered_data_table1, selectedColList2b):
    if (n_clicks != 0):
        selectedDisplayColList = selectedColList2b

        selectedColList = []
        selectedFilterVals = []
        for xx in filtered_data_table1:
            selectedColList += [xx['Column_name']]
            selectedFilterVals += [xx['Value']]

        tmp00 = []
        for i, xx in enumerate(selectedColList):
            tmp00 += ['{}="{}"'.format(xx, selectedFilterVals[i])]
        sqlQ = 'SELECT {} FROM {}  WHERE {}'.format(
            ', '.join(selectedDisplayColList), tableName2, ' AND '.join(tmp00))
        filreredPDF = pd.read_sql(sqlQ, engineCourseApp)

        filreredPDF_JSON = filreredPDF.to_json()
        div = html.Div([
            UI_PDFtoTable(filreredPDF),
            UI_fileDownload('filteredcolumnsfromtablesdownload-btn',
                            'filteredcolumnsfromtablesdownload-dwn', 'Download data')
        ])

        return div, filreredPDF_JSON
    else:
        raise PreventUpdate


# 3.6.2 generate reports -Download Filtered Columns from Table
@app.callback(
    Output("filteredcolumnsfromtablesdownload-dwn", "data"),
    Input("filteredcolumnsfromtablesdownload-btn", "n_clicks"),
    State("store_FilteredColumnsfromTablePDF", "data"),
    State('tableName2', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, store_FilteredColumnsfromTablePDF, tableName):
    if (n_clicks != 0):
        filreredPDF = pd.read_json(store_FilteredColumnsfromTablePDF)
        filename = tableName+'-'+datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")+'.csv'
        return dcc.send_data_frame(filreredPDF.to_csv, filename, index=False)
    else:
        raise PreventUpdate


# 3.6.3 generate reports -user click "proceed " after selecting program in programwise course list
@app.callback(
    Output("select_program_programwise-output", "children"),
    Input("select_program_programwise-btn", "n_clicks"),
    State('selectedProgram_programwise', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, selectedProgram_programwise):
    selectedProgram = selectedProgram_programwise
    programCoursesList = pd.read_sql('SELECT course_code FROM program_structure WHERE program_code="{}"'.format(
        selectedProgram), engineCourseApp)['course_code'].to_list()
    sqlQ = 'SELECT * FROM course WHERE course_code IN ({})'.format(
        '", "'.join(['"']+programCoursesList+['"']))
    programCoursesPDF = pd.read_sql(
        sqlQ, engineCourseApp).drop(columns='course_id')

    div = html.Div([

        UI_PDFtoTable(programCoursesPDF),
        UI_fileDownload('downloadProgramwisecourselist-btn',
                        'downloadProgramwisecourselist-dwn', 'Download data')
    ])

    return div


# 3.6.3 generate reports -Download Programwise course list
@app.callback(
    Output("downloadProgramwisecourselist-dwn", "data"),
    Input("downloadProgramwisecourselist-btn", "n_clicks"),
    State('selectedProgram_programwise', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, selectedProgram_programwise):
    selectedProgram = selectedProgram_programwise
    programCoursesList = pd.read_sql('SELECT course_code FROM program_structure WHERE program_code="{}"'.format(
        selectedProgram), engineCourseApp)['course_code'].to_list()
    sqlQ = 'SELECT * FROM course WHERE course_code IN ({})'.format(
        '", "'.join(['"']+programCoursesList+['"']))
    programCoursesPDF = pd.read_sql(
        sqlQ, engineCourseApp).drop(columns='course_id')

    filename = selectedProgram+'-' + \
        datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")+'.csv'

    return dcc.send_data_frame(programCoursesPDF.to_csv, filename, index=False)

# 3.6.4 generate SQL reports - generate report button click


@app.callback(
    Output("Download_report_SQL-output", "children"),
    Input("Download_report_SQL-btn", "n_clicks"),
    State('Download_report_SQL_text', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, Download_report_SQL_text):
    # to_test= SELECT * FROM course
    sqlQ = Download_report_SQL_text
    outputPDF = pd.read_sql(sqlQ, engineCourseApp)
    div = html.Div([
        UI_PDFtoTable(outputPDF),
        UI_fileDownload('Download_report_SQL_download-btn',
                        'Download_report_SQL_download-dwn', 'Download data')
    ])
    return div


# 3.6.4 generate SQL reports - download data
@app.callback(
    Output("Download_report_SQL_download-dwn", "data"),
    Input("Download_report_SQL_download-btn", "n_clicks"),
    State('Download_report_SQL_text', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, Download_report_SQL_text):
    sqlQ = Download_report_SQL_text
    outputPDF = pd.read_sql(sqlQ, engineCourseApp)

    filename = 'SQL_'+'-'+datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")+'.csv'

    return dcc.send_data_frame(outputPDF.to_csv, filename, index=False)


# 3.7 send email - user click select table2(email) button after picking table2 name from the dropdown
@app.callback(
    Output("send_email_select_table2-output", "children"),
    Input("send_email_select_table2-btn", "n_clicks"),
    State('send_email_tableName2', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, tableName2):
    temp000x = pd.read_sql('SELECT * FROM {}'.format(tableName2),
                           engineCourseApp).drop(columns=[tableName2+'_id'])
    colList = [*temp000x]

    div = html.Div([
        html.P('Pick filter columns'),
        UI_multidropdown('send_email_selectedColList2', colList),
        html.Button('Select filter values',
                    id='send_email_select_columns2-btn', n_clicks=0),
        html.Div(id='send_email_select_columns2-output'),
    ])

    return div

# 3.7 send email - user click Select filter values2 btn


@app.callback(
    Output("send_email_select_columns2-output", "children"),
    Input("send_email_select_columns2-btn", "n_clicks"),
    State('send_email_tableName2', 'value'),
    State('send_email_selectedColList2', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, tableName2, selectedColList2):
    slectedTableDataPDF = pd.read_sql('SELECT {} FROM {}'.format(
        ', '.join(selectedColList2), tableName2), engineCourseApp)
    filterLists = {}
    for col in selectedColList2:
        filterLists[col] = list(set(slectedTableDataPDF[col].to_list()))

    temp000x = pd.read_sql('SELECT * FROM {}'.format(tableName2),
                           engineCourseApp).drop(columns=[tableName2+'_id'])
    colList = [*temp000x]

    div = html.Div([
        html.P('Enter filter values'),
        UI_table_dropdown('send_email_filtered_data_table1', filterLists),
        html.P('Select email column'),
        UI_dropdown('send_email_selectedColList2b', colList),
        html.Button('Get email list',
                    id='send_email_get_filtered_data-btn', n_clicks=0),
        html.Div(id='send_email_get_filtered_data-output'),
    ])

    return div

# 3.7 send email -User clicks get filtered data button - show table and allow download


@app.callback(
    Output("send_email_get_filtered_data-output", "children"),
    Output("store_email_list", "data"),
    Input("send_email_get_filtered_data-btn", "n_clicks"),
    State('send_email_tableName2', 'value'),
    State('send_email_filtered_data_table1', 'data'),
    State('send_email_selectedColList2b', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, tableName2, filtered_data_table1, selectedColList2b):
    if (n_clicks != 0):
        selectedDisplayColList = selectedColList2b

        selectedColList = []
        selectedFilterVals = []
        for xx in filtered_data_table1:
            selectedColList += [xx['Column_name']]
            selectedFilterVals += [xx['Value']]

        tmp00 = []
        for i, xx in enumerate(selectedColList):
            tmp00 += ['{}="{}"'.format(xx, selectedFilterVals[i])]
        sqlQ = 'SELECT {} FROM {}  WHERE {}'.format(
            selectedDisplayColList, tableName2, ' AND '.join(tmp00))
        filreredPDF = pd.read_sql(sqlQ, engineCourseApp)
        emailList = list(set(filreredPDF[selectedDisplayColList].to_list()))
        print(emailList)
        text = (', '.join(emailList))
        div = html.Div([
            # UI_PDFtoTable(filreredPDF),
            html.P(text),
            html.Br(),
            html.Button('Proceed', id='send_email_procced-btn', n_clicks=0),
            html.Div(id='send_email_procced-output'),
        ])

        return div, emailList
    else:
        raise PreventUpdate


# 3.7 send email - Show email panel when user click proceed
@app.callback(
    Output("send_email_procced-output", "children"),
    Input("send_email_procced-btn", "n_clicks"),
    State("store_email_list", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, store_email_list):

    # send_email(senderName,senderEmail,senderEmailPswd,recieverEmail,emailSubject,emailBody)

    div = html.Div([
        html.Br(),
        html.Div([
            html.P('Send email to a specific user group'),
            dcc.Input(id='send_email_subject', type='text',
                      placeholder='Subject', style={'width': '80%'}),
            html.Br(),
            html.Br(),
            dcc.Textarea(id='send_email_body', placeholder='Message',
                         style={'width': '80%', 'height': '150px'}),
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

        html.Div([
            html.P('Edit users'),
            # UI_dropdown('send_email_usrgrp',['Group1','Group2'],{'width':'80%'}),
            UI_multidropdown('send_email_usrgrp', store_email_list),
            html.Br(),
            html.Button('Send', id='send_email_send-btn', n_clicks=0),
            html.Div(id='send_email_send-output'),
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
    ])

    return div


@app.callback(
    Output("send_email_send-output", "children"),
    Input("send_email_send-btn", "n_clicks"),
    State('send_email_subject', 'value'),
    State('send_email_body', 'value'),
    State('send_email_usrgrp', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, send_email_subject, send_email_body, send_email_usrgrp):

    # send_email(senderName,senderEmail,senderEmailPswd,recieverEmail,emailSubject,emailBody)
    send_email_usrgrp.append('mugalan@gmail.com')
    # returnText=send_email('TEAL Program Revision',adminEmailHere,'ADDPASSWORD',send_email_usrgrp,send_email_subject,send_email_body)
    div = html.Div([
        html.P('Message sent'),

    ])

    return div


# 3.8 Blooms level calculation
# 24/11/2022
@app.callback(

    Output("process_course_table-output", "children"),
    Output("store_courseCodes", "data"),
    Input("process_course_table-btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    if (n_clicks != 0):
        # coursesWithNoBlooms=pd.read_sql('SELECT * FROM course WHERE BLOOMS_level="" AND ILO1!="" AND credit_to_ILO_map!=""',engineCourseApp)
        coursesWithNoBlooms = pd.read_sql(
            'SELECT * FROM course WHERE SOLO_level="" AND ILO1!="" AND credit_to_ILO_map!=""', engineCourseApp)
        # coursesWithNoBlooms.to_csv("coursesWithNoBlooms.csv")
        # len(coursesWithNoBlooms.index)
        courseCodes = []
        for idx in range(len(coursesWithNoBlooms.index)):
            # idx=0
            updateCourseDict = {}
            updateCourseDict['ILO1'] = coursesWithNoBlooms['ILO1'][idx]
            updateCourseDict['ILO2'] = coursesWithNoBlooms['ILO2'][idx]
            updateCourseDict['ILO3'] = coursesWithNoBlooms['ILO3'][idx]
            updateCourseDict['ILO4'] = coursesWithNoBlooms['ILO4'][idx]
            updateCourseDict['ILO5'] = coursesWithNoBlooms['ILO5'][idx]
            updateCourseDict['ILO6'] = coursesWithNoBlooms['ILO6'][idx]
            updateCourseDict['credit_to_ILO_map'] = coursesWithNoBlooms['credit_to_ILO_map'][idx]
            updateCourseDict['course_objective'] = coursesWithNoBlooms['course_objective'][idx]
            updateCourseDict['course_code'] = coursesWithNoBlooms['course_code'][idx]
            courseCodes.append(updateCourseDict['course_code'])
            updateCourseDict['CAH3_skill_classification'] = coursesWithNoBlooms['CAH3_skill_classification'][idx]

            temp = courseTaxonomyLevel(engineCourseApp, updateCourseDict)
            sqlQuery = 'UPDATE course SET BLOOMS_level="{}" WHERE course_code="{}"'.format(
                temp['BLOOMS_level'], updateCourseDict['course_code'])
            sqlQuery = 'UPDATE course SET SOLO_level="{}" WHERE course_code="{}"'.format(
                temp['SOLO_level'], updateCourseDict['course_code'])
            sql.execute(sqlQuery, engineCourseApp)

            print(sqlQuery)

        qry2 = 'SELECT * FROM course WHERE course_code IN ("{}")'.format(
            '","'. join(courseCodes))
        coursesWithNoBloomsUpdated = pd.read_sql(qry2, engineCourseApp)

        div = html.Div([
            html.P("Courses with no Blooms Level"),
            UI_PDFtoTable(coursesWithNoBlooms),
            html.Br(),
            html.P("Updated table"),
            UI_PDFtoTable(coursesWithNoBloomsUpdated),
            UI_fileDownload('coursesWithNoBloomsUpdated-btn',
                            'coursesWithNoBloomsUpdated-download', "Download"),
        ])

        return div, courseCodes
    else:
        raise PreventUpdate


@app.callback(
    Output("coursesWithNoBloomsUpdated-download", "data"),
    Input("coursesWithNoBloomsUpdated-btn", "n_clicks"),
    State("store_courseCodes", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, courseCodes):
    if (n_clicks != 0):
        qry2 = 'SELECT * FROM course WHERE course_code IN ("{}")'.format(
            '","'. join(courseCodes))
        coursesWithNoBloomsUpdated = pd.read_sql(qry2, engineCourseApp)
        filename = "Blooms update"+'-' + \
            datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")+'.csv'
        return dcc.send_data_frame(coursesWithNoBloomsUpdated.to_csv, filename, index=False)
    else:
        raise PreventUpdate


# 3.9 Bulk course actions
# 29/01/2023
@app.callback(
    Output('CSVmodeBulkcourseactions-output', 'children'),
    Output('store_CSVmodeBulkcourseactions', 'data'),
    Input('CSVmodeBulkcourseactions-upload', 'contents'),
    State('CSVmodeBulkcourseactions-upload', 'filename'),
    State('CSVmodeBulkcourseactions-upload', 'last_modified'),
    # State('tableName2_CSV','value'),
    prevent_initial_call=True,
)
def func(contents, filename, last_modified):
    if contents is None:
        raise PreventUpdate
        div = html.Div()

    else:  # read CSV data
        updateDataPDF = parse_contents(contents, filename, last_modified)
        updateDataPDF = updateDataPDF.fillna('')
        updateCols = [*updateDataPDF]

        updateDataPDF_JSON = updateDataPDF.to_json()
        # temp000x=updateDataPDF
        # colList=[*temp000x]

        headerList = [*updateDataPDF]

        div = html.Div([
            UI_PDFtoTable(updateDataPDF),

            html.Div([

                html.P('Select course shortname column',
                       style={'font-weight': 'bold'}),
                UI_dropdown('selectedHeader_Bulkcourseactions', headerList),

                html.Br(),
                html.Button(
                    'Update UI', id='afterSelectCshortname-Bulkcourseactions-btn', n_clicks=0),
                html.Div(id='afterSelectCshortname-Bulkcourseactions-output'),
            ]),

        ])

        return div, updateDataPDF_JSON


# Bulk add users - after user upload CSV
# 30/01/2023
@app.callback(
    Output('CSVmodeBulkUserCreate-output', 'children'),
    Output('store_CSVmodeBulkUserCreate', 'data'),
    Input('CSVmodeBulkUserCreate-upload', 'contents'),
    State('CSVmodeBulkUserCreate-upload', 'filename'),
    State('CSVmodeBulkUserCreate-upload', 'last_modified'),
    # State('tableName2_CSV','value'),
    prevent_initial_call=True,
)
def func(contents, filename, last_modified):
    if contents is None:
        raise PreventUpdate
        div = html.Div()

    else:  # read CSV data
        updateDataPDF = parse_contents(contents, filename, last_modified)
        updateDataPDF = updateDataPDF.fillna('')
        updateCols = [*updateDataPDF]

        updateDataPDF_JSON = updateDataPDF.to_json()

        div = html.Div([
            UI_PDFtoTable(updateDataPDF),

            html.Div([
                html.Button(
                    'Add users', id='afterSelectBulkUserAdd-btn', n_clicks=0),
                html.Div(id='afterSelectBulkUserAdd-output'),
            ]),

        ])

        return div, updateDataPDF_JSON


@app.callback(
    Output('afterSelectCshortname-Bulkcourseactions-output', 'children'),
    Input('afterSelectCshortname-Bulkcourseactions-btn', 'n_clicks'),
    State('selectedHeader_Bulkcourseactions', 'value'),
    State('store_CSVmodeBulkcourseactions', 'data'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, selectedHeader_Bulkcourseactions, store_CSVmodeBulkcourseactions, email):
    selectedColumn = selectedHeader_Bulkcourseactions
    DataPDF = pd.read_json(store_CSVmodeBulkcourseactions)

    courseCodeListInApp = pd.read_sql(
        "SELECT course_code FROM course", engineCourseApp)["course_code"].to_list()
    courseCodeListUploaded = DataPDF[selectedColumn].to_list()
    courseNotInApp = list(
        set(courseCodeListUploaded).difference(set(courseCodeListInApp)))
    course2bUpdated = list(
        set(courseCodeListUploaded).intersection(set(courseCodeListInApp)))

    templateShortName = templateCourseSpecifications
    for chosenCourseShortName in course2bUpdated:
        parameters = {'webserviceAccessParams': webserviceAccessParamsCourse, 'access_parameters': {'gToken': githubToken,
                                                                                                    'gUser': course_githubUser}, 'repoName': chosenCourseShortName, 'userEmail': email, 'templateShortName': templateShortName}
        create_update_course_4m_course_db(
            mgGH, engineCourse, engineCourseApp, parameters)

    courseNotInAppTxt = ", ".join(courseNotInApp)
    course2bUpdatedTxt = ", ".join(course2bUpdated)

    div = html.Div([
        html.P("Following courses not in the app DB"),
        html.P(courseNotInAppTxt),
        html.P("Following courses updated in the course UI"),
        html.P(course2bUpdatedTxt),

    ])

    return div


# bulk add users - user click add users button
@app.callback(
    Output('afterSelectBulkUserAdd-output', 'children'),
    Input('afterSelectBulkUserAdd-btn', 'n_clicks'),
    State('store_CSVmodeBulkUserCreate', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, store_CSVmodeBulkUserCreate):
    if (n_clicks != 0):
        uploadedUsersPDF = pd.read_json(store_CSVmodeBulkUserCreate)
        headerListInUploaded = set([*uploadedUsersPDF])

        h1 = set(['username', 'email', 'firstname', 'lastname', 'password'])
        diff = headerListInUploaded.difference(h1)

        if (len(diff) != 0):  # header doesn't tally
            div = html.Div([
                html.P("Invalid headers"),
            ])

        else:  # add users in the CSV
            exitingUsersText = []

            wSp = {
                "Content": webserviceAccessParamsContent,
                "Course": webserviceAccessParamsCourse,
                "Classroom": webserviceAccessParamsClassroom_SERVER
            }

            engs = {
                "Content": engineContent,
                "Course": engineCourse,
                "Classroom": engineClassroom_SERVER
            }

            exitingUsersText = ""

            for xx in ["Content", "Course", "Classroom"]:

                existingUsers = pd.read_sql('SELECT email FROM mdl_user', engs[xx])[
                    'email'].to_list()
                uploadedUsers = uploadedUsersPDF['email'].to_list()
                existingUsersInList = list(
                    set(uploadedUsers).intersection(set(existingUsers)))
                exitingUsersText = exitingUsersText+xx + \
                    " - " + ', '.join(existingUsersInList)
                newUsers = list(
                    set(uploadedUsers).difference(set(existingUsers)))
                newUserListDict = uploadedUsersPDF[uploadedUsersPDF['email'].isin(
                    newUsers)].to_dict(orient='records')

                createdUserList = call(
                    wSp[xx], 'core_user_create_users', users=newUserListDict)

            div = html.Div([
                html.P("Users added"),
                html.P("exitingUsersText:"),
                html.P(exitingUsersText),
            ])

        return div
    else:
        raise PreventUpdate


# ============================course creation==================================

# 2course creation- search - user select search mode
@app.callback(
    Output('search-options', 'children'),
    Input('courseSearchMode', 'value'),
    prevent_initial_call=True,)
def func(courseSearchMode):
    if (courseSearchMode == 'Search by keywords'):
        div = html.Div([
            html.H6("Search by keywords", style={
                    "font-weight": "bold", 'textAlign': 'center'}),




            dcc.Input(id="searchKWs", type="text",
                      placeholder="", debounce=True),
            html.Button('Search', id='search-btn', n_clicks=0),
            html.Div(id='search-output'),
        ])
    elif (courseSearchMode == 'Search by course code'):
        course_code_list = pd.read_sql(
            'SELECT * FROM course', engineCourseApp)['course_code'].tolist()
        course_code_list.sort()

        div = html.Div([
            html.H6('Search by course code', style={
                    'textAlign': 'center', 'font-weight': 'bold'}),

            UI_dropdown('searchCourseCode',
                        course_code_list, {'width': '60%'}),
            html.Button('Search', id='search-btn2', n_clicks=0),
            html.Div(id='search-output2'),
        ])
    elif (courseSearchMode == 'Search by similar course name'):
        div = html.Div([
            html.H6('Search by similar course name', style={
                    'textAlign': 'center', 'font-weight': 'bold'}),
            # UI_dropdown('searchCourseName0',courseNameList,{'width':'80%'}),
            dcc.Input(id="searchCourseName0", type="text",
                      value="Biology Management", placeholder="", debounce=True),
            html.Button('Search', id='search-btn3', n_clicks=0),
            html.Div(id='search-output3'),
        ])
    elif (courseSearchMode == 'Search by course skills'):
        programDomains = list(set(pd.read_sql(
            'SELECT Domain From HECoS_CAH', engineCourseApp)['Domain'].to_list()))
        programDomains.sort()
        div = div_skillSelectionCourseSearch(programDomains),
    else:
        div = html.Div([

        ])

    return div

# Search for course - search mode selection=====================================


@app.callback(  # search_course_by_KW
    Output('search-output', 'children'),
    Input('search-btn', 'n_clicks'),
    State('searchKWs', 'value'),
    prevent_initial_call=True,)
def func(n_clicks, searchKWs):
    courseSummaryPDF = pd.read_sql('SELECT * FROM course', engineCourseApp)
    matchingCoursesPDF = search_course_by_KW(courseSummaryPDF, searchKWs, 0.4)
    matchingCoursesPDF = matchingCoursesPDF.drop(columns=['course_id'])
    div = UI_PDFtoTable(matchingCoursesPDF)
    return div


@app.callback(  # search_course_by_code
    Output('search-output2', 'children'),
    Input('search-btn2', 'n_clicks'),
    State('searchCourseCode', 'value'),
    prevent_initial_call=True,)
def func(n_clicks, searchCourseCode):
    matchingCoursesPDF = pd.read_sql(
        'SELECT * FROM course WHERE course_code="{}"'.format(searchCourseCode), engineCourseApp)
    matchingCoursesPDF = matchingCoursesPDF.drop(columns=['course_id'])
    div = UI_PDFtoTable(matchingCoursesPDF)
    return div


@app.callback(  # search_course_by_name
    Output('search-output3', 'children'),
    Input('search-btn3', 'n_clicks'),
    State('searchCourseName0', 'value'),
    prevent_initial_call=True,)
def func(n_clicks, searchCourseName0):
    courseSummaryPDF = pd.read_sql('SELECT * FROM course', engineCourseApp)
    matchingCoursesPDF = search_course_by_name(
        courseSummaryPDF, searchCourseName0)
    matchingCoursesPDF = matchingCoursesPDF.drop(columns=['course_id'])
    div = UI_PDFtoTable(matchingCoursesPDF)
    return div


# search by course skills - domain,subdomain,skill drop down populate===============
# Search for course -program domain selected
@app.callback(
    Output("program_subdomain", "options"),
    Input("program_domain", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value != None):
        CAHdomain = value
        filteredSubdomainList = list(set(pd.read_sql('SELECT Sub_Domain From HECoS_CAH WHERE Domain="{}"'.format(
            CAHdomain), engineCourseApp)['Sub_Domain'].to_list()))
        filteredSubdomainList.sort()

        return [{'label': i, 'value': i} for i in filteredSubdomainList]
    else:
        return [{'label': i, 'value': i} for i in []]
# Update course - program domain selected


@app.callback(
    Output("program_subdomainCC1", "options"),
    Input("program_domainCC1", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value != None):
        CAHdomain = value
        filteredSubdomainList = list(set(pd.read_sql('SELECT Sub_Domain From HECoS_CAH WHERE Domain="{}"'.format(
            CAHdomain), engineCourseApp)['Sub_Domain'].to_list()))
        filteredSubdomainList.sort()
        return [{'label': i, 'value': i} for i in filteredSubdomainList]
    else:
        return [{'label': i, 'value': i} for i in []]


# Create course - program domain selected
@app.callback(
    Output("program_subdomainCC2", "options"),
    Input("program_domainCC2", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value != None):
        CAHdomain = value
        filteredSubdomainList = list(set(pd.read_sql('SELECT Sub_Domain From HECoS_CAH WHERE Domain="{}"'.format(
            CAHdomain), engineCourseApp)['Sub_Domain'].to_list()))
        filteredSubdomainList.sort()
        return [{'label': i, 'value': i} for i in filteredSubdomainList]
    else:
        return [{'label': i, 'value': i} for i in []]


# Create classroom - program domain selected
@app.callback(
    Output("program_subdomainCC3", "options"),
    Input("program_domainCC3", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value != None):
        CAHdomain = value
        filteredSubdomainList = list(set(pd.read_sql('SELECT Sub_Domain From HECoS_CAH WHERE Domain="{}"'.format(
            CAHdomain), engineCourseApp)['Sub_Domain'].to_list()))
        filteredSubdomainList.sort()
        return [{'label': i, 'value': i} for i in filteredSubdomainList]
    else:
        return [{'label': i, 'value': i} for i in []]


# Add content - program domain selected
@app.callback(
    Output("program_subdomainCC4", "options"),
    Input("program_domainCC4", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value != None):
        CAHdomain = value
        filteredSubdomainList = list(set(pd.read_sql('SELECT Sub_Domain From HECoS_CAH WHERE Domain="{}"'.format(
            CAHdomain), engineCourseApp)['Sub_Domain'].to_list()))
        filteredSubdomainList.sort()
        return [{'label': i, 'value': i} for i in filteredSubdomainList]
    else:
        return [{'label': i, 'value': i} for i in []]

# before pick classroom - program domain selected


@app.callback(
    Output("program_subdomainCC5", "options"),
    Input("program_domainCC5", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value != None):
        CAHdomain = value
        filteredSubdomainList = list(set(pd.read_sql('SELECT Sub_Domain From HECoS_CAH WHERE Domain="{}"'.format(
            CAHdomain), engineCourseApp)['Sub_Domain'].to_list()))
        filteredSubdomainList.sort()
        return [{'label': i, 'value': i} for i in filteredSubdomainList]
    else:
        return [{'label': i, 'value': i} for i in []]


# Search for course -program subdomain selected
@app.callback(
    Output("program_skill", "options"),
    Input("program_domain", "value"),
    Input("program_subdomain", "value"),
    prevent_initial_call=True,
)
def func(program_domain, program_subdomain):
    if (program_subdomain != None):
        CAHdomain = program_domain
        CAH_sub_domain = program_subdomain
        filteredSkillsList = list(set(pd.read_sql('SELECT Skills From HECoS_CAH WHERE Domain="{}" AND Sub_Domain="{}"'.format(
            CAHdomain, CAH_sub_domain), engineCourseApp)['Skills'].to_list()))
        filteredSkillsList.sort()

        return [{'label': i, 'value': i} for i in filteredSkillsList]
    else:
        return [{'label': i, 'value': i} for i in []]


# Update course -program subdomain selected
@app.callback(
    Output("program_skillCC1", "options"),
    Input("program_domainCC1", "value"),
    Input("program_subdomainCC1", "value"),
    prevent_initial_call=True,
)
def func(program_domain, program_subdomain):
    if (program_subdomain != None):
        CAHdomain = program_domain
        CAH_sub_domain = program_subdomain
        filteredSkillsList = list(set(pd.read_sql('SELECT Skills From HECoS_CAH WHERE Domain="{}" AND Sub_Domain="{}"'.format(
            CAHdomain, CAH_sub_domain), engineCourseApp)['Skills'].to_list()))
        filteredSkillsList.sort()
        return [{'label': i, 'value': i} for i in filteredSkillsList]
    else:
        return [{'label': i, 'value': i} for i in []]

# Create course -program subdomain selected


@app.callback(
    Output("program_skillCC2", "options"),
    Input("program_domainCC2", "value"),
    Input("program_subdomainCC2", "value"),
    prevent_initial_call=True,
)
def func(program_domain, program_subdomain):
    if (program_subdomain != None):
        CAHdomain = program_domain
        CAH_sub_domain = program_subdomain
        filteredSkillsList = list(set(pd.read_sql('SELECT Skills From HECoS_CAH WHERE Domain="{}" AND Sub_Domain="{}"'.format(
            CAHdomain, CAH_sub_domain), engineCourseApp)['Skills'].to_list()))
        filteredSkillsList.sort()
        return [{'label': i, 'value': i} for i in filteredSkillsList]
    else:
        return [{'label': i, 'value': i} for i in []]

# Create classroom -program subdomain selected


@app.callback(
    Output("program_skillCC3", "options"),
    Input("program_domainCC3", "value"),
    Input("program_subdomainCC3", "value"),
    prevent_initial_call=True,
)
def func(program_domain, program_subdomain):
    if (program_subdomain != None):
        CAHdomain = program_domain
        CAH_sub_domain = program_subdomain
        filteredSkillsList = list(set(pd.read_sql('SELECT Skills From HECoS_CAH WHERE Domain="{}" AND Sub_Domain="{}"'.format(
            CAHdomain, CAH_sub_domain), engineCourseApp)['Skills'].to_list()))
        filteredSkillsList.sort()
        return [{'label': i, 'value': i} for i in filteredSkillsList]
    else:
        return [{'label': i, 'value': i} for i in []]

# Add content -program subdomain selected


@app.callback(
    Output("program_skillCC4", "options"),
    Input("program_domainCC4", "value"),
    Input("program_subdomainCC4", "value"),
    prevent_initial_call=True,
)
def func(program_domain, program_subdomain):
    if (program_subdomain != None):
        CAHdomain = program_domain
        CAH_sub_domain = program_subdomain
        filteredSkillsList = list(set(pd.read_sql('SELECT Skills From HECoS_CAH WHERE Domain="{}" AND Sub_Domain="{}"'.format(
            CAHdomain, CAH_sub_domain), engineCourseApp)['Skills'].to_list()))
        filteredSkillsList.sort()
        return [{'label': i, 'value': i} for i in filteredSkillsList]
    else:
        return [{'label': i, 'value': i} for i in []]

# before pick classroom - program subdomain selected


@app.callback(
    Output("program_skillCC5", "options"),
    Input("program_domainCC5", "value"),
    Input("program_subdomainCC5", "value"),
    prevent_initial_call=True,
)
def func(program_domain, program_subdomain):
    if (program_subdomain != None):
        CAHdomain = program_domain
        CAH_sub_domain = program_subdomain
        filteredSkillsList = list(set(pd.read_sql('SELECT Skills From HECoS_CAH WHERE Domain="{}" AND Sub_Domain="{}"'.format(
            CAHdomain, CAH_sub_domain), engineCourseApp)['Skills'].to_list()))
        filteredSkillsList.sort()
        return [{'label': i, 'value': i} for i in filteredSkillsList]
    else:
        return [{'label': i, 'value': i} for i in []]


# Search for course  - search_course_by_skill search button clicked
@app.callback(
    Output('search-output4', 'children'),
    Input('search-btn4', 'n_clicks'),
    State('program_skill', 'value'),
    prevent_initial_call=True,)
def func(n_clicks, program_skill):
    matchingCoursesPDF = pd.read_sql(
        'SELECT * FROM course WHERE CAH3_skill_classification="{}"'.format(program_skill), engineCourseApp)
    matchingCoursesPDF = matchingCoursesPDF.drop(columns=['course_id'])
    div = UI_PDFtoTable(matchingCoursesPDF)
    return div

# this removes bug - program_domainCC1 or program_subdomainCC1 cleared program_skillCC1 not set to None


@app.callback(
    Output("program_skillCC1", "value"),
    Input("program_domainCC1", "value"),
    Input("program_subdomainCC1", "value"),
    prevent_initial_call=True,
)
def func(program_domainCC1, program_subdomainCC1):
    if (program_domainCC1 == None or program_subdomainCC1 == None):
        return None


# Course creation - ILO generation ======================

# user selects Solo level - verb list generated
@app.callback(
    Output("verb_ILO11", "options"),
    Input("solo_level_ILO11", "value"),
    prevent_initial_call=True,
)
def func(taxonomyLevel):
    if (taxonomyLevel != None):

        taxonomyPDF = pd.read_sql(
            'SOLO_BLOOMS_Taxonomy', engineCourseApp).fillna("")
        soloVerbs = list(set(taxonomyPDF[taxonomyLevel].to_list()))
        soloVerbs.sort()

        if ('' in soloVerbs):
            soloVerbs.remove('')
        return [{'label': i, 'value': i} for i in soloVerbs]
    else:
        return [{'label': i, 'value': i} for i in []]


@app.callback(
    Output("verb_ILO21", "options"),
    Input("solo_level_ILO21", "value"),
    prevent_initial_call=True,
)
def func(taxonomyLevel):
    if (taxonomyLevel != None):
        taxonomyPDF = pd.read_sql(
            'SOLO_BLOOMS_Taxonomy', engineCourseApp).fillna("")
        soloVerbs = list(set(taxonomyPDF[taxonomyLevel].to_list()))
        soloVerbs.sort()
        if ('' in soloVerbs):
            soloVerbs.remove('')
        return [{'label': i, 'value': i} for i in soloVerbs]
    else:
        return [{'label': i, 'value': i} for i in []]


@app.callback(
    Output("verb_ILO31", "options"),
    Input("solo_level_ILO31", "value"),
    prevent_initial_call=True,
)
def func(taxonomyLevel):
    if (taxonomyLevel != None):
        taxonomyPDF = pd.read_sql(
            'SOLO_BLOOMS_Taxonomy', engineCourseApp).fillna("")
        soloVerbs = list(set(taxonomyPDF[taxonomyLevel].to_list()))
        soloVerbs.sort()
        if ('' in soloVerbs):
            soloVerbs.remove('')
        return [{'label': i, 'value': i} for i in soloVerbs]
    else:
        return [{'label': i, 'value': i} for i in []]


@app.callback(
    Output("verb_ILO41", "options"),
    Input("solo_level_ILO41", "value"),
    prevent_initial_call=True,
)
def func(taxonomyLevel):
    if (taxonomyLevel != None):
        taxonomyPDF = pd.read_sql(
            'SOLO_BLOOMS_Taxonomy', engineCourseApp).fillna("")
        soloVerbs = list(set(taxonomyPDF[taxonomyLevel].to_list()))
        soloVerbs.sort()
        if ('' in soloVerbs):
            soloVerbs.remove('')
        return [{'label': i, 'value': i} for i in soloVerbs]
    else:
        return [{'label': i, 'value': i} for i in []]


@app.callback(
    Output("verb_ILO51", "options"),
    Input("solo_level_ILO51", "value"),
    prevent_initial_call=True,
)
def func(taxonomyLevel):
    if (taxonomyLevel != None):
        taxonomyPDF = pd.read_sql(
            'SOLO_BLOOMS_Taxonomy', engineCourseApp).fillna("")
        soloVerbs = list(set(taxonomyPDF[taxonomyLevel].to_list()))
        soloVerbs.sort()
        if ('' in soloVerbs):
            soloVerbs.remove('')
        return [{'label': i, 'value': i} for i in soloVerbs]
    else:
        return [{'label': i, 'value': i} for i in []]


@app.callback(
    Output("verb_ILO61", "options"),
    Input("solo_level_ILO61", "value"),
    prevent_initial_call=True,
)
def func(taxonomyLevel):
    if (taxonomyLevel != None):
        taxonomyPDF = pd.read_sql(
            'SOLO_BLOOMS_Taxonomy', engineCourseApp).fillna("")
        soloVerbs = list(set(taxonomyPDF[taxonomyLevel].to_list()))
        soloVerbs.sort()
        if ('' in soloVerbs):
            soloVerbs.remove('')
        return [{'label': i, 'value': i} for i in soloVerbs]
    else:
        return [{'label': i, 'value': i} for i in []]


# this removes bug - solo_level_ILOx cleared verb_ILOx not set to None
@app.callback(
    Output("verb_ILO11", "value"),
    Input("solo_level_ILO11", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value == None):
        return None


@app.callback(
    Output("verb_ILO21", "value"),
    Input("solo_level_ILO21", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value == None):
        return None


@app.callback(
    Output("verb_ILO31", "value"),
    Input("solo_level_ILO31", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value == None):
        return None


@app.callback(
    Output("verb_ILO41", "value"),
    Input("solo_level_ILO41", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value == None):
        return None


@app.callback(
    Output("verb_ILO51", "value"),
    Input("solo_level_ILO51", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value == None):
        return None


@app.callback(
    Output("verb_ILO61", "value"),
    Input("solo_level_ILO61", "value"),
    prevent_initial_call=True,
)
def func(value):
    if (value == None):
        return None

# credit slider display output


@app.callback(
    Output("slideroutputx", "children"),
    Input("creditsx", "value"),
    prevent_initial_call=True,
)
def func(value):
    print(value)


# user clicks continue button
@app.callback(
    Output("continueCourse-output", "children"),
    Output("store_propsedCourse", "data"),
    Input("continue-btn", "n_clicks"),
    State('course_code', 'value'),
    State('program_domainCC1', 'value'),
    # not use global variable program_subdomain_value
    State('program_subdomainCC1', 'value'),
    # not use global variable program_skill_value
    State('program_skillCC1', 'value'),
    State('solo_level_ILO11', 'value'),
    State('solo_level_ILO21', 'value'),
    State('solo_level_ILO31', 'value'),
    State('solo_level_ILO41', 'value'),
    State('solo_level_ILO51', 'value'),
    State('solo_level_ILO61', 'value'),
    # Not used 6 global variables for verb values verb_ILOx_value
    State('verb_ILO11', 'value'),
    State('verb_ILO21', 'value'),
    State('verb_ILO31', 'value'),
    State('verb_ILO41', 'value'),
    State('verb_ILO51', 'value'),
    State('verb_ILO61', 'value'),
    State('text_ILO11', 'value'),
    State('text_ILO21', 'value'),
    State('text_ILO31', 'value'),
    State('text_ILO41', 'value'),
    State('text_ILO51', 'value'),
    State('text_ILO61', 'value'),
    State('creditSlider11', 'value'),
    State('creditSlider21', 'value'),
    State('creditSlider31', 'value'),
    State('creditSlider41', 'value'),
    State('creditSlider51', 'value'),
    State('creditSlider61', 'value'),
    State('objective_text', 'value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks,
         course_code,
         program_domainCC1,
         program_subdomainCC1,
         program_skillCC1,
         solo_level_ILO11,
         solo_level_ILO21,
         solo_level_ILO31,
         solo_level_ILO41,
         solo_level_ILO51,
         solo_level_ILO61,
         verb_ILO11,
         verb_ILO21,
         verb_ILO31,
         verb_ILO41,
         verb_ILO51,
         verb_ILO61,
         text_ILO11,
         text_ILO21,
         text_ILO31,
         text_ILO41,
         text_ILO51,
         text_ILO61,
         creditSlider11,
         creditSlider21,
         creditSlider31,
         creditSlider41,
         creditSlider51,
         creditSlider61,
         objective_text,
         userEmail):

    if (n_clicks != 0):
        text_ILO11 = text_ILO11.replace(
            "'", "`") if text_ILO11 != None else text_ILO11
        text_ILO21 = text_ILO21.replace(
            "'", "`") if text_ILO21 != None else text_ILO21
        text_ILO31 = text_ILO31.replace(
            "'", "`") if text_ILO31 != None else text_ILO31
        text_ILO41 = text_ILO41.replace(
            "'", "`") if text_ILO41 != None else text_ILO41
        text_ILO51 = text_ILO51.replace(
            "'", "`") if text_ILO51 != None else text_ILO51
        text_ILO61 = text_ILO61.replace(
            "'", "`") if text_ILO61 != None else text_ILO61

        course_code = course_code.split(
            "-")[0].strip(" ")  # get only course code

        temp00PDF = pd.read_sql('SELECT * FROM course WHERE course_code="{}"'.format(
            course_code), engineCourseApp).drop(columns=['course_id'])
        updateCourseDict = temp00PDF.to_dict(orient='records')[0]
        propsedCourse0 = 0

        creditSlider11 = float(creditSlider11)
        creditSlider21 = float(creditSlider21)
        creditSlider31 = float(creditSlider31)
        creditSlider41 = float(creditSlider41)
        creditSlider51 = float(creditSlider51)
        creditSlider61 = float(creditSlider61)

        # verb1_flag,verb2_flag,verb3_flag,verb4_flag,verb5_flag,verb6_flag=1,0,0,0,0,0
        skill_flag = 1 if program_skillCC1 != None else 0
        verb1_flag = 1 if verb_ILO11 != None else 0
        verb2_flag = 1 if verb_ILO21 != None else 0
        verb3_flag = 1 if verb_ILO31 != None else 0
        verb4_flag = 1 if verb_ILO41 != None else 0
        verb5_flag = 1 if verb_ILO51 != None else 0
        verb6_flag = 1 if verb_ILO61 != None else 0

        # print for debugging
        # print("skill_flag:",skill_flag)
        # print("verb1_flag:",verb1_flag)
        # print("verb2_flag:",verb2_flag)
        # print("verb3_flag:",verb3_flag)
        # print("verb4_flag:",verb4_flag)
        # print("verb5_flag:",verb5_flag)
        # print("verb6_flag:",verb6_flag)

        verb_count = verb1_flag+verb2_flag+verb3_flag+verb4_flag+verb5_flag+verb6_flag

        # Generate ILO map depending on selected verbs
        verb_flags_list = [verb1_flag, verb2_flag,
                           verb3_flag, verb4_flag, verb5_flag, verb6_flag]
        credit_val_list = [str(creditSlider11), str(creditSlider21), str(
            creditSlider31), str(creditSlider41), str(creditSlider51), str(creditSlider61)]

        # check any empty verbflags in middle --> show error
        # verb_flags_list=[1,1,1,0,0,0]
        # verb_flags_list=[1,1,1,1,1,1]

        if (0 in verb_flags_list):  # if all 6 ILOs exist no 0. To avoid that error check are there any zeros first. 21 Jul 2022
            zeros_start_at = min(
                [index for (index, item) in enumerate(verb_flags_list) if item == 0])

        else:
            # when ILO6 complete ones end at 5. Anything greater than that is safe.
            zeros_start_at = 7

        ones_end_at = max([index for (index, item) in enumerate(
            verb_flags_list) if item == 1], default=0)

        if (ones_end_at < zeros_start_at):
            Empty_ILOs_atMiddle = False  # emtpy ILO in middle
        else:
            Empty_ILOs_atMiddle = True  # emtpy ILO in middle

        ILO_Map = ', '.join(credit_val_list[0:ones_end_at+1])

        if (skill_flag == 0 and verb1_flag == 0):
            div = html.Div([
                html.Br(),
                html.P('Please select CAH3 skill classification',
                       style={'font-style': 'italic', 'color': 'red'}),
                html.P('Please create at least one ILO', style={
                       'font-style': 'italic', 'color': 'red'}),
            ])

        elif (skill_flag == 1 and verb1_flag == 0):
            div = html.Div([
                html.Br(),
                html.P('Please create at least one ILO', style={
                       'font-style': 'italic', 'color': 'red'}),
            ])

        elif (skill_flag == 0 and verb1_flag == 1):
            div = html.Div([
                html.Br(),
                html.P('Please select CAH3 skill classification',
                       style={'font-style': 'italic', 'color': 'red'}),
            ])

        elif (Empty_ILOs_atMiddle == True):
            div = html.Div([
                html.Br(),
                html.P('Missing ILO in the middle. Please specify ILOs sequentially', style={
                       'font-style': 'italic', 'color': 'red'}),
            ])

        else:

            try:  # if user forgets to complete text areas concat error will occur. This will avoid it.

                ILO1_in = concat_ILOs(verb_ILO11, text_ILO11, verb1_flag)
                ILO2_in = concat_ILOs(verb_ILO21, text_ILO21, verb2_flag)
                ILO3_in = concat_ILOs(verb_ILO31, text_ILO31, verb3_flag)
                ILO4_in = concat_ILOs(verb_ILO41, text_ILO41, verb4_flag)
                ILO5_in = concat_ILOs(verb_ILO51, text_ILO51, verb5_flag)
                ILO6_in = concat_ILOs(verb_ILO61, text_ILO61, verb6_flag)

                # User Inputs for defining the course information as you now have it - UI function
                # global propsedCourse
                updateCourseDict['ILO1'] = ILO1_in
                updateCourseDict['ILO2'] = ILO2_in
                updateCourseDict['ILO3'] = ILO3_in
                updateCourseDict['ILO4'] = ILO4_in
                updateCourseDict['ILO5'] = ILO5_in
                updateCourseDict['ILO6'] = ILO6_in
                updateCourseDict['credit_to_ILO_map'] = ILO_Map
                updateCourseDict['course_objective'] = objective_text
                updateCourseDict['course_code'] = course_code
                updateCourseDict['CAH3_skill_classification'] = program_skillCC1

                # to avoid NA causing error during keyword search
                courseSummaryPDF = pd.read_sql(
                    'SELECT * FROM course', engineCourseApp).fillna("")
                propsedCourse0, similarCoursesPDF = process_proposed_course(
                    engineCourseApp, course_code, updateCourseDict, courseSummaryPDF)
                propsedCoursePDF = pd.DataFrame(propsedCourse0, index=[0])

                div = html.Div(id='div_proposed_CDetails', children=[
                    # html.P('Proposed course details',style={'textAlign': 'left','font-weight': 'bold'}),

                    html.P([
                        html.P("Proposed course details", style={
                               "font-weight": "bold", "display": "inline"}),
                        UI_toolTipIcon("updateCourseProposedCourseDetails"),
                    ], style={'textAlign': 'left'}),

                    UI_toolTip("updateCourseProposedCourseDetails", "You can see the finalized course information here. Those are not added to the system yet. If you have anything to change, you can change it now. Once you ready, enter a comment mentioning what was updated in the course (for the version controlling system) and click the 'Update course' button."),


                    UI_PDFtoTable(propsedCoursePDF),
                    html.Br(),
                    html.P('Please edit the ILO fields and press the "CONTINUE" button again if you want to make any changes. If not please press the "UPDATE COURSE" button below.', style={
                           'textAlign': 'left', 'font-weight': 'bold', 'color': 'red'}),
                    html.Br(),
                    dcc.Input(id="updateComment", type="text",
                              placeholder="What was updated ?", debounce=True),
                    html.Button('Update course',
                                id='updateCourseWithComment-btn', n_clicks=0),
                    html.Div(id='updateCourseWithComment-output'),
                ])

            except:
                div = html.Div([
                    html.P('Please complete all required information',
                           style={'font-style': 'italic', 'color': 'red'}),
                ])
                propsedCourse0 = 0

        # similarCoursesPDF=similarCoursesPDF.to_json()
        return div, propsedCourse0
    else:
        raise PreventUpdate


# updating existing course
@app.callback(
    Output('updateCourseWithComment-output', 'children'),
    Output('loading-output-6', 'children'),
    Input('updateCourseWithComment-btn', 'n_clicks'),
    State('updateComment', 'value'),
    State('session1Type', 'data'),
    State('store_propsedCourse', 'data'),
    State('course_code', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, updateComment, userEmail, store_propsedCourse, course_code):
    if (n_clicks != 0):
        if (updateComment != None):
            course_code = course_code.split(
                "-")[0].strip(" ")  # get only course code
            print("running update_course_data")
            msg, crsUpdated = update_course_data(
                engineCourseApp, mgDB, course_code, store_propsedCourse, updateComment, userEmail)
            print("completed update_course_data")

            # check course exists
            courseShortName = course_code
            existingContent = [crs for crs in call(webserviceAccessParamsCourse, 'core_course_search_courses', criterianame='search', criteriavalue=courseShortName)[
                'courses'] if crs['shortname'] == courseShortName]

            templateShortName = templateCourseSpecifications
            # Create a course 4m template
            if len(existingContent) == 0:
                createdCourseInfo = create_course_4m_course_db(
                    engineCourse, engineCourseApp, webserviceAccessParamsCourse, course_code, templateShortName, userEmail)
                parameters = {'webserviceAccessParams': webserviceAccessParamsCourse, 'access_parameters': {
                    'gToken': githubToken, 'gUser': course_githubUser}, 'repoName': course_code, 'updateComment': 'course created'}
                msg2 = course_content_GitHub_push(
                    mgGH, engineCourse, parameters)
                msgOut = "Course metadata created"
            else:
                update_moodle_course_info_4m_course_db(
                    engineCourse, engineCourseApp, webserviceAccessParamsCourse, course_code)
                parameters = {'webserviceAccessParams': webserviceAccessParamsCourse, 'access_parameters': {
                    'gToken': githubToken, 'gUser': course_githubUser}, 'repoName': course_code, 'updateComment': 'course created'}
                msg2 = course_content_GitHub_push(
                    mgGH, engineCourse, parameters)
                msgOut = "Course metadata updated"
            print(msg2)

            div = html.Div([
                html.P(msg),
                html.P(msgOut),
                html.Br(),
                html.A(html.Button('Clear fields to add a new entry',
                       id='clearFields-btn', n_clicks=0), href='#CCtop'),
            ])
        else:
            div = html.Div([
                html.P('Please enter update comment', style={
                       'font-style': 'italic', 'color': 'red'})
            ])

        return div, 1

    else:
        raise PreventUpdate


# 2course creation -  proceed button clicked after selecting course to update - Course update history shown
@app.callback(
    Output('after_select_course_to_update-output', 'children'),
    Input('after_select_course_to_update-btn', 'n_clicks'),
    State('session1Type', 'data'),
    State('course_code', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, userEmail, course_code):

    if (n_clicks != 0):
        msg = 'Editing as: '+userEmail
        msg2 = 'Course to be updated: ' + course_code

        course_code = course_code.split(
            "-")[0].strip(" ")  # get only course code

        updateCourseCode = course_code
        courseUpdateHistoryPDF = pd.read_sql('SELECT * FROM course_update_history WHERE course_code="{}"'.format(
            updateCourseCode), engineCourseApp).drop(columns=['course_update_history_id', 'course_update_comment'])
        courseUpdateHistoryPDF = courseUpdateHistoryPDF.sort_index(
            ascending=False)

        div = html.Div(id='div_course_update_history', children=[
            html.P(msg),
            html.P(msg2),
            html.Br(),

            html.Div([
                # html.H5('Course update history',style={'textAlign': 'center'}),

                html.H5([
                    html.H5("Course Update History", style={
                            "font-weight": "bold", "display": "inline"}),
                    UI_toolTipIcon("courseUpdateHistory"),
                ], style={'textAlign': 'center'}),

                UI_toolTip("courseUpdateHistory",
                           "Update history of the selected course will be displayed here in the chronological order."),



                UI_PDFtoTable(courseUpdateHistoryPDF),
            ]),

            html.Button('Update', id='courseCreationAppView-btn', n_clicks=0),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Div(id='courseCreationAppView-output'),



        ])

        return div

    else:
        raise PreventUpdate


# 2course creation - update button clicked after viewing course update history
@app.callback(
    Output("courseCreationAppView-output", "children"),
    Input("courseCreationAppView-btn", "n_clicks"),
    State('course_code', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, course_code):
    course_code = course_code.split("-")[0].strip(" ")

    programDomains = list(set(pd.read_sql(
        'SELECT Domain From HECoS_CAH', engineCourseApp)['Domain'].to_list()))
    programDomains.sort()

    updateCourseCode = course_code
    courseUpdateHistoryPDF = pd.read_sql('SELECT * FROM course_update_history WHERE course_code="{}"'.format(
        updateCourseCode), engineCourseApp).drop(columns=['course_update_history_id', 'course_update_comment'])
    updateCourseDict = courseUpdateHistoryPDF.to_dict(orient='records')[-1]

    # addin autofill option - last history taken and filled into fields - 24 Jul 2022

    CAH3_skill_txt = updateCourseDict['CAH3_skill_classification']

    def get_ILO_data_from_history(ILO_name, updateCourseDict):
        # ILO_name='ILO2'
        ILOx = updateCourseDict[ILO_name]

        if (ILOx != '' and ILOx != None):  # ILO is not empty
            # if(ILOx!=''):#ILO is not empty
            # lstrip() to remove left starting space
            ILOx_verb = ILOx.split('#', 2)[1].lstrip()
            ILOx_txt = ILOx.split('#', 2)[2].lstrip()
        else:
            ILOx_verb = None
            ILOx_txt = None
        return ILOx_verb, ILOx_txt

    ILO1_verb, ILO1_txt = get_ILO_data_from_history('ILO1', updateCourseDict)
    ILO2_verb, ILO2_txt = get_ILO_data_from_history('ILO2', updateCourseDict)
    ILO3_verb, ILO3_txt = get_ILO_data_from_history('ILO3', updateCourseDict)
    ILO4_verb, ILO4_txt = get_ILO_data_from_history('ILO4', updateCourseDict)
    ILO5_verb, ILO5_txt = get_ILO_data_from_history('ILO5', updateCourseDict)
    ILO6_verb, ILO6_txt = get_ILO_data_from_history('ILO6', updateCourseDict)

    ILOmaptemp = updateCourseDict['credit_to_ILO_map']
    # ILOmaptemp='1.9, 2.15, 2.05, 1.85, 2.3'
    # ILOmaptemp=''

    if (ILOmaptemp != None):
        ILOmaptemp = ILOmaptemp.split(',')
    else:
        ILOmaptemp = ['']

    # print(ILOmaptemp[0])
    # print(type(ILOmaptemp[0]))

    credit_to_ILO_map_list = [0, 0, 0, 0, 0, 0]
    idx = 0
    if (ILOmaptemp[0] != ''):  # Assign values if not empty
        for val in ILOmaptemp:
            credit_to_ILO_map_list[idx] = float(val)
            idx = idx+1

    course_objective = updateCourseDict['course_objective']

    div = html.Div(id='div_enterCCdata', children=[

        # html.P('Select classification',style={'textAlign': 'left','font-weight': 'bold'}),

        html.P([
            html.P("Select classification", style={
                   "font-weight": "bold", "display": "inline"}),
            UI_toolTipIcon("selectClassificationUpdateCourse"),
        ], style={'textAlign': 'left'}),

        UI_toolTip("selectClassificationUpdateCourse",
                   "If you want to set/change the CAH3 classification of the course you can change it here. If it's already selected and you don't want to change, keep the selection as it is."),


        div_skillSelectionCourseCreation(programDomains, CAH3_skill_txt, 1),
        html.Br(),
        # html.P('Enter ILOs',style={'textAlign': 'left','font-weight': 'bold'}),

        html.P([
            html.P("Enter ILOs", style={
                   "font-weight": "bold", "display": "inline"}),
            UI_toolTipIcon("enterIlosUpdateCourse"),
        ], style={'textAlign': 'left'}),

        UI_toolTip("enterIlosUpdateCourse",
                   "You can enter new ILOs or edit the existing ILOs here. Maximum of 6 ILOs are allowed. Minimum ILO count is 1."),

        # ,"the structure of organisms that affects their ability to survive and reproduce1"),
        UI_ILOx(1, ILO1_verb, ILO1_txt, credit_to_ILO_map_list[0], 1),
        # ,"the structure of organisms that affects their ability to survive and reproduce2"),
        UI_ILOx(2, ILO2_verb, ILO2_txt, credit_to_ILO_map_list[1], 1),
        # ,"the structure of organisms that affects their ability to survive and reproduce3"),
        UI_ILOx(3, ILO3_verb, ILO3_txt, credit_to_ILO_map_list[2], 1),
        # ,"the structure of organisms that affects their ability to survive and reproduce4"),
        UI_ILOx(4, ILO4_verb, ILO4_txt, credit_to_ILO_map_list[3], 1),
        # ,"the structure of organisms that affects their ability to survive and reproduce5"),
        UI_ILOx(5, ILO5_verb, ILO5_txt, credit_to_ILO_map_list[4], 1),
        # ,"the structure of organisms that affects their ability to survive and reproduce6"),
        UI_ILOx(6, ILO6_verb, ILO6_txt, credit_to_ILO_map_list[5], 1),

        # html.P('Credit to ILO MAP(Enter values seperated by commas)',style={'font-weight': 'bold','textAlign': 'left','marginLeft': 20}),
        # dcc.Input(
        #     id='ILO_Map_in',
        #     type="text",
        #     value='',
        #     placeholder="1.0,1.0,0.5,0.5",
        #     style={'width': '25%','marginLeft': 20},
        # ),

        html.Br(),
        html.Br(),
        # html.P('Objective',style={'font-weight': 'bold','textAlign': 'left','marginLeft': 20}),

        html.P([
            html.P("Objective", style={
                   "font-weight": "bold", "display": "inline"}),
            UI_toolTipIcon("updateCourseObjective"),
        ], style={'textAlign': 'left', 'marginLeft': 20}),

        UI_toolTip("updateCourseObjective",
                   "Add new or modify the existing course objective."),


        dcc.Input(id='objective_text', type='text', value=course_objective,
                  placeholder="The aim of this course is to...", style={'marginLeft': 20, 'width': '90%'}),
        html.Br(),
        html.Br(),
        html.Button('Continue', id='continue-btn',
                    n_clicks=0, style={'marginLeft': 20}),
        html.Div(id='continueCourse-output'),
    ])

    return div


@app.callback(
    Output("downloadTemplate-dwn", "data"),
    Input("downloadTemplate-btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "Templates/temp2234.csv"
    )

# Clear fields button - clears main divs by sending empty div


@app.callback(
    # Output("text_ILO11", "value"),
    # Output("text_ILO21", "value"),
    # Output("text_ILO31", "value"),
    # Output("text_ILO41", "value"),
    # Output("text_ILO51", "value"),
    # Output("text_ILO61", "value"),
    # Output("solo_level_ILO11", "value"),
    # Output("solo_level_ILO21", "value"),
    # Output("solo_level_ILO31", "value"),
    # Output("solo_level_ILO41", "value"),
    # Output("solo_level_ILO51", "value"),
    # Output("solo_level_ILO61", "value"),
    # Output("objective_text", "value"),
    Output("course_code", "value"),  # ****
    # Output("program_domainCC1", "value"),
    Output("div_course_update_history", "children"),  # ****
    # Output("div_proposed_CDetails", "children"),#****
    # Output("div_enterCCdata", "children"),#****
    Input('clearFields-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def func(n_clicks):
    if (n_clicks != 0):
        div = html.Div()
        # return '','','','','','',None,None,None,None,None,None,'','',None,div,div,div
        # return None,div,div,div
        return None, div

    else:
        raise PreventUpdate


# Course creation - 20 Dec 2022
@app.callback(
    Output("after_select_course_to_create-output", "children"),
    Output("course_code", "options"),
    Output('loading-output-7', 'children'),
    Input("after_select_course_to_create-btn", "n_clicks"),
    State("newCourseCodeCreate", "value"),
    State("newCourseNameCreate", "value"),
    State("program_skillCC2", "value"),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, newCourseCodeCreate, newCourseNameCreate, program_skillCC2, email):
    if (n_clicks != 0):

        existingCourseList = pd.read_sql('SELECT course_code FROM course WHERE course_code="{}"'.format(
            newCourseCodeCreate), engineCourseApp)['course_code'].to_list()

        if (len(existingCourseList) == 0):  # course not exist: allow user to create course
            # print("course not exist")

            params = {
                'db_table_name': 'course',
                'updateDict': {
                    'course_code': newCourseCodeCreate,
                    'course_name': newCourseNameCreate,
                    'CAH3_skill_classification': program_skillCC2,
                    'course_updated_by': email,
                    'course_updated_on': datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S"),
                    'ILO1': '',
                    'ILO2': '',
                    'ILO3': '',
                    'ILO4': '',
                    'ILO5': '',
                    'ILO6': '',
                    'course_credits': 0,
                    'course_objective': '',
                    'course_keywords': '',
                    'credit_to_ILO_map': '',
                    'SOLO_level': '',
                    'BLOOMS_level': '',
                    'course_rating': 0,
                }
            }

            # Only allow A-Za-z0-9
            courseCodeCheck = bool(
                re.search('^[A-Za-z0-9]*$', newCourseCodeCreate))
            if (newCourseCodeCreate != None and newCourseNameCreate != None and program_skillCC2 != None and program_skillCC2 != "" and courseCodeCheck):
                # print("program_skillCC2 ",program_skillCC2)

                msg = insert_course(engineCourseApp, params)
                params['db_table_name'] = 'course_update_history'
                msg2 = insert_course(engineCourseApp, params)

                # createdCourseInfo=create_course_4m_course_db(engineCourse,engineCourseApp,webserviceAccessParamsCourse,newCourseCodeCreate,templateShortName,email)

                # parameters={'webserviceAccessParams':webserviceAccessParamsCourse,'access_parameters':{'gToken':githubToken, 'gUser':course_githubUser}, 'repoName':newCourseCodeCreate, 'updateComment':'course created'}

                # course_content_GitHub_push(mgGH,engineCourse,parameters)

                templateShortName = templateCourseSpecifications

                parameters = {'webserviceAccessParams': webserviceAccessParamsCourse, 'access_parameters': {
                    'gToken': githubToken, 'gUser': course_githubUser}, 'repoName': newCourseCodeCreate, 'userEmail': email, 'templateShortName': templateShortName}

                create_update_course_4m_course_db(
                    mgGH, engineCourse, engineCourseApp, parameters)

                txt = "Please proceed to the update section to specify the ILOs and complete the course creation process."
                userCourseListPDF = pd.read_sql(
                    'SELECT * FROM course WHERE course_updated_by LIKE "%{}%"'.format(email), engineCourseApp)  # multiple users added
                userCourseList = userCourseListPDF['course_code'].to_list()

            else:
                msg = "Invalid input. Please fill all fields as instructed."
                txt = ""
                userCourseList = []

            div = html.Div([
                html.P(msg),
                html.P(txt)

            ])

        else:  # course already exist: prevent creating the course
            div = html.Div("Course code already exists")
            userCourseList = []

        return div, userCourseList, 1
    else:
        raise PreventUpdate


# Classroom create - click proceed after select classfication
@app.callback(
    Output("after_select_classificationClassroom-output", "children"),
    Input("after_select_classificationClassroom-btn", "n_clicks"),
    State("program_skillCC3", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, program_skillCC3):
    if (n_clicks != 0):

        userCourseListPDF = pd.read_sql("SELECT course_code, course_name FROM course WHERE CAH3_skill_classification='{}'".format(
            program_skillCC3), engineCourseApp)

        userCourseList = userCourseListPDF['course_code'].str.cat(
            ['-'+zz for zz in userCourseListPDF['course_name'].to_list()])

        div = html.Div([
            html.P('Pick course', style={
                   'textAlign': 'left', 'font-weight': 'bold'}),
            UI_dropdown("classroomCreateSelectedCourse", userCourseList),

            html.Button(
                'Create classroom', id='after_select_course_to_createClassroom-btn', n_clicks=0),
            html.Div(id='after_select_course_to_createClassroom-output'),

        ]),

        return div


# Classroom creation - 19 Jan 2023
@app.callback(
    Output("after_select_course_to_createClassroom-output", "children"),
    # Output("course_codeClassroom", "options"),
    Output('loading-output-8', 'children'),
    Input("after_select_course_to_createClassroom-btn", "n_clicks"),
    State("classroomCreateSelectedCourse", "value"),
    State("program_skillCC3", "value"),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, classroomCreateSelectedCourse, program_skillCC, email):
    if (n_clicks != 0):
        courseCodeClassroom = classroomCreateSelectedCourse.split(
            "-")[0].strip(" ")  # get only course code
        userName = pd.read_sql('SELECT course_updated_by FROM course WHERE course_code="{}"'.format(
            courseCodeClassroom), engineCourseApp)['course_updated_by'].to_list()[0]
        templateShortName = templateClassroom

        # pick correct webservice params depending on the institution email
        emailDomain = email.split("@")[-1]

        webserviceAccessParamsClassroom = classroomDetails[emailDomain][0]

        engineClassroom = classroomDetails[emailDomain][1]

        parameters = {'webserviceAccessParams': webserviceAccessParamsClassroom, 'access_parameters': {'gToken': githubToken,
                                                                                                       'gUser': course_githubUser}, 'repoName': courseCodeClassroom, 'userEmail': email, 'templateShortName': templateShortName}

        # pick engineClassroom depending on the institution email - todo
        output = create_classroom_4m_course_db(
            mgGH, engineClassroom, engineCourseApp, parameters)

        # enrol
        # userRoleShortName=limitedEditingTeacher
        userRoleShortName = EditingTeacher  # added editing privileges 11Jun2023
        enrolMsg = manual_enroll_user_in_course(
            webserviceAccessParamsClassroom, courseCodeClassroom, userName, userRoleShortName, engineClassroom)

        div = html.Div([
            html.A(html.P('Visit classroom'), href=output, target="_blank"),
            html.P(output),
            html.P(enrolMsg),

        ])

        return div, 1
    else:
        raise PreventUpdate


# click proceed after skill selection - Add content 19 Jan 2023

@app.callback(
    Output("after_select_classificationAddContent-output", "children"),
    Input("after_select_classificationAddContent-btn", "n_clicks"),
    State("program_skillCC4", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, program_skillCC):
    if (n_clicks != 0):
        chosenCategoryID = call(webserviceAccessParamsContent, 'core_course_get_categories ', criteria=[
                                {'key': 'name', 'value': program_skillCC}])[0]['id']

        categoryContentListPDF = pd.DataFrame(call(webserviceAccessParamsContent, 'core_course_get_courses_by_field',
                                              field='category', value=str(chosenCategoryID))['courses'])  # New 11/12/2022

        if (len(categoryContentListPDF) != 0):
            categoryContentList = categoryContentListPDF['shortname'].to_list()
            categoryContentList.sort()

            div = html.Div([
                html.P('Pick content', style={
                       'textAlign': 'left', 'font-weight': 'bold'}),
                UI_dropdown("addContentSelected", categoryContentList),

                html.Button('Choose content',
                            id='after_select_content-btn', n_clicks=0),
                html.Div(id='after_select_content-output'),

            ]),
        else:
            msg = "No content in catogory "+program_skillCC
            div = html.Div([
                html.P(msg, style={'textAlign': 'left',
                       'font-weight': 'bold', 'color': 'red'}),
            ]),

        return div


# click proceed after Pick category content
@app.callback(
    Output("after_select_content-output", "children"),
    Output("store_moduleNameUrlList", "data"),
    Input("after_select_content-btn", "n_clicks"),
    State("addContentSelected", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, courseShortName):
    if (n_clicks != 0):
        chosenCourseSummaryDict = [crs for crs in call(webserviceAccessParamsContent, 'core_course_search_courses', criterianame='search', criteriavalue=courseShortName)[
            'courses'] if crs['shortname'] == courseShortName][0]
        courseModules = get_course_modules(
            webserviceAccessParamsContent, courseShortName)

        moduleNamesUrls = {}
        for secn in courseModules:
            if len(secn['sectionmodules']) != 0:
                for mod in secn['sectionmodules']:
                    moduleNamesUrls[mod['name']] = mod['url']

        moduleNameUrlList = [*moduleNamesUrls]

        div = html.Div([
            html.P('Choose module', style={
                   'textAlign': 'left', 'font-weight': 'bold'}),
            UI_dropdown("addContentChosenContent", moduleNameUrlList),

            html.Button(
                'Proceed', id='after_select_addContentChosenContent-btn', n_clicks=0),
            html.Div(id='after_select_addContentChosenContent-output'),

        ]),

        return div, moduleNamesUrls
    else:
        raise PreventUpdate

# Add content - Proceed after choose content


@app.callback(
    Output("after_select_addContentChosenContent-output", "children"),
    Input("after_select_addContentChosenContent-btn", "n_clicks"),
    State("store_moduleNameUrlList", "data"),
    State("addContentChosenContent", "value"),
    State("program_skillCC4", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, moduleNamesUrls, chosenMod, program_skillCC):
    if (n_clicks != 0):
        URL = moduleNamesUrls[chosenMod]
        URL = URL.replace("https://127.0.0.1", serverURL)

        # categoryContentName2Id={crs['shortname']:crs['id'] for crs in categoryContentListPDF.to_dict(orient='records')}

        div = html.Div([
            html.A(html.P('View content'), href=URL, target="_blank"),
            html.Button('Confirm that you want to add the above content?',
                        id='viewConfirm-btn', n_clicks=0),
            html.Div(id='viewConfirm-output'),

            # html.P('Choose classroom to add',style={'textAlign': 'left','font-weight': 'bold'}),
            # UI_dropdown("chosenClassroom2add",categoryContentList),
            # html.Button('Proceed', id='chosenClassroom2add-btn', n_clicks=0),
            # html.Div(id='chosenClassroom2add-output'),
        ])

        return div

# catogory selection for classroom - 01/02/2023


@app.callback(
    Output("viewConfirm-output", "children"),
    Output("store_githubPullModDict", "data"),
    Output('loading-output-9', 'children'),
    Input("viewConfirm-btn", "n_clicks"),
    State("addContentChosenContent", "value"),
    State("addContentSelected", "value"),
    prevent_initial_call=True,
)
def func(n_clicks, chosenModName, contentShortName):
    if (n_clicks != 0):
        try:
            programDomains = list(set(pd.read_sql(
                'SELECT Domain From HECoS_CAH', engineCourseApp)['Domain'].to_list()))
            programDomains.sort()

            chosenGithubContentName = contentShortName
            paramsGitHub = {'gToken': githubToken,
                            'gUser': content_githubUser, 'repoName': chosenGithubContentName}
            githubContent = get_GitHub_repo_content(mgGH, paramsGitHub)
            gitHubModuleInfo = {secn['id']: mod for secn in githubContent['contentSecnsSummary.json']
                                for mod in secn['modules'] if mod['name'] == chosenModName}

            githubModSecnID = [*gitHubModuleInfo][0]
            githubModID = gitHubModuleInfo[githubModSecnID]['id']
            githubModType = gitHubModuleInfo[githubModSecnID]['modname']
            githubModInstance = gitHubModuleInfo[githubModSecnID]['instance']
            githubContentName = 'section_{}_content/mod_{}_{}_{}.json'.format(
                githubModSecnID, githubModID, githubModType, githubModInstance)

            githubModSecnID = [*gitHubModuleInfo][0]
            githubModID = gitHubModuleInfo[githubModSecnID]['id']
            githubModType = gitHubModuleInfo[githubModSecnID]['modname']
            githubModInstance = gitHubModuleInfo[githubModSecnID]['instance']
            githubContentName = 'section_{}_content/mod_{}_{}_{}.json'.format(
                githubModSecnID, githubModID, githubModType, githubModInstance)

            githubPullModDict = githubContent[githubContentName]

            div = html.Div([
                html.P('Select classification', style={
                       'textAlign': 'left', 'font-weight': 'bold'}),
                div_skillSelectionCourseCreation(programDomains, '', 5),

                html.Button(
                    'Proceed', id='after_select_classification5-btn', n_clicks=0),
                html.Div(id='after_select_classification5-output'),
            ])

            return div, githubPullModDict, 1

        except:
            div = html.Div([
                html.P('Content not updated in version control', style={
                       'textAlign': 'left', 'font-weight': 'bold'}),
            ])

            return div, {}, 1
    else:
        raise PreventUpdate


# proceed after selecting catagory for classroom
@app.callback(
    Output("after_select_classification5-output", "children"),
    Input("after_select_classification5-btn", "n_clicks"),
    State("addContentChosenContent", "value"),
    State("addContentSelected", "value"),
    State("program_skillCC5", "value"),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, chosenModName, contentShortName, program_skillCC, email):
    if (n_clicks != 0 and program_skillCC != ""):
        emailDomain = email.split("@")[-1]
        webserviceAccessParamsClassroom = classroomDetails[emailDomain][0]
        engineClassroom = classroomDetails[emailDomain][1]

        chosenCategoryID = call(webserviceAccessParamsClassroom, 'core_course_get_categories ', criteria=[
                                {'key': 'name', 'value': program_skillCC}])[0]['id']

        categoryContentListPDF = pd.DataFrame(call(webserviceAccessParamsClassroom, 'core_course_get_courses_by_field',
                                              field='category', value=str(chosenCategoryID))['courses'])  # New 11/12/2022

        if (len(categoryContentListPDF) != 0):
            categoryContentList = categoryContentListPDF['shortname'].to_list()
            categoryContentList.sort()

            div = html.Div([
                html.P('Choose classroom to add', style={
                       'textAlign': 'left', 'font-weight': 'bold'}),
                UI_dropdown("chosenClassroom2add", categoryContentList),
                html.Button(
                    'Proceed', id='chosenClassroom2add-btn', n_clicks=0),
                html.Div(id='chosenClassroom2add-output'),
            ])
        else:
            txt = 'No classrooms in '+program_skillCC
            div = html.Div([
                html.P(txt, style={'textAlign': 'left',
                       'font-weight': 'bold', 'color': 'red'}),
            ])

        return div

    elif (n_clicks != 0 and program_skillCC == ""):
        div = html.Div([
            html.P("Please select a catogory"),
        ])

    else:
        raise PreventUpdate


# proceed click after Choose classroom to add
@app.callback(
    Output("chosenClassroom2add-output", "children"),
    Output("store_secnHVPModules", "data"),
    Input("chosenClassroom2add-btn", "n_clicks"),
    State("chosenClassroom2add", "value"),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, chosenClassShortName, email):
    if (n_clicks != 0):
        emailDomain = email.split("@")[-1]
        webserviceAccessParamsClassroom = classroomDetails[emailDomain][0]
        engineClassroom = classroomDetails[emailDomain][1]

        chosenClassSummaryDict = [crs for crs in call(webserviceAccessParamsClassroom, 'core_course_search_courses', criterianame='search', criteriavalue=chosenClassShortName)[
            'courses'] if crs['shortname'] == chosenClassShortName][0]
        classSecnModules = get_course_modules(
            webserviceAccessParamsClassroom, chosenClassShortName)
        secnHVPModules = {}
        for secn in classSecnModules:
            if len(secn['sectionmodules']) != 0:
                secnHVPModules[secn['sectionname']] = [
                    mod for mod in secn['sectionmodules'] if mod['modname'] == 'hvp']

        optionList = [*secnHVPModules]
        siteURLpublicClassroom = webserviceAccessParamsClassroom['PURL']
        classroomLink = siteURLpublicClassroom + \
            '/course/view.php?id={}'.format(chosenClassSummaryDict['id'])

        div = html.Div([
            html.A(html.P('Visit classroom'),
                   href=classroomLink, target="_blank"),

            html.P('Choose section to add', style={
                   'textAlign': 'left', 'font-weight': 'bold'}),
            UI_dropdown("chosenSection2add", optionList),
            html.Button('Proceed', id='chosenSection2add-btn', n_clicks=0),
            html.Div(id='chosenSection2add-output'),
        ])

        return div, secnHVPModules

    else:
        raise PreventUpdate

# procced click after chosenSection2add


@app.callback(
    Output("chosenSection2add-output", "children"),
    Input("chosenSection2add-btn", "n_clicks"),
    State("chosenSection2add", "value"),
    State("store_secnHVPModules", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, chosenSectionName, secnHVPModules):
    if (n_clicks != 0):
        chosenSectionHVPs = secnHVPModules[chosenSectionName]
        chosenSectionHVPNames = [hvp['name'] for hvp in chosenSectionHVPs]

        div = html.Div([
            html.P('Choose content to be replaced', style={
                   'textAlign': 'left', 'font-weight': 'bold'}),
            UI_dropdown("chosenContent2bReplaced", chosenSectionHVPNames),
            html.Button(
                'Proceed', id='chosenContent2bReplaced-btn', n_clicks=0),
            html.Div(id='chosenContent2bReplaced-output'),
        ])

        return div
    else:
        raise PreventUpdate


# click proceed after Choose content to be replaced
@app.callback(
    Output("chosenContent2bReplaced-output", "children"),
    Input("chosenContent2bReplaced-btn", "n_clicks"),
    State("chosenClassroom2add", "value"),  # chosenClassShortName
    State("chosenSection2add", "value"),  # chosenSectionName
    State("chosenContent2bReplaced", "value"),  # chosenHVP2updateName
    State("store_githubPullModDict", "data"),  # githubPullModDict
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, chosenClassShortName, chosenSectionName, chosenHVP2updateName, githubPullModDict, email):
    if (n_clicks != 0):
        emailDomain = email.split("@")[-1]
        webserviceAccessParamsClassroom = classroomDetails[emailDomain][0]
        engineClassroom = classroomDetails[emailDomain][1]

        parameters = {'chosenCourseShortName': chosenClassShortName, 'sectionName': chosenSectionName, 'chosenModType': 'hvp',
                      'moduleName': chosenHVP2updateName, 'webserviceAccessParams': webserviceAccessParamsClassroom, 'githubPullModDict': githubPullModDict}
        msg = update_course_module_from_GitHub(engineClassroom, parameters)
        print(msg)

        div = html.Div([
            # html.A(html.P('Visit classroom'),href=output),
            html.P('Module successfully updated'),
        ])

        return div
    else:
        raise PreventUpdate


# ===================PO to ILO mapping all callbacks======================
@app.callback(
    Output('selectProgram_ILOtoPOmapping-output', 'children'),
    Input('selectProgram_ILOtoPOmapping-btn', 'n_clicks'),
    State('selectedProgram_ILOtoPOmapping', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, selectedProgram_ILOtoPOmapping):
    selectedProgram = selectedProgram_ILOtoPOmapping.split(' (')[0]
    selectedProgramCourseList = pd.read_sql('SELECT course_code FROM program_structure WHERE program_code="{}"'.format(
        selectedProgram), engineCourseApp)['course_code'].to_list()

    div = html.Div([
        html.Br(),
        html.P('Please select course code'),

        html.Div([
            UI_dropdown('course2MapCode', selectedProgramCourseList, {
                        'width': '100%'}),
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div([
            html.Button('Proceed', id='selectCC_ILO2PLO-btn', n_clicks=0)
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div(id='selectCC_ILO2PLO-output')
    ]),

    return div


@app.callback(
    Output('selectCC_ILO2PLO-output', 'children'),
    Input('selectCC_ILO2PLO-btn', 'n_clicks'),
    State('selectedProgram_ILOtoPOmapping', 'value'),
    State('course2MapCode', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, selectedProgram_ILOtoPOmapping, course2MapCode):
    selectedProgram = selectedProgram_ILOtoPOmapping
    selectedProgram = selectedProgram_ILOtoPOmapping.split(' (')[0]

    selectedCourseInfoPDF = pd.read_sql(
        'SELECT course_code, course_name, course_credits, ILO1, ILO2, ILO3, ILO4, ILO5, ILO6 FROM course WHERE course_code="{}"'.format(course2MapCode), engineCourseApp)
    selectedCourseInfoDict = selectedCourseInfoPDF.to_dict(orient='records')[0]
    ILOdictNotEmpty = {ky: selectedCourseInfoDict[ky] for ky in [
        'ILO1', 'ILO2', 'ILO3', 'ILO4', 'ILO5', 'ILO6'] if selectedCourseInfoDict[ky] != ''}
    ILOlist = [ky+':'+ILOdictNotEmpty[ky] for ky in [*ILOdictNotEmpty]]
    selectedCourseProgramStructurePDF = pd.read_sql(
        'SELECT course_code, PO1,PO2,PO3,PO4,PO5,PO6,PO7,PO8,PO9,PO10,PO11,PO12,PO13,PO14,PO15 FROM program_structure WHERE program_code="{}" AND course_code="{}"'.format(selectedProgram, course2MapCode), engineCourseApp)
    ILO_count = len(ILOlist)

    POdict = pd.read_sql('SELECT PO1,PO2,PO3,PO4,PO5,PO6,PO7,PO8,PO9,PO10,PO11,PO12,PO13,PO14,PO15 FROM program WHERE program_code="{}"'.format(
        selectedProgram), engineCourseApp).fillna("").to_dict(orient='records')[0]
    POdictNotEmpty = {ky: POdict[ky] for ky in [*POdict] if POdict[ky] != ''}
    POList = [ky+':'+POdictNotEmpty[ky] for ky in [*POdictNotEmpty]]

    if (ILO_count != 0 and POList != []):
        POList1 = [{'PO': ele.split(':')[0], 'Description': ele.split(':')[
            1]} for ele in POList]
        PO_df = pd.DataFrame(POList1)[['PO', 'Description']]

        div = html.Div([
            html.Br(),
            html.P('Existing ILO to PO mapping'),
            UI_PDFtoTable(selectedCourseProgramStructurePDF, '100px'),

            html.P('PO information'),
            UI_PDFtoTable(PO_df),
            html.Br(),

            html.P('Course information'),
            UI_PDFtoTable(selectedCourseInfoPDF, '130px'),

            html.Br(),
            UIapp_POmappingBox(ILO_count, POList),
            html.P('Update comment'),
            dcc.Textarea(id="POmappingUpdateComment", value="ILO to PO map added", style={
                         'width': '100%', 'height': 50}),
            html.Button('Proceed', id='afterPOmapping-btn', n_clicks=0),
            html.Div(id='afterPOmapping-output'),
        ])
    elif (ILO_count == 0):
        div = html.Div([
            html.P("ILOs not specified!")
        ])

    elif (POList == []):
        div = html.Div([
            html.P("POs not specified!")
        ])

    return div


# user click proceed after mapping POs
@app.callback(
    Output("afterPOmapping-output", "children"),
    Input("afterPOmapping-btn", "n_clicks"),
    State('selectedPO_ILO1', 'value'),
    State('selectedPO_ILO2', 'value'),
    State('selectedPO_ILO3', 'value'),
    State('selectedPO_ILO4', 'value'),
    State('selectedPO_ILO5', 'value'),
    State('selectedPO_ILO6', 'value'),
    State('POmappingUpdateComment', 'value'),
    State('selectedProgram_ILOtoPOmapping', 'value'),
    State('course2MapCode', 'value'),
    State('session1Type', 'data'),
    prevent_initial_call=True,
)
def func(n_clicks, selectedPO_ILO1, selectedPO_ILO2, selectedPO_ILO3, selectedPO_ILO4, selectedPO_ILO5, selectedPO_ILO6, POmappingUpdateComment, selectedProgram_ILOtoPOmapping, course2MapCode, userEmail):

    if (selectedPO_ILO1 == None or selectedPO_ILO2 == None or selectedPO_ILO3 == None or selectedPO_ILO4 == None or selectedPO_ILO5 == None or selectedPO_ILO6 == None):

        div = html.Div([
            html.P('Please map all ILOs'),
        ])
    else:
        selectedProgram = selectedProgram_ILOtoPOmapping.split(' (')[0]
        updateComment = POmappingUpdateComment

        selectedPO_ILO1 = selectedPO_ILO1.split(':')[0]
        selectedPO_ILO2 = selectedPO_ILO2.split(':')[0]
        selectedPO_ILO3 = selectedPO_ILO3.split(':')[0]
        selectedPO_ILO4 = selectedPO_ILO4.split(':')[0]
        selectedPO_ILO5 = selectedPO_ILO5.split(':')[0]
        selectedPO_ILO6 = selectedPO_ILO6.split(':')[0]

        # ILO_PO_map=['PO2', 'PO3', 'PO3', 'PO4', '', '']
        ILO_PO_map = [selectedPO_ILO1, selectedPO_ILO2, selectedPO_ILO3,
                      selectedPO_ILO4, selectedPO_ILO5, selectedPO_ILO6]

        selectedPOList = list(set(ILO_PO_map))
        if '' in selectedPOList:
            selectedPOList.remove('')
        selectedPOList.sort()
        selected_PO_ILO_map_list = [','.join(
            [str(i+1) for i in range(len(ILO_PO_map)) if ILO_PO_map[i] == xx]) for xx in selectedPOList]
        msg = update_ILO_PO_map(engineCourseApp, mgDB, selectedProgram, course2MapCode,
                                selectedPOList, selected_PO_ILO_map_list, updateComment, userEmail)

        div = html.Div([
            html.P(msg)
        ])

    return div


# External program mapping 16 Dec 2022

@app.callback(
    Output('display-ext-program-output', 'children'),
    Input('display-ext-program-btn', 'n_clicks'),
    State('selectedProgramExt', 'value'),
    prevent_initial_call=True,)
def func(n_clicks, selectedProgramExt):
    if (n_clicks != 0 and selectedProgramExt != None):

        selectedProgramExt = selectedProgramExt.split(' (')[0]

        mappingPDF = pd.read_sql('SELECT external_program_mapping.external_program_course_code,course.course_code,course.course_name,course.CAH3_skill_classification,course.course_objective,course.course_credits,course.SOLO_level,course.BLOOMS_level,course.credit_to_ILO_map,course.ILO1,course.ILO2,course.ILO3,course.ILO4,course.ILO5,course.ILO6 FROM external_program_mapping INNER JOIN course ON external_program_mapping.course_code=course.course_code WHERE external_program_mapping.program_code="{}"'.format(selectedProgramExt), engineCourseApp)

        # SELECT external_program_mapping.external_program_course_code,course.* FROM external_program_mapping INNER JOIN course ON external_program_mapping.course_code=course.course_code WHERE external_program_mapping.program_code="{}".format(selectedProgramExt)

        div = html.Div([
            # html.P('Table'),
            UI_PDFtoTable(mappingPDF),
            UI_fileDownload('downloadExtProgramList-btn',
                            'downloadExtProgramList-dwn', 'Download data'),

        ])

        return div
    else:
        raise PreventUpdate


# ====================Downloads===========================================
# program structure
@app.callback(
    Output("program_structure_download-download", "data"),
    Input("program_structure_download-btn", "n_clicks"),
    State('selectedProgram', 'value'),
    prevent_initial_call=True,
)
def func(n_clicks, selectedProgram):
    selectedProgram = selectedProgram.split(' (')[0]
    # Generate program structure
    program_structurePDF = pd.read_sql('SELECT * FROM program_structure WHERE program_code="{}"'.format(
        selectedProgram), engineCourseApp).drop(columns=['program_structure_id'])

    filename = selectedProgram+'_' + \
        datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")+'.csv'

    return dcc.send_data_frame(program_structurePDF.to_csv, filename, index=False)


@app.callback(
    Output("course_list_preliminary_stage-dwn", "data"),
    Input("course_list_preliminary_stage-btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "data/course-list-preliminary-stage.csv"
    )


@app.callback(
    Output("TEAL_course_list_compiled-dwn", "data"),
    Input("TEAL_course_list_compiled-btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "data/TEAL-course-list-compiled.csv"
    )


@app.callback(
    Output("TEAL_Program_Structures_ALL-dwn", "data"),
    Input("TEAL_Program_Structures_ALL-btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "data/TEAL-Program-Structures - ALL.csv"
    )


if __name__ == '__main__':
    # app.run_server(debug=False)
    # app.run_server(debug=True)
    app.run_server(debug=True, port=5604)
