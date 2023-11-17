from django.test import TestCase
from django.urls import reverse
from .models import GeneralInformation, Tutorial
from unittest.mock import patch
import requests

"""
Test cases for the GeneralInformation model and associated views.

- test_add_general_information: Tests the addition of GeneralInformation via a form submission.
- test_update_general_information: Tests the update of GeneralInformation via a form submission.
- test_delete_general_information: Tests the deletion of GeneralInformation via a form submission.
"""

class GeneralInformationTests(TestCase):

    """
    Submits a POST request to the 'add_general_info' view with test data.
    Verifies that the response status code is 302 (redirect).
    Checks if the newly added GeneralInformation object exists in the database.
    """

    def test_add_general_information(self):
        response = self.client.post(reverse('add_general_info'), {
                                    'topic': 'Test Topic', 'description': 'Test Description'})
        self.assertEqual(response.status_code, 302)

        general_info = GeneralInformation.objects.get(
            topic='Test Topic', description='Test Description')
        self.assertIsNotNone(general_info)

    """
    Creates an initial GeneralInformation object, then submits a POST request to the 'update_general_info' view with updated data.
    Verifies that the response status code is 302 (redirect).
    Retrieves the updated GeneralInformation object from the database and checks if the changes are reflected.
    """

    def test_update_general_information(self):
        general_info = GeneralInformation.objects.create(
            topic='Old Topic', description='Old Description')

        response = self.client.post(reverse('update_general_info', args=[general_info.id]),
                                    {'topic': 'Updated Topic', 'description': 'Updated Description'})
        self.assertEqual(response.status_code, 302)

        updated_info = GeneralInformation.objects.get(id=general_info.id)
        self.assertEqual(updated_info.topic, 'Updated Topic')
        self.assertEqual(updated_info.description, 'Updated Description')

    """
    Creates a GeneralInformation object, then submits a POST request to the 'delete_general_info' view.
    Verifies that the response status code is 302 (redirect).
    Attempts to retrieve the deleted GeneralInformation object and asserts that it raises a DoesNotExist exception.
    """

    def test_delete_general_information(self):
        general_info = GeneralInformation.objects.create(
            topic='Test Topic', description='Test Description')

        response = self.client.post(
            reverse('delete_general_info', args=[general_info.id]))
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(GeneralInformation.DoesNotExist):
            deleted_info = GeneralInformation.objects.get(id=general_info.id)


"""
Test cases for the Tutorial model and associated views.

- test_add_tutorial: Tests the addition of Tutorial via a form submission.
- test_update_tutorial: Tests the update of Tutorial via a form submission.
- test_delete_tutorial: Tests the deletion of Tutorial via a form submission.
"""

class TutorialTests(TestCase):

    """
    Creates a GeneralInformation object, then submits a POST request to the 'add_tutorial' view with test data.
    Verifies that the response status code is 302 (redirect).
    Checks if the newly added Tutorial object exists in the database.
    """

    def test_add_tutorial(self):
        general_info = GeneralInformation.objects.create(
            topic='Test Topic', description='Test Description')

        response = self.client.post(reverse('add_tutorial'),
                                    {'title': 'Test Tutorial', 'steps': 'Test Steps', 'info': general_info.id})
        self.assertEqual(response.status_code, 302)

        tutorial = Tutorial.objects.get(
            title='Test Tutorial', steps='Test Steps', info=general_info)
        self.assertIsNotNone(tutorial)

    """
    Creates a GeneralInformation and an initial Tutorial object, then submits a POST request to the 'update_tutorial' view with updated data.
    Verifies that the response status code is 302 (redirect).
    Retrieves the updated Tutorial object from the database and checks if the changes are reflected.
    """

    def test_update_tutorial(self):
        general_info = GeneralInformation.objects.create(
            topic='Test Topic', description='Test Description')
        tutorial = Tutorial.objects.create(
            title='Old Title', steps='Old Steps', info=general_info)

        response = self.client.post(reverse('update_tutorial', args=[tutorial.id]),
                                    {'title': 'Updated Title', 'steps': 'Updated Steps', 'info': general_info.id})
        self.assertEqual(response.status_code, 302)

        updated_tutorial = Tutorial.objects.get(id=tutorial.id)
        self.assertEqual(updated_tutorial.title, 'Updated Title')
        self.assertEqual(updated_tutorial.steps, 'Updated Steps')
        self.assertEqual(updated_tutorial.info, general_info)

    """
    Creates a GeneralInformation and a Tutorial object, then submits a POST request to the 'delete_tutorial' view.
    Verifies that the response status code is 302 (redirect).
    Attempts to retrieve the deleted Tutorial object and asserts that it raises a DoesNotExist exception.
    """

    def test_delete_tutorial(self):
        general_info = GeneralInformation.objects.create(
            topic='Test Topic', description='Test Description')
        tutorial = Tutorial.objects.create(
            title='Test Tutorial', steps='Test Steps', info=general_info)

        response = self.client.post(
            reverse('delete_tutorial', args=[tutorial.id]))
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(Tutorial.DoesNotExist):
            deleted_tutorial = Tutorial.objects.get(id=tutorial.id)


class WeatherAPITest(TestCase):

    """
    Tests a successful API response.

    Mocks the requests.get method to simulate a successful API response with mock weather data.
    Sends a GET request to the 'get_weather_data' API.
    Asserts that the response status code is 200 and the JSON content matches the expected data.
    """

    @patch('requests.get')
    def test_get_weather_data_success(self, mock_requests_get):
        mock_data = {
            'main': {'temp': 20, 'humidity': 50},
            'weather': [{'description': 'Clear sky'}]
        }
        mock_response = mock_requests_get.return_value
        mock_response.json.return_value = mock_data

        response = self.client.get(
            reverse('get_weather_data', args=['test_city']))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf-8'),
            {'temperature': 20, 'humidity': 50, 'description': 'Clear sky'}
        )

    """
    Tests an API response with an error.

    Mocks the requests.get method to simulate a failed API response with a specified error message.
    Sends a GET request to the 'get_weather_data' API.
    Asserts that the response status code is 500 and the JSON content includes the expected error message.
    """

    @patch('requests.get')
    def test_get_weather_data_failure(self, mock_requests_get):
        error_message = 'API request failed'
        mock_response = mock_requests_get.return_value
        mock_response.json.side_effect = requests.RequestException(
            error_message)

        response = self.client.get(
            reverse('get_weather_data', args=['test_city']))

        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(
            str(response.content, encoding='utf-8'),
            {'error': error_message}
        )
