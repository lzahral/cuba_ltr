import json
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils.http import http_date
from django.views.decorators.cache import cache_control
from django.utils.cache import patch_cache_control

from letters.views import render
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


from django.views.generic import ListView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
class Register(FormView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        data = form.cleaned_data
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        password2 = form.cleaned_data['password2']
        phone_number = form.cleaned_data['phone']
        city = form.cleaned_data['city']
        is_subscribed = False
        is_error = False
        if User.objects.filter(username=username).exists():
            is_error = True
            form.add_error("username", 
                "A user with this email already exists.")
        if password != password2:
            is_error = True
            form.add_error(
                "password2",  
                    "Password and confirm password do not match.")
        if is_error:
            return super().form_invalid(form)
        user = User.objects.create_user(
            username=data["username"],
            email=data["username"],
            password=data["password"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        
        Profile.objects.create(
            user=user, phone_number=phone_number, city=city, is_subscribed=is_subscribed)
        login(self.request, user)
        messages.success(self.request,  "Registration successful. ✅")
        return super().form_valid(form)


class Login(FormView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy('letters')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.data['login[password]']
        is_error = False
        if username == "":
            is_error = True
            form.add_error("username", "Enter your username.")
        if password == "":
            is_error = True
            form.add_error("password", "Enter your password.")
        if is_error:
            return super().form_invalid(form)
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(self.request, user)
                messages.success(self.request,  "Login successful.")

                return super().form_valid(form)
            else:
                form.add_error(
                    "password", "The username or password is incorrect.")

        return super().form_invalid(form)


class ChangePassword(FormView):
    form_class = ChangePasswordForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('admin-panel')

    def form_valid(self, form):
        data = form.cleaned_data
        print(form.cleaned_data)
        error =False
        old_password = data['old_password']
        print(old_password)
        if not self.request.user.check_password(old_password):
            print('hi')
            form.add_error("old_password", "رمز فعلی نادرست است.")
            error = True
        p1 = data['new_password1']
        p2 = data['new_password2']
        if p1 and p2 and p1 != p2:
            form.add_error('new_password2', "رمزهای جدید با هم تطابق ندارند.")
            error = True

        if error:
            return super().form_invalid(form)

        else:
            password =data['new_password1']
            self.request.user.set_password(password)
            self.request.user.save()
            login(self.request, self.request.user)

        return super().form_valid(form)

    
def logout_page(request):
    logout(request)

    response = redirect('login')
    # response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    # response['Pragma'] = 'no-cache'
    # response['Expires'] = http_date(0)

    return response


# class EditProfile(FormView):
#     form_class = ProfileForm
#     template_name = "accounts/edit_profile.html"
#     success_url = reverse_lazy('edit-profile')

#     def get_initial(self):
#         initial = super(EditProfile, self).get_initial()
#         profile = Profile.objects.get(user=self.request.user)
#         user = self.request.user
#         initial.update(
#             {
#                 'edit':True,
#                 "email": user.email,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "username": user.username,
#                 "phone_number": profile.phone_number,
#                 "avatar": profile.avatar,
#                 # "permissions": profile.permissions.all(),
#                 # 'cou'
#             }
#         )
#         print(initial)
#         return initial

#     def form_valid(self, form):
#         data = form.cleaned_data
#         print(form.cleaned_data)
#         # if form.has_changed():
#         user = self.request.user
#         user.first_name = data["first_name"]
#         user.last_name = data["last_name"]
#         user.email = data["email"]
#         user.save()
#         profile = Profile.objects.get_or_create(user=self.request.user)[0]
#         # print(profile.permissions)
#         print(data['avatar'])
#         profile.avatar = data["avatar"]
#         profile.phone_number = data["phone_number"]
#         profile.save()
#         # profile.permissions.set(profile.permissions.all())
#         return super().form_valid(form)
    

class UsersListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "accounts/list.html"
    context_object_name = "data"
    paginate_by = 10

  

# def read_all_notification(request):
#     if request.method == "GET":
#         notifications = Notification.objects.filter(
#             recipient=request.user, read=False)
#         for item in notifications:
#             item.read = True
#             item.save()
#         return JsonResponse({"count": 0}, status=200)
#     return JsonResponse({"error": "error"}, status=400)
# def delete_all_notifications(request):
#     if request.method == "GET":
#         notifications = Notification.objects.filter(
#             recipient=request.user, is_deleted=False)
#         for item in notifications:
#             item.is_deleted = True
#             item.save()
#         return JsonResponse({"count": 0}, status=200)
#     return JsonResponse({"error": "error"}, status=400)


# def delete_notification(request):
#     if request.method == "POST":
#         id = request.POST["id"]
#         notification = Notification.objects.get(id=id)
#         notification.is_deleted = True
#         notification.read = True
#         notification.save()
#         notifications = Notification.objects.filter(
#             recipient=request.user, is_deleted = False)
#         return JsonResponse({"count": len(notifications)}, status=200)
#     return JsonResponse({"error": "error"}, status=400)

# views.py
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserProfileForm
from django.views import View


class UserCreateView(CreateView):
    form_class = UserProfileForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('users')

class UserUpdateView(UpdateView):
    model = Profile
    form_class = UserProfileForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("users")


class UserDelete(View):

    def delete(self, request, pk):
        User.objects.get(id=pk).delete()
        return JsonResponse({'message': 'successful'}, status=200)