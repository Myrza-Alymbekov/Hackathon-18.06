from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from management.crm_modules.datatables import DataTablesListView
from .forms import FeedbackForm, FeedbackCommentsForm, ChangeStatusForm, SetEmployeeForm
from .models import Feedback, FeedbackFiles, FeedbackComments
from .serializers import FeedbackSerializer
from .tasks import send_message


class FeedbackListView(DataTablesListView):
    model = Feedback
    serializer_class = FeedbackSerializer
    fields = '__all__'
    filtered_fields = ['organization', 'product']

    def get_queryset(self):
        queryset = Feedback.objects.none()  # Создаем пустой quesyet
        if self.request.user.is_authenticated:  # Проверяем, авторизован ли пользователь
            user = self.request.user
            role = user.role
            if role == 'client':
                queryset = Feedback.objects.filter(client=user).exclude(status='done')
            else:
                queryset = Feedback.objects.all().exclude(status='done')

        return queryset


class FeedbackCreateView(SuccessMessageMixin, CreateView):
    model = Feedback
    template_name = 'feedback/feedback_create.html'
    form_class = FeedbackForm
    success_message = 'Заявка успешно создана'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_name'] = 'Создать'
        context['form'] = FeedbackForm
        context['comment'] = FeedbackCommentsForm
        return context

    def post(self, request, *args, **kwargs):
        form_data = request.POST
        form = FeedbackForm(form_data)
        if form.is_valid():
            form.instance.client = request.user
            recipient_list = [settings.EMAIL_HOST_USER]
            subject = f'Новое обращение от {form.instance.organization}'
            message = f'Ошибка: {form.instance.error_description}'
            try:
                send_message.delay(subject, message, recipient_list)
            except Exception as e:
                print("Произошла ошибка при отправке сообщения:", str(e))
            form.save()

        return redirect(reverse('feedback_detail', kwargs={'pk': form.instance.id}))


class FeedbackDetailView(DetailView):
    model = Feedback
    template_name = 'feedback/feedback_detail.html'

    def get_context_data(self, **kwargs):
        context = super(FeedbackDetailView, self).get_context_data(**kwargs)
        context['feedback_comments'] = FeedbackComments.objects.filter(feedback=self.object)
        context['feedback_files'] = FeedbackFiles.objects.filter(feedback=self.object)
        context['feedback_change_form'] = ChangeStatusForm
        context['employee_set_form'] = SetEmployeeForm
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


def set_employee_feedback(request, pk):
    if request.method == 'POST':
        form = SetEmployeeForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            expiration_date = form.cleaned_data['expiration_date']
            feedback = Feedback.objects.get(id=pk)
            feedback.user = user
            feedback.expiration_date = expiration_date
            feedback.save()
            messages.success(request, 'Ответственный разрабочик и сроки добавлены')
            return redirect(reverse('feedback_detail', kwargs={'pk': pk}))


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