# RTarchViz

[![Build Status](https://travis-ci.org/sebam2k4/RTarchViz.svg?branch=master)](https://travis-ci.org/sebam2k4/RTarchViz)
![Test Coverage](./coverage.svg)

## OVERVIEW

### Introduction

RTarchViz is a (fictional) marketplace for high quality assets specially created for use in real-time architectural visualizations in Unreal Engine. These assets can consist of, but are not limited to, in-engine 3d models, sounds, blueprints, scripts, and full environments.

RTarchViz stands for: Real-Time Architectural Visualizations

### How Does It Work

Built with Django, Python based full-stack web framework, uses PostgreSQL database to store user info, products, orders, transaction history, etc., and is styled using Bootstrap4 and custom CSS.

Registered have the ability to buy and list their own digital products as well as have access to a dashboard containing a list of their listed products for easy management (edit or remove product), their sales analytics, total profit, and download links to any product they may have purchased from other users.

### Target Audience

The primary users of my applications would be architects, interior designers, graphic designers, 3d modelers, archviz enthusiasts, and Unreal Engine enthusiasts.

## INITIAL PLANNING

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

- **[django-bootstrap4 0.0.6](http://django-bootstrap4.readthedocs.io/en/latest/index.html)**
  - Used for easy styling of form elements
- **[django-disqus 0.5](https://django-disqus.readthedocs.io/en/latest/)**
  - Used for comments on blog posts
- **[TinyMCE 2.7.0](http://django-tinymce.readthedocs.io/en/latest/)**
  - Provides a WYSIWYG text editor for writing blog posts by staff members in the admin site.
- **[django-social-share 1.1.2](https://pypi.org/project/django-social-share/)**
  - Provides template tags for sharing object data on popular social media networks.
  - I've overriden the templates to implement font-awesome 5 icons and to fit the style of my website.

## VERSION CONTROL

The project uses git for version control and follows the gitflow branching model. This means that the master branch is always the production branch. Then there is a develop branch from which new feature branches are made from. When the feature is completed, the feature branch is then merged back into develop. At this point a release branch is made from develop with the new feature in it and is named, for example release-0.4.0. The release branch is the used to fix bugs and make minor tweaks to finish up the release. Once it's ready, it is then merged with master and develop. I like to use the --no-ff (no fastforward) flag when merging to master as it always creates a new commit with the release version in it. This avoids losing information about the historical existance of a feature branch and groups together all commits that together added the feature.

The current and final release version for assessment of the project is v0.13.1

Each release and its notes can be accessed on [Github](https://github.com/sebam2k4/RTarchViz/releases)

## Note to Assessor

The project takes advantage of Django Admin for some of its features and as such requires a user to be a 'staff' member to access it. The following are login details for a 'staff' user that can be used to access the admin:

email: jon_snow@gmail.com

username: jon_SnOw

password: testtest1

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

- Blog Posts use django's Paginator for their list view to split posts across several pages. A handy navigation is provided on the bottom of each page that user can use to navigate to the next or previous page as well as choose specific page number. Also, posts are filterable by the following options: newset, oldest, most popular, tutorials, and news.

- Each post detail view provides useful navigation to next or previous post or back to posts list.

- Overrides Blog model's save method to generate datetime stamps for published date and updated date for posts. Published date gets stamped when posts is actually published (status is initially changed from 'draft' to 'published'). Once a post is published then saving it again will add updated date. Any consequent saves to the post will update the updated date with current date and time. Published date stays the same and indicates the date when post was originally published.

- Blog posts use Disqus for comments

- Posts are managed only by is_staff (company staff members) who can add, edit, and delete posts in Django's built in, although extended, admin. The staff users are provided with a handy form and a main texarea for the writing the blog content using the tinyMCE WYSIWYG text editor.

- Admin list view for Blog Posts displays a nice table of filterable and orderable fields that makes it easy for staff to search for posts they are working on (drafts) or want to edit or update. Can also get some statistical filters to see which posts are performing well in terms of view count.

- Super User needs to designate the user a staff member in the django admin as well add the user to the 'staff' group to gain add, edit, and delete blog post permissions.

### Products App

Products app for displaying listed products as well as providing means for users to add, edit, and delete products as well as product reviews.

- Products list uses django's Paginator to split product listings across multiple pages. A handy navigation is provided on the bottom of each page that user can use to navigate to the next or previous page as well as choosing specific page number. Also product filtering by category and sorting by newset, oldest, most popular, highest rating, a-z, and z-a is possible through the template.

- There are two checks done to validate product file uploads on a model level. First, the product file is checked if it is a .zip file and size allowed is 2.5MB max.

- The product file and image filenames are generated using a custom method to include the product's slug value and palce the files into user's product folder. A user with username 'John' who lists a product names 'Kitchet Assets' will have their product file and image renamed and uploaded to something similar to: /media/products/seller_id_3/product_name_kitchen_assets.zip and .jpg

- User can only review products they have purchased. 1 review per product allowed.

- One important security feature implemented is to prevent users trying to delete or edit a product or review that does not belong to them (by typing the url in the address bar) by returning a 403 forbidden page. I believe this prevents most if not all such exploits from being possible.

- Implemented star rating for average product rating on card list and detail product views.

- The list and detail templates use the cart's contents to render the product buttons. The default button is 'Add to Cart', but it changes when product is added to cart to 'Already in Cart' and is disabled. Similarly when product is already owned by user, the button chages to 'Owned' and is disabled.

- Deleting products actually sets their 'active' model field to 'False' to prevent users loosing access to products they have purchased. Inactive products do not appear in the site, but users can still access download links for these inactive products from their dashboards.

### Cart App

Session based cart that stores added products items in a dictionary. The dictionary is made available to other views and templates through a context processor in order to display cart contents and allow checks such as whether the user owns or has already purchased a specific products while trying to add it to cart

- The cart features only one template for showing cart contents. It allows for modifying the contents by removing individual items or all at once. It also displays the item count and total.

- The cart app uses ajax request for adding items to cart without requiring a page reload for better user experience. The add_to_cart uses `if request.is_ajax():` conditional to handle the ajax request, and, in case javascript is disabled in browser, allows for the view to handle the request instead.

### Checkout App

The main function of the checkout app is to handle processing payments using the Stripe API.

- The checkout provides a payment form template and a thank you template shows after successfuly making payment.

- A special Purchase History is kept to record product price at time of transaction. This ensures the accuracy of account balance in user's dashboard since seller's can edit their product's price and the price change would reflect on the dashboard.

## TESTING

### Automated Tests

In total, 40 automated unittests have been implemented to perform tests on the Blog and Product apps. Most of the tests performed are described below:

Blog app:

- tests for correct model string representation
- tests absolute_url method is working as expected
- tests get_auther_name methods
- tests published and updated posts methods
- tests views exist at desired urls
- tests publishing and accessing a single and multiple posts
- tests draft posts are not accessible
- tests posts list pagination

Products app:

- tests for correct model string representation
- tests absolute_url method is working as expected
- tests views exist at desired urls
- tests adding and accessing a single and multiple products
- tests draft posts are not accessible
- tests product list pagination
- tests getting product name, seller, and description
- tests redirects for when trying to access the add, edit, and delete product views when user not logged in

### Travis CI

Travis CI runs all the automated tests everytime before the project is deployed to Heroku to make sure that it does not deployed with any broken features, at least for the ones that are tested.

### Coverage

Python Coverage was used for measuring code coverage for testing. It was used to gauge the effectiveness of tests as well as to indicate which parts of the code are not yet tested.

The coverage report can be generated as follows:

`coverage run manage.py test` runs the project's tests and creates a coverage report.

Then, run `coverage report` to view the report in shell

Alternatively, run `coverage html` to pritify the report. This command creates a 'htmlcov' direcroty containing the test coverage. The 'index.html' is the overview file which links to the other files and provides detailed code coverage information.

### Manual Tests

Each new feature was tested manually by me in the browser to make sure it is working as expected.

For testing layout responsiveness I have used both an Android and Windows phone as well as Chrome Developer Tools' device toolbar. The application's responsiveness was checked against different mobile orientations (portrait/landscape) as well as different screen sizes on desktop. I've also tested on different desktop borowsers: Chrome, Mozilla, Brave, and Edge.

## LOCAL DEVELOPMENT SETUP

The following is a guide for setting up the project for local development on Windows.

1. Make sure you have Python 2.7 and git installed, if you don't then install from here:
   - [Python](https://www.python.org/downloads/)
   - [Git](https://git-scm.com/)

1. Clone the projects's git repository

```shell
git clone https://github.com/sebam2k4/RTarchViz
```

2. Install virtualenv and create your virtual environment inside the project's root directory

```shell
pip install virtualenv
```

then create a virtual environment named '.venv':

```shell
virtualenv .venv
```

3. Activate your new virtual environment:

```shell
. .venv/Scripts/activate
```

5. Install project's dependencies from requirements.txt

```shell
pip install -r requirements.txt
```

6. Create a file 'env.py' in the porject's root directory and define two environment variables:

```python
# env.py

import os

# DEVELOPMENT TYPE
os.environ.setdefault("ENV", 'development')

# DJANGO SECRET KEY
os.environ.setdefault("SECRET_KEY", "-your-secret-key-")
```

***Note:** This is a minimal configuration required to make the project work on local development server. Freatures like disqus and stripe payments will not work as they require extra configuration - please refer to the 'deployment' section of this readme for info on configuring these features.*

7. Run migrations to build database tables for all apps

```shell
python manage.py makemigrations
```

then

```shell
python manage.py migrate
```

8. create an admin account

```shell
python manage.py createsuperuser
```

9. Start the project using django's built in development server.

```shell
python manage.py runserver
```

Now, you've got your local developmnet environment up and running. Navigate to localhost:8000 in your browser to see the site.

10. Make changes to the code and refresh the browser window to see your changes.

11. Have fun!

## DEPLOYMENT

Project is deployed to Heroku and uses a Hobby Dev (free) plan of Postgres database add-on.
The application's settings.py file contains production specific settings that require setting aditional environment variables:

### Environment Variables

requires setting the following environment variables in Heroku Settings:

```shell
# General
ENV = 'production'
DATABASE_URL = '<link to your provisioned Heroku Postgres db or other>'
SECRET_KEY, "<your secret django key>"

# Amazon AWS S3 storage
AWS_STORAGE_BUCKET_NAME = '<your S3 bucket name>'
AWS_S3_REGION_NAME = '<your S3 bucket region, ex: eu-west-1'>
AWS_ACCESS_KEY_ID = '<your IAM user access key>'
AWS_SECRET_ACCESS_KEY = '<your IAM user secret access key>'

# Stripe payments
STRIPE_PUBLISHABLE = '<your stripe publishable_key>'
STRIPE_SECRET = '<your stripe secret key>'

# Email configuration
EMAIL_HOST_USER = '<email address>'
EMAIL_HOST_PASSWORD = '<email password>'

# Disqus comments configuration
DISQUS_WEBSITE_SHORTNAME = '<your website shortname>'
DISQUS_API_KEY = '<your secret disqus api key>')
```

Setting ENV to 'production' ensures the application is run using s3 sotrage for media and product files, Postgres db provisioned on Heroku, and debug mode disabled.

To generate your django random key, simply run this command in your shell `python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'`

For setting up AWS S3 and IAM refer to the 'Amazon S3 Setup' portion of [this tutorial](https://simpleisbetterthancomplex.com/tutorial/2017/08/01/how-to-setup-amazon-s3-in-a-django-project.html) Once set up, in your shell run `python manage.py collectstatic` from root directory to copy all static files to your s3 bucket. If you have any user uploaded media files then you may have to copy them to s3 manually. Don't forget to run the command everytime you make changes to your css, js, images and any other static file to update your s3 bucket.

Stripe payments need authentication details obtained from your stipe account. Refer to [Stripe API docs](https://stripe.com/docs/api/python)

The email environment variables are needed for emailing password recovery links to users. May require tweaks to email settings in settings.py as well as changing security settings in your email client. If these are not set, then password recovery links will be printed to console instead.

Disqus api key and website short name are needed for setting up post comments. It requires setting up an account with Disqus and registering the application. Refer to [Disqus API docs](https://disqus.com/api/docs/)

### Live Demo

[https://rtarchviz.herokuapp.com/](https://rtarchviz.herokuapp.com/)

### Packages

Some packages that needed to be inmplemented for Production:

- dj-database-url for Postgresql db connection on Heroku
- gunicorn for serving the app on Heroku
- django-storages for storing static files and user uploaded media on AWS S3 bucket

### Travis CI

Travis Continous Integrations is used to run automated test before the project is deployed to Heroku. Makes sure that a broken app isn't deployed to Heroku.

## BUGS

- Currently when setting `required=True` for the 'credit_card_number' and 'cvv' form fields of the checkout's MakePaymentForm, validation errors ('This field is required') for these fields are returned when submitting the form. This prevents users from making purchases. I'm not sure why this is happening and it requires further investigation. For now I've set required=False for a temporary fix.

- The links to access the Checkout view do not render in templates when no products are in cart, however, checkout is still accessible if typed in url

## CONTRIBUTING

As this is a graded project for a course, no contributions are accepted at this moment :) I suppose after it's been graded then it can be opened to contributions. However, feel free to download the project and experiment!
