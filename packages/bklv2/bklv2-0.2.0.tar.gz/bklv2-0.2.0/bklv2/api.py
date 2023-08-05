# -*- coding: utf-8 -*-

import datetime
import shutil
import requests
import json
import rfc6266


def _gpath( path ):
    """
        "https://test.backlog.jp/" -> "https://test.backlog.jp/"
        "https://test.backlog.jp" -> "https://test.backlog.jp/"
    """
    if path == "":
        return "./"
    elif path.endswith( "/" ):
        return path
    else:
        return path + "/"


def _addkw( dic, k, w ):
    """
        dic[] -> dic[k] = w
    """
    if w != None:
        if isinstance( w, ( tuple, list ) ):
            for i, v in w:
                _addkw( dic, k + "[" + i + "]", v )
        elif isinstance( w, bool ):
            if w == True:
                dic[k] = "true"
            else:
                dic[k] = "false"
        elif isinstance( w, datetime.date ):
                dic[k] = w.strftime( "%Y-%m-%d" )
        else:
            dic[k] = w


def _addkws( dic, k, w ):
    """
        dic[] -> dic[k[]] = w[]
    """
    if w != None:
        if isinstance( w, ( tuple, list ) ):
            i=0
            for v in w:
                _addkw( dic, k + "[" + str(i) + "]", v )
                i+=1
        else:
            _addkw( dic, k + "[0]", w )


def _dicset( dic, k, w, tuples ):
    for t in tuples:
        if k==t:
            _addkws( dic, k[0:-1], w )
            return
    _addkw( dic, k, w )


class api( object ):
    """
    Backlog API version 2 wrapper
    """

    def __init__( self, hostname, apikey ):
        """
            hostname: "https://[spacename].backlog.jp"
            apikey: "nWdhOFxDpAlsFTGSIHisRkUvTq5eTiBDBJ0FFqAdtLTSIvKpfkvb09Kteststring"
        """
        if hostname.endswith( "/" ):
            self.hostname = hostname.rstrip("/")
        else:
            self.hostname = hostname
        self.apikey = apikey


    def _makeurl( self, path ):
        return self.hostname + path


    def _api_return( self, response, **kwargs ):
        self.response = response
        output="json"
        dir_path = "./"
        for k, v in kwargs.items():
            if k == "output":
                output = v
            elif k == "dirpath":
                dirpath = v

        if output == "json":
            try:
                return json.loads( self.response.text )
            except:
                return {}
        elif output == "response":
            return response
        elif output == "path":
            if response.status_code == 200:
                rr = rfc6266.parse_requests_response( response )
                p = _gpath( dirpath ) + rr.filename_unsafe
                with open( p, 'wb' ) as fp:
                    response.raw.decode_content = True
                    shutil.copyfileobj( response.raw, fp )
                return p
        return self.response.text


    def getSpace( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-space
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/space" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getRecentUpdates( self,
                       activityTypeIds = None,
                       minId = None,
                       maxId = None,
                       count = None,
                       order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-recent-updates
        """
        params = { "apiKey": self.apikey }
        _addkws( params, "activityTypeId", activityTypeIds )
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/space/activities" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getSpaceLogo( self,
                       output = "path",
                       dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-space-logo
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/space/image" )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath )


    def getSpaceNotification( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-space-notification
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/space/notification" )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateSpaceNotification( self, content ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-space-notification
        """
        params = { "apiKey": self.apikey }
        data = { "content": content }
        url = self._makeurl( "/api/v2/space/notification" )

        return self._api_return(
            requests.put( url, params = params, data = data ) )


    def getSpaceDiskUsage( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-space-disk-usage
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/space/diskUsage" )

        return self._api_return(
            requests.get( url, params = params ) )


    def postAttachmentFile( self, filepath ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/post-attachment-file
        """
        params = { "apiKey": self.apikey }
        fp = open( filepath, "rb" )
        files = { "file": [ requests.utils.guess_filename( fp ),
                          fp.read(),
                          "application/octet-stream" ] }
        fp.close()
        url = self._makeurl( "/api/v2/space/attachment" )

        return self._api_return(
            requests.post( url, params = params, files = files ) )


    def getUserList( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user-list
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/users" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getUser( self, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/users/" + str( userId ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def addUser( self, userId, password, name, mailAddress, roleType ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-user
        """
        params = { "apiKey": self.apikey }
        data = { "userId": userId, "password": password, "name": name,
                 "mailAddress": mailAddress, "roleType": roleType }
        url = self._makeurl( "/api/v2/users" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateUser( self, userId,
                    password = None,
                    name = None,
                    mailAddress = None,
                    roleType = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-user
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "password", password )
        _addkw( data, "name", name )
        _addkw( data, "mailAddress", mailAddress )
        _addkw( data, "roleType", roleType )
        url = self._makeurl( "/api/v2/users/" + str( userId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteUser( self, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-user
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/users/" + str( userId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getOwnUser( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-own-user
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/users/myself" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getUserIcon( self, userId,
                     output = "path",
                     dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user-icon
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/users/" + str( userId ) + "/icon" )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath )


    def getUserRecentUpdates( self, userId,
                           activityTypeIds = None,
                           minId = None,
                           maxId = None,
                           count = None,
                           order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-user-recent-updates
        """
        params = { "apiKey": self.apikey }
        _addkws( params, "activityTypeIds", activityTypeIds )
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/users/" + str( userId ) + "/activities" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getReceivedStarList( self, userId,
                      minId = None,
                      maxId = None,
                      count = None,
                      order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-received-star-list
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/users/" + str( userId ) + "/stars" )

        return self._api_return(
            requests.get( url, params = params ) )


    def countUserReceivedStars( self, userId,
                           since = None,
                           until = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/count-user-received-stars
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "since", since )
        _addkw( params, "until", until )
        url = self._makeurl( "/api/v2/users/" + str( userId ) + "/stars/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getListOfRecentlyViewedIssues( self,
                                     order = None,
                                     offset = None,
                                     count = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-recently-viewed-issues
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "order", order )
        _addkw( params, "offset", offset )
        _addkw( params, "count", count )
        url = self._makeurl( "/api/v2/users/myself/recentlyViewedIssues" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getListOfRecentlyViewedProjects( self,
                                       order = None,
                                       offset = None,
                                       count = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-recently-viewed-projects
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "order", order )
        _addkw( params, "offset", offset )
        _addkw( params, "count", count )
        url = self._makeurl( "/api/v2/users/myself/recentlyViewedProjects" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getListOfRecentlyViewedWikis( self,
                                    order = None,
                                    offset = None,
                                    count = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-recently-viewed-wikis
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "order", order )
        _addkw( params, "offset", offset )
        _addkw( params, "count", count )
        url = self._makeurl( "/api/v2/users/myself/recentlyViewedWikis" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getListOfGroups( self,
                   order = None,
                   offset = None,
                   count = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-groups
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "order", order )
        _addkw( params, "offset", offset )
        _addkw( params, "count", count )
        url = self._makeurl( "/api/v2/groups" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addGroup( self, name,
                  members = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-group
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        _addkws( data, "members", members )
        url = self._makeurl( "/api/v2/groups" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getGroup( self, groupId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-group
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/groups/" + str( groupId ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateGroup( self, groupId,
                     name = None,
                     members = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-group
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "name", name )
        _addkws( data, "members", members )
        url = self._makeurl( "/api/v2/groups/" + str( groupId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteGroup( self, groupId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-group
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/groups/" + str( groupId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getStatusList( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-status-list
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/statuses" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getResolutionList( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-resolution-list
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/resolutions" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getPriorityList( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-priority-list
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/priorities" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getProjectList( self,
                     archived = None,
                     all = False ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project-list
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "archived", archived )
        _addkw( params, "all", all )
        url = self._makeurl( "/api/v2/projects" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addProject( self, name, key, chartEnabled, subtaskingEnabled, textFormattingRule,
                    projectLeaderCanEditProjectLeader = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-project
        """
        params = { "apiKey": self.apikey }
        data = { "name": name, "key": key }
        _addkw( data, "chartEnabled", chartEnabled )
        _addkw( data, "subtaskingEnabled", subtaskingEnabled )
        _addkw( data, "textFormattingRule", textFormattingRule )
        _addkw( data, "projectLeaderCanEditProjectLeader", projectLeaderCanEditProjectLeader )
        url = self._makeurl( "/api/v2/projects" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getProject( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" ) + str( projectIdOrKey )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateProject( self, projectIdOrKey,
                       name = None,
                       key = None,
                       chartEnabled = None,
                       subtaskingEnabled = None,
                       projectLeaderCanEditProjectLeader = None,
                       textFormattingRule = None,
                       archived = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-project
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "name", name )
        _addkw( data, "key", key )
        _addkw( data, "chartEnabled", chartEnabled )
        _addkw( data, "subtaskingEnabled", subtaskingEnabled )
        _addkw( data, "textFormattingRule", textFormattingRule )
        _addkw( data, "projectLeaderCanEditProjectLeader", projectLeaderCanEditProjectLeader )
        _addkw( data, "archived", archived )
        url = self._makeurl( "/api/v2/projects/" ) + str( projectIdOrKey )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteProject( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-project
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" ) + str( projectIdOrKey )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getProjectIcon( self, projectIdOrKey,
                        output = "path",
                        dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project-icon
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + "/image" )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath  )


    def getProjectRecentUpdates( self, projectIdOrKey,
                              activityTypeIds = None,
                              minId = None,
                              maxId = None,
                              count = None,
                              order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project-recent-updates
        """
        params = { "apiKey": self.apikey }
        _addkws( params, "activityTypeIds", activityTypeIds )
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/activities" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addProjectUser( self, projectIdOrKey, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-project-user
        """
        params = { "apiKey": self.apikey }
        data = { "userId": userId }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/users" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getProjectUserList( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project-user-list
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/users" )

        return self._api_return(
            requests.get( url, params = params ) )


    def deleteProjectUser( self, projectIdOrKey, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-project-user
        """
        params = { "apiKey": self.apikey }
        data = { "userId": userId }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/users" )

        return self._api_return(
            requests.delete( url, params = params, data = data ) )


    def addProjectAdministrator( self, projectIdOrKey, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-project-administrator
        """
        params = { "apiKey": self.apikey }
        data = { "userId": userId }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/administrators" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getListOfProjectAdministrators( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-project-administrators
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/administrators" )

        return self._api_return(
            requests.get( url, params = params ) )


    def deleteProjectAdministrator( self, projectIdOrKey, userId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-project-administrator
        """
        params = { "apiKey": self.apikey }
        data = { "userId": userId }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/administrators" )

        return self._api_return(
            requests.delete( url, params = params, data = data ) )


    def getIssueTypeList( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-issue-type-list
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/issueTypes" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addIssueType( self, projectIdOrKey, name, color ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-issue-type
        """
        params = { "apiKey": self.apikey }
        data = { "name": name, "color": color }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/issueTypes" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateIssueType( self, projectIdOrKey, id,
                         name = None,
                         color = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-issue-type
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "name", name )
        _addkw( data, "color", color )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/issueTypes/" + str( id ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteIssueType( self, projectIdOrKey, id, substituteIssueTypeId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-issue-type
        """
        params = { "apiKey": self.apikey }
        data = { "substituteIssueTypeId": str( substituteIssueTypeId ) }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/issueTypes/" + str( id ) )

        return self._api_return(
            requests.delete( url, params = params, data = data ) )


    def getCategoryList( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-category-list
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/categories" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addCategory( self, projectIdOrKey, name ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-category
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/categories" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateCategory( self, projectIdOrKey, id, name ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-category
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/categories/" + str( id ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteCategory( self, projectIdOrKey, id ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-category
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/categories/" + str( id ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getVersionMilestoneList( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-version-milestone-list
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/versions" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addVersionMilestone( self, projectIdOrKey, name,
                    description = None,
                    startDate = None,
                    releaseDueDate = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-version-milestone
            startDate,releaseDueDate : YYYY-MM-DD
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        _addkw( data, "description", description )
        _addkw( data, "startDate", startDate )
        _addkw( data, "releaseDueDate", releaseDueDate )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/versions" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateVersionMilestone( self, projectIdOrKey, id, name,
                       description = None,
                       startDate = None,
                       releaseDueDate = None,
                       archived = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-version-milestone
            startDate,releaseDueDate : YYYY-MM-DD
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        _addkw( data, "description", description )
        _addkw( data, "startDate", startDate )
        _addkw( data, "releaseDueDate", releaseDueDate )
        _addkw( data, "archived", archived )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/versions/" + str( id ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteVersion( self, projectIdOrKey, id ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-version
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/versions/" + str( id ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getCustomFieldList( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-custom-field-list
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addCustomField( self, projectIdOrKey, typeId, name, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-custom-field
        """
        tuples = ["items", "applicableIssueTypes"]
        params = { "apiKey": self.apikey }
        data = { "typeId": typeId, "name": name }
        for k, v in kwargs.items():
            _dicset( data, k, v, tuples )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateCustomField( self, projectIdOrKey, customFieldId, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-custom-field
        """
        tuples = ["items", "applicableIssueTypes"]
        params = { "apiKey": self.apikey }
        data = {}
        for k, v in kwargs.items():
            _dicset( data, k, v, tuples )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields/" + str( customFieldId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteCustomField( self, projectIdOrKey, customFieldId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-custom-field
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields/" + str( customFieldId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def addListItemForListTypeCustomField( self, projectIdOrKey, customFieldId, name ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-list-item-for-list-type-custom-field
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields/" + str( customFieldId ) + \
                             "/items" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def updateListItemForListTypeCustomField( self, projectIdOrKey, customFieldId, itemId, name ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-list-item-for-list-type-custom-field
        """
        params = { "apiKey": self.apikey }
        data = { "name": name }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields/" + str( customFieldId ) + \
                             "/items/" + str( itemId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteListItemForListTypeCustomField( self, projectIdOrKey, customFieldId, itemId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-list-item-for-list-type-custom-field
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/customFields/" + str( customFieldId ) + \
                             "/items/" + str( itemId ) )

        return self._api_return(
            requests.delete( url, params = params ) )

    def getListOfSharedFiles( self, projectIdOrKey,
                        path = "",
                        order = None,
                        offset = None,
                        count = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-shared-files
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "order", order )
        _addkw( params, "offset", offset )
        _addkw( params, "count", count )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/files/metadata/" + str( path ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def getFile( self, projectIdOrKey, sharedFileId,
                       output = "path",
                       dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-file
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/files/" + str( sharedFileId ) )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath )


    def getProjectDiskUsage( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project-disk-usage
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/diskUsage" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getListOfWebhooks( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-webhooks
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/webhooks" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addWebhook( self, projectIdOrKey, name, hookUrl,
                    description = None,
                    allEvent = None,
                    activityTypeIds = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-webhook
        """
        params = { "apiKey": self.apikey }
        data = { "name": name, "hookUrl": hookUrl }
        _addkw( data, "description", description )
        _addkw( data, "allEvent", allEvent )
        _addkws( data, "activityTypeIds", activityTypeIds )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/webhooks" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getWebhook( self, projectIdOrKey, webhookId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-webhook
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/webhooks/" + str( webhookId ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateWebhook( self, projectIdOrKey, webhookId,
                       name = None,
                       hookUrl = None,
                       description = None,
                       allEvent = None,
                       activityTypeIds = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-webhook
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "name", name )
        _addkw( data, "description", description )
        _addkw( data, "hookUrl", hookUrl )
        _addkw( data, "allEvent", allEvent )
        _addkws( data, "activityTypeIds", activityTypeIds )
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/webhooks/" + str( webhookId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteWebhook( self, projectIdOrKey, webhookId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-webhook
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/webhooks/" + str( webhookId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getIssueList( self, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-issue-list
        """
        tuples = [ "projectIds", "issueTypeIds", "categoryIds", "versionIds", \
                   "milestoneIds", "statusIds", "priorityIds", "assigneeIds", \
                   "createdUserIds", "resolutionIds", "ids", "parentIssueIds" ]
        params = { "apiKey": self.apikey }
        for k, w in kwargs.items():
            _dicset(params,k,w,tuples)
        url = self._makeurl( "/api/v2/issues" )

        return self._api_return(
            requests.get( url, params = params ) )


    def countIssue( self, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/count-issue
        """
        tuples = [ "projectIds", "issueTypeIds", "categoryIds", "versionIds", \
                   "milestoneIds", "statusIds", "priorityIds", "assigneeIds", \
                   "createdUserIds", "resolutionIds", "ids", "parentIssueIds" ]
        params = { "apiKey": self.apikey }
        for k, w in kwargs.items():
            _dicset(params,k,w,tuples)
        url = self._makeurl( "/api/v2/issues/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addIssue( self, projectId, summary, issueTypeId, priorityId, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-issue
        """
        tuples = [ "categoryIds", "versionIds", "milestoneIds", "notifiedUserIds", "attachmentIds" ]
        params = { "apiKey": self.apikey }
        data = { "projectId": projectId, "summary": summary, "issueTypeId": issueTypeId, "priorityId": priorityId }
        for k, w in kwargs.items():
            _dicset(data,k,w,tuples)
        url = self._makeurl( "/api/v2/issues" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getIssue( self, issueIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-issue
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateIssue( self, issueIdOrKey, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-issue
        """
        tuples = [ "categoryIds", "versionIds", "milestoneIds", "notifiedUserIds", "attachmentIds" ]
        params = { "apiKey": self.apikey }
        data = {}
        for k, w in kwargs.items():
            _dicset(data,k,w,tuples)
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteIssue( self, issueIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-issue
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getCommentList( self, issueIdOrKey,
                     minId = None,
                     maxId = None,
                     count = None,
                     order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-comment-list
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addComment( self, issueIdOrKey, content,
                    notifiedUserIds = None,
                    attachmentIds = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-comment
        """
        params = { "apiKey": self.apikey }
        data = {"content": content}
        _addkw( data, "content", content )
        _addkws( data, "notifiedUserId", notifiedUserIds )
        _addkws( data, "attachmentId", attachmentIds )
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def countComment( self, issueIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/count-comment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getComment( self, issueIdOrKey, commentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-comment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/" + str( commentId ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateComment( self, issueIdOrKey, commentId, content ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-comment
        """
        params = { "apiKey": self.apikey }
        data = { "content": content }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/" + str( commentId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def getListPfCommentNotifications( self, issueIdOrKey, commentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-comment-notifications
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/" + str( commentId ) + \
                             "/notifications" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addCommentNotification( self, issueIdOrKey, commentId, notifiedUserIds ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-comment-notification
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkws( data, "notifiedUserId", notifiedUserIds )
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/" + str( commentId ) + \
                             "/notifications" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getListOfIssueAttachments( self, issueIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-issue-attachments
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/attachments" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getIssueAttachment( self, issueIdOrKey, attachmentId,
                            output = "path",
                            dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-issue-attachment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/attachments/" + str( attachmentId ) )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath )

    def deleteIssueAttachment( self, issueIdOrKey, attachmentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-issue-attachment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/attachments/" + str( attachmentId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getListOfLinkedSharedFiles( self, issueIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-linked-shared-files
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/sharedFiles" )

        return self._api_return(
            requests.get( url, params = params ) )


    def removeLinkToSharedFileFromIssue( self, issueIdOrKey, fileId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/remove-link-to-shared-file-from-issue
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "fileId", fileId )
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/sharedFiles/" + str( fileId ) )

        return self._api_return(
            requests.delete( url, params = params, data = data ) )


    def getWikiPageList( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page-list
        """
        params = { "apiKey": self.apikey, "projectIdOrKey": projectIdOrKey }
        url = self._makeurl( "/api/v2/wikis" )

        return self._api_return(
            requests.get( url, params = params ) )


    def countWikiPage( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/count-wiki-page
        """
        params = { "apiKey": self.apikey, "projectIdOrKey": projectIdOrKey }
        url = self._makeurl( "/api/v2/wikis/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getWikiPageTagList( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page-tag-list
        """
        params = { "apiKey": self.apikey, "projectIdOrKey": projectIdOrKey }
        url = self._makeurl( "/api/v2/wikis/tags" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addWikiPage( self, projectId, name, content,
                 mailNotify = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-wiki-page
        """
        params = { "apiKey": self.apikey }
        data = { "projectId": projectId , "name": name, "content": content }
        _addkw( data, "mailNotify", mailNotify )
        url = self._makeurl( "/api/v2/wikis" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getWikiPage( self, wikiId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updateWikiPage( self, wikiId,
                    name = None,
                    content = None,
                    mailNotify = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-wiki-page
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "name", name )
        _addkw( data, "content", content )
        _addkw( data, "mailNotify", mailNotify )
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteWikiPage( self, wikiId,
                    mailNotify = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-wiki-page
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "mailNotify", mailNotify )
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) )

        return self._api_return(
            requests.delete( url, params = params, data = data ) )


    def getListOfWikiAttachments( self, wikiId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-wiki-attachments
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/attachments" )

        return self._api_return(
            requests.get( url, params = params ) )


    def attachFileToWiki( self, wikiId, attachmentIds ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/attach-file-to-wiki
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkws( data, "attachmentId", attachmentIds )
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/attachments" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getWikiPageAttachment( self, wikiId, attachmentId,
                           output = "path",
                           dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page-attachment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/attachments/" + str( attachmentId ) )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath )

    def removeWikiAttachment( self, wikiId, attachmentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/remove-wiki-attachment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/attachments/" + str( attachmentId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getListOfSharedFilesOnWiki( self, wikiId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-shared-files-on-wiki
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/sharedFiles" )

        return self._api_return(
            requests.get( url, params = params ) )


    def linkSharedFilesToWiki( self, wikiId, fileIds ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/link-shared-files-to-wiki
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkws( data, "fileId", fileIds )
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/sharedFiles" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def removeLinkToSharedFileFromWiki( self, wikiId, fileId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/remove-link-to-shared-file-from-wiki
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + \
                             "/sharedFiles/" + str( fileId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getWikiPageHistory( self, wikiId,
                        minId = None,
                        maxId = None,
                        count = None,
                        order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page-history
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + "/history" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getWikiPageStar( self, wikiId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-wiki-page-star
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/wikis/" + str( wikiId ) + "/stars" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addStar( self,
                 issueId = None,
                 commentId = None,
                 wikiId = None,
                 pullRequestsId = None,
                 pullRequestCommentId = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-star
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "issueId", issueId )
        _addkw( data, "commentId", commentId )
        _addkw( data, "wikiId", wikiId )
        _addkw( data, "pullRequestsId", pullRequestsId )
        _addkw( data, "pullRequestCommentId", pullRequestCommentId )
        url = self._makeurl( "/api/v2/stars" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getNotification( self,
                         minId = None,
                         maxId = None,
                         count = None,
                         order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-notification
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/notifications" )

        return self._api_return(
            requests.get( url, params = params ) )


    def countNotification( self,
                              alreadyRead = None,
                              resourceAlreadyRead = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/count-notification
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "alreadyRead", alreadyRead )
        _addkw( params, "resourceAlreadyRead", resourceAlreadyRead )
        url = self._makeurl( "/api/v2/notifications/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def resetUnreadNotificationCount( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/reset-unread-notification-count
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/notifications/markAsRead" )

        return self._api_return(
            requests.post( url, params = params ) )


    def readNotification( self, notificationId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/read-notification
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/notifications/" + str( notificationId ) + \
                             "/markAsRead" )

        return self._api_return(
            requests.post( url, params = params ) )


    def getListOfGitRepositories( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-git-repositories
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getGitRepository( self, projectIdOrKey, repoIdOrName ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-git-repository
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) )

        return self._api_return(
            requests.get( url, params = params ) )


    def getPullRequestList( self, projectIdOrKey, repoIdOrName ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request-list
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getNumberOfPullRequests( self, projectIdOrKey, repoIdOrName ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-number-of-pull-requests
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addPullRequest( self, projectIdOrKey, repoIdOrName, summary, description, base, branch, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-pull-request
        """
        tuples = ["notifiedUserIds","attachmentIds"]
        params = { "apiKey": self.apikey }
        data = { "summary": summary, "description": description , "base": base, "branch ": branch }
        for k, v in kwargs.items():
            _dicset( data, k, v, tuples )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getPullRequest( self, projectIdOrKey, repoIdOrName, number ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) )

        return self._api_return(
            requests.get( url, params = params ) )


    def updatePullRequest( self, projectIdOrKey, repoIdOrName, number, **kwargs ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-pull-request
        """
        tuples = ["notifiedUserIds"]
        params = { "apiKey": self.apikey }
        data = {}
        for k, v in kwargs.items():
            _dicset( data, k, v, tuples )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def getPullRequestComment( self, projectIdOrKey, repoIdOrName, number,
                               minId = None,
                               maxId = None,
                               count = None,
                               order = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request-comment
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "minId", minId )
        _addkw( params, "maxId", maxId )
        _addkw( params, "count", count )
        _addkw( params, "order", order )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + "/comments" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addPullRequestComment( self, projectIdOrKey, repoIdOrName, number, content, notifiedUserIds ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-pull-request-comment
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkw( data, "content", content )
        _addkws( data, "notifiedUserId", notifiedUserIds )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + "/comments" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getNumberOfPullRequestComments( self, projectIdOrKey, repoIdOrName, number ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-number-of-pull-request-comments
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + "/comments/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def updatePullRequestComment( self, projectIdOrKey, repoIdOrName, number, commentId, content ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-pull-request-comment
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "content", content )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + \
                             "/comments/" + str(commentId) )

        return self._api_return(
            requests.patch( url, params = params ) )


    def getListOfPullRequestAttachment( self, projectIdOrKey, repoIdOrName, number ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-pull-request-attachment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + "/attachments" )

        return self._api_return(
            requests.get( url, params = params ) )


    def downloadPullRequestAttachment( self, projectIdOrKey, repoIdOrName, number, attachmentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/download-pull-request-attachment
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "content", content )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + \
                             "/attachments/" + str(attachmentId) )

        return self._api_return(
            requests.get( url, params = params ) )


    def deletePullRequestAttachments( self, projectIdOrKey, repoIdOrName, number, attachmentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-pull-request-attachments
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "content", content )
        url = self._makeurl( "/api/v2/projects/" + str(projectIdOrKey) + \
                             "/git/repositories/" + str(repoIdOrName) + \
                             "/pullRequests/" + str(number) + \
                             "/attachments/" + str(attachmentId) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getWatchingList( self, userId,
                         order = "desc",
                         sort = "issuerUpdated",
                         count = 20,
                         offset = None,
                         resourceAlreadyRead = None,
                         issueIds = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-watching-list
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "order", order )
        _addkw( params, "sort", sort )
        _addkw( params, "count", count )
        _addkw( params, "offset", offset )
        _addkw( params, "resourceAlreadyRead", resourceAlreadyRead )
        _addkws( params, "issueIds", issueIds )
        url = self._makeurl( "/api/v2/users/" + str(userId) + "/watchings" )

        return self._api_return(
            requests.get( url, params = params ) )


    def countWatching( self, userId,
                       resourceAlreadyRead = None,
                       alreadyRead = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/count-watching
        """
        params = { "apiKey": self.apikey }
        _addkw( params, "resourceAlreadyRead", resourceAlreadyRead )
        _addkw( params, "alreadyRead", alreadyRead )
        url = self._makeurl( "/api/v2/users/" + str(userId) + "/watchings/count" )

        return self._api_return(
            requests.get( url, params = params ) )


    def getWatching( self, watchingId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-watching
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/watchings/" + str(watchingId) )

        return self._api_return(
            requests.get( url, params = params ) )


    def addWatching( self, issueIdOrKey, note = None ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-watching
        """
        params = { "apiKey": self.apikey, "issueIdOrKey" : issueIdOrKey }
        _addkw( params, "note", note )
        url = self._makeurl( "/api/v2/watchings" )

        return self._api_return(
            requests.post( url, params = params ) )


    def updateWatching( self, watchingId, note ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-watching
        """
        params = { "apiKey": self.apikey }
        data = { "note" : note }
        url = self._makeurl( "/api/v2/watchings/" + str(watchingId) )

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def deleteWatching( self, watchingId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-watching
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/watchings/" + str(watchingId) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def markWatchingAsRead( self, watchId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/mark-watching-as-read
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/watchings/" + str(watchId) + "/markAsRead" )

        return self._api_return(
            requests.post( url, params = params ) )


    def deleteComment( self, issueIdOrKey, commentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-comment
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/" + str( commentId ) )

        return self._api_return(
            requests.delete( url, params = params ) )


    def getListOfCommentNotifications( self, issueIdOrKey, commentId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-list-of-comment-notifications
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/comments/" + str( commentId ) + \
                             "/notifications" )

        return self._api_return(
            requests.get( url, params = params ) )


    def updatePullRequestCommentInformation( self, projectIdOrKey, repoIdOrName, number, commentId, content ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/update-pull-request-comment-information
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/git/repositories/" + str( commentId ) + \
                             "/pullRequests/" + str( number ) + \
                             "/comments/" + str( commentId ) )

        data = { "content": content }

        return self._api_return(
            requests.patch( url, params = params, data = data ) )


    def linkSharedFilesToIssue( self, issueIdOrKey, fileIds ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/link-shared-files-to-issue
        """
        params = { "apiKey": self.apikey }
        data = {}
        _addkws( data, "fileId", fileIds )
        url = self._makeurl( "/api/v2/issues/" + str( issueIdOrKey ) + \
                             "/sharedFiles" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def getProjectGroupList( self, projectIdOrKey ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-project-group-list
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + "/groups" )

        return self._api_return(
            requests.get( url, params = params ) )


    def addProjectGroup( self, projectIdOrKey, groupId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/add-project-group
        """
        params = { "apiKey": self.apikey }
        data = { "groupId": groupId }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/groups" )

        return self._api_return(
            requests.post( url, params = params, data = data ) )


    def deleteProjectGroup( self, projectIdOrKey, groupId ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/delete-project-group
        """
        params = { "apiKey": self.apikey }
        data = { "groupId": groupId }
        url = self._makeurl( "/api/v2/projects/" + str( projectIdOrKey ) + \
                             "/groups" )

        return self._api_return(
            requests.delete( url, params = params, data = data ) )


    def getGroupIcon( self, groupId,
                     output = "path",
                     dirpath = "." ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-group-icon
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/groups/" + str( groupId ) + "/icon" )

        return self._api_return(
            requests.get( url, params = params, stream = True ),
            output = output,
            dirpath = dirpath )


    def getLicence( self ):
        """
            https://developer.nulab-inc.com/docs/backlog/api/2/get-licence
        """
        params = { "apiKey": self.apikey }
        url = self._makeurl( "/api/v2/space/licence" )

        return self._api_return(
            requests.get( url, params = params ) )
