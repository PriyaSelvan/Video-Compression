from django import forms
from .models import Video
class NameForm(forms.ModelForm):
	name = forms.CharField(label='name',max_length=140)
	mp4 = forms.FileField(label='mp4')
	srt = forms.FileField(label='srt')
	class Meta:
		model = Video
		fields = "__all__"
