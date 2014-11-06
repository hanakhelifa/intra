from django.core.exceptions import ValidationError
from django.test import TestCase
from forum.models import Category

class CategoryManagerTests(TestCase):
    def test_creation_with_correct_tree(self):
        """Category with a correct tree may pass the clean successfully"""
        cat1 = Category(name="Category 1")
        cat2 = Category(name="Category 2", parent=cat1)
        cat3 = Category(name="Category 3", parent=cat1)
        cata = Category(name="Category A")
        catb = Category(name="Category B", parent=cata)
        cat1.full_clean()
        cat2.full_clean()
        cat3.full_clean()
        cata.full_clean()
        catb.full_clean()

    def test_creation_with_loop_tree(self):
        """Category with a loop tree may don't pass the clean successfully"""
        cat1 = Category(name="Category 1")
        cat2 = Category(name="Category 2", parent=cat1)
        cat3 = Category(name="Category 3", parent=cat1)
        cata = Category(name="Category A")
        catb = Category(name="Category B", parent=cata)
        catx = Category(name="Category X")
        caty = Category(name="Category Y", parent=catx)
        catz = Category(name="Category Z", parent=cat1)
        catx.parent = caty
        cat1.parent = catz
        with self.assertRaises(ValidationError):
            cat1.full_clean()
        with self.assertRaises(ValidationError):
            cat2.full_clean()
        with self.assertRaises(ValidationError):
            cat3.full_clean()
        cata.full_clean()
        catb.full_clean()
        with self.assertRaises(ValidationError):
            catz.full_clean()
        with self.assertRaises(ValidationError):
            caty.full_clean()
        with self.assertRaises(ValidationError):
            catz.full_clean()


class CategoryMethodsTests(TestCase):
    def test_path(self):
        pass
