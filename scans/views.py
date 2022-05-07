from django.shortcuts import render, redirect
from django.db.models import Q
#from .models import scan_list, Documents

from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    x = request.GET('x')
    scans = scan_list.objects.filter(
        Q(description_icontains=x)
    )

    scans = scan_list.objects.all()
    scan_count = scans.count()

    context = {'scan_list': scan_list, 'scan': Scan, 'scan_count': scan_count}
    return render(request, 'scans/home.html', context)


def upload(request):
    if request.method == 'POST' and request.files():
        fls = request.files()
        fs = FileSystemStorage()
        filename = fs.save(fls.name, fls)
        uploaded_file_url = fs.url(filename)
        return render(request, 'authentication/index.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return (request, 'authentication/index.html')


def Scan(request, pk):
    scan = scan_list.objects.get(id=pk)
    if Scan.method == 'POST':
        Scan = Scan.objects.create(
            user=request.user,
            Scan=Scan,
            body=request.POST.get('body')
        )
        Scan.user.add(request.user)
        return redirect('home')

    context = {'scan': scan, 'users': user}
    return render(request, 'authentication/home.html', context)


@ login_required(login_url='signin')
def createScan(request):
    form = ScanForm()
    context = {'form': form}
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if scan_list.is_valid():
            scan_list.save()
            return redirect('home')
    context = {{}}
    return render(request, 'Scan.html', context)


@ login_required(login_url='signin')
def updateScan(request, pk):
    scan = scan_list.objects.get(id=pk)
    if request.method == 'POST':
        user = request.POST.get('name')
        scan.description = request.POST.get('description')
        scan.save()
        return redirect('home')

    context = {'scan': scan}
    return render(request, 'scans/home.html', context)


@ login_required(login_url='login')
def deleteScan(request, pk):
    scan = Scan.objects.get(id=pk)

    if request.method == 'POST':
        os.popen('rm', str(scan.Target))
        Scan.delete()
        return redirect('home')
    return render(request, 'authentication/delete.html', {'obj': Scan})
