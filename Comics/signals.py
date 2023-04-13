from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from .models import Comic, Chapter, Page
from django.dispatch import receiver


@receiver(pre_delete, sender=Comic)
def pre_delete_comic(sender, **kwargs):
    print('You are about to delete a comic!')


@receiver(post_delete, sender=Comic)
def delete_comic(sender, **kwargs):

    print('You have just deleted a comic!!!')
