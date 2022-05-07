from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from Django import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from .forms import FileForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import Scan, Documents


def home(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    scans = Scan.objects.filter(user=request.user)
    # print(scans[0].description)
    return render(request, 'authentication/index.html', {'fname': request.user.first_name})
    # , 'scans': scans})


def scan_list(request):
    print(request)
    if not request.user.is_authenticated:
        return redirect("signin")
    else:

        scans = Scan.objects.filter(user=request.user)
        # scans = Scan.objects.all()
        # scan_count = scans.count()
        # context = {'scans': scans, 'scan_count': scan_count}
        return render(request, "authentication/scan_table.html")  # , context)


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        # username= request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist! Pleaqe try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registred")
            return redirect('home')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters ")

        # To Do: check password complexity
        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")
            return redirect('home')

        myuser = User.objects.create_user(
            username=username, email=email, password=pass1, first_name=fname, last_name=lname, is_active=False)

        messages.success(
            request, "Your Account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account. ")

        # Welcome Email
        subject = " Welcome to view - Django Login!"
        message = "Hello" + fname + \
            "!! \n Thank you for using our Automated Platform \n We have also sent you a confirmation email , please confirm your email address in order to activate your account.\n\n Thanking You \n EY RedTeam "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
    return render(request, "authentication/signup.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(s)(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username1 = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username1, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('scan_list')
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('signin')
    return render(request, "authentication/signin.html")


@login_required(login_url=signin)
def signout(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    messages.success(request, "Logged Out Successfully")
    logout(request)
    return redirect('signin')


def model_form_upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.files)
        if form.is_valid():
            form.save()
            return render(request, 'home')
        else:
            form = FileForm()
        return render(request, 'authentication/upload.html', {
            'form': form
        })


def showfile(request):

    lastfile = File.objects.last()

    filepath = lastfile.filepath

    filename = lastfile.name

    form = FileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    context = {'filepath': filepath,
               'form': form,
               'filename': filename
               }

    return render(request, 'authentication/upload.html', context)


def upload_file(request):
    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            form.save()
            return HttpResponseRedirect("home")
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


# def Scan(request, pk):
    # scan = scan_list.objects.get(id=pk)
    # if scan.method == 'POST':
    # scan = scan.objects.create(
    # user=request.user,
    # scan=scan,
    # body=request.POST.get('body')
    # )
    # scan.user.add(request.user)
    # return redirect('home')

    # context = {'scan': scan, 'users': user}
    # return render(request, 'authentication/index.html', context)


@ login_required(login_url='signin')
def createScan(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    else:
        if request.method == 'POST':
            scan_name = request.POST['title'].replace(" ", "_")

            #user = request.user
            upload = request.FILES['images']
            fls = FileSystemStorage()
            context = {
                'scan_name': scan_name,
                'upload': upload
            }
            fs = fls.save('uploads' + request.user.username, context)
            scan_file = fls.url(fs)
            scan = Scan(scan_name=scan_name,
                        scan_file=scan_file, user=scan_user)
            if Scan.is_valid():
                scan.save()
            return redirect('home')
        return render(request, 'authentication/upload.html')


@ login_required(login_url='signin')
def updateScan(request, pk):
    scan = scan_list.objects.get(id=pk)
    if request.method == 'POST':
        user = request.POST.get('name')
        scan.description = request.POST.get('description')
        scan.save()
        return redirect('home')

    context = {'scan': scan}
    return render(request, 'authentication/home.html', context)


@ login_required(login_url='login')
def deleteScan(request, id):
    if not request.user.is_authenticated:
        return render(request, 'authentication/signin.html')
    else:
        scan = Scan.objects.get(pk=id)

        if request.method == 'POST':
            os.popen('rm' + str(scan.scan_file))
        return redirect('home')
    return render(request, 'delete.html', {'obj': scan})


@ login_required(login_url='signin')
def Asset_Discovery(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    else:

        return render(request, 'authentication/asset_discovery.html')


@ login_required(login_url='signin')
def NetworkList(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    else:

        return render(request, 'authentication/network_list.html')


def Table(request):
    #df = pd.read_csv("authentication/Host discovery/interface.txt")

    with open('authentication/Host discovery/interface.txt') as f:
        x = f.readlines()
        print(x)
    context = {'values': x}

    return render(request, 'authentication/asset_discovery.html', context)
    # context)
