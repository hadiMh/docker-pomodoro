from django import template
from jalali_date import datetime2jalali

register = template.Library()


@register.filter
def jalali_date(value, format_string="%Y/%m/%d"):
    """Convert datetime to Jalali date format"""
    if value:
        jalali_date = datetime2jalali(value)
        return jalali_date.strftime(format_string)
    return ""


@register.filter
def jalali_datetime(value, format_string="%Y/%m/%d %H:%M"):
    """Convert datetime to Jalali datetime format"""
    if value:
        jalali_date = datetime2jalali(value)
        return jalali_date.strftime(format_string)
    return ""


@register.filter
def jalali_time(value, format_string="%H:%M"):
    """Convert datetime to Jalali time format"""
    if value:
        jalali_date = datetime2jalali(value)
        return jalali_date.strftime(format_string)
    return ""
