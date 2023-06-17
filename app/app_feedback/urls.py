from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.FeedbackListView.as_view(), name='feedback_list'),
    path('create/', views.FeedbackCreateView.as_view(), name='feedback_create'),
    path('<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback_detail'),
    path('update/<int:pk>/', views.FeedbackUpdateView.as_view(), name='feedback_update'),

    path('<int:pk>/add_files/', views.add_file_to_feedback, name='add_files'),
    path('<int:pk>/add_comment/', views.add_comment_to_feedback, name='add_comment'),
    path('<int:pk>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('<int:pk>/change_status/', views.change_feedback_status, name='change_status'),
    path('<int:pk>/create_donation/', views.donation_create, name='create_donation'),
    path('<int:pk>/create_requisite/', views.create_requisite, name='create_requisite'),

    path('faq/', views.faq_listview, name='question_answer'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
