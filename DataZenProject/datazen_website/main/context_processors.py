from .models import Contact


def user_notifications(request):
    """Add unread notifications count to context for all templates"""
    context = {
        'unread_notifications': 0
    }
    
    if request.user.is_authenticated and not request.user.is_staff:
        # Count unread replies for regular users
        unread_count = Contact.objects.filter(
            user=request.user,
            reply_sent=True,
            reply_seen=False
        ).count()
        context['unread_notifications'] = unread_count
    
    return context
