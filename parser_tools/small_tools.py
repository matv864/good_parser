from typing import List, Callable, Any

from config import main_logger
import time
import threading

# from local_types import Types_links


def time_wrapper(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result_func = func(*args, **kwargs)
        stop = time.time()
        duration = stop - start
        message = f"{func.__name__} with {args[0]} "
        message += f"has duration: {'%.1f' % duration}"
        main_logger.info(message)
        return result_func
    return wrapper


def try_decorator(func):
    def decor(*args, **kwargs):
        for _ in range(5):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                main_logger.error(f"{type(e)} --- {str(e)}")
        return None
    return decor


#     target: Callable[[int], None],
#     args: List[Any],
#     type_links: Types_links = None,
#     with_lock_file: bool = False
def multithreading(
    target: Callable[[int], None],
    args: List[Any],
    **kwargs: dict
) -> None:
    threads: List[threading.Thread] = []

    for arg in args:
        thread = threading.Thread(
            target=target,
            args=(arg, ),
            kwargs=kwargs
        )

        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
