from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

option = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Modul(models.Model):

    class ModulObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    option = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    excerpt = models.TextField(null=True, blank=True)
    content = models.TextField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    slug = models.SlugField(blank=True, editable=False)
    published = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=option, default='published')
    objects = models.Manager()  # default
    modulobjects = ModulObjects()  # custom

    class Meta:
        ordering = ('-published',)
        permissions = [
            ("can_view_frontend_modul", "Can view FrontEnd modules"),
            ("can_view_backend_modul", "Can view BackEnd modules"),
            ("can_view_qa_modul", "Can view QA modules"),
            ("can_view_ui/ux_modul", "Can view UI/UX modules"),
        ]

    def publish(self):
        if self.status == 'published':
            self.published = timezone.now()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.publish()
        super(Modul, self).save(*args, **kwargs)

    def __str__(self):
        return "{}. {} | {}".format(self.id, self.title, dict(option)[self.status])


class Post(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset()

    option = (
        ('sent', 'Sent'),
        ('pending', 'Pending'),
    )

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=255)
    invoice = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=option, default='sent')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    postobjects = PostObjects()

    class Meta:
        ordering = ('-date',)

    def sent(self):
        if self.type == 'sent':
            self.date = timezone.now()

    def save(self, *args, **kwargs):
        self.sent()
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return "{}. {} | {}".format(self.id, self.author, self.category)
