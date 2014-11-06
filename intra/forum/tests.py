from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from forum.models import Category, Post

class CategoryTests(TestCase):
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

    def test_path(self):
        """Path is correct ?"""
        cat1 = Category(name="Category 1")
        cat2 = Category(name="Category 2", parent=cat1)
        cat3 = Category(name="Category 3", parent=cat1)
        cata = Category(name="Category A")
        catb = Category(name="Category B", parent=cata)
        self.assertEqual(cata.get_path(), [cata])
        self.assertEqual(cat3.get_path(), [cat1, cat3])
        catz = Category(name="Category Z", parent=cat2)
        catz.parent = cat2
        self.assertEqual(catz.get_path(), [cat1, cat2, catz])


class ThreadBasicTests(TestCase):
    def test_creation_if_valid_thread(self):
        """Thread can have a title and must not be a comment"""
        User = get_user_model()
        user = User(username="Test")
        cat = Category(name="Category")
        cat.full_clean()
        thread = Post(
                         title="Topic 1",
                         cat=cat,
                         message="Voici un message",
                         author=user
                     )
        thread.full_clean()
