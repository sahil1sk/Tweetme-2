from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import(
    AuthenticationForm, 
    UserCreationForm
)

# Create your views here.
def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        return redirect("/")

    context = {
        "form": form,
        "btn_label": "Login",
        "title": "Login"
    }
    return render(request, "accounts/auth.html", context=context)

def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect("/login")   # after logout we return to the login page

    context = {
        "form": None,
        "description": "Are you sure you want to logout?",
        "btn_label": "Click to Confirm",
        "title": "Logout"
    }    
    return render(request, "accounts/auth.html", context=context)

def register_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        #username = form.cleaned_data.get('username')
        user = form.save(commit=True)
        login(request, user)
        return redirect("/")
        #User.objects.create(username=usernam)                  # if you want to create user
        #user.set_password(form.cleaned_data.get("password1"))  # that's how you set the password
        
        return redirect("/login")

    context = {
        "form": form,
        "btn_label": "Register",
        "title": "Register"
    }
    return render(request, "accounts/auth.html", context=context)    