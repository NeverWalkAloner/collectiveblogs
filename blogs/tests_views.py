import json
import unittest
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import RequestFactory, TestCase
from django.test.client import Client
from .views import BlogsView
from .models import Blog


class BlogViewsTest(TestCase):
    def setUp(self):
        # self.client = Client()
        self.user = User.objects.create_user(username='test',
                                             password='test')
        self.factory = RequestFactory()
        self.blog = Blog.objects.create(name='test',
                            unique_name='test_blog')


    def test_blogs_view(self):
        request = self.factory.get(reverse('blogs:list'))
        request.user = self.user
        # response = self.client.get('/blogs/')
        response = BlogsView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_subscription_view(self):
        request = self.factory.post(reverse('blogs:list'),
                                    data={'blog': self.blog.id})
        request.user = self.user
        # response = self.client.get('/blogs/')
        response = BlogsView.as_view()(request)
        response.client = Client()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blogs:list'))
        response = BlogsView.as_view()(request)
        response.client = Client()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blogs:list'))