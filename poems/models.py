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
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Author')
    text = models.TextField(verbose_name='Poem\'s text')
    theme = models.CharField(max_length=100, choices=THEMES, blank=True)
    category = models.ForeignKey(Theme, null=True, on_delete=models.CASCADE, verbose_name='Category')
    views = models.PositiveIntegerField(default=0, verbose_name='Views')
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
