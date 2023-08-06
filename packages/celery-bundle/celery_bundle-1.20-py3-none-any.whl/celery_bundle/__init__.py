from applauncher.kernel import KernelReadyEvent, KernelShutdownEvent, Configuration
from applauncher.kernel import Kernel
from celery import Celery, signals
import inject

@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass

class CeleryBundle(object):
    def __init__(self):


        self.config_mapping = {
            "celery": {
                "broker": 'pyamqp://guest@localhost//',
                "result_backend": "",
                "debug": False,
                "worker": True,
                "queues": ["celery"],
                "task_routes": [{
                    "pattern": None,
                    "queue": None
                }],
                "task_serializer": "json",
                "accept_content": ['json'],
                "result_serializer": ['json'],
                "result_expires": 3600, # 1 hour
                "timezone": 'Europe/Madrid',
                "concurrency": 0,
                "worker_max_tasks_per_child": -1,
            }
        }

        self.event_listeners = [
            (KernelReadyEvent, self.kernel_ready),
            (KernelShutdownEvent, lambda e: self.app.control.shutdown())
        ]

        self.app = Celery()
        self.app.log.setup()
        self.injection_bindings = {
             Celery: self.app
        }

    @inject.params(config=Configuration)
    def start_sever(self, config):
        # Register mappings
        kernel = inject.instance(Kernel)
        for bundle in kernel.bundles:
            if hasattr(bundle, "register_tasks"):
                getattr(bundle, "register_tasks")()

        tasks_per_child = config.celery.worker_max_tasks_per_child
        if tasks_per_child == -1:
            tasks_per_child = None
            
        self.app.conf.update(
            broker_url=config.celery.broker,
            result_backend=config.celery.result_backend,
            task_track_started=True,
            result_expires=config.celery.result_expires,
            task_serializer=config.celery.task_serializer,
            accept_content=config.celery.accept_content,  # Ignore other content
            result_serializer=config.celery.task_serializer,
            timezone=config.celery.task_serializer.timezone,
            enable_utc=True,
            task_acks_late=True,
            worker_max_tasks_per_child=tasks_per_child
        )

        if len(config.celery.task_routes) > 0:
            task_routes = {}
            for route in config.celery.task_routes:
                task_routes[route.pattern] = route.queue
            self.app.conf.update({"task_routes": task_routes})

        if config.celery.worker:
            argv = [
                'worker',
            ]
            if config.celery.debug:
                argv.append('--loglevel=DEBUG')

            if len(config.celery.queues) > 0:
                argv.append("-Q")
                argv.append(",".join(config.celery.queues))

            if config.celery.concurrency > 0:
                argv.append("--concurrency={concurrency}".format(concurrency=config.celery.concurrency))

            self.app.worker_main(argv)

    @inject.params(kernel=Kernel)
    def kernel_ready(self, event, kernel):
        config = inject.instance(Configuration).celery
        if config.worker:
            kernel.run_service(self.start_sever)
        else:
            self.start_sever()




