# graphene-django-framework

Don't want to use Relay with Graphene? Me either. All other packages for django implement the Relay interface :( 

graphene-django (todo: add link) adds the ability to filter and page but you must follow the Relay specs and that requires the use of Nodes, Edges, Connections, and Global ID's.

Apollo is a great GraphQL client and can still be used with Relay but has it's down sides. 


## Install

    pip install graphene-django-framework

## Hacking

You must have docker and docker-compose

    # setup the docker env with your uid and gid
    echo -e "UID=$(id -u)\nGID=$(id -g)" > .env

    # first migrate the database
    docker-compose run web python manage.py migrate
    
    # create a superuser to login with
    docker-compose run web python manage.py createsuperuser
    
    # run the server
    docker-compose run web python manage.py runserver
    # or tests
    docker-compose run web python manage.py test
