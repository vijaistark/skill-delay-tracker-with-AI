from django.urls import path
from .views import (
    register_user,
    login_user,
    SkillListCreateView,
    SkillDetailView,
    PracticeSessionListCreateView,
    dashboard,
    generate_ai_summary,
    recommendations,
)

urlpatterns = [
    path('api/register/', register_user, name='register_user'),
    path('api/login/', login_user, name='login_user'),
    path('api/skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('api/skills/<int:pk>/', SkillDetailView.as_view(), name='skill-detail'),
    path('api/learning/', PracticeSessionListCreateView.as_view(), name='learning-list-create'),
    path('api/dashboard/', dashboard, name='dashboard'),
    path('api/ai/summary/', generate_ai_summary, name='ai-summary'),
    path('api/recommendations/', recommendations, name='recommendations'),
]
