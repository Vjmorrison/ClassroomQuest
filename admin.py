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
from ndbEntityDefs import Course


class AdminHandler(BaseRequestHandler):


    def RenderSuccess(self):
        if not self.IsUserInAdminWhitelist(users.get_current_user()):
            BaseRequestHandler.handle_404(self.request, self.response, "")
            return

        PAGE_DEFS = {
            "REVIEW": self.RenderSubmissionReview,
            "CHARACTERS": self.RenderCharacterReview,
            "COURSES": self.RenderCourseReview,
            "ADMINS": self.RenderAdminReview,
            "DELETEALLSUBMISSIONS": self.ProcessDeleteAll,
        }

        requestedPage = self.request.get("page")

        if requestedPage is "":
            requestedPage = "REVIEW"

        requestedPage = str(requestedPage).upper()
        PAGE_DEFS[requestedPage]()

    def RenderCharacterReview(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Admin ' + users.get_current_user().nickname()
        user = users.get_current_user()
        waitingCharacters = Character.GetWaitingCharacters()
        allCharacters = Character.GetAllCharacters()
        allCourseNames = {}

        allCourses = Course.GetAllCourses()
        if not allCourses is None:
            for course in allCourses:
                allCourseNames[course.key.integer_id()] = course.courseNumber + ": " + course.courseName

        template_values = {
            'titleDesc': PAGE_DESCRIPTION,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
            'character': Character.GetCharacterByUser(user),
            'waitingCharacters': waitingCharacters,
            'allCharacters': allCharacters,
            'allCourseNames': allCourseNames,
        }
        self.RenderTemplate("admin_Characters", template_values)

        return

    def RenderCourseReview(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Admin ' + users.get_current_user().nickname()
        user = users.get_current_user()

        allCourses = Course.GetAllCourses()

        template_values = {
            'titleDesc': PAGE_DESCRIPTION,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
            'character': Character.GetCharacterByUser(user),
            'allCourses': allCourses,
        }

        self.RenderTemplate("admin_Courses", template_values)

        return

    def RenderAdminReview(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Admin ' + users.get_current_user().nickname()
        user = users.get_current_user()
        return

    def RenderSubmissionReview(self):
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
            PAGE_DEFS = {
            "REVIEW": self.ProcessProjectSubmission,
            "CHARACTERS": self.ProcessCharacterSubmission,
            "COURSES": self.ProcessCourseSubmission,
            "ADMINS": self.RenderAdminReview,
            }
            requestedPage = str(self.request.get('page')).upper()
            if requestedPage is "":
                requestedPage = "REVIEW"

            PAGE_DEFS[requestedPage]()
        else:
            self.handle_404(self.request, self.response, "")

    def ProcessDeleteAll(self):
        ndb.delete_multi(
            SubmittedProject.query().fetch(keys_only=True)
        )

    def ProcessCharacterSubmission(self):
        accepted = self.request.get("Accept") == 'True'
        userID = self.request.get("userID")

        character = Character.GetCharacterByID(userID)
        if character.fullName == "GUEST":
            self.handle_404(self.request, self.response, "")
            return

        if accepted:
            character.isUnderReview = False
            character.put()
        else:
            character.Delete()

    def ProcessCourseSubmission(self):

        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Admin ' + users.get_current_user().nickname()
        user = users.get_current_user()

        template_values = {
            'titleDesc': PAGE_DESCRIPTION,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
            'character': Character.GetCharacterByUser(user),
            'linkURL': "/admin?page=courses",
            'linkText': "Courses",
        }

        delete = self.request.get("delete") == "True"
        courseID = self.request.get("number")
        course = Course.GetCourseByNumber(courseID)

        if delete and course is not None:
            if course:
                course.Delete()
                self.RenderTemplate("failure", template_values)
                return

        name = self.request.get("name")
        number = self.request.get("number")
        description = self.request.get("description")
        maxLevel = self.request.get("maxLevel")
        syllabusLink = self.request.get("link")
        levelReqForA = self.request.get("levelForA")
        iconURL = self.request.get("iconURL")

        if course is None:
            course = Course()

        if len(name) < 0 or len(name) < 0 or len(name) < 0 or len(name) < 0 or len(name) < 0 or len(name) < 0:
            self.RenderTemplate("failure", template_values)
            return

        course.courseName = name
        course.courseNumber = number
        course.courseDescription = description
        course.maxProjectLevel = int(maxLevel)
        course.syllabusLink = syllabusLink
        course.levelReqForA = int(levelReqForA)
        course.iconURL = iconURL

        course.put()

        self.RenderTemplate("success", template_values)

        return

    def ProcessAdminSubmission(self):
        return

    def ProcessProjectSubmission(self):
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