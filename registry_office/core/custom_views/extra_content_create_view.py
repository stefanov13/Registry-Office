from django.views import generic as views
from django.utils import timezone


class ExtraContentCreateView(views.CreateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        last_instance = self.model.objects.order_by('-log_num').first()
        next_log_num = int(last_instance.log_num) + 1 if last_instance else 1

        context['next_log_num'] = next_log_num
        context['current_date'] = timezone.now

        return context
