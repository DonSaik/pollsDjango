from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import EmailForm

# Create your views here.


@permission_required('user.can_send_email')
def email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            send_mail(
                form.data['subject'],
                form.data['message'],
                settings.EMAIL_HOST_USER,
                [form.data['address']],
                fail_silently=False,
            )
            return HttpResponse("Sent")
    else:
        form = EmailForm()
    return render(request, 'pollEmail/email.html', {'form': form})