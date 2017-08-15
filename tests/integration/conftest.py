import pytest

from kore import config_factory, container_factory


@pytest.fixture(scope='session')
def motor_config():
    return {
        'url': 'localhost',
    }


@pytest.fixture(scope='session')
def config(motor_config):
    return config_factory.create('dict', **{'motor': motor_config})


@pytest.fixture
def container(config):
    initial = {
        'config': config,
    }
    return container_factory.create(**initial)


@pytest.fixture
def asyncio_client(container):
    return container('kore.components.motor.asyncio.client')
