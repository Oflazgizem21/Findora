from django.shortcuts import render, redirect, get_object_or_404
from .forms import KayitForm
from .models import Kayit
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

@login_required
def kayip_esya_bildir(request):
    return render(request, 'kayip_esya_bildir.html')

@login_required
def kaybettim(request):
    if request.method == 'POST':
        form = KayitForm(request.POST, request.FILES)
        if form.is_valid():
            kayit = form.save(commit=False)
            kayit.user = request.user
            kayit.kayit_turu = 'kaybettim'
            # Diğer seçeneği işleme
            if request.POST.get('tur') == 'diger':
                kayit.tur = request.POST.get('custom_tur', 'Belirtilmedi')
            if request.POST.get('renk') == 'diger':
                kayit.renk = request.POST.get('custom_renk', 'Belirtilmedi')
            kayit.save()
            return redirect('home')
    else:
        form = KayitForm()
    return render(request, 'kaybettim.html', {'form': form})
