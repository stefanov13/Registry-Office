from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth import  mixins as auth_mixins
from django.views import generic as views
from .models import NewsFeedModel
from .forms import DeleteNewsFeedForm

# Create your views here.


class NewsFeedCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'news_feed/news-create.html'
    model = NewsFeedModel
    fields = ['title', 'description']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.request = self.request  # Pass the request to the model instance
        return super().form_valid(form)

class NewsFeedDetailsView(views.DetailView):
    template_name = 'news_feed/news-details.html'
    model = NewsFeedModel
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(queryset, pk=pk)

class NewsFeedEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'outgoing_log/outgoing-edit.html'
    model = NewsFeedModel
    fields = ['title', 'description']

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        current_object = get_object_or_404(queryset, pk=pk)

        current_user_profile = self.request.user.profile
        
        author = current_object.author
        if not any([
            author == current_user_profile,
            self.request.user.is_superuser,
            self.request.user.is_staff
            ]):
            raise Http404()
        
        return current_object

    def get_success_url(self):
        # Redirect to the details page of the edited object after successful update
        return reverse_lazy('news-details', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        return super().form_valid(form)

class NewsFeedDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    
    template_name = 'news_feed/news-delete.html'
    form_class = DeleteNewsFeedForm
    model = NewsFeedModel
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        current_object = get_object_or_404(queryset, pk=pk)

        current_user_profile = self.request.user.profile
        
        author = current_object.author
        if not any([
            author == current_user_profile,
            self.request.user.is_superuser,
            self.request.user.is_staff
            ]):
            raise Http404()
        
        return current_object
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object

        if hasattr(self, 'form_class'):
            form_class = self.get_form_class()
            form = form_class(instance=instance)
            context['form'] = form

        return context
