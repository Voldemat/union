from typing import Optional
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate


from django.contrib.auth import get_user_model


User:type = get_user_model()

def friend_invite(request, id, *args, **kwargs):
    user:User = get_object_or_404(User.objects.all(), pk = id)

    if request.method == 'POST':
        email:Optional[str]    = request.POST.get("email", None)
        password:Optional[str] = request.POST.get("password", None)

        friend:Optional[User] = authenticate(username = email, password = password)

        if not friend:
            return render(request, "friend_invite.html", {"error":"Wrong credentionals!"})

        else:
            User.bind_friends(user, friend)

            return redirect("http://localhost:9000/")

    return render(request, "friend_invite.html", {"user":user})