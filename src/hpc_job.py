
mesos_hpc_jobtemplate = {
    'name': '',
    'task_id': {'value': 0},
    'agent_id': {'value': 0},
    'resources': [
        {
            'name': 'cpus',
            'type': 'SCALAR',
            'scalar': {'value': 0}
        },
        {
            'name': 'mem',
            'type': 'SCALAR',
            'scalar': {'value': 0}
        }
    ],
    'command': {'value': ''},
}

def mesos_hpc_buildJob(name, command, cpus, ram, task_id, agent_id):
    job = mesos_hpc_jobtemplate.copy()
    job['name'] = name
    job['task_id']['value'] = task_id
    job['agent_id']['value'] = agent_id
    job['command']['value'] = command
    job['resources'][0]['scalar']['value'] = cpus
    job['resources'][1]['scalar']['value'] = ram
    return job