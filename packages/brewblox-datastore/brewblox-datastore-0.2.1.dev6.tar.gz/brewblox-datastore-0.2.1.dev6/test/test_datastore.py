"""
Tests brewblox_datastore.datastore
"""

import asyncio
import json
from tempfile import NamedTemporaryFile

import pytest
from brewblox_service import features, scheduler

from brewblox_datastore import datastore
from brewblox_datastore.datastore import FileStore

TESTED = datastore.__name__


@pytest.fixture
def items():
    return {
        'key1': 'val',
        'container_list': [
            {
                'id': 'testey',
                'value': 'testey',
            },
        ],
        'container_dict': {},
        'container_invalid': 'text',
    }


@pytest.fixture()
def temp_p_file(items):
    f = NamedTemporaryFile(mode='w+t', encoding='utf8')
    f.write(json.dumps(items))
    f.flush()
    yield f.name
    f.close()


@pytest.fixture()
def temp_v_file(items):
    f = NamedTemporaryFile(mode='w+t', encoding='utf8')
    f.write(json.dumps(items))
    f.flush()
    yield f.name
    f.close()


@pytest.fixture
async def app(app, loop, mocker, items, temp_p_file, temp_v_file):
    mocker.patch(TESTED + '.FLUSH_DELAY_S', 0.01)
    app['config']['file'] = temp_p_file
    app['config']['volatile'] = False

    scheduler.setup(app)
    datastore.setup(app)

    features.add(app, FileStore(app, temp_v_file, False), 'volatile')
    return app


@pytest.fixture
async def p_store(app) -> FileStore:
    return datastore.get_store(app)


@pytest.fixture
async def v_store(app) -> FileStore:
    return features.get(app, key='volatile')


def read_file(fname):
    with open(fname) as f:
        data = json.load(f)
    return data


async def response(request):
    retv = await request
    assert retv.status < 400
    return await retv.json()


async def test_read_write_persistent(app, client, items, p_store: FileStore, temp_p_file):
    assert p_store.data == items
    assert p_store.active
    p_store.data['p_key'] = True
    assert p_store.data['p_key'] is True
    p_store.changed()

    await asyncio.sleep(0.2)

    with open(temp_p_file) as f:
        assert json.load(f) == p_store.data


async def test_read_write_volatile(app, client, items, v_store: FileStore, temp_v_file):
    assert v_store.data == items
    assert not v_store.active
    v_store.data['v_key'] = True
    assert v_store.data['v_key'] is True
    v_store.changed()

    await asyncio.sleep(0.2)

    with open(temp_v_file) as f:
        assert json.load(f) == items


async def test_load_error(app, client, mocker):
    open_mock = mocker.patch(TESTED + '.open')

    open_mock.side_effect = RuntimeError
    with pytest.raises(RuntimeError):
        FileStore(app, 'filey', True)

    open_mock.side_effect = FileNotFoundError
    with pytest.raises(FileNotFoundError):
        FileStore(app, 'filey', True)


async def test_write_error(app, client, p_store, mocker):
    save_mock = mocker.patch.object(p_store, 'write_file')
    save_mock.side_effect = RuntimeError

    p_store.changed()

    await asyncio.sleep(0.1)
    assert save_mock.call_count > 0
    assert p_store.active


@pytest.mark.parametrize('container', [
    'container_list',
    'container_dict',
])
async def test_crud(container, app, client, p_store, items, mocker):
    change_spy = mocker.spy(p_store, 'changed')
    item = {
        'id': 'testex',
        'value': {
            'nested': {
                'object': True,
            },
        },
    }

    assert await response(client.get(f'/{container}')) == items[container]
    assert await response(client.get('/container_invalid')) == items['container_invalid']

    assert await response(client.post(f'/{container}', json=item)) == item
    assert await response(client.get(f'/{container}/testex')) == item
    assert change_spy.call_count == 1

    with pytest.raises(AssertionError):
        await response(client.post(f'/{container}', json=item))

    assert await response(client.patch(f'/{container}/testex', json={'k': True})) == {**item, 'k': True}
    assert await response(client.get(f'/{container}/testex')) == {**item, 'k': True}
    assert change_spy.call_count == 2

    assert await response(client.put(f'/{container}/testex', json={'v': True})) == {'id': 'testex', 'v': True}
    assert await response(client.get(f'/{container}/testex')) == {'id': 'testex', 'v': True}
    assert change_spy.call_count == 3

    assert await response(client.delete(f'/{container}/testex')) == {}
    with pytest.raises(AssertionError):
        await response(client.get(f'/{container}/testex'))
    assert change_spy.call_count == 4

    with pytest.raises(AssertionError):
        await response(client.delete(f'/{container}/testex'))

    with pytest.raises(AssertionError):
        await response(client.post(f'/{container}', json='text'))

    with pytest.raises(AssertionError):
        await response(client.put(f'/{container}/testey', json='text'))

    with pytest.raises(AssertionError):
        await response(client.patch(f'/{container}/testey', json='text'))

    with pytest.raises(AssertionError):
        await response(client.post('/container_invalid', json=item))

    with pytest.raises(AssertionError):
        await response(client.get('/container_invalid/testey'))

    assert change_spy.call_count == 4
