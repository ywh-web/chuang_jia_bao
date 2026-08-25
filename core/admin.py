from django.contrib import admin

from .models import Comment, ContactInquiry, UGCSubmission


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'cooperation_type', 'status', 'created_at')
    list_filter = ('cooperation_type', 'status', 'created_at')
    search_fields = ('name', 'contact', 'message')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)


class CommentPageFilter(admin.SimpleListFilter):
    title = '所属页面'
    parameter_name = 'comment_page'

    def lookups(self, request, model_admin):
        return (
            ('experience', '数字体验'),
            ('story', '非遗故事'),
            ('other', '其他页面'),
        )

    def queryset(self, request, queryset):
        if self.value() in {'experience', 'story'}:
            return queryset.filter(page_key=self.value())
        if self.value() == 'other':
            return queryset.exclude(page_key__in={'experience', 'story'})
        return queryset


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'page_name', 'thread_type', 'anchor', 'status', 'like_count', 'created_at')
    list_filter = (CommentPageFilter, 'status', 'created_at')
    search_fields = ('author_name', 'content', 'page_key', 'anchor')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)

    @admin.display(description='所属页面', ordering='page_key')
    def page_name(self, obj):
        return {'experience': '数字体验', 'story': '非遗故事'}.get(obj.page_key, obj.page_key or '未标记')

    @admin.display(description='内容类型')
    def thread_type(self, obj):
        return '回复' if obj.parent_id else '主评论'


@admin.register(UGCSubmission)
class UGCSubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'category', 'status', 'featured', 'like_count', 'created_at')
    list_filter = ('category', 'status', 'featured', 'created_at')
    search_fields = ('title', 'author_name', 'story', 'contact')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status', 'featured')
