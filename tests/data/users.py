from faker import Faker

from dh_backend.models import User


def test_user():
    user = User(user_name="TestUser", password="Test", email="test@nomail.de")
    return user


def test_users(n: int = 50):
    fake = Faker(locale="de-DE")
    fake.seed(1234)

    users = []
    for i in range(n):
        profile = fake.profile()
        u = User(user_name=profile["username"], email=profile["mail"], password=fake.password())
        users.append(u)

    return users
