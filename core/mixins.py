from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

class SuperAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        validation = user.is_staff and user.is_superuser
        return validation

class AdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        validation = user.is_staff and not user.is_superuser
        return validation

# class SuperAdminMixin:
#     def dispatch(self, request, *args, **kwargs):
#         user = request.user
        # validation = user.is_staff and user.is_superuser
        
#         if not validation:
#             message = f"Maaf, {user.username} anda tidak memiliki hak akses untuk mengunjungi halaman ini."
#             print(message)
#             # return HttpResponseRedirect(reverse("dashboard:profil_saya"))
#             return HttpResponseForbidden(message)
#         return super().dispatch(request, *args, **kwargs)

# class AdminMixin:
#     def dispatch(self, request, *args, **kwargs):
#         user = request.user
        # validation = user.is_staff and not user.is_superuser
        
#         if not validation:
#             message = f"Maaf, {user.username} anda tidak memiliki hak akses untuk mengunjungi halaman ini."
#             print(message)
#             # return HttpResponseRedirect(reverse("dashboard:profil_saya"))
#             return HttpResponseForbidden(message)
#         return super().dispatch(request, *args, **kwargs)