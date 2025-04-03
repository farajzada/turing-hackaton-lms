from django.urls import path
from .views import chat_view, chat_ui_view, chat_history_view, chat_sessions_view, chat_session_detail_view
from .views import rename_chat_view, delete_chat_view,feedback_view

urlpatterns = [
    path('chat/', chat_view, name='chat'),
    path('ui/', chat_ui_view, name='chat-ui'),
    path('chat/history/', chat_history_view, name='chat-history'),
    path('chat/sessions/', chat_sessions_view, name='chat-sessions'),
    path('chat/session/<uuid:chat_id>/', chat_session_detail_view, name='chat-session-detail'),
    path('chat/session/<uuid:chat_id>/rename/', rename_chat_view, name='rename-chat'),
    path('chat/session/<uuid:chat_id>/delete/', delete_chat_view, name='delete-chat'),
    path('chat/message/<int:message_id>/feedback/', feedback_view, name='chat-feedback'),
]
