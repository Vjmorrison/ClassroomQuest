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
from ndbEntityDefs import Course


class SignupHandler(BaseRequestHandler):

    def RenderSuccess(self):
        self.RenderSignupPage()

    def RenderGuest(self):
        newUser = self.request.get("fullName")
        if not newUser == "":
            self.ProcessPostMessage()
        else:
            self.RenderSignupPage()

    def RenderSignupPage(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Signup - ' + users.get_current_user().nickname()
        user = users.get_current_user()

        template_values = {
            'titleDesc': PAGE_DESCRIPTION,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
        }

        character = Character.GetCharacterByUser(user)
        if character.username == "GUEST":
            courses = Course.GetCourses()
            template_values["allCourses"] = courses
            self.RenderTemplate("signup", template_values)
        else:
            template_values['character'] = character
            self.RenderTemplate("signupExists", template_values)

    def ProcessPostMessage(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Signup - ' + users.get_current_user().nickname()
        user = users.get_current_user()

        template_values = {
            'titleDesc': PAGE_DESCRIPTION,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
            'linkURL': "/",
            'linkText': "MainPage",
        }

        character = Character.GetCharacterByUser(user)
        if not character.username == "GUEST":
            self.RenderTemplate("failure", template_values)

        fullName = self.request.get("fullName")
        nickname = self.request.get("nickname")
        imgURL = self.request.get("imageURL")
        selectedCourse = self.request.get("selectedCourse")

        Character.PutNewCharacter(user, fullName, nickname, selectedCourse, imgURL)
        self.RenderTemplate("success", template_values)

