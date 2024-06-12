from django.shortcuts import render
from .forms import AdminRegistrationForm
from django.shortcuts import render, redirect

def admin_panel_login(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = AdminRegistrationForm()
    return render(request, 'admin/admin_register.html', {'form': form})