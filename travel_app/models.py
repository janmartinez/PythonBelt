from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt
import re


class UserManager(models.Manager):
    def Uservalidator(self, postData):
        errors = {}
        userExist = User.objects.filter(username = postData['username'])
      
        if len(postData['fname']) < 2:
            errors["fname"] = "First name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "Last Name should be at least 2 characters"
        if len(userExist) > 0:
            errors["username"] = "Username already exist"
        if len(postData['username']) < 3:
            errors["username"] = "Username a be at least 2 characters"   
        if len(postData['password']) < 8:
             errors["pasword"] ="Your Password is a Mierda"
        if postData['cpassword'] != postData['password']:
            errors["confirm_pasword"] ="Pasword don not match"
        return errors
    def LoginValidator(self, postData):
        errors = {}
        userExist = User.objects.filter(username = postData['username'])
        userPassword = postData['password']
        if len(userExist) == 0:
            errors["username"] = "Username do not exist"
            print(errors)
            return errors  
        else:
            if bcrypt.checkpw(userPassword.encode(),userExist[0].password.encode()) == False:
                errors["password"] = "Wrong Password"
                print(errors)
                return errors
            else:
                return errors
        
           
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    username= models.CharField(max_length = 255)
    password= models.CharField(max_length = 255)
    confirm_password= models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripManager(models.Manager):
    def Tripvalidator(self, postData):
        errors = {}
        
        if len(postData['destination']) < 2:
            errors["destination"] = "Destination should be at least 2 characters"
        if len(postData['description']) < 2:
            errors["description"] = "Description should be at least 2 characters"
        if not postData['datefrom']:
            errors["datefrom"] = "Please insert a start date!"
        if not postData['dateto']:
            errors["dateto"] = "Please insert an end date!"
        if postData['dateto'] and postData['datefrom']:
            if postData['dateto'] < postData['datefrom']:
                errors["invaliddate"] = "How do you expect to start your trip after it ended?"
            if datetime.now() > datetime.strptime(postData['datefrom'], '%Y-%m-%d'):
                errors["invaliddate"] = "You can not start your trip in the past"
        print(errors)
        
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.TextField()
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    user_plan = models.ForeignKey(User, related_name = "planed_trip", on_delete=models.CASCADE)
    user_join = models.ManyToManyField(User, related_name="joined_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
