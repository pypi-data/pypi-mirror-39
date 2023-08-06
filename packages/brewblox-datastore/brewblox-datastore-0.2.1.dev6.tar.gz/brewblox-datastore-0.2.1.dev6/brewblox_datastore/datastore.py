"""
Persistent configuration. Is read from file on startup, and then periodically flushes changes to file.
"""

import asyncio
import json
import warnings
from concurrent.futures import CancelledError
from typing import Any, Hashable, Tuple

import aiofiles
from aiohttp import web
from brewblox_service import brewblox_logger, features, scheduler

FLUSH_DELAY_S = 5

LOGGER = brewblox_logger(__name__)
routes = web.RouteTableDef()


def setup(app: web.Application):
    config = FileStore(app, app['config']['file'], not app['config']['volatile'])
    features.add(app, config)
    app.router.add_routes(routes)


def get_store(app: web.Application) -> 'FileStore':
    return features.get(app, FileStore)


class FileStore(features.ServiceFeature):

    def __init__(self, app: web.Application, filename: str, persistent: bool):
        features.ServiceFeature.__init__(self, app)
        self._data: dict = {}
        self._persistent: bool = persistent
        self._filename: str = filename
        self._flush_task: asyncio.Task = None
        self._changed_event: asyncio.Event = None

        try:
            self.read_file()
        except FileNotFoundError:
            LOGGER.error(f'{self} file not found.')
            raise
        except Exception:
            LOGGER.error(f'{self} unable to read objects.')
            raise

    def __str__(self):
        return f'<{type(self).__name__} for {self._filename}>'

    @property
    def active(self):
        return self._flush_task and not self._flush_task.done()

    @property
    def data(self):
        return self._data

    def changed(self):
        if self._changed_event:
            self._changed_event.set()

    def read_file(self):
        with open(self._filename) as f:
            self._data = json.load(f)

    async def write_file(self):
        async with aiofiles.open(self._filename, mode='w') as f:
            await f.write(json.dumps(self._data, indent=2))

    async def _autoflush(self):
        while True:
            try:
                await self._changed_event.wait()
                await asyncio.sleep(FLUSH_DELAY_S)
                await self.write_file()
                self._changed_event.clear()

            except CancelledError:
                await self.write_file()
                break

            except Exception as ex:
                warnings.warn(f'{self} {type(ex).__name__}({ex})')

    async def startup(self, app: web.Application):
        await self.shutdown(app)
        if self._persistent:
            self._changed_event = asyncio.Event()
            self._flush_task = await scheduler.create_task(app, self._autoflush())

    async def shutdown(self, app: web.Application):
        self._changed_event = None
        await scheduler.cancel_task(app, self._flush_task)


async def parse_content_dict(request: web.Request) -> dict:
    content = await request.json()
    if not isinstance(content, dict):
        raise TypeError(f'Content must be an object, not {type(content).__name__}')
    return content


def find_node(container, id) -> Tuple[Hashable, Any]:
    if isinstance(container, dict):
        return id, container.get(id)

    if isinstance(container, list):
        for idx, o in enumerate(container):
            if o.get('id') == id:
                return idx, o
        return len(container), None

    raise TypeError(f'Invalid container type: {type(container).__name__}')


@routes.view(r'/{container:(?!_system)[^/]+}')
class ContainerView(web.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._store = get_store(self.request.app)
        self._container_id = self.request.match_info['container']

    async def get(self) -> web.Response:
        return web.json_response(self._store.data[self._container_id])

    async def post(self) -> web.Response:
        content = await parse_content_dict(self.request)
        container = self._store.data[self._container_id]

        node_id = content['id']
        node_key, existing = find_node(container, node_id)

        if existing is not None:
            raise KeyError(f'Key {node_id} already present')

        if isinstance(container, dict):
            container[node_id] = content
        elif isinstance(container, list):
            container.append(content)
        else:  # pragma: no cover
            raise RuntimeError('Unreachable code reached')

        self._store.changed()
        return web.json_response(content)


@routes.view(r'/{container:(?!_system)[^/]+}/{node:[^/]+}')
class NodeView(web.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._store = get_store(self.request.app)

        self._container_id = self.request.match_info['container']
        self._node_id = self.request.match_info['node']

        self._container = self._store.data[self._container_id]
        self._node_key, self._node = find_node(self._container, self._node_id)

        if self._node is None:
            raise KeyError(f'Object {self._node_id} not found')

    async def get(self) -> web.Response:
        return web.json_response(self._node)

    async def put(self) -> web.Response:
        content = await parse_content_dict(self.request)
        content['id'] = self._node_id
        self._container[self._node_key] = content
        self._store.changed()
        return web.json_response(content)

    async def patch(self) -> web.Response:
        content = await parse_content_dict(self.request)
        content['id'] = self._node_id
        self._node.update(content)
        self._store.changed()
        return web.json_response(self._node)

    async def delete(self) -> web.Response:
        del self._container[self._node_key]
        self._store.changed()
        return web.json_response({})
