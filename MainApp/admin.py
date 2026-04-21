from django.contrib import admin
from .models import Skill, Review


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Skill posts.
    Provides a convenient way for administrators to moderate and manage skills.
    """
    
    # Columns to display in the list view
    list_display = (
        'title',
        'owner',
        'category',
        'price_type',
        'availability_status',
        'created_at',
    )
    
    # Columns that make records clickable
    list_display_links = ('title',)
    
    # Columns by which you can filter the list
    list_filter = (
        'category',
        'price_type',
        'availability_status',
        'created_at',
    )
    
    # Enables search functionality
    search_fields = (
        'title',
        'description',
        'owner__username',
        'owner__email',
    )
    
    # Read-only fields (cannot be edited)
    readonly_fields = (
        'created_at',
        'updated_at',
        'owner',
    )
    
    # Organize fields into fieldsets for better UI
    fieldsets = (
        ('Skill Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Pricing', {
            'fields': ('price_type', 'price')
        }),
        ('Availability & Contact', {
            'fields': ('availability_status', 'contact_preference')
        }),
        ('Owner & Timestamps', {
            'fields': ('owner', 'created_at', 'updated_at'),
            'classes': ('collapse',),  # Collapsed by default
        }),
    )
    
    # Ordering of records in the list
    ordering = ('-created_at',)
    
    def save_model(self, request, obj, form, change):
        """
        Override save to preserve the owner when editing.
        This prevents admin users from changing who owns a skill.
        """
        if not change:  # If creating a new object
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('skill', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('skill__title', 'author__username', 'comment')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
