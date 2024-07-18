from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Booking, Feedback, Inquiry

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
        
    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data("password")
        password2 = cleaned_data("password2")
        
        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match")
            
        return cleaned_data
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out']
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        
class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'message']
        
        