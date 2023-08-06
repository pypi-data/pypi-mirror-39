from django.contrib.auth.mixins import UserPassesTestMixin

class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        current_user = self.request.user
        if current_user == self.model.user:
            return True
        return False

class UserQueryListViewMixin:
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
