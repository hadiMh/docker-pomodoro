from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
from .models import PomodoroSession, PomodoroLog


@admin.register(PomodoroSession)
class PomodoroSessionAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ["session_name", "duration_minutes", "start_time", "end_time", "is_active", "is_paused"]
    list_filter = ["is_active", "is_paused", "start_time"]
    search_fields = ["session_name", "user__username"]
    readonly_fields = ["start_time", "elapsed_time", "remaining_time"]
    ordering = ["-start_time"]

    fieldsets = (
        ("Session Info", {"fields": ("user", "session_name", "duration_minutes")}),
        ("Timing", {"fields": ("start_time", "end_time", "is_active", "is_paused", "paused_at", "total_paused_duration")}),
        ("Calculated Fields", {"fields": ("elapsed_time", "remaining_time"), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


@admin.register(PomodoroLog)
class PomodoroLogAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ["session_name", "duration_minutes", "start_time", "end_time", "completed", "created_at"]
    list_filter = ["completed", "created_at", "duration_minutes"]
    search_fields = ["session_name", "user__username"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Session Info", {"fields": ("user", "session_name", "duration_minutes")}),
        ("Timing", {"fields": ("start_time", "end_time", "completed")}),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
