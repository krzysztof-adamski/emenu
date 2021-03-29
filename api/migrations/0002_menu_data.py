import random
from django.db import migrations

MENU_DATA = [
    (
        "Menu Wigilijne",
        "Święta Bożego Narodzenia to doskonała okazja na wyżerkę.",
    ),
    (
        "Menu Wielkanocne",
        "Jajeczko do jajeczka i mamy pyszne dania wielkanocne.",
    ),
    (
        "Puste Menu",
        "Menu czeka na uzupełnienie.",
    ),
]

def forwards_func(apps, schema_editor):
    Menu = apps.get_model("api", "Menu")
    db_alias = schema_editor.connection.alias
    [
        Menu.objects.using(db_alias).create(**data)
        for data in [
            {
                "name": name,
                "description": description
            } for name, description in MENU_DATA
        ]
    ]


def reverse_func(apps, schema_editor):
    Menu = apps.get_model("api", "Menu")
    db_alias = schema_editor.connection.alias
    Menu.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]
    operations = [migrations.RunPython(forwards_func, reverse_func)]
