from django.contrib.auth.mixins import AccessMixin


class GroupRequiredMixin(AccessMixin):
    group_required = ["trainee", "employee", "manager"]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_superuser:
            # Superuser skips group check
            return super().dispatch(request, *args, **kwargs)

        user_groups = request.user.groups.values_list('name', flat=True)

        if not any(group in user_groups for group in self.group_required):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
