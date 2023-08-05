from nameko.runners import ServiceRunner
from .controllers.data_mongo_controller import DataMongoController

RUNNER = ServiceRunner(config={})
RUNNER.add_service(DataMongoController)
