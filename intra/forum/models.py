from django.db import models
from django.conf import settings


class CategoryManager(models.Manager):
    def get_tree(self, *args, **kwargs):
        ret = {}
        children = list(
                           self
                           .get_queryset()
                           .filter(*args, **kwargs)
                           .order_by('name')
                       )
        for child in children:
            ret[child] = self.get_tree(parent__exact=child.id)
        return ret


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True)
    name = models.CharField(max_length=100)

    objects = CategoryManager()

    def __str__(self):
        path = self.get_path()
        s = ""
        for entry in path[0:-1]:
            s += entry.name + " > "
        s += path[-1].name
        return s

    def clean(self):
        if not (self.parent is None):
            if not (self.pk is None) and self.parent == self:
                raise ValidationError('Category parent create infinite loop')
            ran = []
            cat = self
            while not (cat.parent is None):
                ran.append(cat)
                cat = cat.parent
                if cat in ran:
                    raise ValidationError(
                                  'Category parent create infinite loop'
                              )

    def get_path(self):
        path = [self, ]
        while not (self.parent is None):
            self = self.parent
            path.insert(0, self)
        return path


