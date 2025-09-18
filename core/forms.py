from django import forms
from .models import Destination

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'country', 'city', 'description', 'latitude', 'longitude']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-[#f8fafc] text-[#0f172a] rounded-lg px-3 py-2 border border-[#94cef2]/40 focus:border-[#94cef2] focus:ring-2 focus:ring-[#94cef2] w-full placeholder:text-[#64748b]'
            }),
            'country': forms.TextInput(attrs={
                'class': 'bg-[#f8fafc] text-[#0f172a] rounded-lg px-3 py-2 border border-[#94cef2]/40 focus:border-[#94cef2] focus:ring-2 focus:ring-[#94cef2] w-full placeholder:text-[#64748b]'
            }),
            'city': forms.TextInput(attrs={
                'class': 'bg-[#f8fafc] text-[#0f172a] rounded-lg px-3 py-2 border border-[#94cef2]/40 focus:border-[#94cef2] focus:ring-2 focus:ring-[#94cef2] w-full placeholder:text-[#64748b]'
            }),
            'description': forms.Textarea(attrs={
                'class': 'bg-[#f8fafc] text-[#0f172a] rounded-lg px-3 py-2 border border-[#94cef2]/40 focus:border-[#94cef2] focus:ring-2 focus:ring-[#94cef2] w-full placeholder:text-[#64748b] h-28 resize-none'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
