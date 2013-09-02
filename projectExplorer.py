__author__ = 'vjmor_000'

import os
import urllib
import csv
import types

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
from baseRequestHandler import BaseRequestHandler
from ndbEntityDefs import Project
from ndbEntityDefs import Character


class ProjectsHandler(BaseRequestHandler):

    def RenderSuccess(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Admin ' + users.get_current_user().nickname()
        user = users.get_current_user()

        projectKey = self.request.get("projectKey")
        if not projectKey == "":
            projectKey = int(projectKey)
        if self.IsUserInAdminWhitelist(user) and not projectKey == "":
            self.ProcessPostMessage()
        else:
            projects = Project.GetProjects()
            template_values = {
                'titleDesc': PAGE_DESCRIPTION,
                'url': url,
                'url_linktext': url_linktext,
                'user': user,
                'projects_list': projects,
                'character': Character.GetCharacterByUser(user)
            }
            self.RenderTemplate("projects", template_values)

    def ProcessPostMessage(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Admin ' + users.get_current_user().nickname()
        user = users.get_current_user()
        if self.IsUserInAdminWhitelist(user):
            projectKey = int(self.request.get("projectKey"))

            project = Project.GetProject(projectKey)

            submission = bool(self.request.get("save"))
            if submission:
                newName = self.request.get("projectName")
                newDesc = self.request.get("description")
                newLevel = int(self.request.get("level"))
                newXP = int(self.request.get("xp"))
                newVideoURL = self.request.get("videoURL")
                newRequirements = []

                for i in range(100):
                    requirementValue = self.request.get("requirement_" + str(i))
                    if requirementValue == "":
                        break
                    newRequirements.append(requirementValue)

                project.projectName = newName
                project.xp = newXP
                project.level = newLevel
                project.description = newDesc
                project.requirements = newRequirements
                if not newVideoURL == 'None':
                    project.videoURL = newVideoURL

                project.put()

                projects = Project.GetProjects()
                template_values = {
                    'titleDesc': PAGE_DESCRIPTION,
                    'url': url,
                    'url_linktext': url_linktext,
                    'user': user,
                    'projects_list': projects,
                    'character': Character.GetCharacterByUser(user)
                }
                self.RenderTemplate("projects", template_values)

            else:
                template_values = {
                    'titleDesc': PAGE_DESCRIPTION,
                    'url': url,
                    'url_linktext': url_linktext,
                    'user': user,
                    'project': project,
                    'character': Character.GetCharacterByUser(user)
                }
                self.RenderTemplate("projectEditor", template_values)
        else:
            self.handle_404(self.request, self.response, "")

