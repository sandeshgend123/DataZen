from django.contrib import admin
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import About, Project, Contact, Service, BlogPost, SalesInquiry, Newsletter


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'established_year', 'team_size', 'updated_at')
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'tagline', 'established_year', 'team_size')
        }),
        ('Content', {
            'fields': ('company_description', 'mission', 'vision', 'company_values')
        }),
        ('Founder Information', {
            'fields': ('founded_by', 'founder_title', 'founder_bio', 'about_image')
        }),
        ('Co-Founder Information', {
            'fields': ('cofounder_name', 'cofounder_title', 'cofounder_bio', 'cofounder_image')
        }),
        ('Contact Information', {
            'fields': ('contact_phone', 'contact_email', 'office_address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')
    

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'tools_used', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'read_status', 'reply_status', 'user', 'created_at')
    list_filter = ('is_read', 'reply_sent', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at', 'updated_at', 'user', 'reply_sent_at')
    fieldsets = (
        ('Contact Information', {
            'fields': ('user', 'name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read', 'reply_sent', 'reply_sent_at')
        }),
        ('Reply', {
            'fields': ('reply',),
            'description': 'Enter your reply message to send to the customer'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def read_status(self, obj):
        return '✅ Read' if obj.is_read else '📭 New'
    read_status.short_description = 'Read Status'
    
    def reply_status(self, obj):
        if obj.reply_sent:
            return '✉️ Replied'
        elif obj.reply:
            return '📝 Draft'
        return '❌ No Reply'
    reply_status.short_description = 'Reply Status'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.user = request.user
        super().save_model(request, obj, form, change)



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon')
    search_fields = ('title',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('is_published', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'author')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(SalesInquiry)
class SalesInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'plan', 'inquiry_type', 'is_read', 'reply_sent', 'created_at')
    list_filter = ('plan', 'inquiry_type', 'is_read', 'reply_sent', 'created_at')
    search_fields = ('name', 'email', 'company')
    readonly_fields = ('created_at', 'reply_sent_at')
    actions = ['mark_as_read', 'send_reply']
    
    fieldsets = (
        ('Inquiry Information', {
            'fields': ('name', 'email', 'phone', 'company', 'company_name', 'contact_person')
        }),
        ('Inquiry Details', {
            'fields': ('plan', 'inquiry_type', 'message', 'is_read')
        }),
        ('Reply', {
            'fields': ('reply', 'reply_sent', 'reply_sent_at'),
            'description': 'Compose a reply to send to the customer'
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        })
    )
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} inquiry(ies) marked as read.")
    
    def send_reply(self, request, queryset):
        """Send replies via email to selected inquiries"""
        updated_count = 0
        for inquiry in queryset:
            if inquiry.reply and not inquiry.reply_sent:
                try:
                    send_mail(
                        subject=f'Re: Your DataZen Analytics Inquiry',
                        message=inquiry.reply,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[inquiry.email],
                        fail_silently=False,
                    )
                    inquiry.reply_sent = True
                    inquiry.reply_sent_at = timezone.now()
                    inquiry.save()
                    updated_count += 1
                except Exception as e:
                    self.message_user(request, f"Error sending email to {inquiry.email}: {str(e)}", level='error')
        
        self.message_user(request, f"Reply sent to {updated_count} customer(s).")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'name_display', 'status_badge', 'source', 'subscribed_date', 'last_email_sent')
    list_filter = ('is_active', 'source', 'subscribed_date', 'last_email_sent')
    search_fields = ('email', 'name')
    readonly_fields = ('subscribed_date', 'updated_at', 'subscriber_stats')
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'name', 'source', 'is_active')
        }),
        ('Activity', {
            'fields': ('subscribed_date', 'last_email_sent', 'admin_notes'),
            'classes': ('collapse',)
        }),
        ('Unsubscribe', {
            'fields': ('unsubscribe_reason',),
            'classes': ('collapse',),
            'description': 'Reason provided if subscriber unsubscribed'
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('subscriber_stats',),
            'classes': ('collapse',),
            'description': 'Overall subscriber statistics'
        })
    )
    
    actions = ['mark_active', 'mark_inactive', 'send_newsletter_email', 'export_subscribers_csv', 'mark_unsubscribed', 'send_reengagement_email']
    
    def name_display(self, obj):
        """Display subscriber name or email"""
        if obj.name:
            return f"{obj.name} ({obj.email})"
        return obj.email
    name_display.short_description = 'Subscriber'
    
    def status_badge(self, obj):
        """Display subscription status with visual badge"""
        if obj.is_active:
            return '✅ Active'
        else:
            return '❌ Inactive'
    status_badge.short_description = 'Status'
    
    def subscriber_stats(self, obj):
        """Display overall subscriber statistics"""
        from django.db.models import Count, Q
        from datetime import timedelta
        from django.utils import timezone
        
        total = Newsletter.objects.count()
        active = Newsletter.objects.filter(is_active=True).count()
        inactive = Newsletter.objects.filter(is_active=False).count()
        
        # Count new subscribers in last 7 days
        one_week_ago = timezone.now() - timedelta(days=7)
        new_this_week = Newsletter.objects.filter(subscribed_date__gte=one_week_ago).count()
        
        # Count by source
        by_source = Newsletter.objects.filter(is_active=True).values('source').annotate(count=Count('id')).order_by('-count')
        source_summary = ', '.join([f"{item['source'].title()}: {item['count']}" for item in by_source])
        
        stats_html = f"""
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h4>📊 Newsletter Statistics</h4>
            <p><strong>Total Subscribers:</strong> {total}</p>
            <p><strong>Active:</strong> <span style="color: green; font-weight: bold;">{active}</span> | 
               <strong>Inactive:</strong> <span style="color: red; font-weight: bold;">{inactive}</span></p>
            <p><strong>New This Week:</strong> {new_this_week}</p>
            <p><strong>Sources:</strong> {source_summary or 'N/A'}</p>
        </div>
        """
        from django.utils.html import mark_safe
        return mark_safe(stats_html)
    subscriber_stats.short_description = 'Subscriber Statistics'
    
    def mark_active(self, request, queryset):
        """Mark selected subscribers as active"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"✅ {updated} subscriber(s) marked as active.")
    mark_active.short_description = "✅ Mark selected as active"
    
    def mark_inactive(self, request, queryset):
        """Mark selected subscribers as inactive"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"❌ {updated} subscriber(s) marked as inactive.")
    mark_inactive.short_description = "❌ Mark selected as inactive"
    
    def send_newsletter_email(self, request, queryset):
        """
        Send a custom newsletter to selected active subscribers
        This uses Django admin's change_list to send batch emails
        """
        active_subs = queryset.filter(is_active=True)
        email_count = 0
        
        # Default newsletter template
        subject = "📧 DataZen Analytics Newsletter"
        message = """Hello,

Thank you for subscribing to DataZen Analytics Newsletter!

We're committed to providing you with:
✨ Latest industry insights
📊 Data analytics tips and tricks
🚀 Product updates and new features
💡 Best practices for data-driven decision making

Stay tuned for valuable content!

Best regards,
DataZen Analytics Team

---
If you wish to unsubscribe, please let us know."""
        
        for subscriber in active_subs:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
                # Update last email sent timestamp
                subscriber.last_email_sent = timezone.now()
                subscriber.save(update_fields=['last_email_sent', 'updated_at'])
                email_count += 1
            except Exception as e:
                self.message_user(request, f"❌ Error sending to {subscriber.email}: {str(e)}", level='error')
        
        self.message_user(request, f"📧 Newsletter sent to {email_count} active subscriber(s).")
    send_newsletter_email.short_description = "📧 Send newsletter to active subscribers"
    
    def export_subscribers_csv(self, request, queryset):
        """Export selected subscribers to CSV file"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="newsletter_subscribers.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Name', 'Status', 'Source', 'Subscribed Date', 'Last Email Sent', 'Notes'])
        
        for subscriber in queryset:
            writer.writerow([
                subscriber.email,
                subscriber.name or '',
                'Active' if subscriber.is_active else 'Inactive',
                subscriber.get_source_display(),
                subscriber.subscribed_date.strftime('%Y-%m-%d %H:%M:%S'),
                subscriber.last_email_sent.strftime('%Y-%m-%d %H:%M:%S') if subscriber.last_email_sent else 'Never',
                subscriber.admin_notes or ''
            ])
        
        return response
    export_subscribers_csv.short_description = "📥 Export selected to CSV"
    
    def mark_unsubscribed(self, request, queryset):
        """Mark subscribers as unsubscribed (inactive)"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"🚫 {updated} subscriber(s) marked as unsubscribed.")
    mark_unsubscribed.short_description = "🚫 Mark as unsubscribed"
    
    def send_reengagement_email(self, request, queryset):
        """Send a reengagement email to inactive subscribers"""
        inactive_subs = queryset.filter(is_active=False)
        email_count = 0
        
        subject = "We miss you! 👋 Come back to DataZen Analytics Newsletter"
        message = """Hello,

We noticed you haven't received our newsletter recently, and we'd love to have you back!

Our newsletter has been delivering valuable content:
📊 Exclusive analytics insights
💡 Industry best practices
🎯 DataZen product tips and features
🔥 Success stories from our customers

Would you like to reactivate your subscription? Just reply to this email or visit our newsletter preferences.

Best regards,
DataZen Analytics Team"""
        
        for subscriber in inactive_subs:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
                email_count += 1
            except Exception as e:
                self.message_user(request, f"❌ Error sending to {subscriber.email}: {str(e)}", level='error')
        
        self.message_user(request, f"💌 Reengagement email sent to {email_count} inactive subscriber(s).")
    send_reengagement_email.short_description = "💌 Send reengagement email to inactive"
    
    def get_queryset(self, request):
        """Only allow staff to manage newsletter"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Non-superuser staff can only view, not edit
            pass
        return qs
