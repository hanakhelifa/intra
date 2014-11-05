from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
                raise ValidationError(_('Category parent create infinite loop'))
            ran = []
            cat = self
            while not (cat.parent is None):
                ran.append(cat)
                cat = cat.parent
                if cat in ran:
                    raise ValidationError(
                                  _('Category parent create infinite loop')
                              )

    def get_path(self):
        path = [self, ]
        while not (self.parent is None):
            self = self.parent
            path.insert(0, self)
        return path


class Post(models.Model):
    cat = models.ForeignKey('Category')
    parent = models.ForeignKey('Post', null=True, blank=True)
    comment = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=250, blank=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.parent:
            if not self.title:
                raise ValidationError(
                              _('Title can\'t be empty while the'
                              ' post is a thread')
                          )
            if self.comment is True:
                raise ValidationError(
                              _('The post can\'t be a comment while'
                              ' it is a thread')
                          )
        elif self.parent:
            if self.title:
                raise ValidationError(
                              _('The title can\'t be set while'
                              ' the post isn\'t a thread')
                          )
        if self.comment is True and self.parent.comment is True:
            raise ValidationError(
                          _('A comment post can\'t have a child'
                          ' comment post')
                      )
