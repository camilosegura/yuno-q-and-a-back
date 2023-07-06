from os import getenv
from .healthy_controller import HealthyController
from .example_controller import ExampleController

healthy_controller = HealthyController(getenv)
example_controller = ExampleController()
