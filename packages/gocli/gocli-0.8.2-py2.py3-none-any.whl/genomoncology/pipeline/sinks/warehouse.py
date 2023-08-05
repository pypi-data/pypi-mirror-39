import asyncio
from multiprocessing import Process, Queue

from cytoolz.curried import curry
from cytoolz.curried import dissoc

from genomoncology.parse import DocType
from genomoncology.parse import ensures
from . import Sink

EOL = "EOL"


async def make_call(sdk, in_queue):
    unit = in_queue.get()

    while unit != EOL:
        await sdk.call_with_retry(
            sdk.warehouse_variants.create_warehouse_variants, data=unit
        )
        unit = in_queue.get()


def background_runner(state, queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    sdk = state.create_sdk(async_enabled=True, loop=loop)
    loop.run_until_complete(asyncio.gather(make_call(sdk, queue)))


@curry
class LoadWarehouseSink(Sink):
    def __init__(self, _, state, num_workers=10):
        self.queue = Queue(maxsize=1000)
        self.workers = []

        self.num_workers = num_workers
        self.build = state.build

        for _ in range(num_workers):
            worker = Process(
                target=background_runner, args=(state, self.queue)
            )
            worker.start()
            self.workers.append(worker)

    def close(self):
        for _ in range(self.num_workers):
            self.queue.put(EOL)

        for worker in self.workers:
            worker.join()

    def write(self, data):
        data = ensures.ensure_collection(data)
        data = filter(DocType.HEADER.is_not, data)
        data = [
            dissoc(d, "__type__", "__record__", "annotations") for d in data
        ]
        data = [{**d, "build": self.build} for d in data]

        self.queue.put(data)

        return data
