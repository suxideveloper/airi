from django.db import models
from django.urls import reverse

from blog.models import Tag

# Create your models here.
class Model_of_Programmer(models.Model):
    HOLAT = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name="Ismi")
    age = models.IntegerField(null=False, blank=False, verbose_name="Yoshi")
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False, verbose_name="Emaili")
    bio = models.TextField(blank=True, verbose_name="Bio")
    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False, verbose_name="ID raqami")
    state = models.TextField(blank=True, choices=HOLAT, verbose_name="Davlat")

    def __str__(self):
        return self.name 
    class Meta:
        verbose_name = "Programmer"
        verbose_name_plural = "Programmers"
        ordering = ['name', 'age']

    def save(self, *args, **kwargs):
        # Qo'shimcha saqlash mantiqini shu yerda amalga oshiring
        super().save(*args, **kwargs)   # Asosiy saqlash operatsiyasini chaqirish
    def get_absolute_url(self):
        return reverse("app_name:model_of_programmer_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("app_name:model_of_programmer_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("app_name:model_of_programmer_delete", kwargs={"pk": self.pk})
    
    def get_tags(self):
        return Tag.objects.filter(name__length__lt=6) & Tag.objects.filter(name__contains='programmer')
          # qiymati uzunligi 6 dan kichik bo'lganlarni qaytaradi



def delete_tags(request):
    search_word = request.GET.get('search', '')  # yoki POST bo‘lsa request.POST.get('search', '')
    Tag.objects.filter(name__contains=search_word).delete()
    # boshqa kodlar...

# <form method="get">
#     <input type="text" name="search" placeholder="So‘zni kiriting">
#     <button type="submit">O‘chirish</button>
# </form>

