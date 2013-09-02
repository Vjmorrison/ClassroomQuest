__author__ = 'vjmor_000'

import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
from baseRequestHandler import BaseRequestHandler
from ndbEntityDefs import Character
from ndbEntityDefs import SubmittedProject
from ndbEntityDefs import Project


class AdminHandler(BaseRequestHandler):

    def RenderSuccess(self):
        if not self.IsUserInAdminWhitelist(users.get_current_user()):
            BaseRequestHandler.handle_404(self.request, self.response, "")
            return

        for arg in self.request.arguments():
            print self.request.get(arg)
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Admin ' + users.get_current_user().nickname()
        user = users.get_current_user()

        allSubmissions = SubmittedProject.query().fetch(100)
        waitingList = [i for i in allSubmissions if not i.accepted and not i.rejected]

        allUsers = Character.query().fetch(100)
        submissionList = {}
        print waitingList
        print allUsers
        print submissionList
        for submission in waitingList:
            for thisUser in allUsers:
                if thisUser.userID == submission.userID:
                    submissionList.update({submission.key.integer_id(): [submission, thisUser]})
                    break

        template_values = {
            'titleDesc': PAGE_DESCRIPTION,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
            'character': Character.GetCharacterByUser(user),
            'allSubmissions': submissionList,
            'allUsers': allUsers,
        }
        self.RenderTemplate("admin", template_values)

    def ProcessPostMessage(self):
        user = users.get_current_user()
        if self.IsUserInAdminWhitelist(user):
            subKey = int(self.request.get("submissionKey"))
            accepted = bool(self.request.get("Accept"))
            subCharacter = Character.GetCharacterByID(self.request.get("userID"))
            submittedProject = ''
            for submission in SubmittedProject.query().fetch(100):
                if submission.key.integer_id() == subKey:
                    submittedProject = submission
                    break
            if accepted:
                if not submittedProject == '':
                    submittedProject.accepted = True
                    submittedProject.rejected = False
                    submittedProject.ReviewedTime = datetime.datetime.now() - datetime.timedelta(hours=7)
                    submittedProject.put()
                    subCharacter.xp += Project.GetProject(submittedProject.projectID).xp
                    subCharacter.UpdateLevel()
                    subCharacter.currentProjectKey = 0
                    if subCharacter.numProjects is None:
                        subCharacter.numProjects = 0
                    subCharacter.numProjects += 1
                    subCharacter.put()
            else:
                if not submittedProject == '':
                    submittedProject.accepted = False
                    submittedProject.rejected = True
                    submittedProject.ReviewedTime = datetime.datetime.now() - datetime.timedelta(hours=7)
                    submittedProject.put()
        else:
            self.handle_404(self.request, self.response, "")