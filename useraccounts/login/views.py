from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.sessions.models import Session

# Create your views here.
def loginpage(request):
    return render(request, "login.html")

def registerpage(request):
    return render(request, "register.html")

def registeradmin(request):
    registererrors = []
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        orgname = request.POST["orgname"]
        address = request.POST["address"]
        contact = request.POST["contact"]
        pwd = request.POST["pwd"]
        confirmpwd = request.POST["confirmpwd"]
            
        # check if user exist already
        if userexists(email):
            registererrors.append("This user with this email already exist, please use a different email.")
        else:
            # check if organisation exist already
            if orgexists(orgname):
                registererrors.append("Organisation name already exist, please choose a different name.")
            
            # validate pwd
            registererrors = validatepwd(pwd, confirmpwd, registererrors)

        # Save the details to populate the form fields so the user don't have to retype    
        mydict = {
            "username": username,
            "email": email,
            "orgname": orgname,
            "address": address,
            "contact": contact,
            "registererrors": registererrors
        }
        
        if (len(registererrors) > 0): 
            return render(request, "register.html", context=mydict)
        else:
            # valid form, save into database
            orgObj = Organisation()
            orgObj.name = orgname
            orgObj.address = address
            orgObj.contact = contact
            orgObj.save()  # Save the Organisation instance to the database

            # Create user using custom model
            adminuser = User.objects.create_user(
                email = email,
                password=pwd,
                name = username,
                organization = orgObj, # Set the foreign key relationship with organisation
                role = "Admin"
            )

            # Set the user permissions for Admin user
            User.objects.assign_permissions(adminuser)

            mydict = {
                "success": True
            }
            
            return render(request, 'register.html', context=mydict)

def userexists(email):
    return User.objects.filter(email=email).exists()

def orgexists(name):
    return Organisation.objects.filter(name=name).exists()
                    
def validatepwd(pwd, confirmpwd, registererrors):
    if len(pwd) < 8:
        errormsg = "Password must be at least 8 characters."
        registererrors.append(errormsg)
        
    # Check if password contains at least one uppercase letter and one number
    has_uppercase = any(char.isupper() for char in pwd)
    has_number = any(char.isdigit() for char in pwd)

    if not has_uppercase or not has_number:
        errormsg = "Password must contain at least one uppercase letter and one number."
        registererrors.append(errormsg)
        
    # Check if passwords match
    if pwd != confirmpwd:
        errormsg = "Password and confirm password does not match."
        registererrors.append(errormsg)
        
    return registererrors

def validatelogin(request):
    # Check against database
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pwd']

        # Authenticate the user
        user = User.objects.get(email=email)
        
        # user = authenticate(request, email=email, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('homepage')

        # Check if the entered password matches the hashed password
        if check_password(password, user.password):
            # Login the user
            login(request, user)
            # Set session details
            request.session['email'] = email
            
            return redirect('homepage') 
        else:
            # Authentication failed
            return render(request, 'login.html', {'error': 'Invalid email or password.'})

# @login_required        
def homepage(request):
    # Retrieve user details from the session
    email = request.session.get('email', None)
    user = User.objects.get(email=email)

    # Retrieve organisation details
    orgid = user.organization_id
    org = Organisation.objects.get(id=orgid)

    # Retrive all users from this organisation id
    users_in_org = User.objects.filter(organization_id=orgid)

    # Retrieve permissions
    user_permission = CustomUserPermission.objects.get(user=user)
    # Retrieve all permissions associated with the user
    user_permissions = user_permission.permissions.all()
    print(user_permissions)

    # Check if 'login.add_members' permission is in the queryset
    has_add_members_permission = any(perm.codename == 'add_members' for perm in user_permissions)
    print(has_add_members_permission)

    # Check if 'login.view_members' permission is in the queryset
    has_view_members_permission = any(perm.codename == 'view_members' for perm in user_permissions)
    print(has_view_members_permission)

    mydict = {
        "user": user,
        "org": org,
        "users_in_org": users_in_org,
        "has_add_members_permission": has_add_members_permission,
        "has_view_members_permission": has_view_members_permission,
    }
    return render(request, 'home.html', context=mydict)

# @login_required
def addmemberpage(request):
    # Retrieve user details from the session
    email = request.session.get('email', None)
    user = User.objects.get(email=email)

    # Retrieve organisation details
    orgid = user.organization_id
    org = Organisation.objects.get(id=orgid)
    
    mydict = {
        "user": user,
        "org": org,
    }
    return render(request, 'addmember.html', context=mydict)

# @login_required
def addmember(request):
    # You cannot add members who are admins in other organisations

    registererrors = []

    # Retrieve admin user details from the session
    adminemail = request.session.get('email', None)
    adminuser = User.objects.get(email=adminemail)

    # Retrieve organisation instance
    orgid = adminuser.organization_id
    orgObj = Organisation.objects.get(id=orgid)
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        role = request.POST["role"]
        pwd = request.POST["pwd"]
        confirmpwd = request.POST["confirmpwd"]
            
        # check if user exist already
        if userexists(email):
            registererrors.append("This user with this email already exist in another organisation, please use a different email.")
            
        # validate pwd
        registererrors = validatepwd(pwd, confirmpwd, registererrors)

        # Save the details to populate the form fields so the user don't have to retype    
        mydict = {
            "org": orgObj,
            "username": username,
            "email": email,
            "role": role,
            "registererrors": registererrors
        }
        
        if (len(registererrors) > 0): 
            return render(request, "addmember.html", context=mydict)
        else:
            # valid form, save into database
            newuser = User.objects.create_user(
                email = email,
                password=pwd,
                name = username,
                organization = orgObj, # Set the foreign key relationship with organisation
                role = role
            )

            # Set the user permissions for new user in the organisation
            User.objects.assign_permissions(newuser)

            mydict = {
                "success": True
            }
            
            return render(request, 'addmember.html', context=mydict)

def logoutpage(request):
    logout(request)
    # Clear all sessions
    Session.objects.all().delete()
    # Redirect to login page after logging out
    return render(request, 'login.html')