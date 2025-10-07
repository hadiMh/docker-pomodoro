from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
import json
from .models import PomodoroSession, PomodoroLog


def pomodoro_timer(request):
    active_session = PomodoroSession.objects.filter(is_active=True).first()
    recent_logs = PomodoroLog.objects.all()[:10]

    context = {
        "active_session": active_session,
        "recent_logs": recent_logs,
    }
    return render(request, "pomodoro/timer.html", context)


@csrf_exempt
@require_http_methods(["POST"])
def start_timer(request):
    try:
        data = json.loads(request.body)
        duration = int(data.get("duration", 25))
        session_name = data.get("session_name", "جلسه مطالعه")
        PomodoroSession.objects.filter(is_active=True).update(is_active=False, end_time=timezone.now())
        session = PomodoroSession.objects.create(duration_minutes=duration, session_name=session_name, is_active=True, is_paused=False)

        return JsonResponse({"success": True, "session_id": session.id, "duration": duration, "session_name": session_name, "start_time": session.start_time.isoformat()})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def pause_timer(request):
    try:
        data = json.loads(request.body)
        session_id = data.get("session_id")

        session = get_object_or_404(PomodoroSession, id=session_id, is_active=True)

        if not session.is_paused:
            session.is_paused = True
            session.paused_at = timezone.now()
            session.save()

            return JsonResponse({"success": True, "is_paused": True, "paused_at": session.paused_at.isoformat()})
        else:
            return JsonResponse({"success": False, "error": "Timer is already paused"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def resume_timer(request):
    try:
        data = json.loads(request.body)
        session_id = data.get("session_id")

        session = get_object_or_404(PomodoroSession, id=session_id, is_active=True)

        if session.is_paused:
            if session.paused_at:
                paused_duration = timezone.now() - session.paused_at
                session.total_paused_duration += paused_duration

            session.is_paused = False
            session.paused_at = None
            session.save()

            return JsonResponse({"success": True, "is_paused": False, "resumed_at": timezone.now().isoformat()})
        else:
            return JsonResponse({"success": False, "error": "Timer is not paused"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def stop_timer(request):
    try:
        data = json.loads(request.body)
        session_id = data.get("session_id")
        completed = data.get("completed", False)

        session = get_object_or_404(PomodoroSession, id=session_id, is_active=True)

        if session.is_paused and session.paused_at:
            paused_duration = timezone.now() - session.paused_at
            session.total_paused_duration += paused_duration

        session.is_active = False
        session.end_time = timezone.now()
        session.save()

        log_entry = PomodoroLog.objects.create(session_name=session.session_name, duration_minutes=session.duration_minutes, start_time=session.start_time, end_time=session.end_time, completed=completed)

        return JsonResponse({"success": True, "session_id": session.id, "log_id": log_entry.id, "end_time": session.end_time.isoformat(), "completed": completed})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def update_session_name(request):
    try:
        data = json.loads(request.body)
        session_id = data.get("session_id")
        new_name = data.get("session_name")

        session = get_object_or_404(PomodoroSession, id=session_id, is_active=True)
        session.session_name = new_name
        session.save()

        return JsonResponse({"success": True, "session_name": new_name})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def update_log_name(request):
    try:
        data = json.loads(request.body)
        log_id = data.get("log_id")
        new_name = data.get("session_name")

        log_entry = get_object_or_404(PomodoroLog, id=log_id)
        log_entry.session_name = new_name
        log_entry.save()

        return JsonResponse({"success": True, "session_name": new_name})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


def get_timer_status(request):
    try:
        active_session = PomodoroSession.objects.filter(is_active=True).first()

        if not active_session:
            return JsonResponse({"success": True, "active": False})

        remaining = active_session.remaining_time
        total_seconds = int(remaining.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        return JsonResponse(
            {
                "success": True,
                "active": True,
                "session_id": active_session.id,
                "session_name": active_session.session_name,
                "duration_minutes": active_session.duration_minutes,
                "remaining_minutes": minutes,
                "remaining_seconds": seconds,
                "is_paused": active_session.is_paused,
                "start_time": active_session.start_time.isoformat(),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
