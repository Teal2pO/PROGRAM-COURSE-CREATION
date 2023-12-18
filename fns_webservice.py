# github functions also included inside this file
from static_globals import *

import pandas as pd
import mysql.connector
import sqlalchemy
from sqlalchemy import *
from pandas.io import sql
from requests import get, post
import datetime
import time

import json
from github import Github
import os

# ===========================Github 16 Jan 2023============================


class tealMGitHub:
    def __init__(self):
        self = []

    def get_GitHub_user(self, params):
        self.g = Github(params['gToken'])
        return self.g

    def get_GitHub_organization_repos(self, params):
        self.g = Github(params['gToken'])
        self.organization = self.g.get_organization(params['gUser'])
        repoNames = [repo.name for repo in self.organization.get_repos()]
        return repoNames

    def get_repo_info(self, params):
        self.g = Github(params['gToken'])
        fileNames = []
        repoName = params['repoName']
        repo = self.g.get_repo(params['gUser']+'/'+params['repoName'])
        branches = list(repo.get_branches())
        branchNames = [br.name for br in branches]
        contents = repo.get_contents("")

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                fls = repo.get_contents(file_content.path)
                contents.extend(fls)
            else:
                fileNames += [file_content.path]

        return {'branch_names': branchNames, 'file_names': fileNames}

    def get_repo_file_content(self, params):
        self.g = Github(params['gToken'])
        repoName = params['repoName']
        branchName = params['branchName']
        repo = self.g.get_repo(params['gUser']+'/'+params['repoName'])
        b = repo.get_branch(branch=params['branchName'])
        contents = repo.get_contents(params['fileName'], ref=b.commit.sha)
        # self.contents = self.repo.get_file_contents(params['fileName'], ref=b.commit.sha)
        return {'repo': repo, 'contents': contents}

    def write_file_2_repo(self, params):
        self.g = Github(params['gToken'])
        repoName = params['repoName']
        branchName = params['branchName']
        repo = self.g.get_repo(params['gUser']+'/'+params['repoName'])
        return repo.create_file(params['writeFile'], params['commitComment'], params['content2Write'], branch=params['branchName'])

    def delete_file(self, params):
        self.g = Github(params['gToken'])
        repoName = params['repoName']
        branchName = params['branchName']
        repo = self.g.get_repo(params['gUser']+'/'+params['repoName'])
        b = repo.get_branch(branch=params['branchName'])
        contents = repo.get_contents(params['fileName'], ref=b.commit.sha)
        return repo.delete_file(contents.path, params['commitComment'], contents.sha, branch=params['branchName'])


def GithubViewDeleteApp_fn(func):

    def inner1(b):
        c = func(b)
        return c

    return inner1


def GithubViewDeleteApp(inputDict):
    function_to_be_called = GithubViewDeleteApp_fn(inputDict['functionName'])
    return function_to_be_called(inputDict['functionParameters'])


def create_update_GITHUB_organization_repos(mgGH, parameters):
    functionParameters = {'gToken': parameters['access_parameters']['gToken'], 'gUser': parameters['access_parameters']['gUser'], 'repoName': parameters['repoName'],
                          'branchName': 'main', 'writeFile': parameters['fileInfoDict']['filename'], 'content2Write': parameters['fileInfoDict']['filecontent'], 'commitComment': parameters['updateComment']}
    inputDict = {'functionName': mgGH.get_GitHub_organization_repos,
                 'functionParameters': parameters['access_parameters']}
    reposList = GithubViewDeleteApp(inputDict)
    if parameters['repoName'] in reposList:
        functionParameters['fileName'] = parameters['fileInfoDict']['filename']
        inputDict = {'functionName': mgGH.get_repo_file_content,
                     'functionParameters': functionParameters}
        try:
            fileOut = GithubViewDeleteApp(inputDict)
            content = fileOut['contents']
            repo = fileOut['repo']
            repo.update_file(content.path, parameters['updateComment'],
                             parameters['fileInfoDict']['filecontent'], content.sha, branch='main')
            message = 'Content updated'
        except:
            inputDictWrite = {'functionName': mgGH.write_file_2_repo,
                              'functionParameters': functionParameters}
            GithubViewDeleteApp(inputDictWrite)
            message = 'Content created'

    else:
        mgGH.organization.create_repo(parameters['repoName'], private=True)
        inputDictWrite = {'functionName': mgGH.write_file_2_repo,
                          'functionParameters': functionParameters}
        GithubViewDeleteApp(inputDictWrite)
        message = 'Content created'
    return message


def get_GitHub_repo_content(mgGH, paramsInfo):
    repoFiles = mgGH.get_repo_info(paramsInfo)
    print(repoFiles)
    params = {'gToken': paramsInfo['gToken'], 'gUser': paramsInfo['gUser'],
              'branchName': repoFiles['branch_names'][0], 'repoName': paramsInfo['repoName'], 'fileName': ''}
    outDict = {}
    for file in repoFiles['file_names']:
        params['fileName'] = file
        outDict[file] = json.loads(str(mgGH.get_repo_file_content(
            params)['contents'].decoded_content, encoding="ascii", errors='strict'))
    return outDict


def get_GitHub_repo_content_string(mgGH, paramsInfo):
    repoFiles = mgGH.get_repo_info(paramsInfo)
    print(repoFiles)
    params = {'gToken': paramsInfo['gToken'], 'gUser': paramsInfo['gUser'], 'g': mgGH.g,
              'branchName': repoFiles['branch_names'][0], 'repoName': paramsInfo['repoName'], 'fileName': ''}
    outDict = {}
    for file in repoFiles['file_names']:
        params['fileName'] = file
        outDict[file] = str(mgGH.get_repo_file_content(
            params)['contents'].decoded_content, encoding="ascii", errors='strict')
    return outDict

# ===========================Database 16 Jan 2023============================


def DataBaseAccessApp_fn(func):

    def inner1(a, b):
        c = func(a, b)
        return c

    return inner1


def DataBaseAccessApp(sqlEngine, inputDict):
    function_to_be_called = DataBaseAccessApp_fn(inputDict['functionName'])
    return function_to_be_called(sqlEngine, inputDict['functionParameters'])


def update_record(SQLengine, params):
    db_table_name = params['db_table_name']
    filterDict = params['filterDict']
    updateDict = params['updateDict']
    filterStrLst = [fltcol+'="{}"'.format(params['filterDict'][fltcol])
                    for fltcol in [*params['filterDict']]]
    filterStr = ' AND '.join(filterStrLst)
    numericFieldsInfoDict = updateDict['numericFieldsInfoDict']
    textFieldsInfoDict = updateDict['textFieldsInfoDict']

    if len(textFieldsInfoDict) != 0:
        sqlqText = "UPDATE {} SET ".format(db_table_name) + ', '.join([xx+"='{}'".format(
            textFieldsInfoDict[xx]) for xx in [*textFieldsInfoDict]])+" WHERE {}".format(filterStr)
        sqlqText = sqlqText.replace('\\', '\\\\')
        SQLengine.execute(sqlqText)
    if len(numericFieldsInfoDict) != 0:
        sqlqNumeric = "UPDATE {} SET ".format(db_table_name) + ', '.join([xx+"={}".format(
            numericFieldsInfoDict[xx]) for xx in [*numericFieldsInfoDict]])+" WHERE {}".format(filterStr)
        SQLengine.execute(sqlqNumeric)

    return 'Table {} updated successfully'.format(db_table_name)


def insert_record(sqlEngine, params):
    db_table_name = params['db_table_name']
    updateDict = params['updateDict']
    db_table_PDF = pd.read_sql(
        'SELECT * FROM {} WHERE id=(SELECT max(id) FROM {})'.format(db_table_name, db_table_name), sqlEngine)
    diffCols = set([*updateDict]).difference(set([*db_table_PDF]))
    if len(diffCols) == 0:
        lastIndex = db_table_PDF['id'].values[0]
        insert_entry_PDF = pd.DataFrame(
            columns=[*db_table_PDF], index=[int(lastIndex+1)]).drop(columns=['id'])
        insert_entry_PDF.loc[int(lastIndex+1), [*updateDict]
                             ] = [updateDict[ky] for ky in [*updateDict]]
        insert_entry_PDF.to_sql(db_table_name, sqlEngine,
                                if_exists='append', index=True, index_label='id')
        msg = 'Table {} updated successfully'.format(db_table_name)
    else:
        msg = 'Insert columns'+', '.join(diffCols)+' not in table'
    return msg


# ===========================Webservice 16 Jan 2023============================
def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.

    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict == None:
        out_dict = {}
    if not type(in_args) in (list, dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args) == list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args) == dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict


def call(accessParams, fname, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.

    Example:
    >>> call_mdl_function('core_course_update_courses',
                           courses = [{'id': 1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    parameters.update(
        {"wstoken": accessParams['KEY'], 'moodlewsrestformat': 'json', "wsfunction": fname})

    response = post(accessParams['URL']+accessParams['ENDPOINT'],
                    parameters, verify=False)  # use for http
    # response = post(accessParams['URL']+accessParams['ENDPOINT'], parameters)#use for https

    response = response.json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response


def get_course_modules(webserviceAccessParams, courseShortName):
    chosenContentDict = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=courseShortName)[
        'courses'] if crs['shortname'] == courseShortName][0]
    chosenContentID = chosenContentDict['id']
    contentModules = [{'sectionid': secn['id'], 'sectionname': secn['name'], 'sectionmodules': [{'id': mod['id'], 'name': mod['name'], 'modname': mod['modname'], 'contextid': mod['contextid'],
                                                                                                 'instance': mod['instance'], 'url': mod['url']} for mod in secn['modules']]} for secn in call(webserviceAccessParams, 'core_course_get_contents', courseid=chosenContentID)]
    return contentModules


def create_course_4m_moodle_template(params):
    print('create_course_4m_moodle_template')
    print(params)
    output = {}
    templateShortName = params['templateShortName']
    categoryName = params['categoryName']
    contentName = params['fullname']
    contentShortName = params['shortname']
    webserviceAccessParams = params['webserviceAccessParams']
    customFields = params['customfields']
    categoryInfo = [cat for cat in call(webserviceAccessParams, 'core_course_get_categories ', criteria=[
                                        {'key': 'name', 'value': categoryName}]) if cat['name'] == categoryName][0]
    categoryID = categoryInfo['id']

    templateContentDict = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=templateShortName)[
        'courses'] if crs['shortname'] == templateShortName][0]
    templateCourseID = templateContentDict['id']
    course2AddDict = call(webserviceAccessParams, 'core_course_get_courses', options={
                          'ids': [templateCourseID]})[0]
    for ky in ['id', 'categorysortorder', 'displayname', 'showactivitydates', 'showactivitydates', 'showcompletionconditions', 'timecreated', 'timemodified']:  # ,'lang']:
        try:
            del course2AddDict[ky]
        except:
            output['message'] = 'No {} in keys'.format(ky)

    course2AddDict['shortname'] = contentShortName
    course2AddDict['fullname'] = contentName
    course2AddDict['categoryid'] = categoryID
    course2AddDict['lang'] = 'en'
    # [{ky:course2AddDict['customfields'][0][ky] for ky in ['shortname','value']}]
    course2AddDict['customfields'] = customFields
    print(course2AddDict)
    reponse = call(webserviceAccessParams,
                   'core_course_create_courses', courses=[course2AddDict])
    createdCrsId = reponse[0]['id']
    output['created_content_id'] = createdCrsId
    call(webserviceAccessParams, 'core_course_import_course',
         importfrom=templateCourseID, importto=createdCrsId)
    # output['crs_URL']=webserviceAccessParams['URL']+'/course/view.php?id={}'.format(createdCrsId)
    output['crsModuleInfo'] = call(
        webserviceAccessParams, 'core_course_get_contents', courseid=createdCrsId)[0]['modules']
    output['message'] = 'Content created from template {}'
    return output


def manual_enroll_user_in_course(webserviceAccessParams, courseShortName, userName, userRoleShortName, engine):
    contentDict = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=courseShortName)[
        'courses'] if crs['shortname'] == courseShortName][0]
    contentID = contentDict['id']

    userInfo = [usr for usr in call(webserviceAccessParams, 'core_user_get_users', criteria=[
                                    {'key': 'username', 'value': userName}])['users'] if usr['username'] == userName]

    if (len(userInfo) != 0):
        userID = userInfo[0]['id']
        roleID = pd.read_sql('SELECT id FROM mdl_role WHERE shortname="{}"'.format(
            userRoleShortName), engine)['id'].values[0]  # TEAL2.O Teacher
        enrolmentList = [{'courseid': contentID,
                          'userid': userID, 'roleid': roleID}]
        out_dict = call(webserviceAccessParams,
                        'enrol_manual_enrol_users', enrolments=enrolmentList)
        output = str(out_dict)
        return output
    else:
        return userName+" doesn't exist in the classroom system"


def course_content_GitHub_push(mgGH, SQLengine, parameters):
    # parameters={'access_parameters':{'gToken':githubToken, 'gUser':contentOrganization}, 'repoName':chosenContentShortname, 'updateComment':updateComment}
    webserviceAccessParams = parameters['webserviceAccessParams']
    contentShortName = parameters['repoName']  # .lower()
    chosenContentDict = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=contentShortName)[
        'courses'] if crs['shortname'] == contentShortName][0]
    contentMetaDataSummaryJSON = json.dumps(chosenContentDict, indent=2)
    parameters['fileInfoDict'] = {
        'filename': 'contentMetaDataSummary.json', 'filecontent': contentMetaDataSummaryJSON}
    create_update_GITHUB_organization_repos(mgGH, parameters)
    chosenContentId = chosenContentDict['id']

    chosenContentFullDict = call(
        webserviceAccessParams, 'core_course_get_courses', options={'ids': [chosenContentId]})
    contentMetaDataJSON = json.dumps(chosenContentFullDict, indent=2)
    parameters['fileInfoDict'] = {
        'filename': 'contentMetaData.json', 'filecontent': contentMetaDataJSON}
    create_update_GITHUB_organization_repos(mgGH, parameters)

    chosenContentSecns = call(
        webserviceAccessParams, 'core_course_get_contents', courseid=chosenContentId)
    contentSecnsJSON = json.dumps(chosenContentSecns, indent=2)
    parameters['fileInfoDict'] = {
        'filename': 'contentSecnsSummary.json', 'filecontent': contentSecnsJSON}
    msg = create_update_GITHUB_organization_repos(mgGH, parameters)

    for section in [{'id': secn['id'], 'name': secn['name'], 'modules': secn['modules']} for secn in call(webserviceAccessParams, 'core_course_get_contents', courseid=chosenContentId)]:
        for module in section['modules']:
            fileDict = pd.read_sql('SELECT * FROM mdl_{} WHERE id={}'.format(
                module['modname'], module['instance']), SQLengine).to_dict(orient='records')[0]

            if module['modname'] == 'hvp':
                mainLibraryID = fileDict['main_library_id']
                fileDict['main_library_id'] = pd.read_sql(
                    'SELECT * FROM mdl_hvp_libraries WHERE id={}'.format(mainLibraryID), SQLengine).to_dict(orient='records')[0]

            fileJSON = json.dumps(fileDict, indent=2)
            # parametersV2={'moduleType':'hvp','access_parameters':parameters['access_parameters'], 'repoName':contentShortName, 'fileInfoDict':{'filename':'section_'+str(section['id'])+'_content/'+module['modname']+'.json', 'filecontent':fileJSON}, 'updateComment':parameters['updateComment']}
            parametersV2 = {'access_parameters': parameters['access_parameters'], 'repoName': contentShortName, 'fileInfoDict': {'filename': 'section_'+str(section['id'])+'_content/'+'mod_'+str(
                module['id'])+'_'+module['modname']+'_'+str(module['instance'])+'.json', 'filecontent': fileJSON}, 'updateComment': parameters['updateComment']}
            msg = create_update_GITHUB_organization_repos(mgGH, parametersV2)

    return msg


def create_course_categories_moodle(webserviceAccessParams, categoryStructureDict):
    response = []
    category_structure_PDF = pd.DataFrame(categoryStructureDict)
    categoryLevels = [*category_structure_PDF]
    categoryIds = {}
    proviousLevel = []
    previousLevel = ''
    for level in categoryLevels:
        levelCategoryData = []
        catGps = list(set(category_structure_PDF[level].to_list()))
        catGps.sort()
        for catName in catGps:
            if level == categoryLevels[0]:
                parentId = 0
            else:
                parentLevel = list(set(
                    category_structure_PDF[category_structure_PDF[level] == catName][previousLevel].to_list()))[0]
                parentId = categoryIds[parentLevel]
            levelCategoryData.append({'name': catName, 'idnumber': '', 'description': '',
                                     'descriptionformat': 1, 'parent': parentId, 'theme': ''})
        # print(levelCategoryData)
        resp = call(webserviceAccessParams,
                    'core_course_create_categories', categories=levelCategoryData)
        for dct in resp:
            categoryIds[dct['name']] = dct['id']

        previousLevel = level
        response.append(resp)
    return


def delete_course_categories_moodle(webserviceAccessParams, idList):
    deleteCategories = [{'id': id, 'recursive': 1} for id in idList]
    resp = call(webserviceAccessParams,
                'core_course_delete_categories', categories=deleteCategories)
    return resp


def create_section_moodle(SQLengine, params):
    webserviceAccessParams = params['webserviceAccessParams']
    chosenContentID = params['chosenContentID']
    chosenContentInfoDict = call(
        webserviceAccessParams, 'core_course_get_contents', courseid=chosenContentID)
    crsSections = {secn['section']: secn['name']
                   for secn in chosenContentInfoDict}
    emptySecnDict = {'course': params['chosenContentID'],
                     'section': [*crsSections][-1]+1,
                     'name': params['secnName'],
                     'summary': '',
                     'summaryformat': 1,
                     'sequence': '',
                     'visible': 1,
                     'availability': None,
                     'timemodified': int(time.mktime(datetime.datetime.now().timetuple()))}
    msg = insert_record(SQLengine, {
                        'db_table_name': params['db_table_name'], 'updateDict': emptySecnDict})
    return msg


def copy_from_template_and_update_course_module_from_GitHub(SQLengine, parameters):
    chosenCourseShortName = parameters['chosenCourseShortName']
    sectionName = parameters['sectionName']
    chosenModType = parameters['chosenModType']
    githubPullModDict = parameters['githubPullModDict']
    chosenCourseModules = get_course_modules(
        webserviceAccessParams, chosenCourseShortName)
    chosenCourseTemplateModules = [
        tmplCm for tmplCm in chosenCourseModules if tmplCm['sectionname'] == sectionName][0]['sectionmodules']
    mod2Duplicate = [
        mod for mod in chosenCourseTemplateModules if mod['modname'] == chosenModType]
    call(webserviceAccessParams, 'core_course_edit_module',
         action='duplicate', id=mod2Duplicate[0]['id'])
    updatedCourseModules = get_course_modules(
        webserviceAccessParams, chosenCourseShortName)
    copiedSectionModules0 = [
        tmplCm for tmplCm in updatedCourseModules if tmplCm['sectionname'] == sectionName][0]['sectionmodules']
    copiedSectionModules = [
        cCm for cCm in copiedSectionModules0 if '(copy)' in cCm['name']]
    moduleName = copiedSectionModules[0]['name']
    parametersUpdate = {'chosenCourseShortName': chosenCourseShortName, 'sectionName': sectionName,
                        'moduleName': moduleName, 'webserviceAccessParams': webserviceAccessParams, 'githubPullModDict': githubPullModDict}
    return update_course_module_from_GitHub(SQLengine, parametersUpdate)


def update_course_module_from_GitHub(SQLengine, parameters):
    chosenCourseShortName = parameters['chosenCourseShortName']
    sectionName = parameters['sectionName']
    moduleName = parameters['moduleName']
    webserviceAccessParams = parameters['webserviceAccessParams']
    chosenCourseSummaryDict = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=chosenCourseShortName)[
        'courses'] if crs['shortname'] == chosenCourseShortName][0]
    chosenCourseModules = get_course_modules(
        webserviceAccessParams, chosenCourseShortName)
    sectionModulesInSection = [
        tmplCm for tmplCm in chosenCourseModules if tmplCm['sectionname'] == sectionName][0]['sectionmodules']
    updateModInfoDict = [
        mod for mod in sectionModulesInSection if mod['name'] == moduleName][0]

    githubPullModDict = parameters['githubPullModDict']
    githubPullModDict['id'] = updateModInfoDict['instance']
    githubPullModDict['course'] = chosenCourseSummaryDict['id']
    githubPullModDict['timemodified'] = int(
        time.mktime(datetime.datetime.now().timetuple()))

    if updateModInfoDict['modname'] == 'hvp':
        hvpMainMachineName = githubPullModDict['main_library_id']['machine_name']
        print("hvpMainMachineName=", hvpMainMachineName)
        try:
            githubPullModDict['main_library_id'] = pd.read_sql(
                'SELECT * FROM mdl_hvp_libraries WHERE machine_name ="{}"'.format(hvpMainMachineName), SQLengine)['id'].to_list()[0]
        except:
            msg = '{} HVP machine not installed'.format(hvpMainMachineName)
            print(msg)
        githubPullModDict['filtered'] = githubPullModDict['filtered'].replace(
            "'", "''")
        githubPullModDict['json_content'] = githubPullModDict['json_content'].replace(
            "'", "''")

    keysWithoutID = [*githubPullModDict]
    keysWithoutID.remove('id')
    numericFieldsInfoDict = {ky: githubPullModDict[ky] for ky in keysWithoutID if type(
        githubPullModDict[ky]) in [int, float]}
    textFieldsInfoDict = {ky: githubPullModDict[ky] for ky in [
        *githubPullModDict] if type(githubPullModDict[ky]) == str}
    print("numericFieldsInfoDict=", numericFieldsInfoDict)
    params = {}
    params['db_table_name'] = 'mdl_'+updateModInfoDict['modname']
    params['filterDict'] = {'id': updateModInfoDict['instance']}
    params['updateDict'] = {
        'numericFieldsInfoDict': numericFieldsInfoDict, 'textFieldsInfoDict': textFieldsInfoDict}
    update_record(SQLengine, params)
    outputHTML = call(webserviceAccessParams, 'core_course_edit_module',
                      action='show', id=updateModInfoDict['id'])
    return "Content update success"


def create_empty_classroom_4m_course_MetaData_and_Moodle_Template(mgGH, parameters):
    paramsGitHub = parameters['paramsGitHub']
    paramsGitHub['repoName'] = parameters['courseMetadataDict']['chosenCourseShortName']
    githubContent = get_GitHub_repo_content(mgGH, paramsGitHub)
    courseMetadataJSON = githubContent['contentMetaData.json'][0]
    courseDict = courseMetadataJSON
    params = {}
    params['templateShortName'] = parameters['templateShortName']
    params['categoryName'] = parameters['courseMetadataDict']['categoryName']
    params['fullname'] = courseDict['fullname']
    params['shortname'] = courseDict['shortname']
    params['webserviceAccessParams'] = parameters['webserviceAccessParams']
    params['customfields'] = [{ky: cstflds[ky] for ky in [
        'shortname', 'value']} for cstflds in courseDict['customfields']]
    results = create_course_4m_moodle_template(params)
    updateModInfoDict = [ctmplCm for ctmplCm in results['crsModuleInfo']
                         if ctmplCm['name'] == 'Course Metadata'][0]
    githubContentName = [nm for nm in [*githubContent] if 'hvp' in nm][0]
    githubPullModDict = githubContent[githubContentName]
    sectionName = 'Course Information and General Announcements'
    moduleName = 'Course Metadata'
    parametersUpdate = {'chosenCourseShortName': paramsGitHub['repoName'], 'sectionName': sectionName,
                        'moduleName': moduleName, 'webserviceAccessParams': webserviceAccessParams, 'githubPullModDict': githubPullModDict}
    update_course_module_from_GitHub(engine, parametersUpdate)
    return call(webserviceAccessParams, 'core_course_edit_module', action='show', id=updateModInfoDict['id'])


def get_course_interactive_video_links(mgGH, paramsInfo):
    repoList = mgGH.get_GitHub_organization(paramsInfo)
    githubContent = get_GitHub_repo_content(mgGH, paramsInfo)
    course_HVP_modules = [fileName for fileName in [
        *githubContent] if 'hvp' in fileName]
    interactiveVideoHVP = []
    for fileName in course_HVP_modules:
        temp = {}
        yy = json.loads(githubContent[fileName]['json_content'])
        if 'content' in [*yy]:
            for xx0 in yy['content']:
                xx = xx0['content']
                try:
                    # ['contentType']=='Interactive Video':
                    if 'interactiveVideo' in [*xx['params']]:
                        for vfls in xx['params']['interactiveVideo']['video']['files']:
                            temp['name'] = githubContent[fileName]['name']
                            temp['sectionid'] = int(
                                fileName.split('section_')[1].split('_')[0])
                            temp['courseid'] = githubContent[fileName]['course']
                            temp['cmid'] = int(
                                fileName.split('mod_')[1].split('_')[0])
                            temp['instance'] = githubContent[fileName]['id']
                            temp['githubFileName'] = fileName
                            temp['subContentId'] = xx['subContentId']
                            temp['path'] = vfls['path']
                            temp['mime'] = vfls['mime']
                except:
                    print('no video in:')

        elif 'chapters' in [*yy]:
            for zz in yy['chapters']:
                for xx0 in zz['params']['content']:
                    xx = xx0['content']
                    try:
                        # ['contentType']=='Interactive Video':
                        if 'interactiveVideo' in [*xx['params']]:
                            for vfls in xx['params']['interactiveVideo']['video']['files']:
                                temp['name'] = githubContent[fileName]['name']
                                temp['sectionid'] = int(
                                    fileName.split('section_')[1].split('_')[0])
                                temp['courseid'] = githubContent[fileName]['course']
                                temp['cmid'] = int(
                                    fileName.split('mod_')[1].split('_')[0])
                                temp['instance'] = githubContent[fileName]['id']
                                temp['githubFileName'] = fileName
                                temp['subContentId'] = xx['subContentId']
                                temp['path'] = vfls['path']
                                temp['mime'] = vfls['mime']
                    except:
                        print(xx['content'])

        if len(temp) != 0:
            interactiveVideoHVP += [temp]
    return interactiveVideoHVP


def get_simple_interactive_video_links(mgGH, paramsInfo):
    repoList = mgGH.get_GitHub_organization(paramsInfo)
    githubContent = get_GitHub_content(mgGH, paramsInfo)
    course_HVP_modules = [fileName for fileName in [
        *githubContent] if 'hvp' in fileName]
    interactiveVideoHVP = []
    for fileName in course_HVP_modules:
        temp = {}
        xx = json.loads(githubContent[fileName]['json_content'])
        try:
            # ['contentType']=='Interactive Video':
            if 'interactiveVideo' in [*xx]:
                for vfls in xx['interactiveVideo']['video']['files']:
                    temp['name'] = githubContent[fileName]['name']
                    temp['sectionid'] = int(
                        fileName.split('section_')[1].split('_')[0])
                    temp['courseid'] = githubContent[fileName]['course']
                    temp['cmid'] = int(fileName.split('mod_')[1].split('_')[0])
                    temp['instance'] = githubContent[fileName]['id']
                    temp['githubFileName'] = fileName
                    # temp['subContentId']=xx['subContentId']
                    temp['path'] = vfls['path']
                    temp['mime'] = vfls['mime']
        except:
            print('no video in:')

        if len(temp) != 0:
            interactiveVideoHVP += [temp]
    return interactiveVideoHVP


def update_moodle_course_info_4m_course_db(SQLengine, SQLengineApp, webserviceAccessParams, courseCode4mTable):
    content2BUpdatedShortname = courseCode4mTable
    moduleName = "Course Information"  # added 18/01/2023
    chosenContentDict = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=content2BUpdatedShortname)[
        'courses'] if crs['shortname'] == content2BUpdatedShortname][0]
    contentReplacingid = chosenContentDict['id']
    contentReplacingContents = call(
        webserviceAccessParams, 'core_course_get_contents', courseid=contentReplacingid)
    contentReplacing_hvpModules = [
        mod for secn in contentReplacingContents for mod in secn['modules'] if mod['name'] == moduleName]  # mod['modname']=='hvp']
    chosenhvpModuleID = contentReplacing_hvpModules[0]['instance']
    moduleInfoDict = pd.read_sql('SELECT * FROM mdl_hvp WHERE id={}'.format(
        chosenhvpModuleID), SQLengine).to_dict(orient='records')
    # print(moduleInfoDict[0]['filtered'])
    json_content = moduleInfoDict[0]['json_content']
    filtered = moduleInfoDict[0]['json_content']  # ['filtered']
    parameters = {'courseCode4mTable': courseCode4mTable,
                  'filtered': filtered, 'json_content': json_content}
    updatedJSONSDict = course_table_2_hvp_accordion(SQLengineApp, parameters)
    params = {}
    params['db_table_name'] = 'mdl_hvp'
    params['filterDict'] = {'id': chosenhvpModuleID}
    params['updateDict'] = {'numericFieldsInfoDict': {}, 'textFieldsInfoDict': {
        'name': moduleName, 'filtered': updatedJSONSDict['filtered'], 'json_content': updatedJSONSDict['json_content']}}
    return update_record(SQLengine, params)


def create_classroom_4m_course_db(mgGH, SQLengine, SQLengineApp, parameters):
    courseShortName = parameters['repoName']
    webserviceAccessParams = parameters['webserviceAccessParams']
    templateShortName = parameters['templateShortName']
    userEmail = parameters['userEmail']
    existingContent = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=courseShortName)[
        'courses'] if crs['shortname'] == courseShortName]
    siteURLpublicClassroom = webserviceAccessParams['PURL']

    if len(existingContent) == 0:
        info = create_course_4m_course_db(
            SQLengine, SQLengineApp, webserviceAccessParams, courseShortName, templateShortName, userEmail)
        # output=info['crs_URL']

        output = siteURLpublicClassroom + \
            "/course/view.php?id={}".format(info['created_content_id'])
        # print(output)
        parameters['updateComment'] = 'course created'
        # msg=course_content_GitHub_push(mgGH,SQLengine,parameters)#github push stopped 23 Jan 2023
    else:
        info = update_moodle_course_info_4m_course_db(
            SQLengine, SQLengineApp, webserviceAccessParams, courseShortName)
        print(info)
        cId = existingContent[0]['id']
        output = siteURLpublicClassroom+"/course/view.php?id={}".format(cId)

    return output


def create_update_course_4m_course_db(mgGH, SQLengine, SQLengineApp, parameters):
    courseShortName = parameters['repoName']
    webserviceAccessParams = parameters['webserviceAccessParams']
    templateShortName = parameters['templateShortName']
    userEmail = parameters['userEmail']
    existingContent = [crs for crs in call(webserviceAccessParams, 'core_course_search_courses', criterianame='search', criteriavalue=courseShortName)[
        'courses'] if crs['shortname'] == courseShortName]
    if len(existingContent) == 0:
        output = create_course_4m_course_db(
            SQLengine, SQLengineApp, webserviceAccessParams, courseShortName, templateShortName, userEmail)
        # print(output)
        parameters['updateComment'] = 'course created'
        msg = course_content_GitHub_push(mgGH, SQLengine, parameters)
    else:
        update_moodle_course_info_4m_course_db(
            SQLengine, SQLengineApp, webserviceAccessParams, courseShortName)
        parameters['updateComment'] = 'course updated'
        msg = course_content_GitHub_push(mgGH, SQLengine, parameters)
        output = existingContent[0]
    # print(msg)
    return output


def create_course_4m_course_db(SQLengine, SQLengineApp, webserviceAccessParams, courseCode4mTable, templateShortName, userEmail):
    courseName = pd.read_sql('SELECT course_name FROM course WHERE course_code="{}"'.format(
        courseCode4mTable), SQLengineApp)['course_name'].to_list()[0]
    categoryName = pd.read_sql('SELECT CAH3_skill_classification FROM course WHERE course_code="{}"'.format(
        courseCode4mTable), SQLengineApp)['CAH3_skill_classification'].to_list()[0]
    params = {'webserviceAccessParams': webserviceAccessParams, 'templateShortName': templateShortName, 'categoryName': categoryName,
              'fullname': courseName, 'shortname': courseCode4mTable, 'customfields': [{'shortname': 'author', 'value': userEmail}]}
    output = create_course_4m_moodle_template(params)
    update_moodle_course_info_4m_course_db(
        SQLengine, SQLengineApp, webserviceAccessParams, courseCode4mTable)
    return output


def course_table_2_hvp_accordion(SQLengine, parameters):
    courseCode = parameters['courseCode4mTable']
    # print(courseCode)
    filtered = parameters['filtered']
    json_content = parameters['json_content']
    chosen_course_info_dict = pd.read_sql(
        'SELECT * FROM course WHERE course_code="{}"'.format(courseCode), SQLengine).to_dict(orient='records')[0]
    json_content_dict = json.loads(json_content)
    filtered_dict = json.loads(filtered)
    # print(json_content_dict)
    json_content_panelNames = {
        panel['title']: ip for ip, panel in enumerate(json_content_dict['panels'])}
    filtered_panelNames = {panel['title']: ip for ip,
                           panel in enumerate(filtered_dict['panels'])}
    panel2dbtablemap = {'CAH3 Skill Classification': 'CAH3_skill_classification', 'Total Number of Credits': 'course_credits',
                        'Objective': 'course_objective', 'Author': 'course_updated_by'}
    for chosenPanelName in [*panel2dbtablemap]:
        filtered_dict['panels'][filtered_panelNames[chosenPanelName]]['content']['params']['text'] = '<p>{}</p>'.format(
            chosen_course_info_dict[panel2dbtablemap[chosenPanelName]])
        json_content_dict['panels'][json_content_panelNames[chosenPanelName]
                                    ]['content']['params']['text'] = '<p>{}</p>'.format(chosen_course_info_dict[panel2dbtablemap[chosenPanelName]])
    chosenPanelName = 'Depth Level'
    filtered_dict['panels'][filtered_panelNames[chosenPanelName]]['content']['params']['text'] = '<p>SOLO Level={}</p>\n <p>BLOOMS Level={}</p>'.format(
        chosen_course_info_dict['SOLO_level'], chosen_course_info_dict['BLOOMS_level'])
    json_content_dict['panels'][json_content_panelNames[chosenPanelName]]['content']['params']['text'] = '<p>SOLO Level={}</p>\n <p>BLOOMS Level={}</p>'.format(
        chosen_course_info_dict['SOLO_level'], chosen_course_info_dict['BLOOMS_level'])
    xx1 = []
    for icr, cr in enumerate(chosen_course_info_dict['credit_to_ILO_map'].split(',')):
        xx1.append('<li>ILO{}: (CR-{}) {}</li>'.format(icr+1,
                   cr.replace(' ', ''), chosen_course_info_dict['ILO'+str(icr+1)]))
    chosenPanelName = 'Intended Learning Outcomes (ILOs)'
    filtered_dict['panels'][filtered_panelNames[chosenPanelName]
                            ]['content']['params']['text'] = '<ul>\n'+'\n '.join(xx1)+'</ul>'
    json_content_dict['panels'][json_content_panelNames[chosenPanelName]
                                ]['content']['params']['text'] = '<ul>\n'+'\n '.join(xx1)+'</ul>'
    return {'json_content': json.dumps(json_content_dict), 'filtered': json.dumps(filtered_dict)}
