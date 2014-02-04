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
from ndbEntityDefs import SubmittedProject, Character, Project, Course


class GuestHandler(BaseRequestHandler):

    def get(self):
        if users.get_current_user():
            self.RenderSuccess()
        else:
            self.RenderFailure()

    def RenderSuccess(self):
        url = users.create_logout_url(self.request.uri)

        path = str(self.request.path)

        pathSplit = filter(None, path.split('/'))

        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Welcome Back Guest'
        user = users.get_current_user()
        template_values = {
            'titleDesc': PAGE_DESCRIPTION,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
            'character': Character.GetGuestCharacter(),
            'projects_list': Project.GetProjects(),
            'levelReqForA': Course.GetCourseByNumber("GUEST").levelReqForA,
            'levelIconURL': Character.GetGuestCharacter().GetLevelIconURL(),
        }

        templateRefs = {
            "charactersheet": "charactersheet",
            "contact"       : "contact",
            "projects"      : "projects",
            "admin"         : "admin",
        }
        if len(pathSplit) == 1:
            self.RenderTemplate("index", template_values)
        else:
            self.RenderTemplate(templateRefs.get(pathSplit[1], "index"), template_values)

    def RenderFailure(self):
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'
        PAGE_DESCRIPTION = 'Please Login'
        template_values = {
            'titleDesc': PAGE_DESCRIPTION,
            'url': url,
            'url_linktext': url_linktext,
        }
        self.RenderTemplate("login", template_values)