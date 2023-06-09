from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy, reverse 
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from blog_app.models import UserProfile, Category, Post
from .forms import SignUpForm, EditAccountForm, PasswordChangingForm, ProfileUpdateForm
# Create your views here.
def EditProfilePageView(request, username):
    context = {}
    form = ProfileUpdateForm
    page_user = get_object_or_404(UserProfile, user= request.user)
    # education = get_object_or_404(Education, pk=pk)
    form =  ProfileUpdateForm(instance=page_user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=page_user)
        if form.is_valid():
            form.save()
    username =  page_user.user
    context['page_user'] = page_user
    context['username'] = username
    context['form'] = form
    return render(request, 'registration/edit_profile_page.html', context)

# class ShowProfilePageView(DetailView):
#     model = UserProfile
#     template_name= 'registration/user_profile.html'

#     def get_context_data(self, *args, **kwargs):
#         context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
#         page_user = get_object_or_404(UserProfile, id=self.kwargs['pk'])
#         user_posts = Post.objects.filter(author= page_user.user).order_by('-post_date')
#         username =  page_user.user
#         context['page_user'] = page_user
#         context['user_posts'] = user_posts
#         context['username'] = username
#         return context

def ShowProfilePageView(request, username):
    context = {}
    username = get_object_or_404(User, username=username)   
    page_user = UserProfile.objects.filter(user=username.id)
    user_posts = Post.objects.filter(author= username.id ).order_by('-post_date')
    context['username'] = username
    context['page_user'] = page_user
    context['user_posts'] = user_posts
    return render(request, "registration/user_profile.html", context)



# def ShowProfilePageView(request, username):

#     page_user = get_object_or_404(UserProfile, user=user.id)
#     user_posts = Post.objects.filter(author=page_user.user).order_by("-post_date")
#     username = page_user.user
#     context = {"page_user": page_user, "user_posts": user_posts, "username": username}

#     return render(request, "registration/user_profile.html", context)


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

def  password_success(request):
    return render(request, 'registration/password_success.html', {})



class CreateAccount(SuccessMessageMixin, generic.CreateView):
    form_class= SignUpForm
    template_name='registration/register.html'
    success_url= reverse_lazy('login')
    success_message = "Your account was created successfully"
    

class UpdateAccount(generic.UpdateView):
    model = UserProfile
    form_class= EditAccountForm
    template_name='registration/edit_profile.html'
    success_url= reverse_lazy('blog_list')

    def get_object(self):
        return self.request.user

class CreateProfilePageView(CreateView):
    model = UserProfile
    form_class= ProfileUpdateForm
    template_name = 'registration/create_user_profile_page.html'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def UserDelete(request):
     user = request.user
     if request.method == 'POST':
                user.delete()
                messages.success(request, 'Your account has been deleted successfully')
                return redirect('blog_list')
                
