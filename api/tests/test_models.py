from django.test import TestCase

from api.factories import MealFactory, MenuFactory


class MenuModelTests(TestCase):
    def setUp(self):
        self.name = "Wyjątkowe menu"
        self.obj = MenuFactory.create(name=self.name)

    def test_should_create_object(self):
        """Menu should be created."""
        self.assertEqual(self.obj.__str__(), self.name)


class MealModelTests(TestCase):
    def setUp(self):
        self.name = "Wyjątkowe danie"
        self.obj = MealFactory.create(name=self.name, is_vege=True)

    def test_should_create_object(self):
        """Meal should be created."""
        self.assertEqual(self.obj.__str__(), self.name)

    def test_should_return_vege_meals_status(self):
        """Test sprawdza czy danie jest wegetariańskie"""
        self.assertTrue(self.obj.is_vege)
