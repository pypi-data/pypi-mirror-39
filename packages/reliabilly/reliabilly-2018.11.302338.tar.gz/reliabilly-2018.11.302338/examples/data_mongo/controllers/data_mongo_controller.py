from reliabilly.settings import Settings
from reliabilly.controllers.data_controller import DataController


class DataMongoController(DataController):
    name = Settings.SERVICE_NAME
