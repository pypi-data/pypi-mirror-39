import yaml
import yaml.constructor
import attr
import logging
import pkg_resources
from pathlib import Path
from operator import attrgetter
from functools import partial
from importlib.util import find_spec
from collections.abc import Mapping, Sequence
from contextvars import ContextVar
import attr

_log = logging.getLogger(__name__)

DEVCONFIG_NAMESPACE = "!tag:devconfig:"

class DevconfigLoader(yaml.Loader):
    extensions = []

attrs_logdict = partial(attr.asdict, filter=lambda attr,value: attr.name != 'name')

@attr.s
class YAMLObjectDeclarationBase(object):
    yaml_loader = DevconfigLoader
    handler = attr.ib()
    tag = attr.ib()
    def __setstate__(self, state):
        if isinstance(state, Mapping):
            self.__init__(**state)
        elif isinstance(state, Sequence):
            self.__init__(*state)
        else:
            self.__init__(state)

@attr.s
class ConstructorDeclaration(YAMLObjectDeclarationBase):
    def __attrs_post_init__(self):
        self.apply(context.loader)(self.tag, self.handler)
        _log.debug(f'declare', extra=dict(loader=context.loader, **attrs_logdict(self)))

@attr.s
class SingleConstructorDeclaration(yaml.YAMLObject, ConstructorDeclaration):
    yaml_tag = f'{DEVCONFIG_NAMESPACE}extend/with/constructor/single'
    apply = attrgetter('add_constructor')


@attr.s
class MultiConstructorDeclaration(yaml.YAMLObject, ConstructorDeclaration):
    yaml_tag = f'{DEVCONFIG_NAMESPACE}extend/with/constructor/multi'
    apply = attrgetter('add_multi_constructor')


@attr.s
class YAMLObjectDeclaration(yaml.YAMLObject, YAMLObjectDeclarationBase):
    yaml_tag = f'{DEVCONFIG_NAMESPACE}extend/with/object'
    name = attr.ib()
    attrs = attr.ib()
    result = attr.ib(default=None)
    def __attrs_post_init__(self):
        class YAMLObjectMixin(object):
            def __setstate__(_self, state):
                _self.__init__(**state)
            def __attrs_post_init__(_self):
                self.result = self.handler(**attr.asdict(_self))
                _log.debug(f'handled', extra=dict(yaml_tag=self.tag, **attrs_logdict(self)))

        YAMLObjectAttributes = attr.make_class(self.name+'Attributes',
                                               dict(((k, attr.ib()) for k in self.attrs)))
        c = attr.s(yaml.YAMLObjectMetaclass(self.name,
                    (yaml.YAMLObject, YAMLObjectAttributes, YAMLObjectMixin),
                    {'yaml_tag': self.tag, 'yaml_loader': context.loader}))
        _log.debug(f'declare',  extra=attrs_logdict(self))


class _LoaderContext(object):
    _stack = [DevconfigLoader, ]
    @classmethod
    def push(self, name='ContextedDevconfigLoader', bases=(), members={}):
        stacksize = len(self._stack)
        parent = self._stack[-1]
        members.update({
            'yaml_constructors': parent.yaml_constructors.copy(),
            'yaml_multi_constructors': parent.yaml_multi_constructors.copy(),
            'extensions': parent.extensions.copy()
            })
        return self._stack.append(type(f'{name}_{stacksize}', (DevconfigLoader,) + bases, members))

    @classmethod
    def pop(self):
        return self._stack.pop()

    @property
    def loader(self):
        return self._stack[-1]
context = _LoaderContext()

def documents(stream):
    loader = context.loader(stream)
    while loader.check_node():
        document = loader.get_node()
        try:
            if document.tag.startswith(f'{DEVCONFIG_NAMESPACE}extend'):
                loader.extensions.append(loader.construct_document(document))
            else:
                document.loader = loader
                yield document
        except yaml.constructor.ConstructorError as e:
            _log.exception(e)

for devconfig_ep in pkg_resources.iter_entry_points(__name__):
    if devconfig_ep.name == 'extend':
        for extend_name in devconfig_ep.extras:
            with open(Path(find_spec(devconfig_ep.module_name).origin).parent / extend_name) as extension:
                list(documents(extension))

