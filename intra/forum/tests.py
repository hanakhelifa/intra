from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from forum.models import Category, Post

class CategoryTests(TestCase):
    def test_creation_with_correct_tree(self):
        """Creation of a valid categories tree. This must pass the clean."""
        cat1 = Category(name="Category 1")
        cat2 = Category(name="Category 2", parent=cat1)
        cat3 = Category(name="Category 3", parent=cat1)
        cata = Category(name="Category A")
        catb = Category(name="Category B", parent=cata)
        cat1.full_clean()
        cat1.save()
        cat2.full_clean()
        cat2.save()
        cat3.full_clean()
        cat3.save()
        cata.full_clean()
        cata.save()
        catb.full_clean()
        catb.save()

    def test_creation_with_loop_tree(self):
        """Creation of a categories tree, with a loop. The clean must return"""
        """ a ValidationError."""
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
            cat1.save()
        with self.assertRaises(ValidationError):
            cat2.full_clean()
            cat2.save()
        with self.assertRaises(ValidationError):
            cat3.full_clean()
            cat3.save()
        cata.full_clean()
        cata.save()
        catb.full_clean()
        catb.save()
        with self.assertRaises(ValidationError):
            catx.full_clean()
            catx.save()
        with self.assertRaises(ValidationError):
            caty.full_clean()
            caty.save()
        with self.assertRaises(ValidationError):
            catz.full_clean()
            catz.save()

    def test_path(self):
        """Testing path() return"""
        cat1 = Category(name="Category 1")
        cat2 = Category(name="Category 2", parent=cat1)
        cat3 = Category(name="Category 3", parent=cat1)
        cata = Category(name="Category A")
        catb = Category(name="Category B", parent=cata)
        cat1.full_clean()
        cat1.save()
        cat2.full_clean()
        cat2.save()
        cat3.full_clean()
        cat3.save()
        cata.full_clean()
        cata.save()
        catb.full_clean()
        catb.save()
        self.assertEqual(cata.get_path(), [cata])
        self.assertEqual(cat3.get_path(), [cat1, cat3])
        catz = Category(name="Category Z", parent=cat2)
        catz.full_clean()
        catz.save()
        catz.parent = cat2
        self.assertEqual(catz.get_path(), [cat1, cat2, catz])


class PostTests(TestCase):
    def test_creation_thread(self):
        """Creation of a valid thread"""
        User = get_user_model()
        user = User(**{User.USERNAME_FIELD: "user"})
        user.set_unusable_password()
        user.full_clean()
        user.save()
        cat = Category(name="Category")
        cat.full_clean()
        cat.save()
        thread = Post(
                         cat=cat,
                         author=user,
                         title="Topic 1",
                         message="Voici un message",
                     )
        thread.full_clean()
        thread.save()
        self.assertFalse(thread.is_post())
        self.assertFalse(thread.is_comment())
        self.assertTrue(thread.is_thread())

    def test_creation_post(self):
        """Creation of a valid post"""
        User = get_user_model()
        user = User(**{User.USERNAME_FIELD: "user"})
        user.set_unusable_password()
        user.full_clean()
        user.save()
        cat = Category(name="Category")
        cat.full_clean()
        cat.save()
        thread = Post(
                         cat=cat,
                         author=user,
                         title="Topic 1",
                         message="Voici un message",
                     )
        thread.full_clean()
        thread.save()
        post = Post(
                         cat=cat,
                         author=user,
                         title="RE: Topic 1",
                         message="Voici une réponse",
                         parent=thread,
                   )
        post.full_clean()
        post.save()
        self.assertTrue(post.is_post())
        self.assertFalse(post.is_comment())
        self.assertFalse(post.is_thread())

    def test_creation_comment(self):
        """Creation of a valid comment"""
        User = get_user_model()
        user = User(**{User.USERNAME_FIELD: "user"})
        user.set_unusable_password()
        user.full_clean()
        user.save()
        cat = Category(name="Category")
        cat.full_clean()
        cat.save()
        thread = Post(
                         cat=cat,
                         author=user,
                         title="Topic 1",
                         message="Voici un message",
                     )
        thread.full_clean()
        thread.save()
        post = Post(
                         cat=cat,
                         author=user,
                         title="RE: Topic 1",
                         message="Voici une réponse",
                         parent=thread,
                   )
        post.full_clean()
        post.save()
        comment = Post(
                          cat=cat,
                          author=user,
                          title="RE: RE: Topic 1",
                          message="Voici un commentaire",
                          parent=post,
                      )
        comment.full_clean()
        comment.save()
        self.assertFalse(comment.is_post())
        self.assertTrue(comment.is_comment())
        self.assertFalse(comment.is_thread())

    def test_can_have_comment(self):
        """A post can't have a parent if it parent have a parent."""
        """Understood ?"""
        User = get_user_model()
        user = User(**{User.USERNAME_FIELD: "user"})
        user.set_unusable_password()
        user.full_clean()
        user.save()
        cat = Category(name="Category")
        cat.full_clean()
        cat.save()
        thread = Post(
                         cat=cat,
                         author=user,
                         title="Topic 1",
                         message="Voici un message",
                     )
        thread.full_clean()
        thread.save()
        post = Post(
                         cat=cat,
                         author=user,
                         title="RE: Topic 1",
                         message="Voici une réponse",
                         parent=thread,
                   )
        post.full_clean()
        post.save()
        comment = Post(
                          cat=cat,
                          author=user,
                          title="RE: RE: Topic 1",
                          message="Voici un commentaire",
                          parent=post,
                      )
        comment.full_clean()
        comment.save()
        self.assertFalse(comment.can_have_comment())

    def test_creation_invalid_comment(self):
        """Creation of a invalid comment"""
        User = get_user_model()
        user = User(**{User.USERNAME_FIELD: "user"})
        user.set_unusable_password()
        user.full_clean()
        user.save()
        cat = Category(name="Category")
        cat.full_clean()
        cat.save()
        thread = Post(
                         cat=cat,
                         author=user,
                         title="Topic 1",
                         message="Voici un message",
                     )
        thread.full_clean()
        thread.save()
        post = Post(
                         cat=cat,
                         author=user,
                         title="RE: Topic 1",
                         message="Voici une réponse",
                         parent=thread,
                   )
        post.full_clean()
        post.save()
        comment1 = Post(
                           cat=cat,
                           author=user,
                           title="RE: RE: Topic 1",
                           message="Voici un commentaire",
                           parent=post,
                       )
        comment1.full_clean()
        comment1.save()
        comment2 = Post(
                           cat=cat,
                           author=user,
                           title="RE: RE: Topic 1",
                           message="Voici un commentaire",
                           parent=comment1,
                       )
        with self.assertRaises(ValidationError):
            comment2.full_clean()
            comment2.save()

class RightsTests(TestCase):
    def test_category_rigths_1(self):
        """Testing user with admin rights but no mod rights"""
        User = get_user_model()
        user = User(**{User.USERNAME_FIELD: "user1"})
        user.set_unusable_password()
        user.save()
        user.forumrights.admin = True
        user.save()
        cat = Category(name="cat1")
        cat.save()
        self.assertEqual(cat.have_rights(user), True)

    def test_category_rigths_2(self):
        """Testing user with no admin rights nor mod rights"""
        User = get_user_model()
        user = User(**{User.USERNAME_FIELD: "user1"})
        user.set_unusable_password()
        user.save()
        user.forumrights.admin = False
        user.save()
        cat = Category(name="cat1")
        cat.save()
        self.assertEqual(cat.have_rights(user), False)

    def test_category_rigths_3(self):
        """Testing user with no admin rights but mod rights"""
        User = get_user_model()
        user = User(**{User.USERNAME_FIELD: "user1"})
        user.set_unusable_password()
        user.save()
        user.forumrights.admin = False
        user.save()
        cat = Category(name="cat1")
        cat.save()
        user.forumrights.mod.add(cat)
        user.save()
        self.assertEqual(cat.have_rights(user), True)

