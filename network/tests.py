from django.test import TestCase

from .models import User, Post


class PostTestCase(TestCase):

    def setUp(self):

        # Create users
        u1 = User.objects.create(username='u1')
        u2 = User.objects.create(username='u2')
        u3 = User.objects.create(username='u3')

        # create posts
        p1 = Post.objects.create(created_by=u1)
        p2 = Post.objects.create(created_by=u1)
        p3 = Post.objects.create(created_by=u2)

        # add likes
        u1.liked_posts.add(p3)
        u3.liked_posts.add(p1)
        u3.liked_posts.add(p2)
        u3.liked_posts.add(p3)

        # create follows
        u1.following.add(u2)
        u1.following.add(u3)
        u2.following.add(u1)



    def test_posts_count(self):
        u1 = User.objects.get(username='u1')
        u2 = User.objects.get(username='u2')
        u3 = User.objects.get(username='u3')

        self.assertEqual(u1.posts.count(), 2)
        self.assertEqual(u2.posts.count(), 1)
        self.assertEqual(u3.posts.count(), 0)


    def test_likes_count(self):
        u1 = User.objects.get(username='u1')
        u2 = User.objects.get(username='u2')
        u3 = User.objects.get(username='u3')

        p1 = Post.objects.get(id=1)
        p2 = Post.objects.get(id=2)
        p3 = Post.objects.get(id=3)  

        self.assertEqual(u1.liked_posts.count(), 1)     
        self.assertEqual(u2.liked_posts.count(), 0)     
        self.assertEqual(u3.liked_posts.count(), 3)     
        
        self.assertEqual(p1.liked_by.count(), 1)     
        self.assertEqual(p2.liked_by.count(), 1)     
        self.assertEqual(p3.liked_by.count(), 2)     


    def test_follows_count(self):
        u1 = User.objects.get(username='u1')
        u2 = User.objects.get(username='u2')
        u3 = User.objects.get(username='u3')

        self.assertEqual(u1.followed_by.count(), 1)
        self.assertEqual(u2.followed_by.count(), 1)
        self.assertEqual(u3.followed_by.count(), 1)

        self.assertEqual(u1.following.count(), 2)
        self.assertEqual(u2.following.count(), 1)
        self.assertEqual(u3.following.count(), 0)