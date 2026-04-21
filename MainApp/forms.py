from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Skill, Review


class CustomUserCreationForm(UserCreationForm):
    """
    Extended user registration form.
    Allows new users to sign up with email, username, and password.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name (optional)'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name (optional)'
        })
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def clean_email(self):
        """Validate that email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def save(self, commit=True):
        """Save the user with email"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class SkillForm(forms.ModelForm):
    """
    Form for creating and editing skill posts.
    This form helps users post their skills to the marketplace.
    """
    
    class Meta:
        model = Skill
        fields = ['title', 'description', 'category', 'price_type', 'price', 'contact_preference', 'availability_status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Python Programming Tutoring',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your skill in detail. What will you teach/help with? What are your qualifications?',
                'rows': 5
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'price_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price (e.g., 15.00)',
                'step': '0.01',
                'min': '0'
            }),
            'contact_preference': forms.Select(attrs={
                'class': 'form-control',
            }),
            'availability_status': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
    
    def clean(self):
        """Validate form data"""
        cleaned_data = super().clean()
        price_type = cleaned_data.get('price_type')
        price = cleaned_data.get('price')
        
        # If skill is paid, price must be provided
        if price_type == 'paid' and (price is None or price == ''):
            raise forms.ValidationError('Please enter a price for your paid skill.')
        
        return cleaned_data


class ReviewForm(forms.ModelForm):
    """Form for posting a 1-5 star rating + optional comment on a skill."""

    RATING_CHOICES = [(i, f"{i} ★") for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your experience with this skill (optional)',
            }),
        }


class UserProfileForm(forms.ModelForm):
    """
    Form for users to update their profile information.
    """
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
        }
