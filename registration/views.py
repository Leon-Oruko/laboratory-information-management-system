from django.shortcuts import render,redirect
from .forms import SampleRegistrationForm
from core.models import Sample

from django.db.models import Count
from django.db.models.functions import Coalesce
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
    return render(request, 'registration/new.html', {'form': form})


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

    return render(request, 'registration/samples.html', {'samples': samples, 'stage_stats': stage_stats_with_description})