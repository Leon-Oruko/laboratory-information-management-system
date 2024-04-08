from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter your password'


# Create your views here.
def user_login(request):    
    if request.method == 'POST':        
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)            
            if user is not None:                
                login(request, user)                
                if user.post == 'Lab Manager':                    
                    return redirect('management:samples')
                elif user.post == 'Agronomist':                    
                    return redirect('recommedation:samples')                    
                elif user.post == 'Analyst':                    
                    return redirect('analysis:sample-list-view')
                elif user.post == 'Admin':                    
                    return redirect('registration:samples')                             
            print('user not there')  
        messages.error(request, 'Invalid credentials')
        return redirect('login:login')                                 
    else:
        form = CustomAuthenticationForm()        
    return render(request, 'login/login.html', {'form': form,'messages': messages.get_messages(request)})
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('login:login') #Redirect to the login page


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login:login')  # Redirect to the login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'login/register.html', {'form': form})
