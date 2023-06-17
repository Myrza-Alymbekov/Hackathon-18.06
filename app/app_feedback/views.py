from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.shortcuts import render

from .forms import FeedbackForm, FeedbackCommentsForm, ChangeStatusForm
from .models import Feedback, FeedbackFiles, FeedbackComments, QuestionAnswer
from .tasks import send_message


class FeedbackListView(ListView):
    template_name = 'donation/donation-2.html'
    model = Feedback
    paginate_by = 4
    fields = '__all__'
    filtered_fields = []

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        for feedback in context['object_list']:
            summ = 0
            for requisite in feedback.requisite_set.all():
                summ += sum([i.sum_of_donation for i in requisite.donation_set.all()])
            feedback.status = summ
        return context


class FeedbackCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Feedback
    template_name = 'standart_form.html'
    form_class = FeedbackForm
    success_message = 'Заявка успешно создана'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_name'] = 'Создать'
        context['form'] = FeedbackForm
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FeedbackDetailView(DetailView):
    model = Feedback
    template_name = 'event/evant-details.html'

    def get_context_data(self, **kwargs):
        context = super(FeedbackDetailView, self).get_context_data(**kwargs)
        context['feedback_comments'] = FeedbackComments.objects.filter(feedback=self.object)
        context['feedback_files'] = FeedbackFiles.objects.filter(feedback=self.object)
        context['button_name'] = 'Сохранить'
        return context


class FeedbackUpdateView(SuccessMessageMixin, UpdateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback_create.html'
    success_url = reverse_lazy('feedback_list')
    success_message = 'Заявка успешно обновлена'
    pk_url_kwarg = 'pk'


def add_file_to_feedback(request, pk):
    if request.method == 'POST':
        feedback = Feedback.objects.get(id=pk)
        files = request.FILES.getlist('file')  # Получить список всех загруженных файлов
        description = request.POST.get('description')
        if files:
            for file in files:
                FeedbackFiles.objects.create(
                    files=file,
                    feedback=feedback,
                    description=description,
                )
            messages.success(request, 'Файлы успешно добавлены')
        else:
            messages.error(request, 'Вы не выбрали файл')
        return redirect(reverse('feedback_detail', kwargs={'pk': pk}))


def add_comment_to_feedback(request, pk):
    if request.method == 'POST':
        form = FeedbackCommentsForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                comment = form.save(commit=False)
                comment.feedback_id = pk
                comment.user = request.user
                comment.save()
                messages.success(request, 'Комментарий успешно добавлен')
            else:
                messages.error(request, 'Вы не авторизованы')
        else:
            messages.error(request, 'Комментарий не может быть пустым')

        return redirect(reverse('feedback_detail', kwargs={'pk': pk}))


def delete_comment(request, pk):
    comment = FeedbackComments.objects.get(pk=pk)
    if request.user == comment.user:
        comment.delete()
        messages.success(request, 'Комментарий успешно удален')
        return redirect(reverse('feedback_detail', kwargs={'pk': comment.feedback.id}))
    else:
        messages.error(request, 'Вы можете удалять только свои комментарии')
        return redirect(reverse('feedback_detail', kwargs={'pk': comment.feedback.id}))


def change_feedback_status(request, pk):
    if request.method == 'POST':
        form = ChangeStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            feedback = Feedback.objects.get(id=pk)
            feedback.status = status
            feedback.save()
            messages.success(request, 'Статус успешно изменен')
            if status == 'done':
                feedback = Feedback.objects.get(pk=pk)
                recipient_list = [feedback.client.email]
                subject = 'Техническая поддержка KeyDev'
                message = 'Ваше обращение обработано, ошибка устранена!'
                send_message.delay(subject, message, recipient_list)
            return redirect(reverse('feedback_detail', kwargs={'pk': pk}))
        else:
            messages.error(request, 'Статус не изменен')
            return redirect(reverse('feedback_list'))


def index(request):
    return render(request, 'index.html')


def faq_listview(request):
    faq_list = QuestionAnswer.objects.all()

    context = {
        'faq_list': faq_list,
    }
    return render(request, 'other/faq.html', context)
