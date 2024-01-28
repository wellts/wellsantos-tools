import importlib
import logging
import pkgutil
from functools import lru_cache
from importlib.machinery import SourceFileLoader
from os.path import dirname


def import_module(name: str):
    __import__(name)
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


@lru_cache()
def recursive_import_modules():
    log_level = logging.NOTSET
    path = dirname(dirname(dirname(dirname(__file__)))) + '/'
    for loader, module_name, is_pkg in pkgutil.walk_packages([path + 'app'], prefix='app.'):
        logging.log(log_level, 'loading_module: %s', module_name)
        module: SourceFileLoader = loader.find_module(module_name)
        name = module.path.replace(path, '').replace('.py', '').replace('/', '.').replace('.__init__', '')
        importlib.import_module(name)
