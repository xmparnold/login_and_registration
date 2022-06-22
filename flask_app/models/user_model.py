from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session
import re

# regular expression to check email is valid email address
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# set some constants for minimum length of first and last name when creating user. these can be changed if we need different values
MINIMUM_FIRST_NAME_LENGTH = 2
MINIMUM_LAST_NAME_LENGTH = 2
MINIMUM_PASSWORD_LENGTH = 6
# these constants will hold the string of the minimum length for error messages, make sure these match the int constants above
MINIMUM_FIRST_NAME_LENGTH_STRING = "2"
MINIMUM_LAST_NAME_LENGTH_STRING = "2"
MINIMUM_PASSWORD_LENGTH_STRING = "6"


class User:
    # first we have the constructor for the class that takes in a dictionary to create an instance of the class
    def __init__( self, data ):
        self.id = data[ 'id' ]
        self.first_name = data[ 'first_name' ]
        self.last_name = data[ 'last_name' ]
        self.email = data[ 'email' ]
        self.password = data[ 'password' ]
 
    # class method to get user from db by email address
    @classmethod
    def get_one( cls, data ):
        # build the query here to grab from the users table in db
        query = "SELECT * FROM users WHERE email = %(email)s;"

        # set the result variable to the returned value from the query. if it doesn't find the email in table, the result will have nothing in it
        result = connectToMySQL( DATABASE ).query_db( query, data )

        # if the result has a length greater than 0, then we know it has something in it and it found the user in table
        if len( result ) > 0:
            # return the result
            return cls( result[ 0 ] )
        else:
            # return None if nothing is found
            return None
        
    # class method to create a user in the db
    @classmethod
    def create( cls, data ):
        # build the query to insert user info into user table. values will be entered through the data entered as dictionary
        query = "INSERT INTO users( email, first_name, last_name, password ) VALUES( %(email)s, %(first_name)s, %(last_name)s, %(password)s );"
        # we dont need tor eturn anything so we will just call the method to execute the query
        return connectToMySQL( DATABASE ).query_db( query, data )

    # static method to validate the values in the registration form fields
    @staticmethod
    def validate_register( data ):
        # first set isValid to True and only set to false if we run into any issues during validation
        isValid = True

        # first make sure first name box has something entered in it, if it does't then flash error message
        if data[ 'first_name' ] == "":
            isValid = False
            flash( "Please provide your first name", "error_register_first_name" )
        # make sure first name value is longer than the minimum first name length declared in constant variables at top of file
        if len( data[ 'first_name' ] ) < MINIMUM_FIRST_NAME_LENGTH:
            isValid = False
            flash( "Your first name must be longer than " + MINIMUM_FIRST_NAME_LENGTH_STRING + " characters", "error_register_first_name" )
        # make sure last name box has something in it
        if data[ 'last_name' ] == "":
            isValid = False
            flash( "Please provide your last name", "error_register_last_name" )
        # make sure last name value is longer than the minimum last name length constant declared at top of file
        if len( data[ 'last_name' ] ) < MINIMUM_LAST_NAME_LENGTH:
            isValid = False
            flash( "Your last name must be longer than " + MINIMUM_LAST_NAME_LENGTH_STRING + " characters", "error_register_last_name" )
        # make sure email box has something entered in it
        if data[ 'email' ] == "":
            isValid = False
            flash( "Please provide your email address", "error_register_email" )
        # make sure email value is in fact a valid email address using regular expression constant at top of file
        if not EMAIL_REGEX.match( data[ 'email' ] ):
            isValid = False
            flash( "Please enter a valid email address" )
        # make sure password box has something entered in it
        if data[ 'password' ] == "":
            isValid = False
            flash( "Please enter a password", "error_register_password" )
        # make sure password is longer than minimum password length declared in constant at top of file
        if len(data[ 'password' ]) < MINIMUM_PASSWORD_LENGTH:
            isValid = False
            flash( f"Please enter a password of at least " + MINIMUM_PASSWORD_LENGTH_STRING + " characters", "error_register_password" )
        # make sure password confirmation box has something entered in it
        if data[ 'password_confirmation' ] == "":
            isValid = False
            flash( "Please confirm your password", "error_register_password_confirmation" )
        # make sure password box and password confirmation box values both match to make sure user is entering the correct desired password
        if data[ 'password'] != data[ 'password_confirmation' ]:
            isValid = False
            flash( "Your passwords do not match", "error_register_password" )
        # Now that we have checked all conditions to validate registration form values we can return the isValid variable which will be True if everything is okay and False if any issues were found
        return isValid

    # static method to validate if the user is already logged in in the current session. True = Logged in, False = Not logged in
    @staticmethod
    def validate_session():
        # if user_id isn't in the session then user is not logged in and we will return false
        if "user_id" not in session:
            return False
        # if it is found in current session then user is logged in and we will return true
        else:
            return True