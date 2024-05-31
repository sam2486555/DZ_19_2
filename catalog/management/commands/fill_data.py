import json
from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    # Здесь мы получаем данные из фикстур с категориями и продуктами
    @staticmethod
    def json_read():
        with open('category.json', encoding='UTF-8') as file:
            return json.load(file)

    def handle(self, *args, **options):
        # Удаляем все категории
        Category.objects.all().delete()
        # Удаляем все продукты
        Product.objects.all().delete()
        # Создаём списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фикстуры для получения информации об одном объекте
        for category in Command.json_read():
            if category['model'] == 'catalog.category':
                category_for_create.append(
                    Category(pk=category['pk'], title=category['fields']['title'], desk=category['fields']['desk'])
                )
        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for product in Command.json_read():
            if product['model'] == 'catalog.product':
                product_for_create.append(
                    Product(title=product['fields']['title'], desk=product['fields']['desk'],
                            image=product['fields']['image'],

                            # получаем категорию из базы данных для корректной связки объектов
                            category=Category.objects.get(pk=product['fields']['category']),
                            price=product['fields']['price'], created_at=product['fields']['created_at'],
                            updated_at=product['fields']['updated_at'])
                )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
