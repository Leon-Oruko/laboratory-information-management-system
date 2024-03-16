from django.shortcuts import render,redirect
from .forms import SampleRegistrationForm
from core.models import Sample
# Create your views here.
def sample_registration_view(request):
    if request.method == 'POST':
        form = SampleRegistrationForm(request.POST)
        if form.is_valid():
            # Save the form data to create a new sample object
            sample = form.save(commit=False)
            sample.registered_by = request.user  # Assuming the user is authenticated
            sample.stage = Sample.REGISTRATION  # Set the default stage
            sample.save()
            return render(request, 'registration/success.html')  # Redirect to success page
    else:
        form = SampleRegistrationForm()
    return render(request, 'registration/sample_registration.html', {'form': form})


def sample_list_view(request):
    samples = Sample.objects.all()
    return render(request, 'registration/sample_list.html', {'samples': samples})