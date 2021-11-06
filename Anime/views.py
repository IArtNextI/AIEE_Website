import boto3
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import os

from AIEE.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

first_task = [
    "Everybody knows that our appearance matters in what people think about us. Appearance is important only in "
    "aromatic relationship but also in politics. Appearance is not all about beauty. The moment we see a person our "
    "mind starts evaluating their personality according to their looks. What especially matters is the person's face. "
    "This means that the impression somebody's face makes on others can cost the person his or her political career. "
    "When we vote for a candidate we think what we are weighing his or her personal qualities. In fact, were examining"
    " their face. Research has shown that if a candidate's appearance displays competence, power and leadership, but"
    " not beauty or good looks, it can cause a political victory or defeat. These findings are really important.",

    "Fashion is a popular style in clothing/ accessories, make-up, footwear and body piercing. In ancient Turkey, "
    "India, China and Japan, fashion did not change in over a thousand years. The situation became different with "
    "political and economic developments and with the help of cultural exchange between nations. Fashion from Iraq "
    "came to Spain and, similarly, fashion from Turkey spread to the Middle East. European fashion took shape in the"
    " 14th century. At that time men's shirts shortened from knee length to the waist-long size. Those were worn over"
    " leggings or trousers. Spanish and French styles were competing between themselves. Aristocracy, middle class,"
    " cities and villages dressed differently.'",

    'Hygiene is a set of practical rules for staying healthy and preventing the spread of diseases.'
    ' Hygiene rules help to keep a healthy and healthy lifestyle, create clean environment and stop'
    ' infection. Such behaviour is sometimes described as \"good habits\". Hygiene is often '
    'connected to \"cleanliness\" through washing hands, fruits and vegetables, using safe water, '
    'taking a shower, airing one\'s room, washing the floor and removing dust from furniture. '
    'Wearing a mask during flu epidemics is another recommended practice. The notion of \"hygiene\"'
    ' may include various types of behaviour. That is why we often speak about sleep hygiene, '
    'mental hygiene, dental hygiene, occupational hygiene and others.',

    "Most people immediately think of the light bulb when they think of Thomas Edison. But although this genius did"
    " in fact invent the first practical, long-lasting light bulb, he had a hand in creating many more things we can"
    " still see around us today. He invented or contributed to recorded music, electrical systems, the telephone,"
    " the alkaline battery, X-rays and an early cinema projector. Incredibly, by the end of his life he held 1093 "
    "patents and he is responsible for more inventions than any other inventor in history! Perhaps Edison’s greatest"
    " strength was that he absolutely refused to give up. He said, \"Many of life’s failures are people who did not"
    " realize how close they were to success when they gave up\". Unbelievably, it took Edison thousands of tries"
    " before he found the right filament to use for his light bulb. He wasn't afraid of failure. He simply saw his"
    " bad ideas as stepping stones to better ones. Even after his factory was almost totally destroyed by fire, he"
    " said, “There is great value in disaster. All our mistakes are burned up and we can start a new”. Three weeks "
    "later, Edison delivered the first phonograph."
]

last_task = [
    'You are going to give a talk about the appearance of famous models. You will have to start in 1.5 minutes and '
    'speak for not more than 2 minutes.',

    'You are going to give a talk about school uniform. You will have to start in 1.5 minutes and '
    'speak for not more than 2 minutes.',

    'You are going to give a talk about raising the resistance of your body to infection and diseases. You will have'
    ' to start in 1.5 minutes and speak for not more than 2 minutes.',

    'You are going to give a talk. You will have to start in 1.5 minutes and speak for not more than 2 minutes.'
]

last_task_d = [
    'Remember to say:\n    - what appearance of models you like\n     - what makes some models more successful than '
    'others\n    - why models can be a bad example for young people\'s lifestyle',

    'Remember to say:\n    - what you think about wearing school uniform\n     - what your school uniform looks like '
    '\n    - how school uniform can be improved',

    'Remember to say:\n    - why it is important for people to resist diseases\n     - what food can help people'
    ' resist diseases\n    - what people can do to raise their resistance to diseases',

    'Besides never giving up, what should a person do to become a prominent figure in her/his field?'
    ' You may use the examples from other famous people\'s lives to answer this question.'
]

very_safe_array_of_variants = {
    'alexandrov.maxim': 2,
    'buzanova.anna': 0,
    'bouladi.daniel': 1,
    'vidavsky.maxim': 0,
    'getman.anton': 0,
    'anna.grigorieva': 2,
    'ivanchenko.maria': 3,
    'ivanchenko.maxim': 0,
    'kalinina.julia': 0,
    'karlov.ivan': 1,
    'kirillov.alexander': 2,
    'korotkova.ksenia': 0,
    'kravtsov.dmitry': 3,
    'mefodin.dmitry': 0,
    'mitali.daria': 3,
    'mozhaev.artem': 1,
    'nevretdinov.damir': 3,
    'orentliherman.mark': 1,
    'ostrikova.anastasia': 1,
    'perstnev.pavel': 0,
    'petrov.gleb': 3,
    'polnyakova.uliana': 1,
    'alexey.pchelkin': 3,
    'rostov.elizabeth': 3,
    'ryutova.catherine': 0,
    'saprykin.alexander': 2,
    'selivanova.anna': 3,
    'sergeeva.anastasia': 2,
    'sergeev.vladislav': 2,
    'silin.grigory': 0,
    'skorodumova.anastasia': 1,
    'smirnov.stepan': 2,
    'solovyenko.danila': 3,
    'staretskiy.stepan': 3,
    'stepin.artem': 1,
    'taran.alexandra': 2,
    'terentyev.ilya': 1,
    'tkachenko.mikhail': 0,
    'fedenko.catherine': 1,
    'kharitonova.anastasia': 1,
    'tsvetkov.peter': 2,
    'chekushkin.danila': 0,
    'chernaya.julia': 2,
    'chidirova.tamara': 1,
    'shapovalova.sofia': 2,
    'shechkov.vasily': 1,
    'yakhnenko.ilya': 1,
    'antsiferova.valeria': 0,
    'balandyuk.daria': 0,
    'barymov.ilya': 0,
    'bataev.yan': 3,
    'benz.yan': 3,
    'blinov.danila': 1,
    'vasilyev.artemy': 1,
    'gichka.svetlana': 1,
    'gritsuk.artyom': 2,
    'guliyeva.taisiya': 1,
    'gulyakin.andrey': 0,
    'gusak.maria': 0,
    'zelenov.daniel': 1,
    'zubov.egor': 1,
    'ignatov.ivan': 0,
    'isakov.ivan': 2,
    'karimov.ryan': 2,
    'koseli.yasemin': 2,
    'artyom.kireev': 1,
    'klimenko.maria': 1,
    'kovaleva.valeriya': 1,
    'korchagina.maria': 3,
    'kravchenko.david': 1,
    'kuzovleva.daria': 1,
    'leonenkova.victoria': 0,
    'lokshina.larisa': 1,
    'moiseeva.alexandra': 3,
    'ozzaygyly.denis': 1,
    'osherova.polina': 0,
    'plotnikov.artemy': 1,
    'rarat.vladlen': 0,
    'rudenko.timur': 2,
    'samoilova.anna': 3,
    'sokolov.ivan': 2,
    'sorokorensky.boris': 0,
    'timofeyenko.ilya': 0,
    'urusov.fedor': 2,
    'chernavkin.artemy': 0,
    'shagai.george': 3,
    'sheinberger.martha': 3,
    'shechkov.stepan': 3,
    'demosfen': 0,
    'ArtNext': 1,
    'Median': 2
}


def index_page(request):
    if request.user.is_authenticated:
        return redirect(base_task)
    if len(request.POST) == 0:
        return render(request, 'index.html')
    loginu = request.POST.get('login')
    password = request.POST.get('password')
    user = authenticate(request, username=loginu, password=password)
    if user is not None:
        login(request, user)
        return redirect(base_task)
    else:
        return render(request, 'index.html')


def open_page(request):
    context = dict()  # dictionary, map
    return render(request, 'Steve.html', context)


@login_required
@csrf_exempt
def base_task(request):
    absu = request.build_absolute_uri()
    if request.method == "POST":
        print(request.FILES)
        files = request.FILES
        key = list(files.keys())[0]
        print(key)
        file = files[key]

        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        s3 = session.resource('s3')

        if not os.path.exists(r'recordings/{}'.format(request.user)):
            os.makedirs(r'recordings/{}'.format(request.user))
        npath = ''
        if int(key) == 1:
            npath = '{}_{}'.format(request.user, "text")
        elif 2 <= int(key) <= 7:
            npath = '{}_{}question'.format(request.user, int(key) - 1)
        elif int(key) == 8:
            npath = '{}_monologue'.format(request.user)

        s3.Bucket('aiee-public-files').put_object(Key=r'recordings/{}/{}.wav'.format(request.user, npath), Body=file)
        with open(r'recordings/{}/{}.wav'.format(request.user, npath), 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)
        return HttpResponse("OK")
    else:
        context = dict()
        context['user'] = request.user
        context['task'] = first_task[very_safe_array_of_variants[str(request.user)]]
        context['last_task'] = last_task[very_safe_array_of_variants[str(request.user)]]
        context['task_header'] = "Task {}.1".format(very_safe_array_of_variants[str(request.user)] + 1)
        context['user_variant'] = very_safe_array_of_variants[str(request.user)]
        context['task_description'] = 'You are going to read the text aloud. ' \
                                      'You have 1.5 minutes to read the text silently, ' \
                                      'and then be ready to read it aloud. Remember that ' \
                                      'you will not have more than 2 minutes for reading aloud.'
        context['3t'] = last_task[very_safe_array_of_variants[str(request.user)]]
        context['3td'] = last_task_d[very_safe_array_of_variants[str(request.user)]]
        context['absu'] = absu
        return render(request, 'task.html', context)


def logoutf(request):
    logout(request)
    return redirect(index_page)


@csrf_exempt
def temp_page(request):
    if request.method == "POST":
        print(request.FILES)
        file = request.FILES['ind']
        with open('anime.wav', 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)
    return render(request, "anime.html")
