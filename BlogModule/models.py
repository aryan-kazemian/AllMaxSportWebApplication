from django.db import models

STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
]

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    tags = models.ManyToManyField('Tag', blank=True)
    featured_image = models.ImageField(upload_to='blog/featured_images/', null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    seo_score = models.PositiveIntegerField(default=0)
    seo_score_color = models.CharField(max_length=20, default='text-gray-500')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class SEOStatus(models.Model):
    STATUS_CHOICES = [
        ('ok', 'OK'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]

    blog = models.OneToOneField(Blog, on_delete=models.CASCADE, related_name='seo_status')

    title_length_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    title_length_message = models.TextField()

    content_length_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    content_length_message = models.TextField()

    keyword_density_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    keyword_density_message = models.TextField()

    meta_description_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    meta_description_message = models.TextField()

    headings_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    headings_message = models.TextField()

    images_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    images_message = models.TextField()

    internal_links_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    internal_links_message = models.TextField()

    def __str__(self):
        return f"SEO Status for {self.blog.title}"
