import os
import sys
from functools import partial as _partial, lru_cache
import importlib._bootstrap_external
from importlib.machinery import PathFinder
from importlib.util import find_spec
from importlib import invalidate_caches, import_module
import logging
import locale
from datetime import timedelta
from pathlib import Path
from contextlib import contextmanager
from string import ascii_lowercase
from random import sample
import yaml.nodes
import yaml.constructor
import attr
import devconfig
import devconfig.merge

import pkg_resources

_log = logging.getLogger(__name__)

DEFAULT_STRJOIN_DELIMITER = ''
DEFAULT_FILE_ENCODING = locale.getpreferredencoding(False)


def envvar(loader, delimiter, node):
    varname = delimiter[delimiter.index(':') + 1:]
    if isinstance(node, yaml.nodes.MappingNode):
        envvar_config = loader.construct_mapping(node)
    elif isinstance(node, yaml.nodes.ScalarNode):
        envvar_config = {}
    else:
        raise yaml.constructor.ConstructorError('unknown !envvar format')

    construct = _partial(envvar_config.get('constructor', lambda x:x))
    if 'default' in envvar_config:
        return construct(os.environ.get(varname, envvar_config['default']))
    else:
        return construct(os.environ[varname])

def yaml_file_finder(cls, extensions):
    current_loaders = importlib._bootstrap_external._get_supported_file_loaders()
    current_loaders.append((cls, extensions))
    sys.path_hooks[-1] = importlib.machinery.FileFinder.path_hook(*current_loaders)
    invalidate_caches()
    for name in [name for name in sys.path_importer_cache]:
        del sys.path_importer_cache[name]

def module_extend(loader, delimiter, node):

    extended_module_name = node.tag.rsplit(':', 1)[-1].strip()
    _log.debug(loader.module['spec']['name'],
                extra={ 'extends': extended_module_name,
                        'spec': loader.module})
    if not extended_module_name:
        return loader.construct_mapping(node, deep=True)

    if extended_module_name in sys.modules:
        extended_module_mapping = dict(
            ((k,v) for (k,v) in sys.modules[extended_module_name].__dict__.items() 
                 if not k.startswith('__')))
        return devconfig.merge.mappings(loader.construct_mapping(node, deep=True), extended_module_mapping)
    else:
        extended_module_spec = find_spec(extended_module_name)
        if extended_module_spec is None:
            return loader.construct_mapping(node, deep=True)

        extended_module_path = extended_module_spec.origin
        with open(extended_module_path) as stream:
            extended_module_node = next(devconfig.documents(stream))
            devconfig.merge.extend_node(node, extended_module_node)
        return loader.construct_object(extended_module_node, deep=True)


def strjoin_from_mapping(loader, nodes, default_delimiter=DEFAULT_STRJOIN_DELIMITER):
    joined = []
    for node in nodes.value:
        if isinstance(node[1], yaml.nodes.SequenceNode):
            joined.extend(loader.construct_object(node[1]))

    delimiter = loader.construct_mapping(nodes).get('delimiter', default_delimiter)
    return delimiter.join(str(i) for i in joined)


def strjoin_from_sequence(loader, items, delimiter, default_delimiter=DEFAULT_STRJOIN_DELIMITER):
    if not delimiter:
        delimiter = default_delimiter
    elif delimiter == ':':
        delimiter = ' '
    else:
        delimiter = delimiter[1:] if delimiter[0] == ':' else delimiter
    items = loader.construct_sequence(items)
    return str(delimiter).join(str(i) for i in items)


def strjoin(loader, delimiter, node):
    if isinstance(node, yaml.nodes.SequenceNode):
        return strjoin_from_sequence(loader, node, delimiter)
    elif isinstance(node, yaml.nodes.MappingNode):
        return strjoin_from_mapping(loader, node)
    raise yaml.constructor.ConstructorError('attempt to !strjoin on node with unknown layout')


def timedelta(loader, node):
    '''Timedelta constructor

config:
```
wait: !timedelta 2h
```
usage in code:
```
from datetime import timedelta
assert config['wait'] == timedelta(hours=2)
```

> available codes: d, h, w, m, s
    '''

    item = loader.construct_object(node)

    if not isinstance(item, str) or not item:
        raise yaml.constructor.ConfigurationError(
            "value '%s' cannot be interpreted as date range" % item)
    num, typ = item[:-1], item[-1].lower()

    if not num.isdigit():
        raise yaml.constructor.ConfigurationError(
            "value '%s' cannot be interpreted as date range" % item)

    num = int(num)

    if typ == "d":
        return timedelta(days=num)
    elif typ == "h":
        return timedelta(seconds=num * 3600)
    elif typ == "w":
        return timedelta(days=num * 7)
    elif typ == "m":
        return timedelta(seconds=num * 60)
    elif typ == "s":
        return timedelta(seconds=num)
    else:
        raise yaml.constructor.ConfigurationError(
            "value '%s' cannot be interpreted as date range" % item)


def file_contents(loader, coding, node, default_coding=DEFAULT_FILE_ENCODING):
    if not coding or coding==':':
        coding = default_coding
    else:
        coding = coding[1:] if coding[0] == ':' else coding

    with io.open(loader.construct_object(node), encoding=coding) as file_contents:
        return file_contents.read()


def asset(loader, node):
    _path = Path(pkg_resources.resource_filename(loader.module['package'], '')).resolve()
    if isinstance(node, yaml.nodes.ScalarNode):
        return _path / loader.construct_scalar(node)
    elif isinstance(node, yaml.nodes.SequenceNode):
        for _sub in loader.construct_sequence(node):
            _path = _path / _sub
        return _path
    else:
        raise yaml.constructor.ConstructorError('unknown !path format')


def partial(loader, node):
    config = loader.construct_mapping(node, deep=True)
    return _partial(config['callable'], *config.get('args', ()), **config.get('kwargs', {}))

def path(loader, delimiter, node):
    if not delimiter or delimiter == ':':
        _root = ''
    else:
        _root = delimiter[1:] if delimiter[0] == ':' else delimiter
    _path = Path(_root)
    
    if isinstance(node, yaml.nodes.ScalarNode):
        return _path / loader.construct_scalar(node)
    elif isinstance(node, yaml.nodes.SequenceNode):
        for _sub in loader.construct_sequence(node):
            _path = _path / _sub
        return _path
    else:
        raise yaml.constructor.ConstructorError('unknown !path format')
path.__doc__ = Path.__doc__

def dir(loader, delimiter, node):
    _path = path(loader, delimiter, node)
    _current = Path('.').resolve()
    @contextmanager
    def _dir(create=False, exist_ok=False):
        if create:
            os.makedirs(_path, exist_ok=exist_ok)
        os.chdir(_path)
        try:
            yield _path
        finally:
            os.chdir(_current)
    _dir._current = _current
    _dir._path = _path
    return _dir

@lru_cache(maxsize=1)
def fstring_globals():
    merges = [dict([(k,v) for k,v in __builtins__.items() if not k.startswith('__')])]
    for devconfig_ep in pkg_resources.iter_entry_points('devconfig'):
        if devconfig_ep.name == 'fstring':
            mod_dict = import_module(devconfig_ep.module_name).__dict__
            merges.append(dict([(k, v) for k,v in mod_dict.items() if not k.startswith('__')]))
    return devconfig.merge.mappings(*merges)

def fstring(loader, node):
    f = loader.construct_scalar(node)
    return _partial(eval, f'''f"{f}"''', fstring_globals())

def attrib(loader, node):
    if isinstance(node, yaml.nodes.MappingNode):
        return attr.ib(**loader.construct_mapping(node, deep=True))
    elif isinstance(node, yaml.nodes.ScalarNode):
        return attr.ib(*loader.construct_sequence(node, deep=True))
    else:
        return attr.ib(default=loader.construct_scalar(node))
attrib.__doc__ = attr.ib.__doc__


def attrs(loader, node):
    return attr.s(**loader.construct_mapping(node, deep=True))
attrs.__doc__ = attr.s.__doc__


def merged(loader, node):
    return devconfig.merge.mappings(*loader.construct_sequence(node))
merged.__doc__ = devconfig.merge.mappings.__doc__

def getattribute(loader, delimiter, node):
    if not delimiter.startswith(':'):
        raise yaml.constructor.ConstructorError('unknown !getattribute format')
    else:
        delimiter = delimiter[1:]
    attr_name = loader.construct_scalar(node)
    node.value = None
    return getattr(loader.construct_python_name(delimiter, node), attr_name)
