from django import template
import dateutil.relativedelta as delta
import dateutil.parser as parser
import datetime

register = template.Library()

@register.filter
def get_at_index(list, index):
    return list[index]

@register.filter
def get_remaining_months(registration_upto):
    month = parser.parse(str(registration_upto)).month
    current_month = parser.parse(str(datetime.datetime.today())).month
    if (current_month - month) > 0:
        return (current_month - month + 1)
    else:
        return 1
