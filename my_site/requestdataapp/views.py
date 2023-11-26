from django.conf.global_settings import FILE_UPLOAD_MAX_MEMORY_SIZE
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

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
    return render(request,'requestdataapp/user-bio-form.html')

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('my_file'): # Проверяем наличие загруженного файла
        my_file = request.FILES['my_file']
        max_file_size = 1024 * 1024
        if my_file.size <= max_file_size:
            fs = FileSystemStorage() #Создадим новый экземпляр класса FileSystemStorage(модуль сохранения файлов в систему)
            filename = fs.save(my_file.name, my_file) #Записываем в файл
            print('Saved file:', filename)
        else:
            print('File size is to big:', my_file.size, 'bytes')
            return render(request, 'requestdataapp/upload-error.html')
    return render(request,'requestdataapp/file-upload.html')




