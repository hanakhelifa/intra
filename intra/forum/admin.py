from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField
from forum.models import Category


class CustomParentList(ModelChoiceField):
    def label_from_instance(self, obj):
        name = obj.name
        while not (obj.parent is None):
            obj = obj.parent
            name = obj.name + ' > ' + name
        return name


class CategoryAdminForm(ModelForm):
    parent = CustomParentList(Category.objects.all(), required=False)
    class Meta:
        model = Category
        fields = ['parent', 'name']


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('get_path', )

    def get_path(self, obj):
        name = obj.name
        while not (obj.parent is None):
            obj = obj.parent
            name = obj.name + ' > ' + name
        return name
    get_path.short_description = 'Path'
    get_path.admin_order_field = 'name'


admin.site.register(Category, CategoryAdmin)
