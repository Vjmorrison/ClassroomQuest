__author__ = 'vjmor_000'

import types
import csv
import math

from google.appengine.ext import ndb


class Character(ndb.Model):
    username = ndb.StringProperty()
    fullName = ndb.StringProperty()
    xp = ndb.IntegerProperty()
    level = ndb.IntegerProperty()
    numProjects = ndb.IntegerProperty()
    currentProjectKey = ndb.IntegerProperty()
    courseID = ndb.IntegerProperty()
    avatar = ndb.StringProperty(indexed=False)
    user = ndb.UserProperty()
    userID = ndb.StringProperty()
    isAdmin = ndb.BooleanProperty()
    isUnderReview = ndb.BooleanProperty()

    levelIcons = ['http://i.imgur.com/hUMMKMg.gif', 'http://i.imgur.com/hUMMKMg.gif',
                  'http://i.imgur.com/ymBFo1w.gif',
                  'http://i.imgur.com/2pYN6xR.gif',
                  'http://i.imgur.com/lFzmAH2.gif',
                  'http://i.imgur.com/M8PvDZT.gif',
                  'http://i.imgur.com/YUVmV3x.gif',
                  'http://i.imgur.com/uGd0W1Q.gif',
                  'http://i.imgur.com/sdpyIK7.gif',
                  'http://i.imgur.com/ZdA5r4g.gif',
                  'http://i.imgur.com/r1wuscm.gif']

    def UpdateLevel(self):
        self.level = int(math.floor((1 + math.sqrt(int(self.xp) / 125 + 1)) / 2))

    def XpToNextLevel(self):
        return int(500 * self.level * (self.level + 1)) - self.xp

    def AcceptCharacter(self):
        self.isUnderReview = False

    def RejectCharacter(self):
        self.Delete()

    def Delete(self):
        self.key.delete()

    def GetLevelIconURL(self):
        if self.level > len(self.levelIcons):
            return self.levelIcons[0]
        return self.levelIcons[self.level]

    @classmethod
    def GetCharacterByUser(cls, pUser):
        qry = Character.query(Character.userID == pUser.user_id())
        character = qry.get()
        if character:
            return character
        else:
            return cls.GetGuestCharacter()

    @classmethod
    def GetWaitingCharacters(cls):
        qry = Character.query(Character.isUnderReview == True)
        allRecords = qry.fetch()
        if allRecords is None:
            return None
        if not isinstance(allRecords, types.ListType):
            allRecords = [allRecords]
        return allRecords

    @classmethod
    def GetAllCharacters(cls):
        qry = Character.query()
        allRecords = qry.fetch()
        if allRecords is None:
            return None
        if not isinstance(allRecords, types.ListType):
            allRecords = [allRecords]
        return allRecords

    @classmethod
    def PutNewCharacter(cls, pUser, pFullName, pUsername, pCourseID, avatarURL):
        character = Character()
        character.username = pUsername
        character.fullName = pFullName
        character.user = pUser
        if pUser:
            character.userID = pUser.user_id()
        character.level = 1
        if avatarURL is None:
            avatarURL = "/images/missing.png"
        character.avatar = avatarURL
        character.currentProjectKey = 0
        character.courseID = int(pCourseID)
        character.numProjects = 0
        character.xp = 0
        character.isAdmin = False
        character.isUnderReview = True
        character.put()
        return character

    @classmethod
    def GetCharacterByID(cls, pUserID):
        qry = Character.query(Character.userID == str(pUserID))
        character = qry.get()
        if character:
            return character
        return cls.GetGuestCharacter()

    @classmethod
    def GetCharacterByName(cls, charName):
        char = Character.query(Character.username == str(charName)).fetch(1)
        if isinstance(char, types.ListType) and len(char) > 0:
            char = char[0]
        return char

    @classmethod
    def GetGuestCharacter(cls):
        guestCourse = Course.GetCourseByNumber("GUEST")
        if not guestCourse:
            guestCourse = Course.PutNewCourse("GUEST", "GUEST", "A temp course for users to sample the website", "http://gamedevpanthers.appspot.com/", 100, 101, "http://i.imgur.com/62a8wtI.jpg")

        guestChar = Character.GetCharacterByName("GUEST")
        if not guestChar:
            guestChar = Character.PutNewCharacter(None, "GUEST", "GUEST", -1, "/images/missing.png")
            guestChar.level = 20
            guestChar.xp = 190000
            guestChar.isUnderReview = False
            guestChar.put()
        elif guestChar.courseID == -1:
            guestChar.courseID = guestCourse.key.integer_id()
            guestChar.put()

        return guestChar

    @classmethod
    def UpdateAllRecords(cls):
        allRecords = Character.query()
        for character in allRecords:
            character.put()


class Course(ndb.Model):

    courseName = ndb.StringProperty()
    courseNumber = ndb.StringProperty()
    courseDescription = ndb.StringProperty()
    syllabusLink = ndb.StringProperty()
    maxProjectLevel = ndb.IntegerProperty()
    levelReqForA = ndb.IntegerProperty()
    iconURL = ndb.StringProperty()

    def Delete(self):
        self.key.delete()

    @classmethod
    def UpdateAllRecords(cls):
        allRecords = Course.query()
        for course in allRecords:
            course.put()

    @classmethod
    def GetCourses(cls):
        allRecords = Course.query(Course.courseNumber < "GUEST" or Course.courseNumber > "GUEST").order(cls.courseNumber).fetch()
        if allRecords is None:
            return None
        if not isinstance(allRecords, types.ListType):
            allRecords = [allRecords]
        return allRecords

    @classmethod
    def GetAllCourses(cls):
        allRecords = Course.query().fetch()
        if not allRecords is None and not isinstance(allRecords, types.ListType):
            allRecords = [allRecords]
        return allRecords

    @classmethod
    def GetCourseByNumber(cls, courseNum):
        course = Course.query(Course.courseNumber == courseNum).fetch(1)
        if course is None or len(course) == 0:
            return None
        if isinstance(course, types.ListType):
            course = course[0]
        return course

    @classmethod
    def GetCourse(cls, courseID):
        try:
            return Course.get_by_id(courseID)
        except:
            return None

    @classmethod
    def PutNewCourse(cls, name, number, description, syllabus, maxProjectLevel, levelReqForA, iconURL):

        course = cls.GetCourseByNumber(number)
        if not course:
            course = Course()

        course.courseName = name
        course.courseNumber = number
        course.courseDescription = description
        course.syllabusLink = syllabus
        course.maxProjectLevel = maxProjectLevel
        course.levelReqForA = levelReqForA
        course.iconURL = iconURL

        course.put()
        return course


class Project(ndb.Model):
    projectName = ndb.StringProperty()
    xp = ndb.IntegerProperty()
    level = ndb.IntegerProperty()
    description = ndb.StringProperty(indexed=False)
    requirements = ndb.StringProperty(repeated=True, indexed=False)
    videoURL = ndb.StringProperty(indexed=False)
    attachments = ndb.StringProperty(repeated=True, indexed=False)

    @classmethod
    def GetProjects(cls):
        allProjects = Project.query().order(cls.level, cls.projectName).fetch()
        if not isinstance(allProjects, types.ListType):
            allProjects = [allProjects]
        return allProjects

    @classmethod
    def GetProject(cls, projectID):
        '''
        allProjects = cls.GetProjects()
        for project in allProjects:
            if project.key.integer_id() == projectID:
                return project
        return '''

        return Project.get_by_id(projectID)

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

    @classmethod
    def UpdateAllRecords(cls):
        allProjects = Project.query()
        for project in allProjects:
            project.put()


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

    @classmethod
    def GetAllRecords(cls):
        allRecords = Course.query().fetch()
        if not allRecords is None and not isinstance(allRecords, types.ListType):
            allRecords = [allRecords]
        return allRecords

    @classmethod
    def UpdateAllRecords(cls):
        allSubProjects = SubmittedProject.query()
        for submittedProject in allSubProjects:
            submittedProject.put()

    def Delete(self):
        self.key.delete()
