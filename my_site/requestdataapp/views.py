from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import UserBioForm, UploadFileForm

def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '') # Берем значение переменной a из словаря request.GET. Если переменная не найдена, то вернём пустую строку
    b = request.GET.get('b', '') # Берем значение переменной b из словаря request.GET. Если переменная не найдена, то вернём пустую строку
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)

def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm(),
    }
    return render(request,'requestdataapp/user-bio-form.html', context=context)

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST': # Проверяем метод запроса
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # my_file = request.FILES['my_file']
            my_file = form.cleaned_data['file']
            max_file_size = 1024 * 1024
            if my_file.size <= max_file_size:
                fs = FileSystemStorage() #Создадим новый экземпляр класса FileSystemStorage(модуль сохранения файлов в систему)
                filename = fs.save(my_file.name, my_file) #Записываем в файл
                print('Saved file:', filename)
                return render(request, 'requestdataapp/file-upload.html', context={'size': round((my_file.size / 1024 ** 2), 2)})
            else:
                print('File size is to big:', my_file.size, 'bytes')
                return render(request, 'requestdataapp/upload-error.html', context={'size': round((my_file.size / 1024 ** 2), 2), 'max_file_size': (max_file_size / 1024 ** 2)})
    else:
        form = UploadFileForm() # Необходимо передавать пустую форму если GET запрос
    context = {
        "form": form, # Необходимо передавать форму в контекст, чтобы можно было отрисовать на странице
    }
    return render(request,'requestdataapp/file-upload.html', context=context)




