from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
    # def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) <1:
            errors['first_name'] = "First name can't be blank!"
        elif postData['first_name'].isalpha() == False:
            errors['first_name'] = "First Name can only contain letters"
        else:
            print("models fn pass")

        if len(postData['last_name']) <1:
            errors['last_name'] = "Last name can't be blank!"
        elif postData['last_name'].isalpha() == False:
            errors['last_name'] = "Last Name can only contain letters"
        else:
            print("models ln pass")

        if len(postData['email']) < 1:
            errors['email'] = "Email cannot be blank!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        else:
            print("models email1 pass")

            dupe_check = User.objects.filter(email=postData['email'])
            if len(dupe_check):
                errors['email'] = "Email exists in database!  Please try again!"
            else:
                print("models email2 pass")
        
        if len(postData['password']) < 8:
            errors['password'] = "Password must be 8+ characters."
        else:
            print("models password pass")

        if len(postData['cnf_pw']) > 0:
            if postData['password'] != postData['cnf_pw']:
                errors['cnf_pw'] = "Submitted passwords don't match"
        elif len(postData['cnf_pw']) == 0:
            errors['cnf_pw'] = "Confirm password can't be blank"
        else:
            print("models cnf_pw pass")

        print("models.py errors = ",errors)

        return errors

    def login_validator(self, postData):

        login_errors = {}
        
        if len(postData['log_eml']) < 1:
            login_errors['log_eml'] = "We are unable to log you in.  Please try again."
        elif not EMAIL_REGEX.match(postData['log_eml']):
            login_errors['log_eml'] = "We are unable to log you in.  Please try again."
        else:
            dupe_check = User.objects.filter(email=postData['log_eml'])
            if len(dupe_check) <1 :
                login_errors['log_eml'] = "We are unable to log you in.  Please try again."
                print("dupe_check fail")
            else:
                print("log_eml pass")

            if len(postData['log_wd']) > 0:
                dupe_check = User.objects.filter(email=postData['log_eml'])
                print("dupe_check conf pw = ",dupe_check)
                if len(dupe_check) != 0 :
                    compare = bcrypt.checkpw(postData['log_wd'].encode(), dupe_check[0].password_hash.encode())
                    print("compare result = ",compare)
                    if not compare:
                        login_errors['log_wd'] = "We are unable to log you in.  Please try again."
                else:
                    login_errors['log_wd'] = "We are unable to log you in.  Please try again."

            elif len(postData['log_wd']) == 0:
                login_errors['log_wd'] = "We are unable to log you in.  Please try again."
            else:
                print("log_wd pass")

        print("models.py login_errors = ",login_errors)

        return login_errors


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


    