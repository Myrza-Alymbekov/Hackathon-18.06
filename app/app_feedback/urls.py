from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from global_login_required import login_not_required

from . import views

urlpatterns = [

    path('', login_not_required(views.index), name='index'),
    path('contact/', views.contact, name='contact'),
    path('events/', login_not_required(views.FeedbackListView.as_view()), name='feedback_list'),
    path('events/create/', views.FeedbackCreateView.as_view(), name='feedback_create'),
    path('volunteer/', views.VolunteerListView.as_view(), name="application_list"),
    path('events/<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback_detail'),
    path('events/<int:pk>/add_files/', views.add_file_to_feedback, name='add_files'),
    path('events/<int:pk>/add_comment/', views.add_comment_to_feedback, name='add_comment'),
    path('events/<int:pk>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('volunteer/create', views.VolunteerCreateView.as_view(), name="volunteer_create"),
    path('volunteer/', login_not_required(views.VolunteerListView.as_view()), name="application_list"),
    path('events/<int:pk>/', login_not_required(views.FeedbackDetailView.as_view()), name='feedback_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog-detail/', views.blogDetail, name='blog-detail'),
    path('about/', views.about, name='about'),
    path('donation/', login_not_required(views.donation), name='donation'),


    path('update/<int:pk>/', views.FeedbackUpdateView.as_view(), name='feedback_update'),


    path('<int:pk>/change_status/', views.change_feedback_status, name='change_status'),
    path('<int:pk>/create_donation/', views.donation_create, name='create_donation'),
    path('<int:pk>/create_requisite/', views.create_requisite, name='create_requisite'),

    path('faq/', login_not_required(views.faq_listview), name='question_answer'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
