import faker
from fake_gen.base import Callable
from fake_gen.errors import NoSuchDatatype

class FakeDataFactory(Callable):

    _FAKER_FACTORY = faker.Factory.create()

    def __init__(self, data_type):
        if not hasattr(self._FAKER_FACTORY, data_type):
            raise NoSuchDatatype(data_type)
        self._data_type = data_type
        faker_func = getattr(self._FAKER_FACTORY, data_type)
        super(FakeDataFactory, self).__init__(faker_func)
