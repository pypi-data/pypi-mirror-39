# -*- coding: utf-8 -*-
import importlib
import inspect
import os
import os.path as path
import hashlib
import sys
import dill as pickle


if sys.version_info.major == 2:
    from codecs import open
    PY_SYSVER = 2

elif sys.version_info.major == 3:
    import importlib
    PY_SYSVER = 3


class Experiment(object):
    def __init__(self, name, module_path, module=None):
        self.name = name
        self.module_path = module_path
        self.module = module
        self.default_params = None
        self.param_dict = None
        self.paramsets = None
        self.exp_dir = None
        self.subexp_dirs = None
        self.success = False
        self.analyses = {}

    def update(self, dict_of_values):
        for key, val in dict_of_values.items():
            assert hasattr(self, key), '\'{}\' is not an Experiment parameter'.format(key)
            setattr(self, key, val)


class Analysis(object):
    def __init__(self, name, module_path, module=None):
        self.name = name
        self.module_path = module_path
        self.module = module
        self.experiments = {}
        self.success = False


class Status(object):
    def __init__(self):
        self.activity = None
        self.focus = None
        self.sub_index = None
        self.data_dir = None
        self.parameters = None
        self.tripping = None
        self.ready = False


class Constants(object):
    def __init__(self, dict_of_vals):
        self._asdict = dict(dict_of_vals)
        for key, val in self._asdict.items():
            setattr(self, key, val)

    def __dict__(self):
        return dict(self._asdict)

    def __getitem__(self, item):
        return self._asdict[item]

    def keys(self):
        return self._asdict.keys()

    def values(self):
        return self._asdict.values()

    def items(self):
        return self._asdict.items()


class Alias(object):
    def __init__(self, name, aliases):
        self.name = str(name)
        self.aliases = list(aliases)

    def __contains__(self, item):
        return True if item in self.aliases else False

    def __repr__(self):
        return self.name

    def __add__(self, other):
        assert isinstance(other, (Alias, list, tuple))
        return self.aliases + list(other)

    def __iter__(self):
        return self.aliases.__iter__()

    def __eq__(self, other):
        return self.__contains__(other)


def _get_live_package_object(package_path):
    # module_dir = path.split(module_path)[0]
    # opwd = os.getcwd()
    # os.chdir(module_dir)
    spec = importlib.util.spec_from_file_location(
        path.split(package_path)[-1].rstrip('/'),
        location=package_path+os.sep + '__init__.py')
    package = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(package)
    # os.chdir(opwd)
    return package


# def _get_mainfn_sig(modulepath):
#     raise DeprecationWarning
#     live_module = _get_live_module_object(modulepath)
#     sig = inspect.signature(live_module.main)
#     del live_module
#     return sig


# def _get_module_obj(modulepath, obj_name):
#     module = _get_live_module_object(modulepath)
#     if hasattr(module, obj_name):
#         return getattr(module, obj_name)
#     else:
#         return None


def digest_file(filename):
    if PY_SYSVER == 3:
        return hashlib.sha1(open(filename, 'rb').read()).hexdigest()
    elif PY_SYSVER == 2:
        return hashlib.sha1(open(filename, 'r', encoding='utf-8').read()).hexdigest()


def digest_string(string):
    return hashlib.sha1(string.encode('utf-8')).hexdigest()


def pickle_dump(item, filepath):
    if PY_SYSVER == 3:
        return pickle.dump(item, open(filepath, mode='wb'), 2)
    elif PY_SYSVER == 2:
        return pickle.dump(item, open(filepath, mode='w'), 2)


def pickle_load(filepath):
    if PY_SYSVER == 3:
        return pickle.load(open(filepath, mode='rb'), 2)
    elif PY_SYSVER == 2:
        return pickle.load(open(filepath, mode='r'), 2)
