from django.shortcuts import render
from django.http import HttpResponse
from .forms import NameForm
from django.views.decorators.csrf import csrf_exempt
from .models import Video
import os
import subprocess
import ffmpeg

# Create your views here.

def index(request):
    return render(request, 'video/home.html',{'content':['first','second']})
@csrf_exempt
def compress(request):
	form = NameForm(request.POST, request.FILES)
	if (form.is_valid()):
		form.save()
		name = form.cleaned_data['name']
		srt = form.cleaned_data['srt']
		mp4 = form.cleaned_data['mp4']
		srt_files = request.FILES.getlist('srt')
		mp4_files = request.FILES.getlist('mp4')
		os.system("ffmpeg")
		#start_main(srt_files[0],str(mp4_files[0]))
		
		return render(request,'video/name.html',{'form':form})
		
	
	return render(request,'video/template.html',{'form':form})
	

def start_main(srt,mp4):
	
	#print (srt.readlines())
	filename = mp4.split('.')[0]
	stream = ffmpeg.input('../video/uploads/'+mp4)
	stream = ffmpeg.output(stream,'../video/uploads/'+filename+'.wav')
	ffmpeg.run(stream)

