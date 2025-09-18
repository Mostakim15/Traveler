from django import forms
from .models import Itinerary, Hotel, Activity

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ["name", "start_date", "end_date", "notes"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-[#f8fafc] text-[#0f172a] rounded-lg px-3 py-2 border border-[#94cef2]/40 focus:border-[#94cef2] focus:ring-2 focus:ring-[#94cef2] w-full placeholder:text-[#64748b]'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'bg-[#f8fafc] text-[#0f172a] rounded-lg px-3 py-2 border border-[#94cef2]/40 focus:border-[#94cef2] focus:ring-2 focus:ring-[#94cef2] w-full placeholder:text-[#64748b]'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'bg-[#f8fafc] text-[#0f172a] rounded-lg px-3 py-2 border border-[#94cef2]/40 focus:border-[#94cef2] focus:ring-2 focus:ring-[#94cef2] w-full placeholder:text-[#64748b]'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'bg-[#f8fafc] text-[#0f172a] rounded-lg px-3 py-2 border border-[#94cef2]/40 focus:border-[#94cef2] focus:ring-2 focus:ring-[#94cef2] w-full placeholder:text-[#64748b] h-28 resize-none'
            }),
        }

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["name", "address", "check_in", "check_out"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border-2 border-yellow-200 rounded-lg px-3 py-2'}),
            'address': forms.TextInput(attrs={'class': 'w-full border-2 border-yellow-200 rounded-lg px-3 py-2'}),
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border-2 border-yellow-200 rounded-lg px-3 py-2'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border-2 border-yellow-200 rounded-lg px-3 py-2'}),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["name", "date", "time", "location", "notes"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border-2 border-blue-200 rounded-lg px-3 py-2'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border-2 border-blue-200 rounded-lg px-3 py-2'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full border-2 border-blue-200 rounded-lg px-3 py-2'}),
            'location': forms.TextInput(attrs={'class': 'w-full border-2 border-blue-200 rounded-lg px-3 py-2'}),
            'notes': forms.Textarea(attrs={'class': 'w-full border-2 border-blue-200 rounded-lg px-3 py-2'}),
        }
