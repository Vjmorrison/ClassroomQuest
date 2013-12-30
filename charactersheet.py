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
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
from baseRequestHandler import BaseRequestHandler

from ndbEntityDefs import Character
from ndbEntityDefs import Project
from ndbEntityDefs import SubmittedProject


class CharacterSheetHandler(BaseRequestHandler):

    def RenderSuccess(self):
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
        PAGE_DESCRIPTION = 'Welcome Back ' + users.get_current_user().nickname()
        user = users.get_current_user()
        character = Character.GetCharacterByUser(user)

        allList = SubmittedProject.query(SubmittedProject.userID == user.user_id()).fetch(1000)
        completedList = [i for i in allList if i.accepted]
        waitingList = [i for i in allList if not i.accepted and not i.rejected]

        allProjects = Project.GetProjects()
        projectsToDo = []
        for proj in allProjects:
            addProj = True
            for sub in completedList:
                if sub.projectID == proj.key.integer_id():
                    addProj = False
                    break
            if addProj:
                if proj.level <= character.level or proj.level >= 5:
                    projectsToDo.append(proj)

        template_values = {
            'titleDesc': PAGE_DESCRIPTION,
            'url': url,
            'url_linktext': url_linktext,
            'user': user,
            'character': character,
            'projects_list': projectsToDo
        }

        allList = SubmittedProject.query(SubmittedProject.userID == user.user_id()).fetch(100)
        completedList = [i for i in allList if i.accepted]
        waitingList = [i for i in allList if not i.accepted and not i.rejected]
        if waitingList:
            template_values["submitted"] = True
        if completedList:
            template_values["completed_projects_list"] = completedList

        self.RenderTemplate("charactersheet", template_values)

    def ProcessPostMessage(self):
        newProjectKey = int(self.request.get("currentProjectKey"))

        if newProjectKey:
            user = users.get_current_user()
            character = Character.GetCharacterByUser(user)
            character.currentProjectKey = newProjectKey
            character.put()

        if bool(self.request.get("SubmitProject")):
            self.SubmitNewProject(users.get_current_user(), newProjectKey)
            self.response.write("Submission Passed!")

    def SubmitNewProject(self, user, projectKey):

        allProjects = Project.GetProjects()

        project = [i for i in allProjects if i.key.integer_id() == int(projectKey)]
        print project
        if project:
            project = project[0]
            submission = SubmittedProject()
            submission.projectID = projectKey
            submission.projectName = project.projectName
            submission.submissionTime = datetime.datetime.now() - datetime.timedelta(hours=7)
            submission.userID = user.user_id()
            submission.put()
        return

