from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

from .models import User, Client


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field."""
    
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username',)


class UserAdmin(BaseUserAdmin): # admin.ModelAdmin
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    """The fields to be used in displaying the User model.
    These override the definitions on the base UserAdmin
    that reference specific fields on auth.User."""
    
    list_display = ( 
        'id', 'username', 'last_name', 'first_name', 'email', 'phone',  'date_joined', 'team'
        )
    list_filter = ('team', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'mobile')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'team', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

### For group
"""class UserAdmin(admin.ModelAdmin):
    list_display = ( 
        'id', 'email', 'last_name', 'first_name')"""

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin) 



class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Client/Prospect Info',
         {'fields': ('first_name', 'last_name', 'company_name', 'email', 'phone', 'mobile')}),
        ('Sales', {'fields': ('status', 'sales_contact')}),
        ('Info', {'fields': ('date_created', 'date_updated')})
    )
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('id', 'full_name',  'email', 'phone', 'company_name', 'status', 'sales_contact_id')
    list_filter = ('status', 'sales_contact')
    search_fields = ('first_name', 'last_name', 'company_name', 'sales_contact')

    @staticmethod
    def full_name(obj):
        return f"{obj.last_name}, {obj.first_name}"

# Now register the new ClientAdmin...
admin.site.register(Client, ClientAdmin)