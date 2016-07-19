import flask_transmute


class PetDBException(Exception):
    """ raised when there's a problem with the PetDB """
    pass


class Pet(object):

    def __init__(self, age, name, classification):
        self.age = age
        self.name = name
        self.classification = classification

    transmute_schema = {
        "properties": {
            "name": {"type": str},
            "classification": {"type": str},
            "age": {"type": int},
        },
        "required": ["age", "name", "classification"]
    }

    @staticmethod
    def from_transmute_dict(model):
        return Pet(model["age"], model["name"], model["classification"])


class PetDB(object):

    def __init__(self, url):
        self._url = url
        self._current_pet = None

    @flask_transmute.annotate({"index": int, "return": Pet})
    def get_pet(self, index):
        """ retrieve a pet found at index """
        if not self._current_pet:
            raise PetDBException("no pet found!")
        return self._current_pet

    @flask_transmute.annotate({"pet": Pet, "return": bool})
    @flask_transmute.updates
    def post_pet(self, pet):
        """ create a pet """
        self._current_pet = pet
        return True
