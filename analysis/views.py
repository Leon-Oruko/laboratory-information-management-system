from django.shortcuts import render,redirect
from core.models import Sample,AnalystTask, Chemical, Microbio, Full,CustomUsers,AgronomistTask,Parameter
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ChemicalForm ,MicrobioForm,FullForm
from datetime import datetime
from core.decorator import role_required
from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
from django.core.serializers import serialize
import json
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
@role_required([CustomUsers.ANALYST, CustomUsers.LAB_MANAGER])
def analyse_task(request, sample_id):
    sample = Sample.objects.get(sample_id=sample_id)
    
    if sample.test_id == 'Chemical':
        form = ChemicalForm(request.POST or None)
        model_class = Chemical
    elif sample.test_id == 'Biological':
        form = MicrobioForm(request.POST or None)
        model_class = Microbio
    elif sample.test_id == 'Full':
        form = FullForm(request.POST or None)
        model_class = Full

    if request.method == 'POST' and form.is_valid():
        sample.stage = 'recommendation'
        task, created = AnalystTask.objects.get_or_create(sample=sample)
        task.analysis = form.cleaned_data['analysis']
        task.status = 'Complete'
        task.analysis_date = datetime.now()
        task.save()
        sample.save()
        analysis_instance = model_class.objects.create(sample=sample, analysis=form.cleaned_data['analysis'])
        analysis_instance.save()
        return redirect('analysis:history')

    # Filter parameters based on sample name
    if 'water' in sample.sample_name.lower():
        parameters = Parameter.objects.filter(is_water=True)
    else:
        parameters = Parameter.objects.filter(is_non_water=True)
        
    serialize_parameters = serialize('json', parameters)
    return render(request, 'analysis/analyse_task.html', {'sample': sample, 'form': form, 'type': sample.test_id, 'parameters': serialize_parameters})



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

 


