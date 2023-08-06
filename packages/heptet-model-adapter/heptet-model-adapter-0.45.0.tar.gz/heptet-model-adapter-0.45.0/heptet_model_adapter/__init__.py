import logging

from db_dump import get_mapper_schema
from heptet_app import ResourceManager, _add_resmgr_action, OperationArgument
from pyramid.config import PHASE3_CONFIG

from heptet_model_adapter.entity import EntityFormView
from sqlalchemy import String

from zope.interface import Interface

logger = logging.getLogger(__name__)


class IMapperInfo(Interface):
    pass


# class MapperInfo:
#     def __init__(self, **kwargs):


def _add_model_class(config, model_class, mount=True):
    schema = get_mapper_schema()
    mapper__ = model_class.__mapper__
    data = schema.dump(mapper__)
    mapper_info = schema.load(data)
    config.registry.registerUtility(mapper_info, IMapperInfo, mapper_info.local_table.key)
    if not mount:
        return
    resource = config.get_resource_context()
    if resource is None:
        logger.info("resource is none")
    assert resource is not None

    manager = ResourceManager(
        mapper_key=mapper_info.local_table.key,
        node_name=mapper_info.local_table.key,
        mapper_wrapper=mapper_info
    )
    manager.operation(name='form', view=EntityFormView,
                      args=[OperationArgument.SubpathArgument('action', String, default='create')])

    intr = config.introspectable('resource manager', manager.mapper_key, 'resource manager %s' % manager.mapper_key,
                                 'resource manager')
    config.action(('resource manager', manager.mapper_key), _add_resmgr_action, introspectables=(intr,),
                  args=(config, manager), order=PHASE3_CONFIG)

    #_add_resmgr_action(config, manager)



def includeme(config):
    config.add_directive('add_model_class', _add_model_class)
    config.include('.entity')
