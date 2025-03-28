
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task


class SystemViewTest(TestCase):
    def test_full_system(self):
        print("1. register start")
        # mock user
        data = {
            'username': 'mason1',
            'password': 'mason123',
            'email': 'mason@example.com'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, 201)  # 201 created
        # get user instance
        self.user = User.objects.get(username='mason1')

        # check if user is created
        self.assertTrue(User.objects.filter(username='mason1').exists())
        print("1. register testing finish username:" + self.user.username)

        print("2. login testing start")

        response = self.client.post('/api/login/', {'username': 'mason1', 'password': 'mason123'})
        self.assertEqual(response.status_code, 200)

        self.token = response.json()['token']
        self.assertIsNotNone(self.token)
        print("2. login testing finish, token:" + self.token)


        # print("3. view user testing start")
        # response = self.client.get('/api/user/', HTTP_AUTHORIZATION='Token ' + self.token)
        # # response = self.client.get('/api/user/')
        # self.assertEqual(response.status_code, 200)
        # print("3. user testing finish username:"+response.json()['username'])

        print("3.logout testing start")
        response = self.client.post('/api/logout/',HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, 200)
        print("3.logout testing finish")

        # delete user clean up
        self.user.delete()

#
# class TaskModelTest(TestCase):
#     def test_create_task(self):
#         print("5. create task testing start")
#         user = User.objects.create_user(username='testuser', password='testpass')
#         task = Note.objects.create(title="Test Task", description="desc", status="todo", user=user)
#         self.assertEqual(task.title, "Test Task")
#         print("5. create task testing finish")
