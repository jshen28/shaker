from shaker.engine.executors.shell import ShellExecutor
from shaker.engine.executors import base
import json


class FioExecutor(ShellExecutor):

    def process_reply(self, message):

        stdout = message.get("stdout")

        if not stdout:
            raise base.ExecutorException(
                message,
                'Flent returned no data, stderr: %s' % message['stderr'])

        data = json.loads(stdout)
        jobs = data.get('jobs')

        formalized_results = []
        for job in jobs:
            job_name = job.get('jobname')
            read_bw = job.get('read', {}).get('bw', 0)
            read_iops = job.get('read', {}).get('iops', 0)
            write_bw = job.get('write', {}).get('bw', 0)
            write_iops = job.get('write', {}).get('iops', 0)
            formalized_results.append({
                job_name: {
                    "read_bw": read_bw,
                    "read_iops": read_iops,
                    "write_bw": write_bw,
                    "write_iops": write_iops
                }
            })

        result = dict()
        result['samples'] = formalized_results

        return result


