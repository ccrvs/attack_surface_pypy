import multiprocessing
import pathlib

import invoke


@invoke.task
def up_locust(context, workers=1, locustfile=pathlib.Path('./benchmarks/locustfile.py')):
    base = 'locust -f {locustfile}'.format(locustfile=locustfile)
    if workers == 1:
        context.run(base)
    else:
        with multiprocessing.Pool(workers + 1) as pool:
            pool.map(context.run, [
                base + ' --master',
            ] + [
                base + ' --worker' for _ in range(workers)
            ])
        # run_master = base + ' --master & '
        # run_workers = " & ".join(base + ' --worker' for _ in range(workers))
        # context.run(run_master + run_workers)


benchmarks = invoke.Collection('benchmarks')
benchmarks.add_task(up_locust, 'up')
