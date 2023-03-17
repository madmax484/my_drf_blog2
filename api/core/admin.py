from django.contrib import admin

from .models import Post, UserPostRelation, Comment


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)


@admin.register(UserPostRelation)
class UserPostRelationAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    pass
