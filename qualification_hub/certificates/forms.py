"""
CertificateForm for Managing Certificate Information

This form class is used to create and update `Certificate` instances.
It handles certificate-related information such as certificate name, organization,
description, expiration date, issuing authority, certificate number, verification URL, 
and date earned. 

Key Features:
- Uses Crispy Forms for enhanced styling and layout.
- Designed to integrate with JavaScript-based date pickers (like Flatpickr).
- Validates unique certificate numbers to avoid conflicts.

Dependencies:
- Requires the `Certificate` model from the current module.
- Utilizes Crispy Forms for form layout and Bootstrap for styling.

Author: Kaiyrtay
"""

from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit
from .models import Certificate


class CertificateForm(forms.ModelForm):
    certificate_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Certificate Name'}
    ))
    organization = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Organization'}
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Description', 'rows': 3}
    ))
    expiration_date = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'datepicker', 'placeholder': 'Expiration Date'}
        )
    )
    issuing_authority = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Issuing Authority'}),
        required=False,
    )
    certificate_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Certificate Number'}
    ))
    verification_url = forms.URLField(
        widget=forms.URLInput(attrs={'placeholder': 'Verification URL'}),
        required=False,
    )
    date_earned = forms.DateField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'datepicker', 'placeholder': 'Date Earned'}
        )
    )

    class Meta:
        model = Certificate
        fields = [
            'certificate_name', 'organization', 'description', 'expiration_date',
            'issuing_authority', 'certificate_number', 'verification_url', 'date_earned',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('certificate_name', css_class='form-control'),
                Field('organization', css_class='form-control'),
                Field('description', css_class='form-control'),
                Field('expiration_date', css_class='datepicker'),
                Field('issuing_authority', css_class='form-control'),
                Field('certificate_number', css_class='form-control'),
                Field('verification_url', css_class='form-control'),
                Field('date_earned', css_class='datepicker'),
                Submit('submit', 'Save Changes', css_class='btn btn-primary'),
            )
        )

    def clean_certificate_number(self):
        certificate_number = self.cleaned_data.get('certificate_number', '')

        # Get the current instance (the certificate being updated or created)
        current_certificate = self.instance

        # Ensure the unique check doesn't include the current certificate being updated
        if Certificate.objects.filter(certificate_number=certificate_number).exclude(id=current_certificate.id).exists():
            raise ValidationError(
                "A certificate with this number already exists.")

        return certificate_number
