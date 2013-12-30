__author__ = 'vjmor_000'

import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
import logging
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

        waitingList = SubmittedProject.query(SubmittedProject.accepted == None and SubmittedProject.rejected == None).fetch(1000)

        allUsers = Character.query().fetch(10000)
        submissionList = {}
        #print waitingList
        #print allUsers
        #print submissionList
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
            userID = str(self.request.get("userID"))
            subCharacter = Character.GetCharacterByID(userID)
            submittedProject = SubmittedProject.query(SubmittedProject.userID == subCharacter.userID and (SubmittedProject.accepted == None and SubmittedProject.rejected == None)).fetch(1)
            #submittedProject = SubmittedProject.query(ndb.AND(SubmittedProject.userID == subCharacter.userID, ndb.AND(SubmittedProject.accepted == None , SubmittedProject.rejected == None))).fetch(1)
            if accepted:
                logging.info(submittedProject)
                if not submittedProject is None and len(submittedProject) == 1:
                    submittedProject = submittedProject[0]
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
                    logging.error("Could not find Submitted Project!")
            else:
                if not submittedProject is None and len(submittedProject) == 1:
                    submittedProject = submittedProject[0]
                    submittedProject.accepted = False
                    submittedProject.rejected = True
                    submittedProject.ReviewedTime = datetime.datetime.now() - datetime.timedelta(hours=7)
                    submittedProject.put()
                else:
                    logging.error("Could not find Submitted Project!")
        else:
            self.handle_404(self.request, self.response, "")