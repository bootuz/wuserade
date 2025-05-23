from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone


class Theme(models.Model):
    title = models.CharField(max_length=150, verbose_name='Title')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Theme'
        verbose_name_plural = 'Themes'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('poem', args=[self.slug])


class Author(models.Model):
    name = models.CharField(max_length=150, verbose_name='Name')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    bio = models.TextField(blank=True, verbose_name='Bio')
    photo = models.ImageField(upload_to='photos', blank=True, verbose_name='Photo')
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(editable=False, verbose_name='Date published')
    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def update_views(self):
        self.views += 1
        self.save()

    def get_absolute_url(self):
        return reverse('author', args=[self.slug])


class Poem(models.Model):
    LOVE = 'love'
    HOMELAND = 'homeland'
    ADIGA = 'adiga'
    LIFE = 'life'
    FRIENDSHIP = 'friendship'
    NATURE = 'nature'
    KID = 'kid'
    ANIMAL = 'animal'
    SEASONS = 'seasons'
    WAR = 'war'
    PARENTS = 'parents'
    HUMOR = 'humor'

    THEMES = [
        (LOVE, 'Лъагъуныгъэ'),
        (HOMELAND, 'Хэку'),
        (ADIGA, 'Адыгэ'),
        (LIFE, 'Гъащӏэ'),
        (FRIENDSHIP, 'Ныбжьэгъугъэ'),
        (NATURE, 'Щӏыуэпс'),
        (KID, 'Сабий'),
        (ANIMAL, 'Псэущхьэ'),
        (SEASONS, 'Лъэхъэнэ'),
        (WAR, 'Зауэ'),
        (PARENTS, 'Адэ-Анэ'),
        (HUMOR, 'Гушыӏэ'),
    ]

    title = models.CharField(max_length=250, verbose_name='Title', db_index=True)
    slug = models.SlugField(unique=True, verbose_name='Slug')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Author', related_name='poems')
    text = models.TextField(verbose_name='Poem\'s text')
    theme = models.CharField(max_length=100, choices=THEMES, blank=True)
    category = models.ForeignKey(Theme, null=True, on_delete=models.CASCADE, verbose_name='Category', related_name='poems')
    views = models.PositiveIntegerField(default=0, verbose_name='Views')
    likes = models.PositiveIntegerField(default=0, verbose_name='Likes', editable=False)
    created_at = models.DateTimeField(editable=False, verbose_name='Date published', db_index=True)
    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Poem'
        verbose_name_plural = 'Poems'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def update_views(self):
        self.views += 1
        self.save()

    def get_absolute_url(self):
        return reverse('poem', args=[self.slug])


class FeaturedPoemManager(models.Manager):
    def get_for_date(self, date):
        """Get featured poem for a specific date, or None if not exists"""
        return self.filter(featured_date=date).select_related('poem__author', 'poem__category').first()
    
    def get_latest(self):
        """Get the most recently featured poem"""
        return self.order_by('-featured_date').select_related('poem').first()


class FeaturedPoem(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='featured_dates')
    featured_date = models.DateField(unique=True, db_index=True)
    
    objects = FeaturedPoemManager()
    
    class Meta:
        ordering = ['-featured_date']
        verbose_name = 'Featured Poem'
        verbose_name_plural = 'Featured Poems'
    
    def __str__(self):
        return f"{self.poem.title} - {self.featured_date.strftime('%Y-%m-%d')}"
