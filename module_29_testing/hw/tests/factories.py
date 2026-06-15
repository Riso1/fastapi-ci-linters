import random
import factory
from app.models import Client, Parking


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.LazyFunction(
        lambda: random.choice([None, '1111 2222 3333 4444'])
    )
    car_number = factory.Faker('bothify', text='?###??')


class ParkingFactory(factory.Factory):
    class Meta:
        model = Parking

    address = factory.Faker('address')
    opened = factory.Faker('boolean')
    count_places = factory.Faker('random_int', min=1, max=100)
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places)
