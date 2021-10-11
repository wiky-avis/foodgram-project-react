from recipes.models import Tag


def create_users(django_user_model):
    django_user_model.objects.create_user(
        email="vpupkin@yandex.ru",
        username="vasya.pupkin",
        first_name="Вася",
        last_name="Пупкин",
        password="Qwerty123"
    )
    django_user_model.objects.create_user(
        email="vgaksentii@test.ru",
        username="vg",
        first_name="Victoria",
        last_name="Axentii",
        password="Qwerty123"
    )


def create_tags(user_client):
    tag = Tag.objects.create(name='Борщ', color='#ffffff', slug='borsh')
    data1 = {
        'name': {tag.name},
        'color': {tag.color},
        'slug': {tag.slug}
    }

    tag_2 = Tag.objects.create(name='Суп', color='#ff00ff', slug='sup')
    data2 = {
        'name': {tag_2.name},
        'color': {tag_2.color},
        'slug': {tag_2.slug}
    }
    return [data1, data2]
