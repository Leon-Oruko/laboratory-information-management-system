from django.shortcuts import render
from django.shortcuts import render,redirect
from core.models import Sample,CustomUsers,Chemical,Microbio,Full,AnalystTask,AgronomistTask
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required, permission_required
from core.decorator import role_required
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.
import ast
import json
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
        interpretation_text=request.POST.get('interpretation_text')
        sample_id=request.POST.get('sample_id')
        sample=Sample.objects.get(sample_id=sample_id)
        sample.stage=Sample.LAB_MANAGER_TASK
        sample.save()
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
        model.save()        
        try:
            with transaction.atomic():
                new_recommendation = AgronomistTask(
                    sample=sample,
                    recommendation=recommendation_text,
                    interpretation=interpretation_text,
                    reviewed_by=request.user
                )
                new_recommendation.save()
                # If there are any related actions, they can be performed here within the transaction block.
        except Exception as e:
            # Handle the error, possibly logging it or informing the user.
            print(f"An error occurred: {e}")        
        redirect('recommedation:recommend')    
   return render(request, 'recommendation/recommend.html',{'chemical_samples':samples_with_chemical,'microbio_samples':samples_with_microbio,'full_samples':samples_with_full})

@login_required
@role_required([CustomUsers.AGRONOMIST,CustomUsers.LAB_MANAGER])
def history(request):      
    samples_with_chemical = Sample.objects.filter(test_id=Sample.CHEMICAL).exclude(stage__in=['analysis', 'registration']).select_related('chemical','agronomist_task','analysttask').all()
    samples_with_microbio = Sample.objects.filter(test_id=Sample.MICROBIO).exclude(stage__in=['analysis', 'registration']).select_related('microbio','agronomist_task','analysttask').all()
    samples_with_full = Sample.objects.filter(test_id=Sample.FULL).exclude(stage__in=['analysis', 'registration']).select_related('full','agronomist_task','analysttask').all()
    return render(request, 'recommendation/history.html',{'samples_with_chemical': samples_with_chemical,'samples_with_microbio':samples_with_microbio,'samples_with_full':samples_with_full})
def fix_json_format(json_str):
    # Replace single quotes with double quotes for keys
    fixed_json_str = json_str.replace("'", '"')
    return fixed_json_str

def viewCertificate(request, sample_id):
    main_sample = Sample.objects.get(sample_id=sample_id)
    sample = AnalystTask.objects.get(sample=main_sample)
    reco_sample = AgronomistTask.objects.get(sample=main_sample)

    # Assuming sample.analysis is a queryset or related manager
    analysis_data = list(ast.literal_eval(fix_json_format(sample.analysis)))
    # analysis_data = json.loads(fix_json_format(sample.analysis))
    print(json.loads(fix_json_format(sample.analysis))[0]['parameters'])
    # print(analysis_data)

    context = {
        'main_sample': main_sample,
        'sample': sample,
        'reco_sample': reco_sample,
        'analysis_data': analysis_data,  # Pass the serialized data as a list of dictionaries
    }

    return render(request, 'recommendation/i.html', context)
#  [json.loads(e) for e in analysis_data]