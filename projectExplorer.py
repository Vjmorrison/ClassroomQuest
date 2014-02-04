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
        user = users.get_current_user()

        projectKey = self.request.get("projectKey")
        if not projectKey == "":
            projectKey = int(projectKey)
        if self.IsUserInAdminWhitelist(user) and not projectKey == "":
            self.ProcessPostMessage()
        else:
            self.RenderProjectList()

    def RenderProjectList(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Admin ' + users.get_current_user().nickname()
        user = users.get_current_user()

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
            stringKey = self.request.get("projectKey")
            if not stringKey == '':
                projectKey = int(stringKey)
            else:
                projectKey = -1

            project = Project()

            if not projectKey == -1:
                project = Project.GetProject(projectKey)
                if project is None:
                    self.RenderProjectList()
                    return
                if bool(self.request.get("delete")):
                    project.key.delete()
                    self.RenderProjectList()
                    return

            isSubmission = bool(self.request.get("save"))

            if isSubmission:
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

                newAttachments = []

                for j in range(100):
                    attachmentValue = self.request.get("attachment_" + str(j))
                    if attachmentValue == "":
                        break
                    newAttachments.append(attachmentValue)

                project.projectName = newName
                project.xp = newXP
                project.level = newLevel
                project.description = newDesc
                project.requirements = newRequirements
                project.attachments = newAttachments
                if not newVideoURL == 'None' or newVideoURL == "":
                    project.videoURL = newVideoURL

                project.put()

                self.RenderProjectList()

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

