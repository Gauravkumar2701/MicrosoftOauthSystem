from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from microsoft_authentication.auth.auth_utils import (
    get_django_user,
    get_logout_url,
    get_sign_in_flow,
    get_token_from_code,
    get_user, remove_user_and_token,
)


def home(request):
    context = {}
    return render(request, "home.html", context)


def microsoft_login(request):
    request.session["next_url"] = request.GET.get("next")
    flow = get_sign_in_flow()

    try:
        request.session["auth_flow"] = flow

    except Exception as e:
        print(e)

    return HttpResponseRedirect(flow["auth_uri"])


def microsoft_logout(request):
    # logout(request)
    # return HttpResponseRedirect(get_logout_url())
    remove_user_and_token(request)
    # return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(get_logout_url())


def callback(request):
    result = get_token_from_code(request)

    next_url = request.session.pop("next_url", None)
    ms_user = get_user(result["access_token"])
    print(ms_user, "hello dfdfsdfsdf", result["access_token"])
    user = get_django_user(email=ms_user.get("userPrincipalName"))

    # if user:
    #     login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    if not user:
        return HttpResponseForbidden("User not created because email is not valid.")

    if next_url:
        return HttpResponseRedirect(next_url)
    # return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL or "/admin")
    context = {'user': user}
    print(user.id, "kjlkjkljlklk")
    return render(request, 'login.html', context)
