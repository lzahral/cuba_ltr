from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import  DetailView
from django.db.models import Q
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse
from django.views.generic import CreateView
from django.core.exceptions import PermissionDenied
from .models import *
from .forms import *
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Task



class TaskUpdateView( UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks")

    def get_queryset(self):
        # فقط کسی که تسک رو ساخته می‌تونه ویرایش کنه
        return Task.objects.filter(creator=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context


    def form_valid(self, form):
        task = form.save()

        # -------------------------
        # 1️⃣ فایل‌های قبلی که کاربر نگه داشته
        # -------------------------
        kept_ids = self.request.POST.getlist("existing_attachments")
        kept_ids = list(map(int, kept_ids))

        # -------------------------
        # 2️⃣ حذف فایل‌هایی که دیگه نیستن
        # -------------------------
        TaskAttachment.objects.filter(task=task)\
            .exclude(id__in=kept_ids)\
            .delete()

        # -------------------------
        # 3️⃣ اضافه کردن فایل‌های جدید
        # -------------------------
        new_files = self.request.FILES.getlist("attachments")
        for f in new_files:
            TaskAttachment.objects.create(
                task=task,
                file=f
            )

        return redirect(self.success_url)
    

class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "item"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("attachments")
    
class TodoTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/todo_tasks.html"
    context_object_name = "data"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(
             Q(assignee=user)
        ).select_related(
            "creator", "assignee"
        ).order_by("-deadline")
User = get_user_model()

class AssignedTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/assigned_tasks.html"
    context_object_name = "data"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(
        creator=user
        )
User = get_user_model()

def index(request):
    return render(request, "tasks/tasks.html")


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks")
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["users"] = User.objects.all()
            return context

    def form_valid(self, form):
        task = form.save(commit=False)
        task.creator = self.request.user

        task.save()

        files = self.request.FILES.getlist("attachments")
        for f in files:
            TaskAttachment.objects.create(
                task=task,
                file=f
            )

        return redirect(self.success_url)



class TaskDelete(View):

    def delete(self, request, pk):
        Task.objects.get(id=pk).delete()
        return JsonResponse({'message': 'successful'}, status=200)
    
class TaskSubmissionCreateView(CreateView):
    model = TaskSubmission
    form_class = TaskSubmissionForm
    template_name = "tasks/form.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=kwargs['task_id'])

        # 🔒 فقط کسی که تسک بهش اساین شده
        if self.task.assignee != request.user:
            raise PermissionDenied

        # ⛔ جلوگیری از سابمیت مجدد
        if hasattr(self.task, 'submission'):
            raise PermissionDenied("Task already submitted")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        submission = form.save(commit=False)
        submission.task = self.task
        submission.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_detail', args=[self.task.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.task.title
        return context
