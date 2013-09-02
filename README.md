ClassroomQuest
==============

A GAE (google app engine) project that gives classrooms the ability to have student driven experiences.  Students complete assignments, gain XP, and level up!

Tech Structure
---------
* The app is written in Python using the Google App Engine as a platform.  
* The Web responses are built upon webapp2.
* Page rendering is handled with Jinja2.
* The HTML portions of the site use Bootstap.css and Javascript for all formatting and interactivity.
* Because of Bootstrap and the current javascript, this site runs best in Chrome and FireFox.  IE has some formatting issues.


How To Use
----------
Currently these is a lot of work that needs to be done to make this more user friendly.  As it stands, much of the personalization and editing must be done in code/html.

1. Download the current build.
2. Change the whitelist checking in the IsUserInWhitelist function, Line 64 of 
2. Upload the system to your App Engine project (to set up google app engine, please try the following tutorial:(https://developers.google.com/appengine/docs/python/gettingstartedpython27/introduction)
3. 
