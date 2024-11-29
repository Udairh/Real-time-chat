from django.shortcuts import render

# Index view
def index(request):
    return render(request, 'chat/index.html')

# Room view
def room(request, room_name):
    return render(request, 'chat/room.html', {'room_name': room_name})
