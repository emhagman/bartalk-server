from tools.database import Database
import re
import hashlib
from sqlalchemy.exc import SQLAlchemyError
from django.views.decorators.csrf import csrf_exempt
from dateutil.parser import *


@csrf_exempt
def register(request):
    # get the details
    if request.POST:

        # get the details
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        birthday = request.POST.get('birthday')

        # keep track of validation errors
        errors = []

        # make sure they exist
        if not name:
            errors.append('missing name')
        if not email:
            errors.append('missing email')
        if not password or not password_confirm:
            errors.append('missing password')
        if password != password_confirm:
            errors.append('passwords do not match')
        if not birthday:
            errors.append('missing birthday')

        # make sure they pass validation
        if email and not re.match("[^@]+@[^@]+\.[^@]+", email):
            errors.append('invalid email')
        if birthday and not parse(birthday):
            errors.append('invalid date')

        # make sure there are no errors
        if len(errors) == 0:

            # hash the password
            salt = 'drunkdevs'
            hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

            # store the user into the database
            query = Database.drinker.insert().values(name=name, email=email, password=hashed_password,
                                                     birthday=birthday)

            # make sure it succeeds
            try:
                Database.connection.execute(query)
            except SQLAlchemyError:
                return Database.error('error creating the user')

            # return success
            return Database.success('user has been created')

        else:

            # return validation errors
            return Database.errors(errors)
    else:
        return Database.error('invalid request')


@csrf_exempt
def login(request):

    # check for post
    if request.POST:

        # get the values
        email = request.POST.get('email')
        password = request.POST.get('password')

        # hash the password
        salt = 'drunkdevs'
        hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

        # check database to see if they exist
        query = Database.drinker.select().where(Database.drinker.c.email == email).\
            where(Database.drinker.c.password == hashed_password)

        # make sure it works
        try:
            result = Database.connection.execute(query).first()
            if result:
                request.session['user'] = True
                return Database.response(Database.object({"success": True, "user": result}))
            else:
                return Database.error('username or password was incorrect')
        except SQLAlchemyError:
            return Database.error('error checking database')
    else:
        return Database.error('invalid request')
