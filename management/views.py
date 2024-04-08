from django.shortcuts import render
from django.contrib.auth.decorators import permission_required, login_required
# Create your views here.
from django.shortcuts import render,redirect
from registration.forms import SampleRegistrationForm
from core.models import Sample,CustomUsers,LabManagerTask
from .forms import  UserRegisterationForm
from django.db.models import Count
from django.db.models.functions import Coalesce
from registration.forms import ClientRegisterationForm
# Create your views here.
from core.decorator import role_required
# setting permissions for Lab Manager post
@login_required
@role_required([CustomUsers.LAB_MANAGER])
def sample_list_view(request):
    samples = Sample.objects.all()
    interested_groups = ['registration', 'analysis', 'recommendation', 'processing', 'complete']

    # Group the samples by the stage field and count the number of samples in each group
    stage_groups = (
        Sample.objects
        .values('stage')
        .annotate(count=Coalesce(Count('stage'), 0))  # Ensure count is 0 if no records found
        .filter(stage__in=interested_groups)  # Filter to include only interested groups
    )

    # Create a dictionary to store counts for each stage
    counts_dict = {group['stage']: group['count'] for group in stage_groups}

    # Initialize counts for stages not found in records
    for stage in interested_groups:
        if stage not in counts_dict:
            counts_dict[stage] = 0

    # Define the mapping from stage to description
    stage_mapping = {
        'registration': 'awaiting',
        'analysis': 'analysing',
        'recommendation': 'recommending',
        'processing': 'processing',
        'complete': 'complete'
    }

    # Replace each stage with its corresponding description
    stage_stats_with_description = {stage_mapping.get(stage, stage): count for stage, count in counts_dict.items()}

    return render(request, 'management/sample-list.html', {'samples': samples, 'stage_stats': stage_stats_with_description})


@login_required
@role_required([CustomUsers.LAB_MANAGER])
def users(request):
    users = CustomUsers.objects.all()    
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            print('HELLO')
            # Save the form data to create a new sample object
            user = form.save(commit=False)
            print('HELLO')
            # user.registered_by = request.user  
            user.save()
            return redirect('management:users')  # Redirect to success page
    else:
        form = UserRegisterationForm()
    return render(request, 'management/users-list.html', {'form': form,'users':users})
@login_required
@role_required([CustomUsers.LAB_MANAGER])
def sample_registration_view(request):
    if request.method == 'POST':
        form = SampleRegistrationForm(request.POST)
        client_form=ClientRegisterationForm(request.POST)
        if form.is_valid():
            # Save the form data to create a new sample object
            sample = form.save(commit=False)
            sample.registered_by = request.user  # Assuming the user is authenticated
            sample.stage = Sample.REGISTRATION  # Set the default stage
            sample.save()
            return redirect('management:samples')  # Redirect to success page
        if client_form.is_valid():
            client=client_form.save(commit=False)
            # client.registered_by=request.user
            client.save()
            return redirect('registration:new')
    else:
        form = SampleRegistrationForm()
        client_form=ClientRegisterationForm()
    return render(request, 'management/new.html', {'form': form,'client_form':client_form})

@login_required
@role_required([CustomUsers.LAB_MANAGER])
def tasks(request):
    if request.method == 'POST':
        # the post request is click from a button to confirm invoice this changes the stage to complete and saves an invoice pdf
        sample_id=request.POST.get('sample_id')        
        sample=Sample.objects.get(sample_id=sample_id)
        # print(sample.sample_id)
        sample.stage=Sample.COMPLETE
        sample.save()
        return redirect( 'management:manager-tasks')
    # pick samples from labtask whose stage value in the sample model reads as Processing
    tasks = Sample.objects.filter(stage=Sample.LAB_MANAGER_TASK)      
    return render(request, 'management/tasks.html', {'tasks': tasks})

@login_required
@role_required([CustomUsers.LAB_MANAGER])
def history(request):
    # pick samples from labtask whose stage value in the sample model reads as Complete
    history = Sample.objects.filter(stage=Sample.COMPLETE)
    return render(request, 'management/history.html',{'history': history})