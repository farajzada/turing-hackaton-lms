from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ai_models import call_model
from .models import ChatMessage
from django.conf import settings
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatMessage
from django.db.models import Max
from uuid import uuid4


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from uuid import uuid4, UUID
from .models import ChatMessage
from .ai_models import call_model
import json

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt")
            model = data.get("model")
            chat_id_str = data.get("chat_id")

            if not prompt or not model:
                return JsonResponse({"error": "prompt və model tələb olunur"}, status=400)

            # chat_id varsa istifadə et, yoxdursa yenisini yarat
            try:
                chat_id = UUID(chat_id_str) if chat_id_str else uuid4()
            except:
                chat_id = uuid4()

            # İstifadəçi varsa əlavə et (anonimdirsə, boş burax)
            user = request.user if request.user.is_authenticated else None

            # Əgər bu chat_id üçün bu ilk mesajdırsa, title təyin et
            is_first = not ChatMessage.objects.filter(chat_id=chat_id).exists()
            title = " ".join(prompt.split()[:4]) + "..." if is_first else ""

            # Modeldən cavab al
            response = call_model(prompt, model)

            # DB-ə yaz
            ChatMessage.objects.create(
                chat_id=chat_id,
                title=title if title else "Yeni Chat",
                prompt=prompt,
                response=response,
                model_used=model,
                user=user
            )

            return JsonResponse({
                "chat_id": str(chat_id),
                "response": response
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Yalnız POST sorğusu icazəlidir"}, status=405)


def chat_ui_view(request):
    return render(request, 'chatbox/chat.html')



def chat_history_view(request):
    messages = ChatMessage.objects.order_by('-created_at')[:10]
    data = [
        {
            "prompt": msg.prompt,
            "response": msg.response,
            "model": msg.model_used,
            "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for msg in messages
    ]
    return JsonResponse(data, safe=False)





def chat_sessions_view(request):
    sessions = (
        ChatMessage.objects
        .values('chat_id')
        .annotate(
            title=Max('title'),
            latest_time=Max('created_at')
        )
        .order_by('-latest_time')
    )
    return JsonResponse(list(sessions), safe=False)

def chat_session_detail_view(request, chat_id):
    messages = ChatMessage.objects.filter(chat_id=chat_id).order_by('created_at')
    data = [
        {
            "id": msg.id,  
            "prompt": msg.prompt,
            "response": msg.response,
            "model": msg.model_used,
            "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for msg in messages
    ]
    return JsonResponse(data, safe=False)




@csrf_exempt
def rename_chat_view(request, chat_id):
    if request.method == "POST":
        data = json.loads(request.body)
        new_title = data.get("title")
        if new_title:
            ChatMessage.objects.filter(chat_id=chat_id).update(title=new_title)
            return JsonResponse({"status": "ok", "title": new_title})
        return JsonResponse({"error": "Başlıq göndərilməyib"}, status=400)

@csrf_exempt
def delete_chat_view(request, chat_id):
    if request.method == "DELETE":
        ChatMessage.objects.filter(chat_id=chat_id).delete()
        return JsonResponse({"status": "deleted"})
    
@csrf_exempt
def feedback_view(request, message_id):
    if request.method == "POST":
        data = json.loads(request.body)
        feedback = data.get("feedback")
        if feedback in ["like", "dislike"]:
            ChatMessage.objects.filter(id=message_id).update(feedback=feedback)
            return JsonResponse({"status": "ok"})
        return JsonResponse({"error": "Invalid feedback"}, status=400)