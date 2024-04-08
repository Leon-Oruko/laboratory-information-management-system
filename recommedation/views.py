from django.shortcuts import render
from django.shortcuts import render,redirect
from core.models import Sample,CustomUsers,Chemical,Microbio,Full
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required, permission_required
from core.decorator import role_required
# Create your views here.
@login_required
@role_required([CustomUsers.AGRONOMIST,CustomUsers.LAB_MANAGER])
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

    return render(request, 'recommendation/sample-list.html', {'samples': samples, 'stage_stats': stage_stats_with_description})

# C:\Users\User\Desktop\items\vs code\django\lab_management_system\recommedation\templates\recommendation\sample-list.html

@login_required
@role_required([CustomUsers.AGRONOMIST,CustomUsers.LAB_MANAGER])
def recommend(request):    
   samples_with_chemical = Sample.objects.filter(stage='recommendation', test_id=Sample.CHEMICAL).select_related('chemical').all()
   samples_with_microbio = Sample.objects.filter(stage='recommendation', test_id=Sample.MICROBIO).select_related('microbio').all()
   samples_with_full = Sample.objects.filter(stage='recommendation', test_id=Sample.FULL).select_related('full').all()

   if request.method=='POST':
        #    get recommendation from text area
        recommendation_text = request.POST.get('recommendation_text')  # Assuming 'recommendation_text' is the name of your textarea
        sample_id=request.POST.get('sample_id')
        sample=Sample.objects.get(sample_id=sample_id)
        # print(sample.sample_id)
        try:
    # Try to get Chemical model instance related to the sample
            model = Chemical.objects.get(sample=sample)
        except ObjectDoesNotExist:
            try:
                # If Chemical model instance doesn't exist, try to get Microbio model instance
                model = Microbio.objects.get(sample=sample)
            except ObjectDoesNotExist:
                try:
                    # If neither Chemical nor Microbio model instance exists, try to get Full model instance
                    model = Full.objects.get(sample=sample)
                except ObjectDoesNotExist:
                    model=None
        model.recommendation=recommendation_text
        sample.stage=Sample.LAB_MANAGER_TASK
        model.save()
        sample.save()
        redirect('recommedation:recommend')    
   return render(request, 'recommendation/recommend.html',{'chemical_samples':samples_with_chemical,'microbio_samples':samples_with_microbio,'full_samples':samples_with_full})

@login_required
@role_required([CustomUsers.AGRONOMIST,CustomUsers.LAB_MANAGER])
def history(request):
    # samples = AgronomistTask.objects.all()    
    samples_with_chemical = Sample.objects.filter(stage='processing', test_id=Sample.CHEMICAL).select_related('chemical').all()
    samples_with_microbio = Sample.objects.filter(stage='processing', test_id=Sample.MICROBIO).select_related('microbio').all()
    samples_with_full = Sample.objects.filter(stage='processing', test_id=Sample.FULL).select_related('full').all()
    return render(request, 'recommendation/history.h    tml',{'samples_with_chemical': samples_with_chemical,'samples_with_microbio':samples_with_microbio,'samples_with_full':samples_with_full})
