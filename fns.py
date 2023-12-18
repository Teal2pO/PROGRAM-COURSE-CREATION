import pandas as pd
import csv
import plotly.graph_objects as go
from csv import DictWriter
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import spacy
nlp = spacy.load("en_core_web_sm")  # make sure to use larger package!

import mysql.connector
import sqlalchemy
from sqlalchemy import *
from pandas.io import sql
from sqlalchemy import text as sql_text



#==========================APP Functions===============================================
def concat_ILOs(verb_ILOx_value,text_ILOx,verbx_flag):
    #ILO1_in,ILO2_in,ILO3_in,ILO4_in,ILO5_in,ILO6_in generation with concatenating strings only if action verb selected. Otherwise considered ''
    if (verbx_flag == 1):
      verb_ILOx_value=verb_ILOx_value.replace(" ", "")#remove # verb# this space
   
    ILOx_in=('#'+verb_ILOx_value+'# '+text_ILOx) if verbx_flag == 1 else ''
    return ILOx_in

def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        valid_email=True
    else:
        valid_email=False
    return valid_email
#=====================================================================================

#send email function
def send_email(senderName,senderEmail,senderEmailPswd,recieverEmail,emailSubject,emailBody):
  # creates SMTP session
  s = smtplib.SMTP('smtp.gmail.com', 587)
  # start TLS for security
  s.starttls()
  # Authentication
  s.login(senderEmail,senderEmailPswd)
  # message to be sent
  toEmails=', '.join(recieverEmail)
  #message = 'From: '+senderName+'<'+senderEmail+'>\n'+'To: <'+toEmails+'>\n'+'Subject: '+emailSubject+'\n\n'+emailBody;
  message = 'From: '+senderName+'<'+senderEmail+'>\n'+'To: <'+toEmails+'>\n'+'Subject: '+emailSubject+'\n\n'+emailBody;

  # sending the mail

  # s.sendmail(senderEmail, recieverEmail, message)

  # terminating the session
  s.quit()
  return print('e-mail sent to '+toEmails)

#DB Query Functions
class mugas_DB_functions:

  def __init__(self):
    self=[];

  def read_table_2_PDF(self,engine,db_table_name):
    return pd.read_sql(db_table_name,engine, index_col=db_table_name+'_id')

  def read_columns_4m_table_2_PDF(self,engine,db_table_name,colNames):
    sqlQuery="SELECT {} FROM {}".format(', '.join(colNames),db_table_name)
    return pd.read_sql(sqlQuery, engine)

  def retrieve_record_2_PDF(self,engine,db_table_name,filterDict):
    filterStrLst=[];
    for fltcol in [*filterDict]:
      filterStrLst+=[fltcol+'="'+str(filterDict[fltcol])+'"']
    filterStr=' AND '.join(filterStrLst)

    sqlQuery="SELECT * FROM {} WHERE {}".format(db_table_name,filterStr)
    return pd.read_sql(sqlQuery, engine)

  def delete_records(self,engine,db_table_name,filterDict):
    filterStrLst=[];
    for fltcol in [*filterDict]:
      filterStrLst+=[fltcol+'="'+str(filterDict[fltcol])+'"']
    filterStr=' AND '.join(filterStrLst)

    sqlQuery="DELETE FROM {} WHERE {}".format(db_table_name,filterStr)
    return sql.execute(sqlQuery, engine)

  def update_records(self,engine,db_table_name, filterDict, updateColNamesList,updateValuesList):
    filterStrLst=[];
    for fltcol in [*filterDict]:
      filterStrLst+=[fltcol+'="'+str(filterDict[fltcol])+'"']
    filterStr=' AND '.join(filterStrLst)
    updatePairs=[clnm+'='+"'"+str(updateValuesList[nn])+"'" for nn,clnm in enumerate(updateColNamesList)]
    sqlQuery='UPDATE {} SET {} WHERE {}'.format(db_table_name,', '.join(updatePairs),filterStr)
    return sql.execute(sqlQuery, engine)

  def insert_records(self, sqlEngine,db_table_name,cols2bUpdated,vals2bUpdated):
      #quick fix  - 21Feb2023
      db_table_PDF0=pd.read_sql(db_table_name, sqlEngine)
      db_table_PDF=db_table_PDF0.drop(columns=[db_table_name+'_id'])
      diffCols=set(cols2bUpdated).difference(set([*db_table_PDF]))
      if len(diffCols) == 0:
        if(len(db_table_PDF.index.values)!=0):#table is not empty
          lastIndex=max(db_table_PDF0[db_table_name+'_id'].to_list())
          # lastIndex=db_table_PDF.index.values[-1]

        else:
          lastIndex=-1#table is empty; no last index    

        insert_entry_PDF=pd.DataFrame(columns=[*db_table_PDF],index=[lastIndex+1]).fillna('')

        insert_entry_PDF.loc[lastIndex+1,cols2bUpdated]=vals2bUpdated
        insert_entry_PDF.to_sql(db_table_name,sqlEngine,if_exists='append',index=True,index_label=db_table_name+'_id')
        msg='Table updated successfully'
      else:
        msg='Insert columns'+', '.join(diffCols)+' not in table'
      return msg


  def get_all_tables(self,sqlEngine):
    return pd.read_sql_query('SHOW TABLES', sqlEngine)

#Program Creation tool Functions
def filter_PDF_by_column(inputPDF,colName,colVals):
  return inputPDF[inputPDF[colName].isin(colVals)]

def pi_plot_values(dataPDF, plotFieldName, valueField, figTitle):
    xx1=[]; yy1=[]; cc1=[]; traceNames1=[];
    for xx in set(dataPDF[plotFieldName].tolist()):
      temp=dataPDF[dataPDF[plotFieldName]==xx];
      xx1+=[xx]
      cc1+=[temp[temp[plotFieldName]==xx]];
      if valueField==None:
        yy1+=[len(temp[temp[plotFieldName]==xx])];
      else:
        yy1+=[sum(temp[temp[plotFieldName]==xx][valueField].tolist())];


    fig = go.Figure()

    fig.add_trace(go.Pie(labels=xx1, values=yy1, name=plotFieldName))


    fig.update_traces(hole=0.4, hoverinfo='label+value+name', textinfo='percent')
    fig.update_layout(
        title_text=figTitle,
        #annotations=[dict(text='Colombo', x=0.18, y=0.5, font_size=15, showarrow=False), dict(text='Anuradhapura', x=0.84, y=0.5, font_size=15, showarrow=False)])
        )
    #fig.show()
    return fig

def get_program_data(SQLengine,DB_access_object,program_structure_DB_table_name,semester_label_DB_name,course_color_map_DB_name,course_type_DB_table_name,program_code0):
  selectedProgramStructurePDF0=pd.read_sql('SELECT * FROM {} WHERE program_code="{}"'.format(program_structure_DB_table_name,program_code0),SQLengine)
  courseTypesList=DB_access_object.read_table_2_PDF(SQLengine,course_type_DB_table_name)
  selectedProgramCourseList=list(set(selectedProgramStructurePDF0['course_code'].to_list()))
  selectedProgramCourseList.sort()
  prgrmCrsCrdts=[]
  prgrmCrsNms=[]
  courseIDs=selectedProgramStructurePDF0.index.values
  for idx in courseIDs:
    tempCourseCode=selectedProgramStructurePDF0.loc[idx,'course_code']
    tempPDF=pd.read_sql('SELECT course_credits, course_name FROM course WHERE course_code="{}"'.format(tempCourseCode),SQLengine)
    print(tempCourseCode)
    prgrmCrsCrdts+=[tempPDF['course_credits'].to_list()[-1]]
    prgrmCrsNms+=[tempPDF['course_name'].to_list()[-1]]
  selectedProgramStructurePDF0.loc[courseIDs,'course_credits']=prgrmCrsCrdts
  selectedProgramStructurePDF0.loc[courseIDs,'course_name']=prgrmCrsNms
  selectedPrgCourseInfoTables={}
  for typ in courseTypesList:
    tmp=filter_PDF_by_column(selectedProgramStructurePDF0,'program_course_type',[typ])
    selectedPrgCourseInfoTables[typ]={'course_information':tmp, 'total_credits':str(tmp['course_credits'].sum())}
  selectedProgramCreditDistFig=pi_plot_values(selectedProgramStructurePDF0, 'program_course_type', 'course_credits', program_code0+'-Credit Distribution')
  figProgramDeliveryPlan=display_program_delivery_plan(SQLengine,DB_access_object,semester_label_DB_name,course_color_map_DB_name,selectedProgramStructurePDF0)

  return [selectedProgramCreditDistFig,figProgramDeliveryPlan,selectedPrgCourseInfoTables,selectedProgramStructurePDF0]

def display_program_delivery_plan(SQLengine,DB_access_object,semester_label_DB_name,course_color_map_DB_name,selectedProgramStructurePDF):
  course_color_map_PDF=DB_access_object.read_table_2_PDF(SQLengine,course_color_map_DB_name)
  semester_label_PDF=DB_access_object.read_table_2_PDF(SQLengine,semester_label_DB_name)
  semesterLabels0=semester_label_PDF.loc[semester_label_PDF.index.values[-1],:].to_list()[:8]
  #[semester_label_PDF[xx].values[0] for xx in [*semester_label_PDF][:-1]]
  chosenProgramDeliveryPlanDict={}
  for sem in semesterLabels0:
    chosenProgramDeliveryPlanDict[sem]=selectedProgramStructurePDF[selectedProgramStructurePDF['program_course_semester']==sem]['course_code'].to_list()

  df=pd.DataFrame.from_dict(chosenProgramDeliveryPlanDict, orient='index').T #.fillna('')

  values=[['Course -'+str(nnn+1) for nnn in df.index.values.tolist()]+['Credits']]
  colorValues=['rgba(0, 0, 0, 0.2)']

  for sem in semesterLabels0:
    colVals=[]
    colColorValues=[]
    semesterCredits=[]

    for nn in df.index.values:
      colVals+=[df.loc[nn,sem]]
      if df.loc[nn,sem]!=None:
        trr=selectedProgramStructurePDF[selectedProgramStructurePDF['course_code']==df.loc[nn,sem]]['program_course_type'].to_list()[0]
        clrtmp=course_color_map_PDF[trr]
        colColorValues+=[clrtmp.to_list()[0]]

        semesterCredits+=[selectedProgramStructurePDF[selectedProgramStructurePDF['course_code']==df.loc[nn,sem]]['course_credits'].values[0]]
      else:
        colColorValues+=['rgba(0, 0, 0, 0)']
        semesterCredits+=[0]
    colVals+=[sum(semesterCredits)]
    colColorValues+=['rgba(0, 0, 0, 0.2)']
    values+=[colVals]
    colorValues+=[colColorValues]

    coloredCells= dict(
      values=values,
      #line_color=colorValues,
      fill_color=colorValues,
      align='center', font=dict(color='black', size=11))

  fig = go.Figure(data=[go.Table(
    header=dict(
      values=['Semester']+semesterLabels0,
      line_color='white', fill_color='rgba(0, 0, 0, 0.2)',#'white',
      align='center', font=dict(color='black', size=14)
    ),

    cells=coloredCells

    )
  ])

  return fig

def update_and_log(SQLEngine,DB_query_object,db_table_name,db_update_history_table_name,filterDict, updateColNames,updateValues,updateComment,userEmail0):
  updateComment=updateComment+' : '
  for ii,xx in enumerate(updateColNames):
    updateComment+=xx+' updated to '+ str(updateValues[ii])+', '

  filterStrLst=[];
  for fltcol in [*filterDict]:
    filterStrLst+=[fltcol+'="'+str(filterDict[fltcol])+'"']
  filterStr=' AND '.join(filterStrLst)

  updateColNames=updateColNames+[db_table_name+'_updated_on',db_table_name+'_updated_by']
  updateValues=updateValues+[datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S"),userEmail0]

  DB_query_object.update_records(SQLEngine,db_table_name, filterDict, updateColNames,updateValues)

  insert_db_table_PDF=pd.read_sql(db_update_history_table_name, SQLEngine)
  lastIndex=insert_db_table_PDF.index.values[-1]


  insert_entry_PDF=pd.read_sql('SELECT * FROM {} WHERE {}'.format(db_table_name,filterStr), SQLEngine).drop(columns=[db_table_name+'_id'])
  cols2bUpdated=[*insert_entry_PDF]+[db_table_name+'_update_comment']
  vals2bUpdated=[insert_entry_PDF[xx].to_list()[0] for xx in [*insert_entry_PDF]]+[updateComment]
  msg=DB_query_object.insert_records(SQLEngine,db_update_history_table_name,cols2bUpdated,vals2bUpdated)
  return msg

def update_delivery_plan(SQLEngine,DB_query_object,db_table_name,semesterLableDBname,course2ColorMapDBname,courseTypeDBname,selectedProgram0,chosenSemesterCourses0,updateSemester0,updateComment,userEmail0):
  for crscd in chosenSemesterCourses0:
    filterDict={'program_code':selectedProgram0, 'course_code':crscd}
    updateColNames=['program_course_semester']
    updateValues=[updateSemester0]
    update_and_log(SQLEngine,DB_query_object,db_table_name,db_table_name+'_update_history',filterDict, updateColNames,updateValues,updateComment,userEmail0)
    [selectedProgramCreditDistFig,figProgramDeliveryPlan,selectedPrgCourseInfoTables,selectedPorgramInfoPDF]=get_program_data(SQLEngine, DB_query_object,db_table_name,semesterLableDBname,course2ColorMapDBname,courseTypeDBname,selectedProgram0)
  return figProgramDeliveryPlan

def get_course_data(SQLengine,DB_access_object,courseCode):
  courseInfoPDF=pd.read_sql('SELECT * FROM course WHERE course_code="{}"'.format(courseCode),SQLengine)
  return courseInfoPDF

def create_course_4m_old_course(SQLengine,DB_access_object,oldCourseCode,newCourseCode,newCourseName,userEmail00):
  courseUpdatePDF=pd.read_sql('SELECT * FROM course WHERE course_code="{}"'.format(oldCourseCode),SQLengine)
  newCourseIfExist=pd.read_sql('SELECT * FROM course WHERE course_code="{}"'.format(newCourseCode),SQLengine)
  if len(newCourseIfExist)!=0:
    msg='Course Exists.'
    crsInfoPDF=newCourseIfExist
  else:
    timeNow=datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    courseUpdatePDF[['course_code','course_name', 'course_updated_on','course_updated_by']]=[newCourseCode, newCourseName, timeNow,userEmail00]
    cols2bUpdated=[*courseUpdatePDF.drop(labels=['course_id'], axis=1)]
    vals2bUpdated=[courseUpdatePDF[xx].to_list()[0] for xx in cols2bUpdated]
    DB_access_object.insert_records(SQLengine,'course',cols2bUpdated,vals2bUpdated)

    lastIndex=pd.read_sql('course_update_history', SQLengine).index.values[-1]

    insert_entry_PDF=courseUpdatePDF.drop(columns=['course_id'])
    cols2bUpdated2=[*insert_entry_PDF]+['course_update_comment']
    vals2bUpdated2=[insert_entry_PDF[xx].to_list()[0] for xx in [*insert_entry_PDF]]+['course cloned from '+oldCourseCode]
    msg=DB_access_object.insert_records(SQLengine,'course_update_history',cols2bUpdated2,vals2bUpdated2)

    msg=newCourseCode+' created at '+timeNow+' by '+userEmail00
    crsInfoPDF=pd.read_sql('SELECT * FROM course WHERE course_code="{}"'.format(newCourseCode),SQLengine)
  return msg, crsInfoPDF




def update_course_data(SQLengine,DB_access_object,course2bChangedCode00,courseInfoDict,updateComment,userEmail00):
  timeNow=datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
  cols2bUpdated=[*courseInfoDict]
  vals2bUpdated=[courseInfoDict[xx] for xx in [*courseInfoDict]]

  msg2=update_and_log(SQLengine,DB_access_object,'course','course_update_history',{'course_code':course2bChangedCode00}, cols2bUpdated,vals2bUpdated,updateComment,userEmail00)

  print(timeNow)
  emailText=course2bChangedCode00+': course was updated at '+timeNow+' by '+ userEmail00+'\n'+updateComment
  msg=course2bChangedCode00+': course was updated at '+timeNow+' by '+ userEmail00
  
  #Updating moodle 14/12/2022

  
  
  return msg, pd.read_sql('SELECT * FROM course WHERE course_code="{}"'.format(course2bChangedCode00),SQLengine)




def delete_course_from_program(SQLengine,DB_access_object,course2bChangedCode00,program2bDeletedFrom00,updateComment,userEmail00):
  timeNow=datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
  entry2bDeletedPDF=pd.read_sql('SELECT * FROM program_structure WHERE program_code="{}" AND course_code="{}"'.format(program2bDeletedFrom00,course2bChangedCode00),SQLengine).drop(columns=['program_structure_id'])
  entry2bDeletedPDF[['program_structure_updated_by','program_structure_updated_on']]=[userEmail00,timeNow]# Changed on 9 Aug 2022
  cols2bupdated=[*entry2bDeletedPDF]+['program_structure_update_comment']# Changed on 9 Aug 2022 - updated on, updated by added
  vals2bupdated=[entry2bDeletedPDF[xx].to_list()[0] for xx in [*entry2bDeletedPDF]]+['Course '+course2bChangedCode00+' deleted - '+updateComment]## Changed on 9 Aug 2022 - updated on, updated by added

  DB_access_object.delete_records(SQLengine,'program_structure',{'program_code':program2bDeletedFrom00,'course_code':course2bChangedCode00})
  DB_access_object.insert_records(SQLengine,'program_structure_update_history',cols2bupdated,vals2bupdated)

  msg='Course '+course2bChangedCode00+' was deleted from '+program2bDeletedFrom00+' at '+timeNow+' by '+userEmail00
  return msg

def add_course_to_a_program(SQLengine,DB_access_object,course2bAddedCode00,courseType00,program2bAdded00,updateComment,userEmail00):
  timeNow=datetime.datetime.now().strftime("%m-%d%Y-%H:%M:%S")

  tempPrgStrPDF=pd.read_sql('SELECT * FROM program_structure WHERE program_code="{}"'.format(program2bAdded00),SQLengine)

  if course2bAddedCode00 in tempPrgStrPDF['course_code'].to_list():
    msg='Course '+ course2bAddedCode00 +' already offered'
    returnPDF=tempPrgStrPDF
  else:
    updateColNamesList=['program_code','course_code',	'program_course_type','program_structure_updated_on',	'program_structure_updated_by']
    updateValuesList=[program2bAdded00,course2bAddedCode00,courseType00,timeNow, userEmail00]
    msg2=DB_access_object.insert_records(SQLengine,'program_structure',updateColNamesList,updateValuesList)
    msg3=DB_access_object.insert_records(SQLengine,'program_structure_update_history',updateColNamesList+['program_structure_update_comment'],updateValuesList+['Course '+course2bAddedCode00+' added - '+updateComment])


    msg='Course '+course2bAddedCode00+' was added to '+program2bAdded00
    returnPDF=pd.read_sql('SELECT * FROM program_structure WHERE program_code="{}"'.format(program2bAdded00),SQLengine)

  return msg, returnPDF

def course_kw_creation(courseInfo0):
  #courseInfo0=pd.read_sql(courseCode,SQLengine).to_dict(orient='records')[0]
  ILOsCombined=[];
  for ILO in ['ILO1','ILO2','ILO3','ILO4','ILO5','ILO6']:
    xx=courseInfo0[ILO];
    if xx!='':
      ILOsCombined+=[xx.split('#')[2]]
  courseILODoc=nlp(' '.join(ILOsCombined))
  courseKW0=[];
  for token in courseILODoc:
    if (token.pos_=='NOUN' or token.pos_=='PRON'):
      courseKW0+=[token.text]
  courseKW=set(courseKW0)
  kwdsList=list(courseKW)
  kwdsList.sort()
  keywdsDoc0=', '.join(kwdsList)
  keywdsDoc=keywdsDoc0.lower()
  return keywdsDoc #22/06/2022 1350

def courseTaxonomyLevel(SQLengine,courseDict): # SQLengine,courseCode):
  #courseDict=pd.read_sql(courseCode,SQLengine).to_dict(orient='records')[0]
  coureseLevels={};
  soloLevel=0.0;
  bloomsLevel=0.0;
  courseCredits=0.0;
  ILOwiseCredits=courseDict['credit_to_ILO_map'].split(','); #.values[0].split(',');
  if '' in ILOwiseCredits:
    print('ILOs undefined')
  else:
    for kk in range(len(ILOwiseCredits)):
        ILONo='ILO'+str(kk+1);
        ILOcredit=float(ILOwiseCredits[kk]);
        courseCredits+=ILOcredit;
        keyVerb=str(courseDict[ILONo]).split('#')[1]; #.values[0].split('#')[1];
        sql_qf="SELECT {} FROM {} WHERE {} LIKE '%{}%'".format('*', 'SOLO_BLOOMS_taxonomy_list', 'key_verbs', keyVerb)
        temp1PDF=pd.read_sql_query(sql_qf,SQLengine)  #['SOLO_BLOOMS_Taxonomy_id'].to_list()
        temp1=temp1PDF['taxonomy_type'].to_list()
        for xx in temp1:
          temp2=xx.split('_')
          taxonomyType=temp2[0];
          taxonomyLevel=int(temp2[1])
          if taxonomyType=='SOLO':
            soloLevel+=ILOcredit*taxonomyLevel
          elif taxonomyType=='BLOOMS':
            bloomsLevel+=ILOcredit*taxonomyLevel
    soloLevel=round(soloLevel/courseCredits,2)
    bloomsLevel=round(bloomsLevel/courseCredits,2)
  coureseLevels['course_credits']=courseCredits
  coureseLevels['SOLO_level']=soloLevel
  coureseLevels['BLOOMS_level']=bloomsLevel
  return coureseLevels

def key_word_search(searchPDF0, searchCol, searchKWsList0, simThreshold0): #added searchCol 13/03/2022 - 1234
  searchKWsList0=searchKWsList0.lower()
  searchKWsDoc=nlp(searchKWsList0)
  KW0=[];
  for token in searchKWsDoc:
    if (token.pos_=='NOUN' or token.pos_=='PRON'):
      KW0+=[token.text]
  KW=set(KW0)
  kwList2Search=list(KW)
  kwList2Search.sort()
  if len(kwList2Search)==0:
    similarElementsPDF=pd.DataFrame(columns=[*searchPDF0])
    similarElementsPDF['similarity_score']=0
  else:
    similarElements=[]
    similarityScore=[]
    for nn in searchPDF0.index.values:
      item_nn_KW0=searchPDF0.loc[nn, searchCol] #added searchCol 13/03/2022 - 1234
      # print("item_nn_KW0:",item_nn_KW0)
      item_nn_KW=item_nn_KW0.lower()
      itemKWList0=item_nn_KW.split(', ')
      tempKWs=' '.join(itemKWList0)
      itemKWset=set(tempKWs.split(' '))

      xx=len(itemKWset.intersection(set(kwList2Search)))/len(set(kwList2Search))
      if xx>simThreshold0:
        similarElements+=[nn]
        similarityScore+=[str(int(xx*100))+'%']
    similarElementsPDF=searchPDF0.loc[similarElements]
    similarElementsPDF['similarity_score']=similarityScore
  return similarElementsPDF

def search_course_by_KW(courseSearchPDF, searchKWs0, similariryThreshold0):
  searchKWs0=searchKWs0.lower()
  searchKWsDoc=nlp(searchKWs0)
  courseKW0=[];
  for token in searchKWsDoc:
    if (token.pos_=='NOUN' or token.pos_=='PRON'):
      courseKW0+=[token.text]
  courseKW=set(courseKW0)
  searchKWsList=list(courseKW)
  searchKWsStr=' '.join(searchKWsList)
  searchKWsStr=searchKWsStr.lower()
  matchingCoursesPDF=key_word_search(courseSearchPDF, 'course_keywords', searchKWsStr, similariryThreshold0)
  return matchingCoursesPDF

def search_course_by_name(courseSearchPDF, searchCourseName0):
  searchCourseName=searchCourseName0.lower()
  searchCNsDoc=nlp(searchCourseName)
  courseNM0=[];
  for token in searchCNsDoc:
    if (token.pos_=='NOUN' or token.pos_=='PRON'):
      courseNM0+=[token.text]
  courseNM=set(courseNM0)
  searchNMsList=list(courseNM)
  searchNMsStr=' '.join(searchNMsList)
  matchingCoursesPDF=key_word_search(courseSearchPDF, 'course_name', searchNMsStr, 0.0) #Error corrected - courseList changed to courseList0
  return matchingCoursesPDF

def search_course_by_skill(courseSearchPDF,colName,filterValue):
  return courseSearchPDF[courseSearchPDF[colName]==filterValue]

def pick_classifier(menuFlds, tempPDF): #This is a UI function - Niuru already created ignore
  for fld in menuFlds:
    menuFldsList=list(set(tempPDF[fld].to_list()))
    menuFldsList.sort()
    print(menuFldsList) #Part of the dropdown
    specificFld=input() #User to choose from menu menuFldsList
    tempPDF=tempPDF.loc[tempPDF[fld]==specificFld,:]
  return specificFld

def process_proposed_course(SQLengine,updateCourseCourseCode0,updateCourseDict0, courseSummaryPDF0):
  temp=courseTaxonomyLevel(SQLengine,updateCourseDict0)
  updateCourseDict0['SOLO_level']=temp['SOLO_level'];
  updateCourseDict0['BLOOMS_level']=temp['BLOOMS_level'];
  updateCourseDict0['course_credits']=sum([float(aa) for aa in updateCourseDict0['credit_to_ILO_map'].split(',')]) #New 11/03/2022
  updateCourseDict0['course_keywords']=course_kw_creation(updateCourseDict0)
  courseKWList2Search=updateCourseDict0['course_keywords'].split(', ')
  courseKWstr2Search=' '.join(courseKWList2Search)
  similarCoursesPDF00=search_course_by_KW(courseSummaryPDF0, courseKWstr2Search, 0.4)
  return updateCourseDict0, similarCoursesPDF00


#updated on 15 Aug 2022
def update_table(SQLengine,DB_query_obj,tableName0,filterColList0,updateDataPDF0,updateComment0,userEmail0):
    updateDataDict=updateDataPDF0.to_dict(orient='records')
    filterDict={}
    for dct in updateDataDict:
        updateCols=list(set([*updateDataPDF0]).difference(set(filterColList0)))
        updateVals=[dct[xx] for xx in updateCols]
        updateCols+=[tableName0+'_updated_on']
        updateVals+=[datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")]
        filterDict={fcs:dct[fcs] for fcs in filterColList0}
        DB_query_obj.update_records(SQLengine,tableName0,filterDict,updateCols,updateVals)
        whereStr=' AND '.join([ky+'="'+str(filterDict[ky])+'"' for ky in [*filterDict]])
        updatedEntryDict=pd.read_sql('SELECT * FROM {} WHERE {}'.format(tableName0,whereStr),SQLengine).fillna('').drop(columns=[tableName0+'_id']).to_dict(orient='records')[0]
        updateHistoryCols=[*updatedEntryDict]
        updateHistoryVals=[updatedEntryDict[xx] for xx in updateHistoryCols]
        updateHistoryCols+=[tableName0+'_update_comment']
        updateHistoryVals+=['Updated by admin '+userEmail0+' - '+updateComment0]
        msg2=DB_query_obj.insert_records(SQLengine,tableName0+'_update_history',updateHistoryCols,updateHistoryVals)
    return msg2

#Program mapping functions updated 23 Aug 2022
def programDepthBreadth(selectedProgram0,SQLengine):

  programStructurePDF=pd.read_sql('SELECT * FROM program_structure WHERE program_code="{}"'.format(selectedProgram0),SQLengine)

  courseListPDF=pd.read_sql('SELECT course_code FROM course',SQLengine)
  taxonomyPDF=pd.read_sql('SELECT * FROM SOLO_BLOOMS_Taxonomy',SQLengine)
  lst1=[]
  for idx in programStructurePDF.index.values:
    course4mProgramPDF=programStructurePDF.iloc[idx];
    courseLabel=course4mProgramPDF['course_code']
    dict1=pd.read_sql('SELECT course_code, course_name, CAH3_skill_classification, credit_to_ILO_map,course_credits, ILO1, ILO2, ILO3, ILO4, ILO5, ILO6, SOLO_level,	BLOOMS_level FROM course WHERE course_code="{}"'.format(courseLabel),SQLengine).to_dict(orient='records')
    if len(dict1)!=0:
      course4mCourseDict=dict1[0]
      print("course4mCourseDict: ",course4mCourseDict)  
      ILOwiseCredits=course4mCourseDict['credit_to_ILO_map'].replace(' ','').split(',');
      for nn in range(15):
        POlabel='PO'+str(nn+1);
        POILOlist=course4mProgramPDF[POlabel];
        if  POILOlist!='':
          POILOs=str(POILOlist).split(',')
          soloLevel=0;
          bloomsLevel=0;
          if len(POILOs)>len(ILOwiseCredits):
            print('Number of program ILOs greater than the number of course ILOs for course'+' '+courseLabel)
          else:
            for kk0 in POILOs:
              print("kk0: ",kk0)
              kk=int(float(kk0))
              if kk>len(ILOwiseCredits):
                print(POlabel+' ILO-'+kk0+' not in the list of course ILOs for course'+' '+courseLabel)
              else:
                ILONo='ILO'+str(int(float(kk0)));
                ILOcredit=float(ILOwiseCredits[kk-1]);
                keyVerb=str(course4mCourseDict[ILONo]).split('#')[1].replace(" ",""); #.values[0].split('#')[1];
                sql_qf="SELECT {} FROM {} WHERE {} LIKE '%{}%'".format('*', 'SOLO_BLOOMS_taxonomy_list', 'key_verbs', keyVerb)
                temp1PDF=pd.read_sql_query(sql_qf,SQLengine)  #['SOLO_BLOOMS_Taxonomy_id'].to_list()
                temp1=temp1PDF['taxonomy_type'].to_list()

                for xx in temp1:
                  temp2=xx.split('_')
                  taxonomyType=temp2[0];
                  taxonomyLevel=int(temp2[1])
                  if taxonomyType=='SOLO':
                    soloLevel+=ILOcredit*taxonomyLevel
                  elif taxonomyType=='BLOOMS':
                    bloomsLevel+=ILOcredit*taxonomyLevel
            #soloLevel=round(soloLevel,1);
            #bloomsLevel=round(bloomsLevel,1);
            # course4mCourseDict['course_credits']=sum([float(kzx) for kzx in ILOwiseCredits])
            course4mCourseDict[POlabel+'_SOLO_level']=round(soloLevel,2); #/dict1['SOLO-Level']
            course4mCourseDict[POlabel+'_BLOOMS_level']=round(bloomsLevel,2); #/dict1['BLOOM-Level']

      #lst1+=[dict1]
    else:
      print(courseLabel+' '+'Course not in course catalog')
    lst1+=[course4mCourseDict]
  return pd.DataFrame(lst1).fillna('')


def program_PO_depth_breadth_graph(SQLengine,selectedProgram0):
  tempPO=programDepthBreadth(selectedProgram0,SQLengine)
  yySOLO=[]; yyBLOOMS=[];
  xxSOLO=[]
  xxBLOOMS=[]
  POlist=[*tempPO][13:]
  POlist.sort()
  for POx in POlist:
    if POx.find('SOLO')!=-1:
      xxSOLO+=[POx.split('_')[0]];
      yySOLO+=[sum(tempPO[POx].replace('',0).to_list())/132] #newProgram['total US credits']];
    else:
      xxBLOOMS+=[POx.split('_')[0]];
      yyBLOOMS+=[sum(tempPO[POx].replace('',0).to_list())/132] #newProgram['total US credits']];
  xx1=[xxSOLO,xxBLOOMS] #[xx,xx] #
  yy1=[yySOLO,yyBLOOMS]
  traceNames1=['SOLO','BLOOMS']
  fig = go.Figure()
  for i,x in enumerate(xx1):
    fig.add_trace(go.Bar(y=yy1[i], x=x, name=traceNames1[i]))


  fig.update_layout(
      title='', xaxis_title='', yaxis_title='Depth Value'#, barmode='group'
  )
  #fig.show()
  return fig


def program_competency_depth_breadth_graph(SQLengine,selectedProgram0,plotFieldName, depthLabel, figTitle):
  #competencyFig=program_competency_depth_breadth_graph(engine,selectedProgram,'CAH3_skill_classification', 'SOLO_level', 'Competency Depth and Bredth Map')
  xx1=[]; yy1=[];
  temp=programDepthBreadth(selectedProgram0,SQLengine)
  temp00=temp[plotFieldName].to_list();
  temp00.sort()#x-axis name list
  for tstdt in set(temp00):
    temp000=temp[temp[plotFieldName]==tstdt]
    print("↗️ "+tstdt+" = "+ temp000[depthLabel])
    xx1+=[tstdt]
    tmp004=[float(xxx4) for xxx4 in temp000[depthLabel].replace('',0).to_list()]
    yy1+=[sum(tmp004)/sum(temp['course_credits'].replace('',0).values)];
    # print(tstdt+" : ",sum(tmp004)/sum(temp['course_credits'].replace('',0).values))



  fig = go.Figure()
  fig.add_trace(go.Bar(y=yy1, x=xx1))


  fig.update_layout(
      title=figTitle, xaxis_title='', yaxis_title=depthLabel, barmode='stack'
  )
  #fig.show()
  return fig


#functions to ILO to PLO Mapping
def update_ILO_PO_map(SQLengine,DB_query_object,selectedProgram0,course2MapCode0,selectedPOList0,selected_PO_ILO_map_list0,updateComment0,userEmail0):
    timeNow=datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
    cols2bUpdated0=['PO1','PO2','PO3','PO4','PO5','PO6','PO7','PO8','PO9','PO10','PO11','PO12','PO13','PO14','PO15']
    vals2bUpdated0=["","","","","","","","","","","","","","",""]
    DB_query_object.update_records(SQLengine,'program_structure',{'program_code':selectedProgram0,'course_code':course2MapCode0},cols2bUpdated0,vals2bUpdated0)
    
    cols2bUpdated=selectedPOList0+['program_structure_updated_on','program_structure_updated_by']
    vals2bUpdated=selected_PO_ILO_map_list0+[timeNow,userEmail0]
    DB_query_object.update_records(SQLengine,'program_structure',{'program_code':selectedProgram0,'course_code':course2MapCode0},cols2bUpdated,vals2bUpdated)
    insertUpdateHistoryPDF=pd.read_sql('SELECT * FROM program_structure WHERE program_code="{}" AND course_code="{}"'.format(selectedProgram0,course2MapCode0),SQLengine).drop(columns=['program_structure_id'])
    insertUpdateHistoryPDF['program_structure_update_comment']=updateComment0
    cols2bInserted=[*insertUpdateHistoryPDF]
    vals2bInserted=[insertUpdateHistoryPDF[ky].to_list()[0] for ky in cols2bInserted]
    DB_query_object.insert_records(SQLengine,'program_structure_update_history',cols2bInserted,vals2bInserted)
    return 'Table Updated Successfully'

#function for insert records - 13 Aug 2022 (Updated on 15 Aug 2022)
def insert_records(SQLengine,DB_query_obj,tableName0,updateDataPDF0,updateComment0,userEmail0):
    updateDataDict=updateDataPDF0.to_dict(orient='records')
    filterDict={}
    for dct in updateDataDict:
        updateCols=[*updateDataPDF0]
        updateVals=[dct[xx] for xx in updateCols]
        updateCols+=[tableName0+'_updated_on']
        updateVals+=[datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")]
        msg1=DB_query_obj.insert_records(SQLengine,tableName0,updateCols,updateVals)

        updateHistoryCols=updateCols+[tableName0+'_update_comment']
        updateHistoryVals=updateVals+['Updated by admin '+userEmail0+' - '+updateComment0]
        msg2=DB_query_obj.insert_records(SQLengine,tableName0+'_update_history',updateHistoryCols,updateHistoryVals)
    return msg1, msg2

#Bulk delete records function added 14 Aug 2022
def delete_records(SQLengine,DB_query_obj,tableName0,filterColList0,updateDataPDF0,updateComment0,userEmail0):
    updateDataDict=updateDataPDF0.to_dict(orient='records')
    filterDict={}
    for dct in updateDataDict:
        filterDict={fcs:str(dct[fcs]) for fcs in filterColList0}
        whereStr=' AND '.join([ky+'="'+str(filterDict[ky])+'"' for ky in [*filterDict]])
        updatedEntryDict=pd.read_sql('SELECT * FROM {} WHERE {}'.format(tableName0,whereStr),SQLengine).fillna('').drop(columns=[tableName0+'_id']).to_dict(orient='records')[0]
        updatedEntryDict[tableName0+'_updated_by']=userEmail0
        updatedEntryDict[tableName0+'_updated_on']=datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
        updateHistoryCols=[*updatedEntryDict]
        updateHistoryVals=[updatedEntryDict[xx] for xx in updateHistoryCols]
        updateHistoryCols+=[tableName0+'_update_comment']
        updateHistoryVals+=[updateComment0]

        DB_query_obj.delete_records(SQLengine,tableName0,filterDict)

        msg2=DB_query_obj.insert_records(SQLengine,tableName0+'_update_history',updateHistoryCols,updateHistoryVals)
    emailText=tableName0+' was updated :'+'\n'+updateComment0
    # returnText=send_email('TEAL Program Revision','email@email.email','ADD_PASSWORD',['manager@manager.manager',userEmail0],tableName0+' was updated',emailText)
    return msg2


#added 20 Dec 2022
def insert_course(sqlEngine,params):
    db_table_name=params['db_table_name']
    tableID=db_table_name+'_id'
    updateDict=params['updateDict']
    db_table_PDF=pd.read_sql('SELECT * FROM {} WHERE {}=(SELECT max({}) FROM {})'.format(db_table_name,tableID,tableID,db_table_name), sqlEngine)
    diffCols=set([*updateDict]).difference(set([*db_table_PDF]))
  

    if len(diffCols) == 0:
        
        if len(db_table_PDF[tableID].values)==0:
          lastIndex=-1 
        else:
          lastIndex=db_table_PDF[tableID].values[0]
        

        insert_entry_PDF=pd.DataFrame(columns=[*db_table_PDF],index=[int(lastIndex+1)]).drop(columns=[tableID])
        insert_entry_PDF.loc[int(lastIndex+1),[*updateDict]]=[updateDict[ky] for ky in [*updateDict]]
        insert_entry_PDF.to_sql(db_table_name,sqlEngine,if_exists='append',index=True,index_label=tableID)
        msg='Table {} updated successfully'.format(db_table_name)
    else:
        msg='Insert columns'+', '.join(diffCols)+' not in table'
    return msg