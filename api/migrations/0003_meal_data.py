import random
from django.db import migrations

MEAL_DATA = [
    (
        "Łosoś w galarecie",
        "Łosoś w galarecie to nie tylko piękne, ale i pyszne danie, które podajemy na zimno. Można więc zrobić go wcześniej i serwować w dowolnym momencie. Przepis ten idealnie sprawdzi się na specjalne okazje oraz na Święta.",
        12.50,
        True,
        60
    ),
    (
        "Karkówka pieczona",
        "Karkówka pieczona w całości to świetny pomysł nie tylko na pyszny obiad, ale i na domową wędlinę na kanapki. Przepis jest bardzo prosty, a karczek z rękawa wychodzi soczysty i aromatyczny.",
        35.50,
        False,
        400
    ),
    (
        "Herbata z imbirem",
        "Pyszna i rozgrzewająca herbata z imbirem to świetny napój na chłodniejsze dni. Przepis jest bardzo uniwersalny, ponieważ podaję kilka sposobów na przygotowanie imbirowej herbatki.",
        5.50,
        False,
        10
    ),
    (
        "Szakszuka",
        "Szakszuka to jeden z pyszniejszych pomysłów na zdrowe śniadanie. Przepis jest niezwykle prosty, a shakshuka super smaczna i efektowana. To połącznie jajek i pomidorów w najlepszym wydaniu. ",
        13.50,
        True,
        30
    ),
]


def prepare_meal_data(name, description, price, is_vege, prepartion_time, menu_qs):
    menus_id = [id for id in menu_qs.values_list('id', flat=True)]
    menu_id = random.choice(menus_id)
    return {
        "name": name,
        "description": description,
        "price": price,
        "is_vege": is_vege,
        "prepartion_time": prepartion_time,
        "menu_id": menu_id,
    }


def forwards_func(apps, schema_editor):
    Meal = apps.get_model("api", "Meal")
    Menu = apps.get_model("api", "Menu")

    db_alias = schema_editor.connection.alias
    menu_qs = Menu.objects.using(db_alias)
    [
        Meal.objects.using(db_alias).create(**data)
        for data in [
            prepare_meal_data(name, description, price, is_vege, prepartion_time, menu_qs)
            for name, description, price, is_vege, prepartion_time in MEAL_DATA
        ]
    ]


def reverse_func(apps, schema_editor):
    Meal = apps.get_model("api", "Meal")
    db_alias = schema_editor.connection.alias
    Meal.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_menu_data"),
    ]
    operations = [migrations.RunPython(forwards_func, reverse_func)]
