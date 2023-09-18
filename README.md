# blog_application

Setup:

    1. first step, clone this repository

            - git clone https://github.com/Ajananth27/blog_application.git
          
    2. Create a virtual environment to install dependencies in and activate it.

    3. Then install the dependencies,

            - pip install -r requirements.txt
    
    4. Then simply apply the migrations:

            python manage.py makemigrations
            python manage.py migrate
    
    4. Once has finished downloading all dependencies, run the local server,

            - python manage.py runserver
    
    Run Tests to ensure everything is set up and working correctly.

        python managr.py test
    

API Endpoints:

    Register new user.

        POST  :  {base_url}/api/register

            Data Required: {"username": "USERNAME", "email": "EMAIL", "password":"PASSWORD"}
    
    Login and get JWT token:

        POST   :  {base_url}/api/login

            Data Required : {"username": "USERNAME", "password": "PASSWORD"}
    
    Create new Blog:

        POST  :  {base_url}/api/user/blog

            Data required:  {"title": "TITLE", "content":"BLOG CONTENT", "author":"AUTHOR NAME"}
    
    Update/Edit blog:

        POST  : {base_url}/api/user/blog/<int:blog_pk>

            Data required : {"title": "TITLE", "content":"BLOG CONTENT", "author":"AUTHOR NAME"}
    
    Delete blog:

        DELETE  : {base_url}/api/user/blog/<int:blog_pk>

    Get the list of all blogs by all users

        GET   :{base_url}/api/user/blog
    
    Get single blog:

        GET  : {base_url}/api/user/blog/<int:blog_pk>
    
    Create Comment 
    
        POST  :{base_url}/api/user/comment
                                
            Data required = {"content": "CONTENT", "commenter_name": "NAME", "blog_id": "BLOG ID"}
    
    Delete Comment:

        DELETE : {base_url}/api/user/comment

            Data Required : {"comment_id": "COMMENT_ID"}
