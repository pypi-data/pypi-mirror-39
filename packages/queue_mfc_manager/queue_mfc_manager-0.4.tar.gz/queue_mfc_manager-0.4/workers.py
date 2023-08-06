#
# module for launching workers.
#
#
# Copyright (c) 2018, Gavrilov S
# Licensed MIT License.
#

from json_tricks import loads
from worker_helpers import get_queue_manager_instance, get_file_manager
from multiprocessing import Process, Lock
import click
file_manager = get_file_manager()
manager = get_queue_manager_instance(file_manager)


@click.command()
@click.argument('count_workers', type=int, default=1)
def start_workers(count_workers):
    """
    :param count_workers: amount of workers which should run tusks
    """
    processes = []
    lock = Lock()
    for i in range(count_workers):
        p = Process(target=run_worker, args=(manager, lock))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

@click.command()
@click.argument('queue_name', type='str', default='tasks')
def delete_workers_from_queue(queue_name):
    manager.delete_all_tasks(queue_name)


def run_worker(manager, lock):
    """
    processing tasks from manager
    :param manager: QMnager object
    :param lock: lock object
    :return:
    """

    while True:
        lock.acquire()
        try:
            task_from_redis = manager.take_from_queue()
        finally:
            lock.release()
        if task_from_redis:
            json_from_redis = loads(task_from_redis.decode())
            task = manager.get_task(json_from_redis.function_name)
            call_task(task, json_from_redis)
        else:
            break


def call_task(current_task, object_json):
    """
    run current tuak with arguments
    :param current_task:
    :param object_json: Json
    :return:
    """

    position_args = object_json.arguments['positional']
    keyword_args = object_json.arguments['keyword']
    current_task(*position_args, **keyword_args)

