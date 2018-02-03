from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from collections import Counter


def log_crear(user_id, obj, repr_txt):
    LogEntry(user_id=user_id, content_type_id=ContentType.objects.get_for_model(type(obj)).pk, object_id=obj.pk,
             object_repr=repr_txt + ' - ' + str(obj), action_flag=ADDITION).save()


def log_modificar(user_id, obj, repr_txt):
    LogEntry(user_id=user_id, content_type_id=ContentType.objects.get_for_model(type(obj)).pk, object_id=obj.pk,
             object_repr=repr_txt + ' - ' + str(obj), action_flag=CHANGE).save()


def log_eliminar(user_id, obj, repr_txt):
    LogEntry(user_id=user_id, content_type_id=ContentType.objects.get_for_model(type(obj)).pk, object_id=obj.pk,
             object_repr=repr_txt + ' - ' + str(obj), action_flag=DELETION).save()


def to_counter(model, kwargs, values):
    qs = model.objects.filter(**kwargs).values_list(*values)
    return Counter(qs)
