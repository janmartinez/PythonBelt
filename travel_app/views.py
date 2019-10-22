from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from travel_app.models import *
from django.db.models import Q

def index(request):
	return render(request,"index.html")

def allTravels(request):
    print(request.method)
    loggedinuser = User.objects.get(id = request.session['loggedinuserID'])
    context = {
        "alltrips": Trip.objects.all(),
        "tripsfilter": Trip.objects.filter(Q(user_plan = loggedinuser) | Q( user_join =loggedinuser)),
        "allusertrips": Trip.objects.filter(user_plan  = request.session['loggedinuserID']),  
        "users": User.objects.all().exclude(id = loggedinuser.id),
        "trips": Trip.objects.all().exclude(Q(user_plan = loggedinuser) | Q( user_join =loggedinuser)),
        "loggedinuser": loggedinuser, 
    }
    return render(request,"alltravels.html",context)
    

def addTravel(request):
    return render(request,"addtrip.html")



def addnewtrip(request):
    errors = Trip.objects.Tripvalidator(request.POST)
    print(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/travels/add")
    else:
        loggedinuser= User.objects.get(id = request.session['loggedinuserID'])
        newtrip = Trip.objects.create(destination = request.POST['destination'], description = request.POST['description'], date_from = request.POST['datefrom'], date_to = request.POST['dateto'], user_plan = loggedinuser)

    return redirect("/travels")

def tripinfo(request,trips_id):
    context = {
        "trip": Trip.objects.get(id = trips_id),
        "users": User.objects.filter(joined_trips = trips_id),
          
    }
    return render(request,"tripinfo.html",context)

def jointrip(request,trips_id):
    loggedinuser= User.objects.get(id = request.session['loggedinuserID'])
    jointrip = Trip.objects.get(id = trips_id)
    jointrip.user_join.add(loggedinuser)
    print(jointrip.user_join )
    return redirect("/travels/destination/" + trips_id)


def addUser(request):
	if request.method == "POST":
		errors = User.objects.Uservalidator(request.POST)
		passwordFromForm = request.POST['password']
		cpasswordFromForm = request.POST['cpassword']
		hashcpassword = bcrypt.hashpw(cpasswordFromForm.encode(), bcrypt.gensalt())
		hashpassword = bcrypt.hashpw(passwordFromForm.encode(), bcrypt.gensalt())
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value)
				
			return redirect("/")
		else:
			user = User.objects.create( first_name = request.POST['fname'], last_name = request.POST['lname'], username = request.POST['username'], password = hashpassword.decode() ,confirm_password = hashcpassword.decode() )
			print("******")
			print(user.id)
			request.session['loggedinuserID'] = user.id
			
			return redirect("/travels")
	else:
		return redirect("/")


def login(request):
	errors = User.objects.LoginValidator(request.POST)
	
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
			
		return redirect("/")
	else:

		user = User.objects.get(username = request.POST['username'])
		request.session['loggedinuserID'] = user.id
		print("^^^^^^")
		print(request.POST)
			
		return redirect("/travels")

def clear(request):
	if request.method == "POST":
		request.session.clear()
		return redirect("/")
	else:
		return redirect("/travels")