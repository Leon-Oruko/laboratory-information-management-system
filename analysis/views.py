from django.shortcuts import render,redirect
from core.models import Sample,AnalystTask, Chemical, Microbio, Full,CustomUsers
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ChemicalForm ,MicrobioForm,FullForm
from datetime import datetime
from core.decorator import role_required
# Create your views here.
@login_required
@role_required([CustomUsers.ANALYST,CustomUsers.LAB_MANAGER])
def sample_list_view(request):    
    samples = Sample.objects.filter(stage='registration')
    if request.method == 'POST':
        sample_id = request.POST.get('sample_id')
        if sample_id:
            sample = Sample.objects.get(sample_id=sample_id)
            sample.stage = 'analysis'
            sample.is_processed = False
            task=AnalystTask(sample=sample,status='Incomplete',analyzed_by=request.user)
            sample.save()
            task.save()
            redirect('analysis:analyse') # Redirect to a view showing picked samples
        redirect ('analysis:sample-list-view')                
    return render(request, 'analysis/sample-list.html', {'samples': samples})

@login_required
@role_required([CustomUsers.ANALYST,CustomUsers.LAB_MANAGER])
def picked_samples(request):
    samples = Sample.objects.filter(stage='analysis')    
    return render(request, 'analysis/picked_samples.html', {'samples': samples})

@login_required
@role_required([CustomUsers.ANALYST,CustomUsers.LAB_MANAGER])
def past_analysis(request):
    samples = AnalystTask.objects.filter(status='Complete')
    return render(request, 'analysis/past_analysis.html', {'samples': samples})

@login_required
@role_required([CustomUsers.ANALYST,CustomUsers.LAB_MANAGER])
def analyse_task(request, sample_id):         
    if request.method == 'POST':                      
        sample = Sample.objects.get(sample_id=sample_id)                      
        if sample.test_id == 'Chemical':
            form = ChemicalForm(request.POST)
            model_class = Chemical
        elif sample.test_id == 'Biological':
            form = MicrobioForm(request.POST)
            model_class = Microbio
        elif sample.test_id == 'Full':
            form = FullForm(request.POST)
            model_class = Full
        if form.is_valid():           
            sample.stage='recommendation' 
            task, created = AnalystTask.objects.get_or_create(sample=sample)
            task.analysis = form.cleaned_data['analysis']
            task.status = 'Complete'
            task.analysis_date = datetime.now()  # Call the function to get the current date and time
            task.save()
            sample.save()
            # Create an instance of the respective model and save it
            analysis_instance = model_class.objects.create(sample=sample, analysis=form.cleaned_data['analysis'])
            analysis_instance.save()
            return redirect('analysis:history')
        else:
            print('error')
    else:
        sample = Sample.objects.get(sample_id=sample_id) 
        if sample.test_id == 'Chemical':
            form = ChemicalForm(initial={'sample': sample})            
        elif sample.test_id == 'Biological':
            form = MicrobioForm(initial={'sample': sample})
        elif sample.test_id == 'Full':
            form = FullForm(initial={'sample': sample})              
    return render(request, 'analysis/analyse_task.html', {'sample': sample, 'form': form})