# RTarchViz

[![Build Status](https://travis-ci.org/sebam2k4/RTarchViz.svg?branch=master)](https://travis-ci.org/sebam2k4/RTarchViz)
![Test Coverage](./coverage.svg)


**In Early Development**

## Introduction

(Real-Time Architectural Visualizations)

Market for 3d assets in Unreal Engine for arch viz

Users can register and then both buy and sell assets using the application

### Target Audience


## APPS
### Account App
Reused accounts app created in one of the Lessons
It included a custom Email Authentication Backend for authenticating users based on email address instead of django's default username. Also, it contained views and templates for login, registration, profile, and logout as well as forms for registration and login.

I extended the app in the following ways:
- Added EditProfileForm that extends forms.ModelForm and allows authenticated user to edit their email, username, name, date of birth, bio, and address. The update profile view passes in the instance of user data as argument to the form which prefills all form fields with correct user information.
- Created change_password view that integrates django's built in PasswordChangeForm to provide a simple password change form available to users. The form is available from user's profile page. The view also updates the session hash appropriately to prevent a pasword change from loggin out the session.
- Removed the app's custom password validation on registration form as django's built in password validation is more sufficient.
- Integrated password reset via email for cases when user forgets their password and cannot login. Also, created custom templates for the password reset stages
- User profile pages now accessible by other users
- Added a private user dashboard for sale and purchase stats


#### Validation
- Password: Using Django's Built in Password validation
  - password can't be too similar to your other personal information. (on password change)
  - password must contain at least 8 characters.
  - password can't be a commonly used password.
  - password can't be entirely numeric.
- Username:
  - case sensitive, but unique in a way that no two users can have same letters usernames no matter what letter case. If a user has a username 'JoHn' then another user cannot register or change their username to 'john'.
- Email:
  - email is always saved in db in lowercase no matter how it was entered at registration and all validation checks against it are case insensitive.

#### ToDo
- prevent password_reset access to logged in users. Currently using django's built in password reset views and not sure how to do this without rewriting the views using `is_authenticated`
- Split the long registration into two forms or use ajax to split it up for better user experience. As it is now, the registration form requires user to fill in lots of fields in one go. 1st page: email, username, password. 2nd page: bio, dob, address.

#### Issues/Bugs

### Homepage App
The project's homepage that uses custom inclusion tags to display most recent products and blog posts.

### Blog App
Blog app for latest news and tutorials. Managed only by is_staff (company staff) who can add, edit, and delete posts in Django's built in, although extended/modified, admin. The staff users are provided with a handy form and a main texarea for the writing the blog content using the tinyMCE WYSIWYG text editor.

admin for Blog Posts sports a nice display of filterable and orderable fields that makes it easy for staff to search for posts they are working on (drafts) or want to edit/update. Can also get some statistical filters to see which posts are performing well (have most views or comments).

Super User needs to designate the user a staff member in the django admin as well add the user to the STAFF group to have add/edit/delete blog post permissions.

Blog posts use Disqus for comments

Blog Posts use django's Paginator for their list view to split posts across several pages. A handy navigation is provided on the bottom of each page that user can use to navigate to the next or previous page as well as choosing specific page number. Provide better user experience. Also, each post detail view provides useful navigation to next or previous post or back to posts list.

Post filtering available to user on blog list page. options: newset, oldest, most popular, tutorials, news

Custom model save method - Overriding the save method to generate datetime stamps for published date and updated date for posts. Published date gets stamped when posts is actually published (status is initially changed from 'draft' to 'published'). Once a post is published then saving it again will add updated date. Any consequent saves to the post will update the updated date with current date and time. Published date stays the same and indicates the date when post was originally published.

#### ToDo:
- Add ability for staff to add/upload images to post's content through tinyMCE. May need some file manager for this or some kind of many-to-many post-media setup.

#### Useful Docs:
- https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_for_foreignkey

#### Issues/Bugs
- title model field is unique but case sensitive. Can accept both 'Post 1' and 'post 1' but if both added will get MultipleObjectsReturned exception. (clean title by changing first letters to uppercase except for 'the', 'a', etc.)
- getting 2 duplicated sql queries in post_detail view for selecting "accounts_user"."id" = "id" ??? - investigate

### Products App
Products app for displaying listed products as well as providing means for users to add, edit, and delete products as well as product reviews.

Products list uses django's Paginator to split product listings across multiple pages. A handy navigation is provided on the bottom of each page that user can use to navigate to the next or previous page as well as choosing specific page number. Provides better user experience.

Product filtering by category and sorting by newset, oldest, most popular, highest rating, a-z, and z-a provided on product list as well. A 'Back' button on botto of product detail page takes user back to products list preserving the user applied filter and sorting.

1 review per product per user allowed.

context processor used to keep track of user's owned products

There are two checks done to validate product file uploads. First, the product file is checked if it is a .zip file size is 2.5MB max.

#### To Do:
- check user uploads 'zip' or '7z' and not other file type.
- look into proper file upload and donwload solution (serving files from MEDA_ROOT is not recommended for production)
- uploading multiple files for product images
- Add optional fields to product such as: No of materials, no of modesl, no of triangles... etc.
- Consider moving Add Review Form logic from product_detail view into its own

#### Useful Docs:
- https://docs.djangoproject.com/en/2.0/topics/http/file-uploads/
- https://www.allbuttonspressed.com/projects/django-filetransfers

#### Issues/Bugs
- Change or modify the Product Detail carousel to make displaying product images more uniform. User may upload images with different measurements and they may display cropped depending on screen size/browser size. Currently Images are diaplay using css background-image. Don't want users restricted to having to uplaod a very specific image resolution sieze. Explore this maybe: http://kenwheeler.github.io/slick/ for responsive slider
- Product file will be uploaded to MEDIA_ROOT/seller_id_<id>/product_id_<id>-<filename> note: see if can incorporate username in addition to seller_id (need to import User model?)

### Cart App
Session based cart

### Checkout App
Stripe payments

## LOCAL DEVELOPMENT SETUP

coming soon...

## DEPLOYMENT
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

## 3RD PARTY APPS USED:
- django-bootstrap4: used for forms [docs](http://django-bootstrap4.readthedocs.io/en/latest/index.html)
- Disqus: used for blog post comments
- TinyMCE: WYSIWYG text editor used in project's admin site used by staff members to write blog posts.

## Other Todo/issues

#### General
- better way to do filters? Is it a good or bad to have object filters in views?
- Prevent multiple form submissions when user clicks submit button multiple times

#### Bootstrap Forms
- disable error message on top of form or change erros to only indicate the form fields that are invalid  (same error messages appear under appropriate form fields)

#### Other
- Possible help for preserving get query strings from view instead of templates (nice to have improvement): https://stackoverflow.com/questions/4477090/django-redirect-using-reverse-to-a-url-that-relies-on-query-strings

## General

### URLs
Now using get_absolute_url model methods for any urls that take arguments, such as review_edit, product_detail, etc. Easier to maintain and if urls change then will need to make changes in only one place.

## TESTING
Iintegration and unit testing.
Travis-CI
Coverage

### Coverage

'coverage run manage.py test' runs the project's tests and creates a coverage report.

Then, run 'coverage report' to view the report in shell

Alternatively, run 'coverage html' to pritify the report. This command creates a 'htmlcov' direcroty containing the test coverage. The 'index.html' is the overview file which links to the other files and provides detail code coverage information. 