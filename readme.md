# RTarchViz

[![Build Status](https://travis-ci.org/sebam2k4/RTarchViz.svg?branch=master)](https://travis-ci.org/sebam2k4/RTarchViz)
![Test Coverage](./coverage.svg)

## Overview

### Introduction

RTarchViz is a (fictional) marketplace for high quality assets specially created for use in real-time architectural visualizations in Unreal Engine. These assets can consist of, but are not limited to, in-engine 3d models, sounds, blueprints, scripts, and full environments.

RTarchViz stands for: Real-Time Architectural Visualizations

### Overview
Built with Django, Python based full-stack web framework, and uses PostgreSQL database to store user info, products, orders, transaction history and more. Registered have the ability to buy and list their own digital products as well as have access to a dashboard containing a list of their listed products for easy management (edit or remove product), their sales analytics, total profit, and download links to any product they may have purchased from other users.

## Initial Planning
The following is a list of documents and aids I've prepared as initial planning of the project before starting any development:

- Project oberview, objectives, and user stories - [link](https://docs.google.com/document/d/1-eduWsa66LwbZy3K1NvCp19e98N5x2WGsnXL32zCHBE/edit#)
- Initial Database Design - [link](https://drive.google.com/file/d/1gwDZj5uqMsBzC_gA1S25YVLqELmQa6zC/view?usp=drive_web)
- Interactive Prototype created in Adobe XD: [link](https://xd.adobe.com/view/c8d0be9e-8251-4f8b-84d9-ca2848a9b181/)

## APPS

### Account App
Reused accounts app created in one of the Stream 3 Lessons from the Code Institute's LMS
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

#### Issues/Bugs
- title model field is unique but case sensitive. Can accept both 'Post 1' and 'post 1' but if both added will get MultipleObjectsReturned exception. (clean title by changing first letters to uppercase except for 'the', 'a', etc.)

### Products App
Products app for displaying listed products as well as providing means for users to add, edit, and delete products as well as product reviews.

Products list uses django's Paginator to split product listings across multiple pages. A handy navigation is provided on the bottom of each page that user can use to navigate to the next or previous page as well as choosing specific page number. Provides better user experience.

Product filtering by category and sorting by newset, oldest, most popular, highest rating, a-z, and z-a provided on product list as well. A 'Back' button on botto of product detail page takes user back to products list preserving the user applied filter and sorting.

1 review per product per user allowed.

context processor used to keep track of user's owned products

There are two checks done to validate product file uploads. First, the product file is checked if it is a .zip file size is 2.5MB max.

The product file and image filenames are generated using a custom method to include the product's slug value and palce the files into user's product folder.

### Cart App
Session based cart

### Checkout App
Stripe payments - Stripe v2 API
Purchase History - keep accurate record of all transactions.
Thank You Page - copy cart session contents to purchase session to list purchased products on thank you page.

## LOCAL DEVELOPMENT SETUP

coming soon...

## DEPLOYMENT
Project is deployed to Heroku and uses a free trier of Postgres add-on for the database.
The project's settings.py contains production specific settings...

#### Live Demo
[https://rtarchviz.herokuapp.com/](https://rtarchviz.herokuapp.com/)

#### Environment Variables
requires setting the following environment variables in Heroku Settings:
```
DATABASE_URL=<link to your provisioned Heroku Postgres db or other>
ENV=production
SECRET_KEY='<your django secret key>'
```

optional ENVIRONMENT VARIABLES:
```
EMAIL_HOST_USER='<email address>'
EMAIL_HOST_PASSWORD='<email password>'
```
The above is needed for emailing password recovery links to users. May require changing security settings in your email client. If not set, the password recovery links will be printed to console instead.

django-storages
```
AWS_STORAGE_BUCKET_NAME='<your S3 bucket name>'
AWS_S3_REGION_NAME='<your S3 bucket region, ex: eu-west-1'>
AWS_ACCESS_KEY_ID='<your IAM user access key>'
AWS_SECRET_ACCESS_KEY='<your IAM user secret access key>'
```
for setting up AWS S3 and IAM refer to the 'Amazon S3 Setup' portion of this [tutorial](https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html)

Once set up, run `python manage.py collectstatic` which is going to copy all static files to your s3 bucket. If you have any user uploaded media files then you may have to copy them to s3 manually. Don't forget to run the command everytime you make changes to your css, js, and static images to update your s3 bucket.

#### Packages
Some packages that needed to be inmplemented for Production:
- dj-database-url for Postgresql db connection on Heroku
- gunicorn for serving the app on Heroku
- whitenoise to allow the web app to serve its own static
files (is this needed when using django-storages with AWS S3?)
- django-storages for storing static files and user uploaded media on AWS S3 bucket

### Travis CI
Travis Continous Integrations is used to test builds before they're deployed to Heroku. Automated test will be implemented to run on builds to make sure app's code is performing as expected to minimize the risk of a broken production app. 

## 3RD PARTY APPS USED:
- [django-bootstrap4](http://django-bootstrap4.readthedocs.io/en/latest/index.html): used for forms
- [Disqus](https://django-disqus.readthedocs.io/en/latest/): used for comments on blog posts
- [TinyMCE](http://django-tinymce.readthedocs.io/en/latest/): Provides a WYSIWYG text editor for writing blog posts by staff members in the admin site. 
- [django-social-share](https://pypi.org/project/django-social-share/): provides template tags for sharing object data on popular social media networks. I've overriden the templates to implement font-awesome 5 icons and to fit the style of my website.

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