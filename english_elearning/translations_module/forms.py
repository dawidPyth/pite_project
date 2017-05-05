from django import forms

class TranslationForm(form.ModelForm):
	suggestions = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))	
	pol_eng = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))
	eng_pol = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))
