import datetime
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from api.factories import MenuFactory, MealFactory, UserFactory
from api.models import Menu, Meal
from api.serializers import MenuSerializer


class MenusAcceptanceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.cookies.load({'pl': 'pl'})
        Meal.objects.all().delete()
        Menu.objects.all().delete()
        self.user = UserFactory.create(username="Jan")

    def test_return_list_menus_without_empty_meals_without_auth(self):
        """Test sprawdza czy wyswietlamy listę menu bez pustych dań bez logowania."""
        MenuFactory.create()
        self.menu = MenuFactory.create()
        self.meal = MealFactory.create(menu=self.menu)

        url = reverse("menu-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(len(response.json()[0]['meals']), 1)

    def test_return_list_all_menus_with_auth(self):
        """Test sprawdza czy wyswietlamy listę wszystkich menu będąc zalogowanym z domyślnym sortowaniem po nazwie menu."""
        MenuFactory.create(name="A")
        self.menu = MenuFactory.create(name="B")
        self.meal = MealFactory.create(menu=self.menu)
        self.client.force_authenticate(user=self.user)

        url = reverse("menu-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(len(response.json()[1]['meals']), 1)

    def test_return_list_menus_ordering_by_count_meals(self):
        """Test sprawdza czy wyswietlamy listę menu w kolejności malejącej ilości dań w menu."""
        self.menu_one = MenuFactory.create(name="Menu One")
        MealFactory.create_batch(menu=self.menu_one, size=5)
        self.menu_two = MenuFactory.create(name="Menu Two")
        MealFactory.create_batch(menu=self.menu_two, size=3)

        url = reverse("menu-list")
        response = self.client.get(url, {"ordering": "-meals_count"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(len(response.json()[0]['meals']), self.menu_one.meals.count())
        self.assertEqual(len(response.json()[1]['meals']), self.menu_two.meals.count())

    def test_return_list_menus_ordering_by_name_mealsAZ(self):
        """Test sprawdza czy wyswietlamy listę menu alfabtycznie A-Z po nazwie dań."""
        self.menu_one = MenuFactory.create(name="Menu One")
        MealFactory.create(menu=self.menu_one, name="Burak")
        self.menu_two = MenuFactory.create(name="Menu Two")
        MealFactory.create(menu=self.menu_two, name="Ananas")

        url = reverse("menu-list")
        response = self.client.get(url, {"ordering": "meals"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(len(response.json()[1]['meals']), self.menu_one.meals.count())
        self.assertEqual(len(response.json()[0]['meals']), self.menu_two.meals.count())

    def test_return_list_menus_ordering_by_name_mealsZA(self):
        """Test sprawdza czy wyswietlamy listę menu alfabtycznie Z-A po nazwie dań."""
        self.menu_one = MenuFactory.create(name="Menu One")
        MealFactory.create(menu=self.menu_one, name="Burak")
        self.menu_two = MenuFactory.create(name="Menu Two")
        MealFactory.create(menu=self.menu_two, name="Ananas")

        url = reverse("menu-list")
        response = self.client.get(url, {"ordering": "-meals"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(len(response.json()[0]['meals']), self.menu_one.meals.count())
        self.assertEqual(len(response.json()[1]['meals']), self.menu_two.meals.count())

    def test_return_list_menus_filtering_by_menu_name(self):
        """Test sprawdza czy wyswietlamy menu odfiltrowane po nazwie."""
        menu_one = MenuFactory.create(name="Jajecznica")
        MealFactory.create(menu=menu_one)
        menu_two = MenuFactory.create(name="Polędwica")
        MealFactory.create(menu=menu_two)

        url = reverse("menu-list")
        response = self.client.get(url, {"name": "Jajecznica"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_return_list_menus_filtering_by_create_date(self):
        """Test sprawdza czy wyswietlamy menu odfiltrowane po dacie utworzenia."""
        menu_one = MenuFactory.create(name="Jajecznica")
        MealFactory.create(menu=menu_one)
        yesterday = datetime.datetime.now() - timedelta(days=3)
        menu_two = MenuFactory.create(name="Polędwica")
        menu_two.created = yesterday
        menu_two.save()
        MealFactory.create(menu=menu_two)

        search_date = yesterday.strftime('%Y-%m-%d')
        url = reverse("menu-list")

        response = self.client.get(url, {"created": search_date})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_return_list_menus_filtering_by_update_date(self):
        """Test sprawdza czy wyswietlamy menu odfiltrowane po dacie aktualizacji."""
        today = datetime.datetime.today()
        past = today - timedelta(days=3)
        menu_two = MenuFactory.create(name="Polędwica")
        menu_two.created = past
        menu_two.name = "Dziczyzna"
        menu_two.save()
        menu_two.refresh_from_db()
        MealFactory.create(menu=menu_two)

        search_date = today.strftime('%Y-%m-%d')
        url = reverse("menu-list")

        response = self.client.get(url, {"updated": search_date})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_menu_should_return_403_without_auth(self):
        """Test sprawdza czy utworzymy menu bez logowania."""
        data = {
            "name": "Nowe Menu",
            "description": "Opis menu"
        }
        url = reverse("menu-list")
        response = self.client.post(url, json=data)
        self.assertEqual(response.status_code, 403)

    def test_create_menu_should_return_201(self):
        """Test sprawdza czy utworzymy menu z logowaniem."""
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Nowe Menu",
            "description": "Opis menu"
        }
        url = reverse("menu-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertTrue(all([True for attr in ["name", "description", "id", "meals"] if attr in response.json().keys()]))
        self.assertEqual(response.json()['meals'], [])

    def test_create_menu_should_return_400_with_existing_name(self):
        """Test sprawdza czy utworzymy menu z już istniejącą nazwą."""
        self.client.force_authenticate(user=self.user)
        MenuFactory.create(name="Nowe Menu")
        data = {
            "name": "Nowe Menu",
            "description": "Opis menu"
        }
        url = reverse("menu-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'name': ['Istnieje już menu z tą nazwą!']})

    def test_create_menu_should_return_400_with_long_name(self):
        """Test sprawdza czy utworzymy menu z za długą nazwą."""
        self.client.force_authenticate(user=self.user)
        menu_name = "N"*60
        data = {
            "name": menu_name,
            "description": "Opis menu"
        }
        url = reverse("menu-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'name': ['Maksymalna ilość znaków: 50.']})

    def test_detail_view_menu_should_return_404_without_auth(self):
        """Test sprawdza czy wyświetlimy menu bez autoryzacji."""
        menu = MenuFactory.create(name="Menu Trzy")
        url = reverse("menu-detail", kwargs={"pk": menu.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_detail_view_menu_should_return_200_with_auth(self):
        """Test sprawdza czy wyświetlimy menu z autoryzacją."""
        self.client.force_authenticate(user=self.user)
        menu = MenuFactory.create(name="Menu Trzy")
        url = reverse("menu-detail", kwargs={"pk": menu.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], menu.id)

    def test_update_patch_menu_name_should_return_200(self):
        """Test sprawdza czy zaktualizujemy nazwę menu."""
        self.client.force_authenticate(user=self.user)
        menu = MenuFactory.create(name="Menu Trzy")
        url = reverse("menu-detail", kwargs={"pk": menu.id})
        response = self.client.patch(url, {"name": "Nowa Nazwa"})
        menu.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], menu.name)

    def test_update_put_menu_should_return_200(self):
        """Test sprawdza czy zaktualizujemy menu."""
        self.client.force_authenticate(user=self.user)
        menu = MenuFactory.create(name="Menu Trzy")
        url = reverse("menu-detail", kwargs={"pk": menu.id})

        data = MenuSerializer(menu).data
        data["name"] = "Nowa Nazwa"
        response = self.client.put(url, data)
        menu.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], menu.name)

    def test_update_patch_no_exists_menu_should_return_404(self):
        """Test sprawdza czy zaktualizujemy nieistniejące menu."""
        self.client.force_authenticate(user=self.user)
        url = reverse("menu-detail", kwargs={"pk": 123})
        response = self.client.patch(url, {"name": "Nowa Nazwa"})
        self.assertEqual(response.status_code, 404)


class MealsAcceptanceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Meal.objects.all().delete()
        Menu.objects.all().delete()
        self.user = UserFactory.create(username="Jan")

    def test_create_meal_in_no_exists_menu_return_404(self):
        """Test sprawdza czy utworzymy posiłęk w nieistniejącym menu."""
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Jajecznica",
            "description": "Super Hajecznica",
            "price": 2.35,
            "is_vege": True,
            "prepartion_time": 10
        }
        url = reverse("menus-meal-list", kwargs={"parent_lookup_menu": 2})
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 404)

    def test_create_meal_in_exist_menu(self):
        """Test sprawdza czy utworzymy posiłęk w menu."""
        self.client.force_authenticate(user=self.user)
        menu = MenuFactory.create(name="Menu Jajeczne")
        meal_name = "Jajecznica"
        data = {
            "name": meal_name,
            "description": "Super Hajecznica",
            "price": 2.35,
            "is_vege": True,
            "prepartion_time": 10
        }
        url = reverse("menus-meal-list", kwargs={"parent_lookup_menu": menu.id})
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['menu'], menu.id)
        self.assertEqual(response.json()['name'], meal_name)

    def test_create_meal_without_auth_403(self):
        """Test sprawdza czy utworzymy posiłęk bez logowania."""
        url = reverse("menus-meal-list", kwargs={"parent_lookup_menu": 1})
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, 403)

    def test_get_detail_meal_should_return_200(self):
        """Test sprawdza czy wyświetlimy posiłek."""
        self.client.force_authenticate(user=self.user)
        menu = MenuFactory.create(name="Menu Jajeczne")
        meal = MealFactory.create(menu=menu)
        url = reverse("menus-meal-detail", kwargs={"parent_lookup_menu": menu.id, "pk": meal.id})

        response = self.client.get(url)
        #import ipdb; ipdb.set_trace()
        self.assertEqual(response.status_code, 200)

    def test_update_patch_no_exists_meal_should_return_404(self):
        """Test sprawdza czy zaktualizujemy nieistniejący posiłek."""
        self.client.force_authenticate(user=self.user)
        menu = MenuFactory.create(name="Menu Jajeczne")
        url = reverse("menus-meal-detail", kwargs={"parent_lookup_menu": menu.id, "pk": 123})

        response = self.client.patch(url, {"name": "Nowa Nazwa"})

        self.assertEqual(response.status_code, 404)

    def test_update_patch_exists_meal_should_return_200(self):
        """Test sprawdza czy zaktualizujemy nieistniejący posiłek."""
        self.client.force_authenticate(user=self.user)
        menu = MenuFactory.create(name="Menu Jajeczne")
        meal = MealFactory.create(menu=menu)
        menu.refresh_from_db()
        meal.refresh_from_db()

        url = reverse("menus-meal-detail", kwargs={"parent_lookup_menu": menu.id, "pk": meal.id})

        response = self.client.patch(url, {"name": "Nowa Nazwa"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "Nowa Nazwa")

    def test_delete_meal_return_204(self):
        """Test sprawdza czy usuniemy posiłęk z menu."""
        self.client.force_authenticate(user=self.user)
        menu = MenuFactory.create(name="Menu Jajeczne")
        meal = MealFactory.create(menu=menu)
        menu.refresh_from_db()
        meal.refresh_from_db()

        url = reverse("menus-meal-detail", kwargs={"parent_lookup_menu": menu.id, "pk": meal.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Meal.objects.count(), 0)