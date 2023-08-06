# from django.http import HttpResponseRedirect
# from django.shortcuts import render
#
# # Create your views here.
# from django.urls import reverse
# from registration.backends.default.views import RegistrationView
#
# from stem_registration.forms import RegistrationForm
#
#
# class RegistrationViewStem(RegistrationView):
#     form_class = RegistrationForm
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {
#             'form': self.form_class,
#         })
#
#     def post(self, request, *args, **kwargs):
#
#         form_class = self.form_class(request.POST, request.FILES)
#
#         client_pre_save = super(RegistrationViewStem, self)
#         if form_class.is_valid():
#             client = client_pre_save.register(form_class)
#             client.save()
#             return HttpResponseRedirect(reverse('registration_complete'))
#
#         return render(request, self.template_name, {
#             'form': form_class,
#         })
