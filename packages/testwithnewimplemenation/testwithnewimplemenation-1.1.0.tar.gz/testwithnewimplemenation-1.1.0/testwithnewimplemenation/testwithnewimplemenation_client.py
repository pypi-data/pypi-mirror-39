# -*- coding: utf-8 -*-

from .decorators import lazy_property
from .configuration import Configuration
from .controllers.simple_calculator_controller import SimpleCalculatorController

class TestwithnewimplemenationClient(object):

    config = Configuration

    @lazy_property
    def simple_calculator(self):
        return SimpleCalculatorController()



