import pandas as pd
import csv
import plotly.graph_objects as go
from csv import DictWriter
import datetime
import smtplib
import datetime

from fns import mugas_DB_functions,create_engine
from static_globals import *
from fns_webservice import *

searchModes=['Search by keywords','Search by course code','Search by similar course name','Search by course skills']

csvFilePath='institutional_templates/{}'
mgDB=mugas_DB_functions()

engineCourse = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(userCourse, passwordCourse,hostCourse, dbnameCourse))

engineContent = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(userContent, passwordContent,hostContent, dbnameContent))

#=========================Classroom engines ===================



#Since there are limited institutions engines created seperately

engineClassroom_SERVER = create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(userClassroom_SERVER, passwordClassroom_SERVER,hostClassroom_SERVER,portClassroom_SERVER, dbnameClassroom_SERVER))

engineClassroom_RKU = create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(userClassroom_RKU, passwordClassroom_RKU,hostClassroom_RKU,portClassroom_RKU, dbnameClassroom_RKU))

engineClassroom_AIT = create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(userClassroom_AIT, passwordClassroom_AIT,hostClassroom_AIT,portClassroom_AIT, dbnameClassroom_AIT))



#Classroom moodle data in other partner institutions. Modify as required.
classroomDetails={
    "abc.abc":[webserviceAccessParamsClassroom_SERVER,engineClassroom_SERVER],
    "eng.pdn.ac.lk":[webserviceAccessParamsClassroom_SERVER,engineClassroom_SERVER],
    "rku.ac.in":[webserviceAccessParamsClassroom_RKU,engineClassroom_RKU],
    "sltc.ac.lk":[webserviceAccessParamsClassroom_SERVER,engineClassroom_SERVER],
    "ait.ac.th":[webserviceAccessParamsClassroom_AITTH,engineClassroom_AIT],
    "nu.ac.th":[webserviceAccessParamsClassroom_NUTH,engineClassroom_SERVER],
    "uis.no":[webserviceAccessParamsClassroom_SERVER,engineClassroom_SERVER],
    "unitbv.ro":[webserviceAccessParamsClassroom_SERVER,engineClassroom_SERVER],
    "vit.ac.in":[webserviceAccessParamsClassroom_SERVER,engineClassroom_SERVER],
    "iiita.ac.in":[webserviceAccessParamsClassroom_SERVER,engineClassroom_SERVER],
    "ecq-bg.com":[webserviceAccessParamsClassroom_SERVER,engineClassroom_SERVER]
}

engineCourseApp = create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(userCourseApp, passwordCourseApp,hostCourseApp, dbnameCourseApp))


mgGH=tealMGitHub()


# print(editorRoleID)
# editorRoleID=9
# templateCourseDict=[crs for crs in call(webserviceAccessParamsCourse,'core_course_search_courses',criterianame='search',criteriavalue=shortName)['courses'] if crs['shortname']==shortName][0]
# templateCourseID=templateCourseDict['id']
allCategories=call(webserviceAccessParamsCourse,'core_course_get_categories')
listCategory=[cat['name'] for cat in allCategories if cat['depth']==3]
listCategory.sort()
# contentInfo={}

