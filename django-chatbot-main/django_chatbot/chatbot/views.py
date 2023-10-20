from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.core.files.base import ContentFile
import os,requests
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat,Image
from dotenv import load_dotenv
load_dotenv()
from django.utils import timezone
from django.contrib.auth.decorators import login_required

openai_api_key = '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'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer

@login_required(login_url='/logins/')
def chatpage(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbots.html', {'chats': chats})  

api_key=os.getenv('OPENAI_KEY',None)
openai.api_key=api_key

@login_required(login_url='/logins/')
def img_gen(request):
    obj = None
    img_url = None
    prompt = None
    img = Image.objects.filter(user=request.user)
    if api_key is not None and request.method == 'POST':
        user_input = request.POST.get("user_input")
        prompt = user_input
        response = openai.Image.create(
            prompt=prompt,
            size='256x256',
        )

        img_url = response["data"][0]["url"]

        response = requests.get(img_url)

        img_file = ContentFile(response.content)

        count = Image.objects.count() + 1
        fname = f"image{count}.jpg"
        obj = Image(user=request.user,phrase=user_input,created_at=timezone.now())
        obj.ai_image.save(fname,img_file)
        obj.save()



    # return render(request,"index3.html",{"images":img})
    return render(request,"img_gen.html",{"images":img})  

def log(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'log.html', {'error_message': error_message})
    else:    
        return render(request, 'log.html')

def reg(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'reg.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'reg.html', {'error_message': error_message})    
    return render(request,'reg.html')


def logout(request):
    auth.logout(request)
    return redirect('/logins/')
