from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tasks"
    ) 

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_tasks"
    ) 

    deadline = models.DateField() 
    created_at = models.DateTimeField(auto_now_add=True)

    # is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    @property
    def days_remaining(self):
        today = timezone.now().date()
        return (self.deadline - today).days

    @property
    def is_completed(self):
        return hasattr(self, "submission")

    @property
    def is_overdue(self):
        if self.is_completed:
            return False
        return self.deadline < timezone.localdate()



    @property
    def status_message(self):
        today = timezone.localdate()

        # Completed
        if hasattr(self, "submission"):
            submitted_date = self.submission.submitted_at.date()
            days = (submitted_date - self.deadline).days

            if days <= 0:
                return f"Submitted on {submitted_date.strftime('%d %B %Y')}"
            else:
                return f"Submitted {days} days late ({submitted_date.strftime('%d %B %Y')})"

        # Not submitted yet
        delta = (self.deadline - today).days

        if delta > 0:
            return f"{delta} days left until deadline"
        elif delta == 0:
            return "Due today"
        else:
            return f"Overdue by {abs(delta)} days"

class TaskSubmission(models.Model):
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name="submission"
    )

    comment = models.TextField(blank=True)

    file = models.FileField(
        upload_to="uploads/task_submissions/",
        blank=True,
        null=True
    )
    original_name = models.CharField(max_length=255, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.task.title}"
    
    @property
    def is_late(self):
        return self.submitted_at > self.task.deadline
    
    def save(self, *args, **kwargs):
        if not self.original_name and self.file:
            self.original_name = self.file.name
        super().save(*args, **kwargs)
    
class TaskAttachment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to='uploads/task_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Attachment for {self.task.title}"
    
    def save(self, *args, **kwargs):
        if not self.original_name and self.file:
            self.original_name = self.file.name
        super().save(*args, **kwargs)