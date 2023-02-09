from django.db import models
from django.contrib.auth.models import User  # Импорт встроенной модели
from django.db.models import Sum  # Импорт функции для суммирования


# Создание сущности "Автор" в БД (для создания сущностей в БД через ООП, нужно наследоваться от "models.Model")
class Author(models.Model):
    autorUsers = models.OneToOneField(User, on_delete=models.CASCADE)  # Отношения Один к Одному. Первый параметр
    # указывает, с какой моделью будет ассоциирована данная сущность (модель User). Второй параметр on_delete =
    # models.CASCADE говорит, что данные текущей модели (autorUsers) будут удаляться в случае удаления связанного
    # объекта главной модели (User)
    ratingAuthor = models.SmallIntegerField(default=0)  # SQLite: smallint NOT NULL, хранит целочисленные значения
    # типа Number. По дефолту ноль

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))  # Данное поле записывает сумму всех данных
        # поля "рейтинг" модели "Публикация" со значением в формате queryset
        pRat = 0  # Промежуточная переменная
        pRat += postRat.get('postRating')  # в которую записываем извлеченные данные методом "get" из postRating

        commentRat = self.autorUsers.comment_set.aggregate(commentRating=Sum('rating'))  # Данное поле записывает
        # сумму всех данных поля "рейтинг" модели "Комментарии", обращаемся через поле autorUsers
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat  # Суммируем переменные
        self.save()  # Сохраняем


# Создание сущности "Категория" в БД
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)  # SQLite: varchar(N) NOT NULL, хранит строку не более
    # N-символов (2 в n-степени). Максимальная длинна 64, уникальное значение


# Создание сущности "Публикация" в БД
class Post(models.Model):
    # Создаем две переменные вида публикаций: NW - news(новость) или AR - article(статья). Эти значения будут в БД
    news = 'NW'
    article = 'AR'

    # Создаем список выбора вида публикаций
    category_choices = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]

    categoryType = models.CharField(max_length=2, choices=category_choices, default=article)  # Выбор из списка
    # "category_choices", по умолчанию - статья
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Создаем связь Один ко Многим поля author через
    # внешний ключ с моделью Author (первый параметр), второй параметр: on_delete, задает опцию удаления объекта
    # текущей модели при удалении связанного объекта главной модели
    dateCreation = models.DateTimeField(auto_now_add=True)  # SQLite: datetime NULL. Автоматически добавляем
    # временное поле, которое хранит время и дату, при создании экземпляра
    postCategory = models.ManyToManyField(Category, through='PostCategory')  # Отношения Многие ко Многим сущности
    # Category через PostCategory.
    title = models.CharField(max_length=128)  # Поле с оглавлением, максимальная длинна символов - 128
    text = models.TextField()  # Поле с текстом, максимальная длинна символов - неограниченно
    rating = models.SmallIntegerField(default=0)  # SQLite: smallint NOT NULL, хранит целочисленные значения
    # типа Number. По дефолту ноль

    # Метод рейтинга
    def like(self):
        self.rating += 1  # Увеличиваем рейтинг при вызове
        self.save()  # Сохраняем рейтинг

    # Метод рейтинга
    def dislike(self):
        self.rating -= 1  # Уменьшаем рейтинг при вызове
        self.save()  # Сохраняем рейтинг

    # Метод превью
    def preview(self):
        return f'{self.text[:123]} + {"..."}'  # Через f-строки выводим превью текста из 123 символов и добавляем
        # многоточие в конце


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)  # Создаем связь Один ко Многим поля postThrough
    # через внешний ключ с моделью Post (первый параметр), второй параметр: on_delete
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)  # Создаем связь Один ко Многим поля
    # categoryThrough через внешний ключ с моделью Category (первый параметр), второй параметр: on_delete


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)  # Создаем связь Один ко Многим поля
    # commentPost через внешний ключ с моделью Category (первый параметр), второй параметр: on_delete
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)  # Создаем связь Один ко Многим поля
    # commentUser через внешний ключ с моделью User (выбираем сущность User, а не Author, чтобы оставлять комментарии
    # могли все пользователи, а не только авторы), второй параметр: on_delete
    text = models.TextField()  # Поле с текстом комментария, максимальная длинна символов - неограниченно
    dateCreation = models.DateTimeField(auto_now_add=True)  # SQLite: datetime NULL. Автоматически добавляем
    # временное поле, которое хранит время и дату, при создании экземпляра
    rating = models.SmallIntegerField(default=0)  # SQLite: smallint NOT NULL, хранит целочисленные значения
    # типа Number. По дефолту ноль

    # Метод рейтинга
    def like(self):
        self.rating += 1  # Увеличиваем рейтинг при вызове
        self.save()  # Сохраняем рейтинг

    # Метод рейтинга
    def dislike(self):
        self.rating -= 1  # Уменьшаем рейтинг при вызове
        self.save()  # Сохраняем рейтинг
# Create your models here.
