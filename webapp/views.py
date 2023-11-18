from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record

def home(request):
    return render(request, 'webapp/index.html')

# Create your views here.
def register(request):
    form  = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'webapp/register.html', context=context)

def Login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context = {"form":form}
    return render(request, "webapp/login.html", context=context)

@login_required(login_url='login')
def dashboard(request):
    records = Record.objects.all()
    context = {"records":records}
    return render(request, 'webapp/dashboard.html', context=context)


@login_required(login_url=True)
def create_record(request):
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("dashboard")
    context = {"form":form}
    return render(request, "webapp/create-record.html", context=context)

@login_required(login_url=True)
def update_record(request, id):
    record = Record.objects.get(pk = id)
    form = UpdateRecordForm(instance=record)
    if request.method == "POST":
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {"form":form}
    return render(request, 'webapp/update-record.html', context)

@login_required(login_url=True)
def view_record(request, id):
    record = Record.objects.get(pk = id)
    context = {"record":record}
    return render(request, 'webapp/view-record.html', context)

@login_required(login_url=True)
def delete_record(request, id):
    record = Record.objects.get(pk = id)
    record.delete()
    return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')
