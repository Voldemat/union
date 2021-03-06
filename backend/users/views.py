from typing import Optional
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate


from django.contrib.auth import get_user_model


User:type = get_user_model()

def friend_invite(request, id:str, *args, **kwargs):
    print(id)
    user:User = get_object_or_404(User.objects.all(), pk = id)
    print(user)
    error:str = ""

    if request.method == 'POST':
        email:Optional[str]    = request.POST.get("email", None)
        password:Optional[str] = request.POST.get("password", None)

        friend:Optional[User] = authenticate(username = email, password = password)

        if not friend:
            error = "Wrong credentionals"
            return render(request, "friend_invite.html", {"user":user, "error":error})

        else:
            User.bind_friends_and_add_chat(user_1 = user, user_2 = friend)

            return redirect("http://localhost:9000/friends")

    else:
        return render(request, "friend_invite.html", {"user":user, "error":error})