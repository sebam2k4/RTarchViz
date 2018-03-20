# RTarchViz

## Introduction

(Real-Time Architectural Visualizations)

Market for 3d assets in Unreal Engine for arch viz

Users can register and then both buy and sell assets using the application

### Target Audience


## Apps
### Account App
Reused accounts app created in one of the Lessons
It included a custom Email Authentication Backend for authenticating users based on email address instead of django's default username. Also, it contained views and templates for login, registration, profile, and logout as well as forms for registration and login.

I extended the app in the following ways:
- Added EditProfileForm that extends forms.ModelForm and allows authenticated user to edit their email, username, name, date of birth, bio, and address. The update profile view passes in the instance of user data as argument to the form which prefills all form fields with correct user information.
- Created change_password view that integrates django's built in PasswordChangeForm to provide a simple password change form available to users. The form is available from user's profile page. The view also updates the session hash appropriately to prevent a pasword change from loggin out the session.
- Removed the app's custom password validation on registration form as django's built in password validation is more sufficient.
- Integrated password reset via email for cases when user forgets their password and cannot login. Also, created custom templates for the password reset stages

#### Password Validation
Using Django's Built in Password validation:
- password can't be too similar to your other personal information. (on password change)
- password must contain at least 8 characters.
- password can't be a commonly used password.
- password can't be entirely numeric.

#### ToDo
- prevent password_reset access to logged in users. Currently using django's built in password reset views and not sure how to do this without rewriting the views using `is_authenticated`
- Split the long registration into two forms or use ajax to split it up for better user experience. As it is now, the registration form requires user to fill in lots of fields in one go. 1st page: email, username, password. 2nd page: bio, dob, address.

### Pages App
Static pages like the homepage and about

## Production Deployment

### Heroku
Project is deployed to Heroku and uses a free trier of Postgres add-on for the database.

The project's settings.py contains production specific settings...

#### Live Demo
[https://rtarchviz.herokuapp.com/](https://rtarchviz.herokuapp.com/)

#### Environment Variables
requires setting the following ENVIRONMENT VARIABLES in Heroku Settings:
```
DATABASE_URL=<link to your provisioned Heroku Postgres db or other>
ENV=production
SECRET_KEY=<your django secret key>

```

optional ENVIRONMENT VARIABLES:
```
EMAIL_HOST_USER=<email address>
EMAIL_HOST_PASSWORD=<email password>
```
The above is needed for emailing password recovery links to users. May require changing security settings in your email client. If not set, the password recovery links will be printed to console instead.

#### Packages
Some packages that needed to be inmplemented for Production:
- dj-database-url for Postgresql db connection on Heroku
- gunicorn for serving the app on Heroku
- whitenoise to allow the web app to serve its own static
files

### Travis CI
Travis Continous Integrations is used to test builds before they're deployed to Heroku. Automated test will be implemented to run on builds to make sure app's code is performing as expected to minimize the risk of a broken production app.

## 3rd Party Apps/Packages Used:
- django-bootstrap4: [docs](http://django-bootstrap4.readthedocs.io/en/latest/index.html)

## Other Todo
#### Bootstrap Forms
- disable error message on top of form or change erros to only indicate the form fields that are invalid  (same error messages appear under appropriate form fields)

