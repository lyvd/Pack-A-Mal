from django import forms



class PackageSubmitForm(forms.Form):

    package_name = forms.CharField(
        label='Package Name', 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Submit package name', 
            'class': 'form-control',   
            'id': 'package_name',
            'list': 'package_name_list'
        })
    )
    
        
    # package_version = forms.CharField(label='Package Version', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Submit package version', 'class': 'form-control'}))
    ecosystem = forms.ChoiceField(
        label='Ecosystem',
        choices=[
            ('wolfi', 'Wolfi'),
            ('npm', 'npm'),
            ('pypi', 'PyPI'),
            ('rubygems', 'RubyGems'),
            ('crates.io', 'Crates.io'),
            ('maven_central', 'Maven Central'),
            ('packagist', 'Packagist'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )