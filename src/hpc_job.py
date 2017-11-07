import copy

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
    job = copy.deepcopy(mesos_hpc_jobtemplate)
    job['name'] = copy.copy(name)
    job['task_id']['value'] = copy.copy(task_id)
    job['agent_id']['value'] = copy.copy(agent_id)
    job['command']['value'] = copy.copy(command)
    job['resources'][0]['scalar']['value'] = copy.copy(cpus)
    job['resources'][1]['scalar']['value'] = copy.copy(ram)
    return job