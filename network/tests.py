import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import User, Post

# initialize the APIClient app
client = Client()

class PagesTestCase(TestCase):

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


    def test_index(self):

        # Send get request to index page and store response
        response = client.get("/")

        # Make sure status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure three posts are returned in the context
        self.assertEqual(len(response.context["page_obj"]), 3)



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


class CreateNewPostTestCase(TestCase):
    
    def setUp(self):

        # Create user
        u1 = User.objects.create(username='u1')
        u1.set_password('12345')
        u1.save()
        # log in user
        client.login(username='u1', password='12345')

        # Create payloads
        self.valid_payload = {
            'post_content': 'Test',
        }
        self.invalid_payload = {
            'post_content': '',
        }

    def test_create_valid_post(self):        
        response = client.post(
            reverse('posts'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)


    def test_create_invalid_post(self):        
        response = client.post(
            reverse('posts'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)