from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from .models import Project, Contact, Service, BlogPost, About, SalesInquiry


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('services')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                messages.error(request, 'Admin users must use the admin login panel.')
                return redirect('user_login')
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_url = request.GET.get('next', 'services')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    context = {'page_title': 'User Login'}
    return render(request, 'main/user_login.html', context)


def admin_login(request):
    """Admin login view"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if not user.is_staff:
                messages.error(request, 'User accounts must use the user login panel.')
                return redirect('admin_login')
            login(request, user)
            messages.success(request, f'Welcome back, Admin {username}!')
            return redirect('admin:index')
        else:
            messages.error(request, 'Invalid admin credentials.')
    
    context = {'page_title': 'Admin Login'}
    return render(request, 'main/admin_login.html', context)


def user_logout(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='user_login')
@login_required(login_url='user_login')
def user_profile(request):
    """User profile page"""
    user = request.user
    
    # If admin user, redirect to admin profile
    if user.is_staff:
        return redirect('admin_profile')
    
    if request.method == 'POST':
        action = request.POST.get('action', 'update_profile')
        
        if action == 'update_profile':
            # Update profile information
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            
            # Validate email uniqueness
            if email != user.email and User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered.')
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('user_profile')
        
        elif action == 'toggle_newsletter':
            # Toggle newsletter subscription
            from .models import Newsletter
            try:
                newsletter_sub = Newsletter.objects.get(user=user)
                newsletter_sub.is_active = not newsletter_sub.is_active
                newsletter_sub.save()
                status = 'enabled' if newsletter_sub.is_active else 'disabled'
                messages.success(request, f'Newsletter subscription {status}!')
            except Newsletter.DoesNotExist:
                # Create new subscription if it doesn't exist
                Newsletter.objects.create(
                    user=user,
                    email=user.email,
                    name=f"{user.first_name} {user.last_name}".strip() or user.username,
                    is_active=True,
                    source='user_profile'
                )
                messages.success(request, 'You have been subscribed to our newsletter!')
            return redirect('user_profile')
    
    # Get newsletter subscription status
    from .models import Newsletter
    try:
        newsletter_sub = Newsletter.objects.get(user=user)
    except Newsletter.DoesNotExist:
        newsletter_sub = None
    
    context = {
        'page_title': 'User Profile',
        'user': user,
        'newsletter_subscription': newsletter_sub
    }
    return render(request, 'main/user_profile.html', context)


@login_required(login_url='user_login')
def user_notifications(request):
    """User notifications page - shows replies to their contact submissions"""
    user = request.user
    
    # If admin user, redirect to admin profile
    if user.is_staff:
        return redirect('admin_profile')
    
    # Get all contact submissions from this user
    user_contacts = Contact.objects.filter(user=user).order_by('-created_at')
    
    # Get contacts with replies
    contacts_with_replies = user_contacts.filter(reply_sent=True)
    unread_replies = user_contacts.filter(reply_sent=True, reply_seen=False)
    
    # Mark all as seen when user views the notification page
    unread_replies.update(reply_seen=True)
    
    context = {
        'page_title': 'Notifications',
        'user': user,
        'contacts_with_replies': contacts_with_replies,
        'unread_count': 0  # Reset count after viewing
    }
    return render(request, 'main/user_notifications.html', context)


@login_required(login_url='admin_login')
def mark_inquiry_read(request, inquiry_id):
    """Mark a sales inquiry as read"""
    if not request.user.is_staff:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Permission denied'})
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('user_profile')
    
    try:
        inquiry = get_object_or_404(SalesInquiry, id=inquiry_id)
        inquiry.is_read = True
        inquiry.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        messages.success(request, 'Inquiry marked as read.')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': str(e)})
        messages.error(request, 'Error marking inquiry as read.')
    
    return redirect('admin_profile')


@login_required(login_url='admin_login')
def admin_profile(request):
    """Admin profile page"""
    user = request.user
    
    # Check if user is admin
    if not user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('user_profile')
    
    # Get all sales inquiries
    inquiries = SalesInquiry.objects.all()
    
    if request.method == 'POST':
        # Update admin profile information
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        
        # Validate email uniqueness
        if email != user.email and User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, 'Admin profile updated successfully!')
            return redirect('admin_profile')
    
    context = {
        'page_title': 'Admin Dashboard',
        'user': user,
        'inquiries': inquiries
    }
    return render(request, 'main/admin_profile.html', context)


def select_plan(request):
    """Select plan - requires login"""
    if not request.user.is_authenticated:
        return redirect(f"{reverse('user_login')}?next=select_plan")
    
    plan = request.GET.get('plan', None)
    
    if request.method == 'POST':
        # Create sales inquiry
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        company = request.POST.get('company', '')
        message = request.POST.get('message', '')
        inquiry_type = request.POST.get('inquiry_type', 'contact_form')
        
        SalesInquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            company=company,
            plan=plan or 'starter',
            message=message,
            inquiry_type=inquiry_type
        )
        
        messages.success(request, 'Thank you for your inquiry! Our sales team will contact you soon.')
        return redirect('services')
    
    context = {
        'plan': plan,
        'page_title': 'Select Plan',
        'plans': {
            'starter': {'name': 'Starter', 'price': '$999/month'},
            'professional': {'name': 'Professional', 'price': '$2,999/month'},
            'enterprise': {'name': 'Enterprise', 'price': '$9,999/month'},
        }
    }
    return render(request, 'main/select_plan.html', context)


def signup(request):
    """User signup/registration view"""
    if request.user.is_authenticated:
        return redirect('services')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not username or not email or not password:
            messages.error(request, 'Please fill in all fields.')
            return redirect('signup')
        
        if len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters long.')
            return redirect('signup')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return redirect('signup')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('signup')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('user_login')
    
    context = {'page_title': 'Sign Up'}
    return render(request, 'main/signup.html', context)


def forgot_password(request):
    """Forgot password view - send reset email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            # Generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset link
            reset_link = f"{request.build_absolute_uri('/password-reset-confirm/')}{uid}/{token}/"
            
            # Send email
            send_mail(
                'DataZen Analytics - Password Reset',
                f'Click the link to reset your password:\n\n{reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('user_login')
        except User.DoesNotExist:
            messages.error(request, 'Email not found in our system.')
        except Exception as e:
            messages.error(request, f'Error sending email: {str(e)}')
    
    context = {'page_title': 'Forgot Password'}
    return render(request, 'main/forgot_password.html', context)


def password_reset_confirm(request, uidb64, token):
    """Password reset confirmation view"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            if not password or not password_confirm:
                messages.error(request, 'Please fill in all fields.')
                return redirect(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
            
            if len(password) < 6:
                messages.error(request, 'Password must be at least 6 characters long.')
                return redirect(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
            
            if password != password_confirm:
                messages.error(request, 'Passwords do not match.')
                return redirect(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
            
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been reset successfully. You can now log in.')
            return redirect('user_login')
        
        context = {
            'page_title': 'Reset Password',
            'uidb64': uidb64,
            'token': token,
            'valid_link': True
        }
        return render(request, 'main/password_reset_confirm.html', context)
    else:
        context = {
            'page_title': 'Reset Password',
            'valid_link': False
        }
        return render(request, 'main/password_reset_confirm.html', context)



def home(request):
    projects = Project.objects.all()[:3]  # Show 3 latest projects
    services = Service.objects.all()
    context = {
        'projects': projects,
        'services': services,
        'page_title': 'Home'
    }
    return render(request, 'main/home.html', context)


def about(request):
    about = About.objects.first()
    context = {
        'page_title': 'About Us',
        'about': about
    }
    return render(request, 'main/about.html', context)


def services(request):
    services = Service.objects.all()
    context = {
        'services': services,
        'page_title': 'Services'
    }
    return render(request, 'main/services.html', context)


def portfolio(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
        'page_title': 'Portfolio'
    }
    return render(request, 'main/portfolio.html', context)


def contact(request):
    # Check if user is admin/staff
    is_admin = request.user.is_authenticated and request.user.is_staff
    
    if is_admin:
        # Admin view: show all contact submissions
        contacts = Contact.objects.all().order_by('-created_at')
        unread_count = Contact.objects.filter(is_read=False).count()
        context = {
            'page_title': 'Contact Us',
            'is_admin': True,
            'contacts': contacts,
            'unread_count': unread_count
        }
    else:
        # User view: show contact form
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone', '')
            message = request.POST.get('message')

            if name and email and message:
                # Save with user if logged in
                user = request.user if request.user.is_authenticated else None
                Contact.objects.create(
                    user=user,
                    name=name,
                    email=email,
                    phone=phone,
                    message=message
                )
                messages.success(request, 'Thank you! Your message has been received. We will contact you soon.')
                return redirect('contact')
            else:
                messages.error(request, 'Please fill in all fields.')

        context = {
            'page_title': 'Contact Us',
            'is_admin': False
        }
    
    return render(request, 'main/contact.html', context)


@login_required(login_url='admin_login')
def mark_contact_read(request, contact_id):
    """Mark a contact submission as read"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('contact')
    
    try:
        contact = get_object_or_404(Contact, id=contact_id)
        contact.is_read = True
        contact.save()
        messages.success(request, 'Contact marked as read.')
    except Exception as e:
        messages.error(request, f'Error marking contact as read: {str(e)}')
    
    return redirect('contact')


@login_required(login_url='admin_login')
def send_contact_reply(request, contact_id):
    """Send reply to contact submission"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('contact')
    
    try:
        contact = get_object_or_404(Contact, id=contact_id)
        
        if request.method == 'POST':
            reply_message = request.POST.get('reply', '')
            
            if reply_message:
                contact.reply = reply_message
                contact.is_read = True
                contact.reply_sent = True
                contact.reply_seen = False  # Mark as unseen so user gets notification
                contact.reply_sent_at = datetime.now()
                contact.save()
                
                # Send email
                try:
                    subject = f"Re: Your contact message - DataZen Analytics"
                    email_body = f"""Dear {contact.name},

Thank you for reaching out to DataZen Analytics. Here is our response to your message:

{reply_message}

Best regards,
DataZen Analytics Team
info@datazen.com
"""
                    send_mail(
                        subject,
                        email_body,
                        settings.DEFAULT_FROM_EMAIL,
                        [contact.email],
                        fail_silently=False,
                    )
                    messages.success(request, f'Reply sent to {contact.email}')
                except Exception as email_error:
                    messages.warning(request, f'Reply saved but email sending failed: {str(email_error)}')
            else:
                messages.error(request, 'Please enter a reply message.')
        
        return redirect('contact')
    except Exception as e:
        messages.error(request, f'Error sending reply: {str(e)}')
        return redirect('contact')


@login_required(login_url='admin_login')
def delete_contact(request, contact_id):
    """Delete a contact submission"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('contact')
    
    try:
        contact = get_object_or_404(Contact, id=contact_id)
        contact_name = contact.name
        contact.delete()
        messages.success(request, f'Contact from {contact_name} has been deleted.')
    except Exception as e:
        messages.error(request, f'Error deleting contact: {str(e)}')
    
    return redirect('contact')





def blog(request):
    posts = BlogPost.objects.filter(is_published=True)
    
    # Get subscriber data if user is admin/staff
    from .models import Newsletter
    subscribers = None
    is_admin = False
    
    if request.user.is_authenticated and request.user.is_staff:
        try:
            # Get all active subscribers for admin view, ordered by newest first
            subscribers = list(Newsletter.objects.filter(is_active=True).order_by('-subscribed_date'))
            is_admin = True
        except Exception as e:
            print(f"Error fetching subscribers: {e}")
            subscribers = []
            is_admin = True
    
    context = {
        'posts': posts,
        'page_title': 'Blog',
        'subscribers': subscribers,
        'is_admin': is_admin,
        'user': request.user,
    }
    return render(request, 'main/blog.html', context)


def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    context = {
        'post': post,
        'page_title': post.title
    }
    return render(request, 'main/blog_detail.html', context)


def subscribe_newsletter(request):
    """Handle newsletter subscription with AJAX support"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        
        # Check if this is an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if email:
            from .models import Newsletter
            
            try:
                # Determine subscription source from referrer
                referer = request.META.get('HTTP_REFERER', '')
                if 'blog' in referer:
                    source = 'blog'
                elif 'user_login' in referer or 'login' in referer:
                    source = 'user_login'
                elif 'contact' in referer:
                    source = 'contact_form'
                else:
                    source = 'homepage'
                
                # Try to create a new subscriber
                subscriber, created = Newsletter.objects.get_or_create(
                    email=email,
                    defaults={
                        'is_active': True,
                        'name': name or email.split('@')[0],
                        'source': source,
                        'user': request.user if request.user.is_authenticated else None
                    }
                )
                
                if created:
                    # Send welcome email
                    try:
                        send_mail(
                            subject='Welcome to DataZen Analytics Newsletter',
                            message=f"""Dear Subscriber,

Thank you for subscribing to DataZen Analytics Newsletter! 

We'll send you the latest analytics insights, tips, and industry news directly to your inbox.

Best regards,
DataZen Analytics Team
info@datazen.com""",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[email],
                            fail_silently=True,
                        )
                    except:
                        pass
                    
                    if is_ajax:
                        return JsonResponse({
                            'success': True,
                            'message': '✓ Welcome! You\'ve been subscribed to our newsletter.'
                        })
                    else:
                        messages.success(request, '✓ Welcome! You\'ve been subscribed to our newsletter.')
                else:
                    if subscriber.is_active:
                        if is_ajax:
                            return JsonResponse({
                                'success': False,
                                'message': '✓ You are already subscribed to our newsletter!'
                            })
                        else:
                            messages.info(request, 'You are already subscribed to our newsletter!')
                            return redirect(request.META.get('HTTP_REFERER', 'blog'))
                    else:
                        subscriber.is_active = True
                        subscriber.save(update_fields=['is_active', 'updated_at'])
                        if is_ajax:
                            return JsonResponse({
                                'success': True,
                                'message': '✓ You have been reactivated for our newsletter.'
                            })
                        else:
                            messages.success(request, 'You have been reactivated for our newsletter.')
            except Exception as e:
                error_msg = f'An error occurred: {str(e)}'
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'message': f'❌ {error_msg}'
                    })
                else:
                    messages.error(request, error_msg)
        else:
            error_msg = 'Please enter a valid email address.'
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'message': f'❌ {error_msg}'
                })
            else:
                messages.error(request, error_msg)
    
    # For AJAX POST requests, return JSON (should have returned above)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': '❌ Invalid request'})
    
    # For non-AJAX POST, redirect to referring page or blog
    return redirect(request.META.get('HTTP_REFERER', 'blog'))


@login_required(login_url='user_login')
def sales_department(request, plan=None):
    """Sales department page - shows inquiries for admins, form for users"""
    from django.contrib import messages
    from django.core.mail import send_mail
    from django.conf import settings
    from .models import SalesInquiry
    
    user = request.user
    form_submitted = False
    email_sent = False
    
    # Check if user is admin
    if user.is_staff:
        # Admin view - show sales inquiries
        
        # Handle send email action from admin
        if request.method == 'POST' and 'send_email' in request.POST:
            inquiry_id = request.POST.get('inquiry_id')
            try:
                inquiry = SalesInquiry.objects.get(id=inquiry_id)
                
                # Send confirmation email to customer
                send_mail(
                    subject='We Received Your Inquiry - DataZen Analytics',
                    message=f"Thank you {inquiry.contact_person},\n\nWe have received your inquiry for {inquiry.plan} plan. Our sales team will review your requirements and contact you shortly.\n\nBest Regards,\nDataZen Analytics Sales Team",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[inquiry.email],
                    fail_silently=False,
                )
                messages.success(request, f'Email sent to {inquiry.email}')
            except SalesInquiry.DoesNotExist:
                messages.error(request, 'Inquiry not found')
            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}')
        
        inquiries = SalesInquiry.objects.all()
        context = {
            'page_title': 'Sales Department',
            'user': user,
            'inquiries': inquiries,
            'is_admin': True,
        }
        return render(request, 'main/sales_department.html', context)
    
    # Regular user view - show sales form
    if request.method == 'POST':
        # Handle quick contact from "Get in Touch" section
        if request.POST.get('quick_contact') == 'true':
            try:
                # Send email to admin about the quick contact
                send_mail(
                    subject='Quick Contact: Sales Inquiry from DataZen Website',
                    message=f"User {user.username} ({user.email}) clicked the 'Send Email' button from the 'Get in Touch with Our Sales Team' section.\n\nThey are interested in discussing analytics solutions.\n\nPlease reach out to them soon.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                
                # Confirmation email to user
                send_mail(
                    subject='We Received Your Message - DataZen Analytics',
                    message=f"Hello {user.first_name or user.username},\n\nThank you for reaching out to our sales team! We have received your inquiry and will get back to you shortly with analytics solutions tailored to your needs.\n\nBest Regards,\nDataZen Analytics Sales Team",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                
                messages.success(request, 'Thank you! We have received your message. Our sales team will contact you soon.')
                email_sent = True
            except Exception as e:
                messages.warning(request, f'Message sent but email notification failed: {str(e)}')
        else:
            # Handle regular inquiry form submission
            company_name = request.POST.get('company_name')
            contact_person = request.POST.get('contact_person')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message_text = request.POST.get('message')
            send_email = request.POST.get('send_email') == 'on'
            
            # Validate required fields
            if company_name and contact_person and email and phone and plan:
                # Create the inquiry
                inquiry = SalesInquiry.objects.create(
                    user=user,
                    plan=plan,
                    company_name=company_name,
                    contact_person=contact_person,
                    email=email,
                    phone=phone,
                    message=message_text,
                    inquiry_type='contact_form'
                )
                
                # Send email notification to admin if user requests
                if send_email:
                    try:
                        # Email to admin
                        send_mail(
                            subject=f'New Sales Inquiry: {company_name}',
                            message=f"New Sales Inquiry\n\nCompany: {company_name}\nContact: {contact_person}\nEmail: {email}\nPhone: {phone}\nPlan: {inquiry.plan}\n\nMessage:\n{message_text}",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[settings.DEFAULT_FROM_EMAIL],
                            fail_silently=False,
                        )
                        
                        # Confirmation email to user
                        send_mail(
                            subject='We Received Your Inquiry - DataZen Analytics',
                            message=f"Thank you {contact_person},\n\nWe have received your inquiry for {inquiry.plan} plan. Our sales team will review your requirements and contact you shortly.\n\nBest Regards,\nDataZen Analytics Sales Team",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[email],
                            fail_silently=False,
                        )
                        
                        messages.success(request, 'Your inquiry has been submitted and confirmation email sent!')
                        email_sent = True
                    except Exception as e:
                        messages.warning(request, f'Inquiry submitted but email sending failed: {str(e)}')
                else:
                    messages.success(request, 'Your inquiry has been submitted successfully! Our sales team will contact you soon.')
                
                form_submitted = True
            else:
                messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'page_title': 'Sales Department',
        'user': user,
        'plan': plan,
        'form_submitted': form_submitted,
        'email_sent': email_sent,
        'is_admin': False,
    }
    return render(request, 'main/sales_department.html', context)
