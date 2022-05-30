from googlepicturesaver.googlepicturesaver import *


def test_consoleapp_init():
    consoleapp = ConsoleApp()
    assert consoleapp.engine == 'Google'
    assert consoleapp.numbers_of_pictures == 15


