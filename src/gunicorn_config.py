import multiprocessing


from uvicorn.workers import UvicornWorker


class PatchedUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "proxy_headers": True,
    }


WORKERS_PER_CORE: float = 2.0
MAX_WORKERS: int = 2
HOST = "0.0.0.0"
PORT: int = 3000


def get_workers_count(max_workers: int, workers_per_core: float) -> int:
    cores = multiprocessing.cpu_count()
    default_web_concurrency = workers_per_core * cores
    web_concurrency = max(int(default_web_concurrency), 2)
    if max_workers:
        web_concurrency = min(web_concurrency, max_workers)
    return web_concurrency


# Gunicorn config variables
loglevel = "info"
workers = get_workers_count(max_workers=MAX_WORKERS, workers_per_core=WORKERS_PER_CORE)
bind = f"{HOST}:{PORT}"
worker_tmp_dir = "/dev/shm"
graceful_timeout = 600
timeout = 1200
keepalive = 5
worker_class = "gunicorn_config.PatchedUvicornWorker"
