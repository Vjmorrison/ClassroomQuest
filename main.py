#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import logging
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from charactersheet import CharacterSheetHandler
from baseRequestHandler import BaseRequestHandler
from projectExplorer import ProjectsHandler
from contact import ContactHandler
from admin import AdminHandler
from ndbEntityDefs import Character
from ndbEntityDefs import SubmittedProject
from GuestHandlers import GuestHandler
from signup import SignupHandler


class MainHandler(BaseRequestHandler):

    def RenderSuccess(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Welcome Back ' + users.get_current_user().nickname()
        user = users.get_current_user()
        template_values = {
            'titleDesc': PAGE_DESCRIPTION,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
            'character': Character.GetCharacterByUser(user),
            'waitingSubmission': SubmittedProject.UserHasWaitingSubmission(user),
        }
        self.RenderTemplate("index", template_values)

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



app = webapp2.WSGIApplication(debug=True)
app.router.add(('/', MainHandler))
app.router.add(('/guest', GuestHandler))
app.router.add(('/guest/.*', GuestHandler))
app.router.add(('/charactersheet', CharacterSheetHandler))
app.router.add(('/contact', ContactHandler))
app.router.add(('/projects', ProjectsHandler))
app.router.add(('/admin', AdminHandler))
app.router.add(('/signup', SignupHandler))


app.error_handlers[404] = BaseRequestHandler.handle_404
