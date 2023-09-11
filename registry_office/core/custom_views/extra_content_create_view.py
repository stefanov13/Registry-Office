from django.views import generic as views
from django.utils import timezone


class ExtraContentCreateView(views.CreateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        last_instance = self.model.objects.order_by('-creation_date', '-log_num').first()

        current_year = timezone.now().year

        if last_instance and last_instance.creation_date.year == current_year:
            last_log_num = last_instance.log_num
        else:
            last_log_num = '0'

        numeric_part = ''.join(filter(str.isdigit, last_log_num))

        next_log_num = int(numeric_part) + 1

        context['next_log_num'] = next_log_num
        context['current_date'] = timezone.now

        return context
