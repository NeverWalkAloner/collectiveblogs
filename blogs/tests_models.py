from django.contrib.auth.models import User
from django.test import TestCase
from .models import Blog, Subscription


# Create your tests here.
class BlogTest(TestCase):
    def setUp(self):
        Blog.objects.create(name='test',
                            unique_name='test_blog')

    def test_srt_representation(self):
        blog = Blog.objects.get(unique_name='test_blog')
        self.assertEqual('test', str(blog))


class SubscriptionTest(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(name='test',
                                   unique_name='test_blog')
        self.user = User.objects._create_user(username='test',
                                              password='test',
                                              email='')
        Subscription.objects.create(blog=self.blog,
                                    user=self.user)

    def test_subscription_representation(self):
        s = Subscription.objects.get(blog=self.blog)
        self.assertEqual('test', str(s))