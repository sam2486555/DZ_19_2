from django.db import models


class Product(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Наименование продукта",
        help_text="Введите название продукта",
    )

    desk = models.CharField(
        max_length=100,
        verbose_name="Описание продукта",
        help_text="Введите описание продукта",
    )

    image = models.ImageField(
        upload_to="product/photo",
        blank=True,
        null=True,
        verbose_name="Изображение(превью)",
        help_text="Загрузите изображение продукта",
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите Категорию продукта",
        null=True,
        blank=True,
        related_name="products",
    )

    price = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Цена за покупку",
        help_text="Введите Цену за покупку продукта",
    )

    created_at = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата создания(записи в БД)",
        help_text="Введите Дату создания продукта",
    )

    updated_at = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата последнего изменения(записи в БД)",
        help_text="Введите Дату последнего изменения продукта",
    )

    manufactured_at = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата производства продукта",
        help_text="Введите Дата производства продукта",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "title"]


class Category(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Наименование категории",
        help_text="Введите название категории",
    )

    desk = models.TextField(
        verbose_name="Описание категории", help_text="Введите описание категории"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
