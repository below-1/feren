from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db import transaction
from app.models import Pegawai, Sex, User
from app.forms import PegawaiForm, CreatePegawaiForm

@transaction.atomic
def create_pegawai(request):
    context = {}
    if request.method == 'POST':
        form = CreatePegawaiForm(request.POST)
        if form.is_valid():
            nama = form.cleaned_data['nama']
            jabatan = form.cleaned_data['jabatan']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            sex = form.cleaned_data['sex']
            user = get_user_model().objects.create_user(                
                username,
                email,
                password,
                is_pegawai=True
            )
            pegawai = Pegawai(
                nama=nama,
                jabatan=jabatan,
                user=user,
                sex=sex
            )
            pegawai.save()
            
        return redirect('list_pegawai')
    else:
        context['form'] = CreatePegawaiForm()
    context['page_title'] = 'Data Pegawai'
    context['page_pretitle'] = 'Tambah Data Pegawai'

    return render(request, 'app/pegawai/create.html', context)

def list_pegawai(request):
    context = {}
    context['items'] = Pegawai.objects.all()
    context['page_title'] = 'Data Pegawai'
    context['page_pretitle'] = 'List Data Pegawai'

    return render(request, 'app/pegawai/list.html', context)

@transaction.atomic
def remove_pegawai(request, id):
    pegawai = Pegawai.objects.get(id=id)
    user = pegawai.user
    user.delete()
    return redirect('list_pegawai')
