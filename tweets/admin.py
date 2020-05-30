from django.contrib import admin
from .models import Tweet, TweetLike

# TabularInline will show in the tabular form
class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike


class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]          # here we show the inlines TweetLikeAdmin
    list_display = ['__str__', 'user']      # __str__ means this will display which we return in the model
    search_fields = ['content','user__username', 'user__email']
    class Meta:
        model = Tweet

admin.site.register(Tweet, TweetAdmin)