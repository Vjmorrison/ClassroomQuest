__author__ = 'vjmor_000'

import types
import csv
import math

from google.appengine.ext import ndb


class Character(ndb.Model):
    xp = ndb.IntegerProperty()
    level = ndb.IntegerProperty()
    numProjects = ndb.IntegerProperty()
    currentProjectKey = ndb.IntegerProperty()
    className = ndb.StringProperty(indexed=False)
    avatar = ndb.StringProperty(indexed=False)
    user = ndb.UserProperty()
    userID = ndb.StringProperty()
    isAdmin = ndb.BooleanProperty()

    def UpdateLevel(self):
        self.level = int(math.floor((1 + math.sqrt(int(self.xp) / 125 + 1)) / 2))

    def XpToNextLevel(self):
        return int(500 * self.level * (self.level + 1)) - self.xp

    @classmethod
    def GetCharacterByUser(cls, pUser):
        qry = Character.query(Character.userID == pUser.user_id())
        character = qry.get()
        if character:
            return character
        else:
            character = Character()
            character.user = pUser
            character.userID = pUser.user_id()
            character.level = 1
            character.avatar = "images/missing.png"
            character.currentProjectKey = 0
            character.className = "NONE"
            character.numProjects = 0
            character.xp = 0
            character.isAdmin = False
            character.put()
            return character

    @classmethod
    def GetCharacterByID(cls, pUserID):
        print pUserID
        qry = Character.query(Character.userID == str(pUserID))
        character = qry.get()
        print character
        if character:
            return character


class Project(ndb.Model):
    projectName = ndb.StringProperty()
    xp = ndb.IntegerProperty()
    level = ndb.IntegerProperty()
    description = ndb.StringProperty(indexed=False)
    requirements = ndb.StringProperty(repeated=True, indexed=False)
    videoURL = ndb.StringProperty(indexed=False)

    @classmethod
    def GetProjects(cls):
        qry = Project.query().order(cls.level)
        allProjects = qry.fetch(100)
        if not allProjects:
            reader = csv.reader(open("projects.csv"), delimiter=',', quotechar='"')
            products = list(map(cls.ParseProductRow, reader))
            for product in products:
                product.put()
            allProjects = products
        if not isinstance(allProjects, types.ListType):
            allProjects = [allProjects]
        return allProjects

    @classmethod
    def GetProject(cls, projectID):
        allProjects = cls.GetProjects()
        for project in allProjects:
            if project.key.integer_id() == projectID:
                return project
        return

    @classmethod
    def ParseProductRow(cls, row):
        projectData = Project()
        print(row)
        projectData.projectName = row[0]
        projectData.xp = int(row[1])
        projectData.level = int(row[2])
        projectData.description = row[3]
        projectData.requirements = row[4].split('|')
        return projectData


class SubmittedProject(ndb.Model):
    projectName = ndb.StringProperty(indexed=False)
    projectID = ndb.IntegerProperty()
    submissionTime = ndb.DateTimeProperty()
    ReviewedTime = ndb.DateTimeProperty(indexed=False)
    userID = ndb.StringProperty()
    accepted = ndb.BooleanProperty()
    rejected = ndb.BooleanProperty()

    @classmethod
    def UserHasWaitingSubmission(cls, user):
        allList = SubmittedProject.query(SubmittedProject.userID == user.user_id()).fetch(100)
        waitingList = [i for i in allList if not i.accepted and not i.rejected]
        if len(waitingList) > 0:
            return waitingList[0]
        else:
            return False

    def Delete(self):
        self.key.delete()