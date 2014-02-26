from datetime import timedelta
from django.contrib import admin
from tracking.models import Visitor, Pageview
from tracking.settings import TRACK_PAGEVIEWS

class ReadonlyAdmin(admin.ModelAdmin):
   def __init__(self, model, admin_site):
      super(ReadonlyAdmin, self).__init__(model, admin_site)
      self.readonly_fields = [field.name for field in filter(lambda f: not f.auto_created, model._meta.fields)]

   def get_actions(self, request):
       actions = super(ReadonlyAdmin, self).get_actions(request)
       if 'delete_selected' in actions:
           del actions['delete_selected']
       return actions
   def has_delete_permission(self, request, obj=None):
       return False
   def has_add_permission(self, request, obj=None):
       return False

class VisitorAdmin(ReadonlyAdmin):
    date_hierarchy = 'start_time'

    list_display = ('session_key', 'user', 'start_time', 'session_over',
        'pretty_time_on_site', 'ip_address', 'user_agent')
    list_filter = ('user', 'ip_address')

    def session_over(self, obj):
        return obj.session_ended() or obj.session_expired()
    session_over.boolean = True

    def pretty_time_on_site(self, obj):
        if obj.time_on_site is not None:
            return timedelta(seconds=obj.time_on_site)
    pretty_time_on_site.short_description = 'Time on site'

admin.site.register(Visitor, VisitorAdmin)


class PageviewAdmin(ReadonlyAdmin):
    date_hierarchy = 'view_time'

    list_display = ('view_time', 'method', 'url', 'status')

if TRACK_PAGEVIEWS:
    admin.site.register(Pageview, PageviewAdmin)
