# RTarchViz

[![Build Status](https://travis-ci.org/sebam2k4/RTarchViz.svg?branch=master)](https://travis-ci.org/sebam2k4/RTarchViz)
![Test Coverage](./coverage.svg)

## Overview

### Introduction

RTarchViz is a (fictional) marketplace for high quality assets specially created for use in real-time architectural visualizations in Unreal Engine. These assets can consist of, but are not limited to, in-engine 3d models, sounds, blueprints, scripts, and full environments.

RTarchViz stands for: Real-Time Architectural Visualizations

### Overview
Built with Django, Python based full-stack web framework, uses PostgreSQL database to store user info, products, orders, transaction history, etc., and is styled using Bootstrap4 and custom CSS.

Registered have the ability to buy and list their own digital products as well as have access to a dashboard containing a list of their listed products for easy management (edit or remove product), their sales analytics, total profit, and download links to any product they may have purchased from other users.

## Initial Planning
The following is a list of documents and aids I've prepared as initial planning of the project before starting any development:

- **[Project overview, objectives, and user stories](https://docs.google.com/document/d/1-eduWsa66LwbZy3K1NvCp19e98N5x2WGsnXL32zCHBE/edit#)**
- **[Initial Database Design](https://drive.google.com/file/d/1gwDZj5uqMsBzC_gA1S25YVLqELmQa6zC/view?usp=drive_web)**
- **[Interactive Prototype created in Adobe XD](https://xd.adobe.com/view/c8d0be9e-8251-4f8b-84d9-ca2848a9b181/)**

## TECH USED
The project is built using Python 2.7.14 and [Django 1.11](https://www.djangoproject.com/). Django is a high-level Python full-stack web framework.

### Front End Libraries
- **[Bootstrap 4.0](https://getbootstrap.com/)**
  - To give the project a nice responsive, mobile-first, grid layout
  - Easily add prebuilt components like navbar, cards, paginations, etc.
- **[jQuery 3.3.1](https://jquery.com/)**
  - Used for general javascript, DOM manipulation, and Ajax
  - Also a dependancy of Bootstrap 4
- **[FontAwesome 5.0.8](https://fontawesome.com/)**
  - To add awesome icons throughout the website, like cart, rating stars, and social icons.

### 3rd party Django modules (Back-End)
- **[django-bootstrap4 0.0.6](http://django-bootstrap4.readthedocs.io/en/latest/index.html)
  - Used for easy styling of form elements
- **[django-disqus 0.5](https://django-disqus.readthedocs.io/en/latest/)**
  - Used for comments on blog posts
- **[TinyMCE 2.7.0](http://django-tinymce.readthedocs.io/en/latest/)**
  - Provides a WYSIWYG text editor for writing blog posts by staff members in the admin site. 
- **[django-social-share 1.1.2](https://pypi.org/project/django-social-share/)**
  - Provides template tags for sharing object data on popular social media networks. 
  - I've overriden the templates to implement font-awesome 5 icons and to fit the style of my website.

###

## Note to Assessor

The project takes advantage of Django Admin for some of its features and as such requires a user to be a 'staff' member to access it. The following are login details for a 'staff' user that can be used to access the admin:

email:
username:
password:

## APPS

### Account App
Reused accounts app created in one of the Stream 3 Lessons from the Code Institute's LMS. It included a custom Email Authentication Backend for authenticating users based on email address instead of django's default username. Also, it contained views and templates for login, registration, profile, and logout as well as forms for registration and login.

I extended the app in the following ways:
- Added EditProfileForm that extends forms.ModelForm and allows authenticated user to edit their email, username, name, date of birth, bio, and address. The update profile view passes in the instance of user data as argument to the form which prefills all form fields with the user information.
- Created change_password view that integrates django's built in PasswordChangeForm to provide a simple password change form available to users. The form is available from user's profile page. The view also updates the session hash appropriately to prevent logging out the session after password change is perfomred.
- Removed the app's custom password validation on registration form as django's built in password validation is more sufficient.
- Integrated password reset via email for cases when user forgets their password and cannot login. Also, created custom templates for the password reset process.
- User profile page list the user's product and is accessible by other users, both anonymous and authenticated.
- Added a private user dashboard for displaying sale and purchase stats and managing products. User can easily add, edit, or delete new products from one place. User can also download any products they have purchased from a list of their purchases.
- Added Sales History list view
- Added Purchase History list view
- After successful authentication, cart contents are checked for any items that the user may already own or has listed and are removed. Any other items will remain in cart. User should not have the ability to buy own products or ones already purchased.

The Accounts App also handles validation for most common scenarios:
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
The project's homepage uses custom inclusion tags from blog and products apps to display most recent products and blog posts. Also, the homepage handles newsletter sign up form found in the footer by sending a confirmation email to the provided email address.

### Blog App
Blog app for displaying latest news and tutorials.

Blog Posts use django's Paginator for their list view to split posts across several pages. A handy navigation is provided on the bottom of each page that user can use to navigate to the next or previous page as well as choose specific page number. Also, posts are filterable by the following options: newset, oldest, most popular, tutorials, and news.

Also, each post detail view provides useful navigation to next or previous post or back to posts list.

Custom model save method - Overriding the save method to generate datetime stamps for published date and updated date for posts. Published date gets stamped when posts is actually published (status is initially changed from 'draft' to 'published'). Once a post is published then saving it again will add updated date. Any consequent saves to the post will update the updated date with current date and time. Published date stays the same and indicates the date when post was originally published.

Blog posts use Disqus for comments

Managed only by is_staff (company staff members) who can add, edit, and delete posts in Django's built in, although extended, admin. The staff users are provided with a handy form and a main texarea for the writing the blog content using the tinyMCE WYSIWYG text editor.

Admin list view for Blog Posts displays a nice table of filterable and orderable fields that makes it easy for staff to search for posts they are working on (drafts) or want to edit or update. Can also get some statistical filters to see which posts are performing well in terms of view count.

Super User needs to designate the user a staff member in the django admin as well add the user to the 'staff' group to gain add, edit, and delete blog post permissions.

### Products App
Products app for displaying listed products as well as providing means for users to add, edit, and delete products as well as product reviews.

Products list uses django's Paginator to split product listings across multiple pages. A handy navigation is provided on the bottom of each page that user can use to navigate to the next or previous page as well as choosing specific page number. Also product filtering by category and sorting by newset, oldest, most popular, highest rating, a-z, and z-a is possible through the template.

1 review per product per user allowed.

There are two checks done to validate product file uploads on a model level. First, the product file is checked if it is a .zip file size is 2.5MB max.

The product file and image filenames are generated using a custom method to include the product's slug value and palce the files into user's product folder. A user with username 'John' who lists a product names 'Kitchet Assets' will have their product file and image renamed and uploaded to something similar to: /media/products/seller_id_3/product_name_kitchen_assets.zip and .jpg

### Cart App
Session based cart that stores added products items in a dictionary. The dictionary is made available to other views and templates through a context processor in order to display cart contents and allow check 

cart view:


Adding to cart:
  no quantity to products so just one product stored and its id.
  Ajax
  still works when js disabled
  prevents adding items already owned, that are already in cart, and ones user owns.

removing from cart

### Checkout App
Stripe payments - Stripe v2 API
Purchase History - keep accurate record of all transactions.
Thank You Page - copy cart session contents to purchase session to list purchased products on thank you page.
Checkout link is hidden when cart contents are 0
view still accessible if typed in url but don't render form when no products in cart.

## SECURITY
restricting views, etc.
403 forbidden


## TESTING
Integration and unit testing.
Travis-CI
Coverage

### Coverage

'coverage run manage.py test' runs the project's tests and creates a coverage report.

Then, run 'coverage report' to view the report in shell

Alternatively, run 'coverage html' to pritify the report. This command creates a 'htmlcov' direcroty containing the test coverage. The 'index.html' is the overview file which links to the other files and provides detail code coverage information.


## LOCAL DEVELOPMENT SETUP
The following is a guide for setting up the project for local development on Windows.

1. Make sure you have Python 2.7 and git installed, if you don't then install from here:
  - [Python](https://www.python.org/downloads/)
  - [Git](https://git-scm.com/)

2. Clone the projects's git repository
```
git clone https://github.com/sebam2k4/RTarchViz
```

3. install virtualenv and create your virtual environment inside the project's root directory

```
pip install virtualenv
```
then create a virtual environment named '.venv':
```
virtualenv .venv
```

4. Activate your new virtual environment
```
. .venv/Scripts/activate
```

5. Install project's dependencies from requirements.txt
```
pip install -r requirements.txt
```

6. Run migrations to build database tables for all apps
```
python manage.py makemigrations
```
then
```
python manage.py migrate
```

7. create an admin account
```
python manage.py createsuperuser
```

8. Start the project using django's built in development server. 
```
python manage.py runserver
```
Now, you've got your local developmnet environment up and running. Navigate to localhost:8000 in your browser to see the site.

9. Make changes to the code and refresh the browser window to see your changes.

10. Have fun!
 

## DEPLOYMENT
Project is deployed to Heroku and uses a free trier of Postgres add-on for the database.
The project's settings.py contains production specific settings...

### Live Demo
[https://rtarchviz.herokuapp.com/](https://rtarchviz.herokuapp.com/)

### Environment Variables
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

### Packages
Some packages that needed to be inmplemented for Production:
- dj-database-url for Postgresql db connection on Heroku
- gunicorn for serving the app on Heroku
- django-storages for storing static files and user uploaded media on AWS S3 bucket

### Travis CI
Travis Continous Integrations is used to test builds before they're deployed to Heroku. There are currently 


## General

### URLs
Now using get_absolute_url model methods for any urls that take arguments, such as review_edit, product_detail, etc. Easier to maintain and if urls change then will need to make changes in only one place.


## CONTRIBUTING
- As this is a graded project for a course, no contributions are accepted at this moment :) I suppose after it's been graded then it can be opened to contributions. However, feel free to download the project and experiment!