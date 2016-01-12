from django.http import HttpRequest
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.template.loader import render_to_string

from habit_lists.models import Habit
from habit_lists.views import home_page

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)
	
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['habit_text'] = 'A new habit'
		
		response = home_page(request)
		
		self.assertEqual(Habit.objects.count(), 1)
		new_habit = Habit.objects.first()
		self.assertEqual(new_habit.text, 'A new habit')

	def test_home_page_redirects_after_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['habit_text'] = 'A new habit'
		
		response = home_page(request)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/')

	def test_home_page_only_saves_habits_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Habit.objects.count(), 0)

	def test_home_page_displays_all_habits(self):
		Habit.objects.create(text='habit 1')
		Habit.objects.create(text='habit 2')
		
		request = HttpRequest()
		response = home_page(request)

		self.assertIn('habit 1', response.content.decode())
		self.assertIn('habit 2', response.content.decode())

class HabitModelTest(TestCase):

	def test_saving_and_retrieving_habits(self):
		first_habit = Habit()
		first_habit.text = 'The first habit'
		first_habit.save()

		second_habit = Habit()
		second_habit.text = 'The second habit'
		second_habit.save()

		saved_habits = Habit.objects.all()
		self.assertEqual(saved_habits.count(), 2)

		first_saved_habit = saved_habits[0]
		second_saved_habit = saved_habits[1]
		self.assertEqual(first_saved_habit.text, 'The first habit')
		self.assertEqual(second_saved_habit.text, 'The second habit')
