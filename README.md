ClassroomQuest
==============

A GAE (google app engine) project that gives classrooms the ability to have student driven experiences.  Students complete assignments, gain XP, and level up!

View a live sample at [http://gamedevpanthers.appspot.com/](http://gamedevpanthers.appspot.com/)

Tech Structure
---------
* The app is written in Python using the Google App Engine as a platform.  
* The Web responses are built upon webapp2.
* Page rendering is handled with Jinja2.
* The HTML portions of the site use Bootstap.css and Javascript for all formatting and interactivity.
* Because of Bootstrap and the current javascript, this site runs best in Chrome and FireFox.  IE has some formatting issues.
* Current User Verification is a combination of default Google users API and a built in Whitelist function.


How To Use
----------
Currently these is a lot of work that needs to be done to make this more user friendly.  As it stands, much of the personalization and editing must be done in code/html.

1. Download the current build.
2. Change the Whitelist checking in the IsUserInWhitelist function, Line 64 of baseRequestHandler.py
3. Upload the system to your App Engine project (to set up google app engine, please try the following tutorial:(https://developers.google.com/appengine/docs/python/gettingstartedpython27/introduction)
4. Visit your page and get started!

Personalization
---------------
The Whitelist of email addresses or base email addresses is added in the config.ini file.
Your first admin email should also be added there.

Since there are very limited admin personalization controls yet within the app, all visual and formatting changes must be done in code.

Main.py: The core Python class for handling web requests.  If a different handler is required (admin, charactersheet, etc..) it is detailed at the bottom of main.py.

```python
app = webapp2.WSGIApplication(debug=True)
app.router.add(('/', MainHandler))
app.router.add(('/charactersheet', CharacterSheetHandler))
app.router.add(('/contact', ContactHandler))
app.router.add(('/projects', ProjectsHandler))
app.router.add(('/admin', AdminHandler))

app.error_handlers[404] = BaseRequestHandler.handle_404
```

Each of the other classes only handle the requests for that routed web-request.

