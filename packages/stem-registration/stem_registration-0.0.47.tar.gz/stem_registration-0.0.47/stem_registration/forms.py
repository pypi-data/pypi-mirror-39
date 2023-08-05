from cities_light.models import Country
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_select2.forms import ModelSelect2Widget
from registration.forms import RegistrationFormUniqueEmail

from django import forms
from django.utils.translation import ugettext as _

from stem_registration.models import RegistrationData


class RegistrationDataForm(forms.ModelForm):
    class Meta:
        model = RegistrationData
        fields = '__all__'


class RegistrationForm(RegistrationFormUniqueEmail):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        registration_form_fields = RegistrationDataForm().fields
        if not getattr(settings, 'SHOW_LOGIN', True):
            self.fields['username'].required = False

        if not getattr(settings, 'SHOW_LAST_FIRST_NAME', True):
            # Делаем поля скрытыми
            self.fields['first_name'].widget = forms.HiddenInput()
            self.fields['last_name'].widget = forms.HiddenInput()

        if getattr(settings, 'SHOW_CONTRACTOR_TYPE', True):
            self.fields['contractor_type'] = forms.ChoiceField(
                required=False,
                choices=RegistrationData.CONTRACTOR_TYPE,
                widget=forms.RadioSelect(),
                label=_("Компания"), initial=RegistrationData.PRIVATE_PERSON
            )

        _show_address = getattr(settings, 'SHOW_ADDRESS', True)
        if _show_address:
            registration_form_fields['address'].required = getattr(settings, 'ADDRESS_IS_REQUIRED', True)
            self.fields['address'] = registration_form_fields['address']
            # self.fields['address'].required = getattr(settings, 'ADDRESS_IS_REQUIRED', True)
            self.fields['address_optional'] = registration_form_fields['address_optional']
            self.fields['city'] = registration_form_fields['city']
            self.fields['country'] = registration_form_fields['country']
            self.fields['country'].widget = ModelSelect2Widget(
                model=Country,
                search_fields=['name__icontains'],
                attrs={'data-placeholder': _("Страна"), },
            )
            self.initial['country'] = Country.objects.get(code3=getattr(settings, 'DEFAULT_COUNTRY', 'UKR'))
            # self.fields['country'].initial = Country.objects.get(code3=getattr(settings, 'DEFAULT_COUNTRY', 'UKR'))
            self.fields['zip'] = registration_form_fields['zip']

        _show_billing_address = getattr(settings, 'SHOW_BILLING_ADDRESS', True)
        if _show_billing_address:
            if _show_address:
                self.fields['same'] = forms.BooleanField(
                    widget=forms.CheckboxInput(), label=_("Same"),
                    required=False, initial=True
                )

            self.fields['billing_address'] = registration_form_fields['billing_address']
            self.fields['bill_address_optional'] = registration_form_fields['bill_address_optional']
            self.fields['bill_city'] = registration_form_fields['bill_city']
            self.fields['bill_zip'] = registration_form_fields['bill_zip']
            self.fields['bill_country'] = registration_form_fields['bill_country']
            self.fields['bill_country'].widget = ModelSelect2Widget(
                model=Country,
                search_fields=['name__icontains'],
                attrs={'data-placeholder': _("Страна"), 'data-width': '10em'},
            )
            self.fields['bill_country'].initial = Country.objects.get(code3=getattr(settings, 'DEFAULT_COUNTRY', 'UKR'))

        if getattr(settings, 'SHOW_NUMBER', True):
            self.fields['number'] = registration_form_fields['number']
            self.fields['number'].required = getattr(settings, 'NUMBER_IS_REQUIRED', True)

        if getattr(settings, 'SHOW_TAX_NUMBER', True):
            self.fields['tax_number'] = registration_form_fields['tax_number']
            self.fields['tax_number'].required = getattr(settings, 'TAX_NUMBER_IS_REQUIRED', True)

        if getattr(settings, 'SHOW_ID_CARD_FIELDS', True):
            for field in ('file1', 'file2', 'file3', 'file4', 'file5'):
                self.fields[field] = registration_form_fields[field]
                self.fields[field].widget = forms.FileInput(attrs={'class': 'd-none file'})

        if getattr(settings, 'SHOW_NAME_LEGAL', True):
            self.fields['name_legal'] = registration_form_fields['name_legal']
            self.fields['name_legal'].required = getattr(settings, 'NAME_LEGAL_IS_REQUIRED', False)

        if getattr(settings, 'SHOW_ACCOUNTING_NUMBER', True):
            self.fields['accounting_number'] = registration_form_fields['accounting_number']
            # self.fields['accounting_number'] = CharField(max_length=30, label=_("ЕГРПОУ"), required=False)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        user.is_active = False

        if user.username == '':
            user.username = user.email

        user.save()

        fields = (
            'contractor_type',
            'address',
            'address_optional',
            'country',
            'city',
            'zip',
            'billing_address',
            'bill_address_optional',
            'bill_city',
            'bill_zip',
            'number',
            'tax_number',
            'country',
            'bill_country',
            'name_legal',
            'accounting_number',
            'file1', 'file2', 'file3', 'file4', 'file5',
        )

        registration_data = {}
        for item in self.cleaned_data:
            if item in fields:
                registration_data[item] = self.cleaned_data[item]

        RegistrationData.objects.create(user=user, **registration_data)

        if commit:
            user.save()
            return user

    # def clean(self):
    #     data = self.cleaned_data
    #     if data.get('tax_number', '') != '' and data.get('contractor_type', False):
    #         if not data['tax_number'].isdigit():
    #             raise ValidationError(_("ИНН должен содержать только цифры"))
    #         if data['contractor_type'] == RegistrationData.PRIVATE_PERSON or \
    #                 data['contractor_type'] == RegistrationData.INDIVIDUAL_ENTREPRENEUR:
    #             if len(data['tax_number']) != 10:
    #                 raise ValidationError(_("ИНН должен содержать 10 символов"))
    #         elif data['contractor_type'] == RegistrationData.COMPANY:
    #             if len(data['tax_number']) != 12:
    #                 raise ValidationError(_("ИНН должен содержать 12 символов"))
    #     if data.get('accounting_number', '') != '':
    #         if not data['accounting_number'].isdigit():
    #             raise ValidationError(_("ЕГРПОУ должен содержать только цифры"))

    def clean_tax_number(self):
        tax_number = self.cleaned_data.get('tax_number', '')
        contractor_type = self.cleaned_data.get('contractor_type', False)
        if tax_number != '' and contractor_type:
            if not tax_number.isdigit():
                raise ValidationError(_("ИНН должен содержать только цифры"))
            if contractor_type == RegistrationData.PRIVATE_PERSON or \
                    contractor_type == RegistrationData.INDIVIDUAL_ENTREPRENEUR:
                if len(tax_number) != 10:
                    raise ValidationError(_("ИНН должен содержать 10 символов"))
            elif contractor_type == RegistrationData.COMPANY:
                if len(tax_number) != 12:
                    raise ValidationError(_("ИНН должен содержать 12 символов"))
        return tax_number

    def clean_accounting_number(self):
        data = self.cleaned_data.get('accounting_number', '')
        if data != '':
            if not data.isdigit():
                raise forms.ValidationError(_("ЕГРПОУ должен содержать только цифры"))
        return data

