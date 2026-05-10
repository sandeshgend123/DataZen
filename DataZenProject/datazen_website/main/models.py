from django.db import models
from django.contrib.auth.models import User


class About(models.Model):
    """
    About page content - Singleton model (only one instance expected)
    """
    company_name = models.CharField(max_length=200, default='DataZen Analytics')
    tagline = models.CharField(max_length=500, blank=True)
    company_description = models.TextField(help_text="Main description about the company")
    mission = models.TextField(help_text="Company mission statement")
    vision = models.TextField(help_text="Company vision statement")
    established_year = models.IntegerField(default=2019)
    team_size = models.CharField(max_length=100, default='15+')
    company_values = models.TextField(blank=True, help_text="Core values (one per line)")
    
    # Founder Information
    founded_by = models.CharField(max_length=200, blank=True, help_text="Founder's name")
    founder_title = models.CharField(max_length=200, default='Founder & CEO', blank=True, null=True, help_text="Founder's title")
    founder_bio = models.TextField(blank=True, null=True, help_text="Founder's biography")
    about_image = models.ImageField(upload_to='about/', blank=True, null=True, help_text="Founder's photo")
    
    # Co-Founder Information
    cofounder_name = models.CharField(max_length=200, blank=True, null=True, help_text="Co-Founder name")
    cofounder_title = models.CharField(max_length=200, default='Co-Founder', blank=True, null=True)
    cofounder_bio = models.TextField(blank=True, null=True, help_text="Co-Founder biography")
    cofounder_image = models.ImageField(upload_to='about/', blank=True, null=True)
    
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    office_address = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return f"About - {self.company_name}"

    def save(self, *args, **kwargs):
        # Ensure only one About instance exists
        if not self.pk and About.objects.exists():
            raise ValueError("Only one About page instance is allowed")
        super().save(*args, **kwargs)


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tools_used = models.CharField(max_length=200)
    image = models.ImageField(upload_to='projects/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_submissions')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    reply = models.TextField(blank=True, null=True, help_text="Reply message to send to the customer")
    reply_sent = models.BooleanField(default=False)
    reply_sent_at = models.DateTimeField(blank=True, null=True)
    reply_seen = models.BooleanField(default=False, help_text="Has the user seen the reply?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.name} - {self.email}"


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, default='⚙️')

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SalesInquiry(models.Model):
    """
    Model to store sales inquiries from customers interested in plans
    """
    PLAN_CHOICES = [
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    
    INQUIRY_TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('email', 'Email Inquiry'),
        ('contact_form', 'Contact Form')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_inquiries', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='starter')
    message = models.TextField(blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES, default='contact_form')
    is_read = models.BooleanField(default=False)
    reply = models.TextField(blank=True, null=True, help_text="Reply message to send to the customer")
    reply_sent = models.BooleanField(default=False)
    reply_sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sales Inquiry"
        verbose_name_plural = "Sales Inquiries"
    
    def __str__(self):
        display_name = self.company_name or self.name
        return f"{display_name} - {self.plan.capitalize()} Plan"


class Newsletter(models.Model):
    """
    Newsletter subscription model with enhanced tracking
    """
    SOURCE_CHOICES = [
        ('blog', 'Blog Page'),
        ('user_login', 'User Login Page'),
        ('homepage', 'Homepage'),
        ('manual', 'Manual Entry'),
        ('import', 'Imported'),
        ('contact_form', 'Contact Form'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='newsletter_subscription', help_text="Link to user account (if subscribed as logged-in user)")
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True, null=True, help_text="Subscriber name (optional)")
    subscribed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Is this subscriber active?")
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='other', help_text="How did they subscribe?")
    last_email_sent = models.DateTimeField(blank=True, null=True, help_text="When was the last newsletter sent to this subscriber?")
    admin_notes = models.TextField(blank=True, null=True, help_text="Internal admin notes about this subscriber")
    unsubscribe_reason = models.TextField(blank=True, null=True, help_text="Reason for unsubscribing")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-subscribed_date']
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        indexes = [
            models.Index(fields=['is_active', '-subscribed_date']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        status = '✅ Active' if self.is_active else '❌ Inactive'
        name_display = f" ({self.name})" if self.name else ""
        return f"{self.email}{name_display} - {status}"
