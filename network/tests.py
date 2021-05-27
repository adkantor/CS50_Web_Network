import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import User, Post

# initialize the APIClient app
client = Client()


class IndexPageViewTestCase(TestCase):

    def setUp(self):

        # Create users
        u1 = User.objects.create(username='u1')        
        # create  posts
        for _ in range(25):
            Post.objects.create(created_by=u1)


    def test_view_url_exists_at_proper_location(self):
        """ Tests whether page is properly loaded. """        
        response = client.get("/")
        self.assertEqual(response.status_code, 200)        


    def test_view_url_by_name(self):
        """ Tests whether page is accessible by name. """
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        """ Tests whether page uses correct template. """
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')


    def test_view_pagination(self):
        """ Tests page pagination. """
        response = client.get("/")
        
        # Request without argument: make sure 10 posts are returned in the context
        self.assertEqual(len(response.context["page_obj"]), 10)

        # Send get request to index page for page 1 and store response
        response = client.get("/?page=1")
        # Make sure 10 posts are returned in the context
        self.assertEqual(len(response.context["page_obj"]), 10)

        # Send get request to index page for page 2 and store response
        response = client.get("/?page=2")
        # Make sure 10 posts are returned in the context
        self.assertEqual(len(response.context["page_obj"]), 10)

        # Send get request to index page for page 3 and store response
        response = client.get("/?page=3")
        # Make sure 5 posts are returned in the context
        self.assertEqual(len(response.context["page_obj"]), 5)



class UnauthenticatedFollowingPageViewTestCase(TestCase):

    def test_following_non_authenticated(self):
        """ Tests whether Following page is unreachable by non-authenticated user. """
        response = client.get("/following")
        # Make sure status code is 302: redirect to /accounts/login/?next=/following
        self.assertEqual(response.status_code, 302)


class FollowingPageViewTestCase(TestCase):

    def setUp(self):

        # Create users
        u1 = User.objects.create(username='u1')
        u2 = User.objects.create(username='u2')
        u3 = User.objects.create(username='u3')
        u4 = User.objects.create(username='u4')        

        # create posts
        p1 = Post.objects.create(created_by=u1)
        p2 = Post.objects.create(created_by=u1)
        p3 = Post.objects.create(created_by=u2)
        for _ in range(25):
            Post.objects.create(created_by=u4)

        # add likes
        u1.liked_posts.add(p3)
        u3.liked_posts.add(p1)
        u3.liked_posts.add(p2)
        u3.liked_posts.add(p3)

        # create follows
        u1.following.add(u2)
        u1.following.add(u3)
        u2.following.add(u1)
        u1.following.add(u4)

        # log in user 1
        client.force_login(u1)


    def test_view_url_exists_at_proper_location(self):
        """ Tests whether page is properly loaded. """        
        response = client.get("/following")
        self.assertEqual(response.status_code, 200)


    def test_view_url_by_name(self):
        """ Tests whether page is accessible by name. """
        response = client.get(reverse('following'))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        """ Tests whether page uses correct template. """
        response = client.get(reverse('following'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'network/index.html')


class ControlsTestCase(TestCase):
    pass


class PostTestCase(TestCase):

    def setUp(self):

        # Create users
        u1 = User.objects.create(username='u1')
        u2 = User.objects.create(username='u2')
        u3 = User.objects.create(username='u3')

        # create posts
        p1 = Post.objects.create(created_by=u1, content='abc')
        p2 = Post.objects.create(created_by=u1, content='def')
        p3 = Post.objects.create(created_by=u2, content='ghi')

        # add likes
        u1.liked_posts.add(p3)
        u3.liked_posts.add(p1)
        u3.liked_posts.add(p2)
        u3.liked_posts.add(p3)

        # create follows
        u1.following.add(u2)
        u1.following.add(u3)
        u2.following.add(u1)


    def test_text_content(self):
        p1 = Post.objects.get(id=1)
        p2 = Post.objects.get(id=2)
        p3 = Post.objects.get(id=3)
        
        content1 = f'{p1.content}'
        content2 = f'{p2.content}'
        content3 = f'{p3.content}'
        
        self.assertEqual(content1, 'abc')
        self.assertEqual(content2, 'def')
        self.assertEqual(content3, 'ghi')


    def test_posts_count(self):
        u1 = User.objects.get(username='u1')
        u2 = User.objects.get(username='u2')
        u3 = User.objects.get(username='u3')

        self.assertEqual(Post.objects.all().count(), 3)
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


    def test_get_all_posts(self):
        u1 = User.objects.get(username='u1')
        u2 = User.objects.get(username='u2')
        u3 = User.objects.get(username='u3')

        p1 = Post.objects.get(pk=1)
        p2 = Post.objects.get(pk=2)
        p3 = Post.objects.get(pk=3)

        all_posts = Post.get_all_posts()

        self.assertEqual(len(all_posts), 3)
        self.assertIn(p1, all_posts)
        self.assertIn(p2, all_posts)
        self.assertIn(p3, all_posts)


    def test_get_posts_of_followed_people(self):
        u1 = User.objects.get(username='u1')
        u2 = User.objects.get(username='u2')
        u3 = User.objects.get(username='u3')

        p1 = Post.objects.get(pk=1)
        p2 = Post.objects.get(pk=2)
        p3 = Post.objects.get(pk=3)

        posts1 = u1.get_posts_of_followed_people()
        self.assertEqual(len(posts1), 1)
        self.assertIn(p3, posts1)
        
        posts2 = u2.get_posts_of_followed_people()
        self.assertEqual(len(posts2), 2)

        self.assertIn(p1, posts2)
        self.assertIn(p2, posts2)
        
        posts3 = u3.get_posts_of_followed_people()
        self.assertEqual(len(posts3), 0)
       
        
        
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


    def tearDown(self):
        client.logout()


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


class FollowTestCase(TestCase):

    def setUp(self):

        # Create users
        u1 = User.objects.create(username='u1')
        u1.set_password('12345')
        u1.save()
        u2 = User.objects.create(username='u2')
        # log in u1
        client.login(username='u1', password='12345')

        # Create PUT payloads
        self.payload_follow = {
            'isfollowing': True,
        }
        self.payload_unfollow = {
            'isfollowing': False,
        }


    def tearDown(self):
        client.logout()


    def test_get_status(self):

        u1 = User.objects.get(username='u1')
        u2 = User.objects.get(username='u2')

        # test initial status --> not following
        response = client.get(reverse('follow', kwargs={'user_id': u2.id}))
        data = response.json()
        self.assertFalse(data['isfollowing'])
        self.assertEqual(response.status_code, 200)
        # make u1 follow u2
        u1.follow(u2)
        response = client.get(reverse('follow', kwargs={'user_id': u2.id}))
        data = response.json()
        self.assertTrue(data['isfollowing'])
        self.assertEqual(response.status_code, 200)        


    def test_toggle_status(self):

        u1 = User.objects.get(username='u1')
        u2 = User.objects.get(username='u2')

        # reset follow status
        u1.unfollow(u2)
        self.assertFalse(u1.is_following(u2))

        # follow
        response = client.put(
            reverse('follow', kwargs={'user_id': u2.id}),
            data=json.dumps(self.payload_follow),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertTrue(u1.is_following(u2))

        # follow again
        response = client.put(
            reverse('follow', kwargs={'user_id': u2.id}),
            data=json.dumps(self.payload_follow),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertTrue(u1.is_following(u2))

        # unfollow
        response = client.put(
            reverse('follow', kwargs={'user_id': u2.id}),
            data=json.dumps(self.payload_unfollow),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(u1.is_following(u2))

        # unfollow again
        response = client.put(
            reverse('follow', kwargs={'user_id': u2.id}),
            data=json.dumps(self.payload_unfollow),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(u1.is_following(u2))


    def test_invalid_method(self):

        u1 = User.objects.get(username='u1')
        u2 = User.objects.get(username='u2')

        response = client.post(
            reverse('follow', kwargs={'user_id': u2.id}),
            data=json.dumps(self.payload_follow),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


    def test_get_status_invalid_user(self):

        response = client.get(reverse('follow', kwargs={'user_id': 3}))
        self.assertEqual(response.status_code, 404)


    def test_toggle_status_invalid_user(self):

        response = client.put(
            reverse('follow', kwargs={'user_id': 3}),
            data=json.dumps(self.payload_follow),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)


# https://realpython.com/test-driven-development-of-a-django-restful-api/