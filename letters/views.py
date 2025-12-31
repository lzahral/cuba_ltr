from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import View, DetailView
from django.db.models import Q
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Letter, LetterAttachment
from .forms import LetterCreateForm, ReplyLetterForm

User = get_user_model()


class DeleteLetterView(LoginRequiredMixin, View):
    def post(self, request, pk):
        letter = get_object_or_404(Letter, pk=pk)
        if letter.recipient == request.user:
            letter.is_deleted_recipient = not letter.is_deleted_recipient
            letter.save()
        elif letter.sender == request.user:
            letter.is_deleted_sender = not letter.is_deleted_sender
            letter.save()
        return redirect("letters")  

class LetterDetailView(DetailView):
    model = Letter
    template_name = "letters/detail.html"
    context_object_name = "letter"

    def get_queryset(self):
        # فقط برای بهینه‌سازی (اتچمنت‌ها)
        return super().get_queryset().prefetch_related("attachments")
    
class Letters(TemplateView):
    template_name = "letters/letters.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        letters = Letter.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).order_by("-created_at")

        categorized = {
            "inbox": [],
            "sent": [],
            # "draft": [],
            "trash": [],
        }

        for letter in letters:
            # inbox
            if letter.recipient == user and not letter.is_draft and not letter.is_deleted_recipient:
                categorized["inbox"].append(letter)

            # sent
            elif letter.sender == user and not letter.is_draft and not letter.is_deleted_sender:
                categorized["sent"].append(letter)

            # draft
            # elif letter.sender == user and letter.is_draft:
            #     categorized["draft"].append(letter)
            #     print('hio')

            # trash
            elif (
                (letter.sender == user and letter.is_deleted_sender) or
                (letter.recipient == user and letter.is_deleted_recipient)
            ):
                categorized["trash"].append(letter)
        print(categorized)
        context["categories"] = categorized
        
        return context

class LetterCreateView(CreateView):
    model = Letter
    form_class = LetterCreateForm
    template_name = "letters/letter_form.html"
    success_url = reverse_lazy("letters")
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["users"] = User.objects.all()
            return context
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['action'] = self.request.POST.get('action', 'send')
        return kwargs
    def form_valid(self, form):
        letter = form.save(commit=False)
        letter.sender = self.request.user

        action = self.request.POST.get("action")

        if action == "draft":
            letter.is_draft = True
            letter.sent_at = None  # پیش‌نویس هنوز ارسال نشده
        else:
            letter.is_draft = False
            letter.sent_at = timezone.now()  # زمان واقعی ارسال


        letter.save()

        files = self.request.FILES.getlist("attachments")
        for f in files:
            LetterAttachment.objects.create(
                letter=letter,
                file=f
            )

        return redirect(self.success_url)


class ReplyLetterView(LoginRequiredMixin, FormView):
    template_name = "letters/letter_form.html"
    form_class = ReplyLetterForm
    success_url = reverse_lazy("letters")

    def dispatch(self, request, *args, **kwargs):
        self.original_letter = get_object_or_404(Letter, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        original = self.original_letter
        user = self.request.user
        subject = original.subject
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"
        # if user not in [original.sender, original.recipient]:
        #     raise PermissionDenied

        recipient = (
            original.recipient
            if original.sender == user
            else original.sender
        )

        letter = Letter.objects.create(
            sender=user,
            recipient=recipient,
            subject=subject,
            body=form.cleaned_data["body"],
            parent=original
        )

        files = self.request.FILES.getlist("attachments")
        for f in files:
            LetterAttachment.objects.create(
                letter=letter,
                file=f
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["letter"] = self.original_letter
        return context