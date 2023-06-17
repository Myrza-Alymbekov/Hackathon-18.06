from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.FeedbackListView.as_view(), name='feedback_list'),
    path('events/create/', views.FeedbackCreateView.as_view(), name='feedback_create'),
    path('volunteer/create', views.VolunteerCreateView.as_view(), name="application_create"),
    path('volunteer/', views.VolunteerListView.as_view(), name="application_list"),
    path('events/<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog-detail/', views.blogDetail, name='blog-detail'),
    path('about/', views.about, name='about'),
    path('donation/', views.donation, name='donation'),


    path('update/<int:pk>/', views.FeedbackUpdateView.as_view(), name='feedback_update'),

    path('<int:pk>/add_files/', views.add_file_to_feedback, name='add_files'),
    path('<int:pk>/add_comment/', views.add_comment_to_feedback, name='add_comment'),
    path('<int:pk>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('<int:pk>/change_status/', views.change_feedback_status, name='change_status'),
    # path('<int:pk>/set_employee/', views.set_employee_feedback, name='set_employee'),

    path('faq/', views.faq_listview, name='question_answer'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
