from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Add product to the database'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()
        category, _ = Category.objects.get_or_create(name = 'Пылесосы', description = 'Категория пылесосов')

        products = [
            {'name': 'Polaris', 'description': 'Станет надежным помощником при уборке в доме и не только.',
             'category': category , 'price': 35000},
            {'name': 'Dreame H13 Pro', 'description': 'Мощный многофункциональный пылесос для сухой и влажной уборки.',
             'category': category, 'price': 40000}
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Available in stock: {product.name}'))