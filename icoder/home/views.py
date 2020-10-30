from django.contrib.auth.models import User #used to create users.
from django.shortcuts import render, redirect, HttpResponse #returning response.
from home.models import Contact #import model Contact.
from blog.models import Post #import model Post.
from django.contrib import messages #use to show messages.
from django.contrib.auth import authenticate, login, logout #use in login and logout function.
# Create your views here.


def home(request):
    '''This function is used to access the data from the database and sending it to the frontend.'''
    popPost = Post.objects.all()
    context = {'popPost': popPost}
    return render(request, 'home/home.html', context)


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    """This function is used to access the data from frontend and storing it in the database."""
    # processing data from front-end
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 2 or len(phone) < 10 or len(content) < 4:
            messages.error(request, 'Please fill the form details correctly!')
        # sending data to the backend.
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(
                request, 'Your message has been successfully submited.')
    return render(request, 'home/contact.html')


def search(request):
    # making search algorithm
    query = request.GET['query']
    if len(query) > 80 or len(query) == 0:
        # If query is greater than 80 words and equal to 0, it will create an empty queryset object.
        allPost = Post.objects.none()
    else:
        # Fetch from database by using query and make a union of allPosts.
        allPosttitle = Post.objects.filter(title__icontains=query)
        allPostauthor = Post.objects.filter(author__icontains=query)
        allPostcontent = Post.objects.filter(content__icontains=query)
        allPost = allPostauthor.union(allPosttitle, allPostcontent)
    if allPost.count() == 0:
        # display a warning if allPost has no related post.
        messages.warning(request, 'Please check your query and search again!')
    searchcount = allPost.count()
    context = {'allPost': allPost, 'query': query, 'searchcount': searchcount}
    return render(request, 'home/search.html', context)


def handleSignUp(request):
    """This function will handle the signup requests coming from the backend."""
    if request.method == "POST":
        # Get the parameters
        username = request.POST['signupusername']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check the error in inputs.
        if len(username) < 6:
            #checking the length of the username.
            messages.error(
            request, "Your username must be under 6 characters!")
            return redirect("/")
        
        if not username.isalnum():
            #checking the username will only contains latters and numbers.
            messages.error(
            request, "Your username should only contains letters and numbers!")
            return redirect("/")
        
        if (pass1 != pass2):
            #checking the pass1 is equal to pass2.
            messages.error(
            request, "Your password did not matched!")
            return redirect("/")


        # creating the user by using the User model in django.
        newuser = User.objects.create_user(username, email, pass1)
        newuser.first_name = fname
        newuser.last_name = lname
        newuser.save()
        messages.success(
            request, "Your icoder account has been successfully created.")
        return redirect("/")

    else:
        return HttpResponse("404-not found")

def handlelogin(request):
    '''This function is used to handle login request from the the frontend.'''
    #function to handle login.
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(
            request, "Successfully logged In.")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials, Please try again!")
            return redirect("/")
    else:
        return HttpResponse("404-Not Found!")

def handlelogout(request):
    '''This function is used to handle logout request from the the frontend.'''
    #function to handle logout.
    user = request.user.is_authenticated
    if user == True:
        logout(request)
        messages.success(request, "User Successfully logged Out")
        return redirect("/")
    else:
        return HttpResponse("404-Not Found!")