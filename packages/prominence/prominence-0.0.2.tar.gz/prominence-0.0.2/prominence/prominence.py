from collections import namedtuple
import json
import requests

class ProminenceJob(object):
    """
    PROMINENCE job class
    """

    # List of all attribute names
    attrs = ['image',
             'cmd',
             'args',
             'nodes',
             'cpus',
             'memory',
             'disk',
             'runtime',
             'env',
             'labels',
             'artifacts',
             'inputs',
             'output_files',
             'output_dirs',
             'type',
             'mpi_version',
             'constraints']

    # The key is the attribute name and the value is the JSON key
    attr_map = {'image':'image',
                'cmd':'cmd',
                'args':'args',
                'nodes':'nodes',
                'cpus':'cpus',
                'memory':'memory',
                'disk':'disk',
                'runtime':'runtime',
                'env':'env',
                'labels':'labels',
                'artifacts':'artifacts',
                'inputs':'inputs',
                'output_files':'outputFiles',
                'output_dirs':'outputDirs',
                'type':'type',
                'mpi_version':'mpiVersion',
                'constraints':'constraints'}

    def __init__(self, image=None, cmd=None, args=None, nodes=None, cpus=None, memory=None, disk=None, runtime=None, env=None, labels=None, artifacts=None, inputs=None, output_files=None, output_dirs=None, type=None, mpi_version=None, constraints=None):

        self._image = image
        self._cmd = cmd
        self._args = args
        self._nodes = nodes
        self._cpus = cpus
        self._memory = memory
        self._disk = disk
        self._runtime = runtime
        self._env = env
        self._labels = labels
        self._artifacts = artifacts
        self._inputs = inputs
        self._output_files = output_files
        self._output_dirs = output_dirs
        self._type = type
        self._mpi_version = mpi_version
        self._constraints = constraints

    @property
    def image(self):
        """
        Gets the container image
        """
        return self._image

    @image.setter
    def image(self, image):
        """
        Sets the container image
        """
        self._image = image

    @property
    def cmd(self):
        """
        Gets the command
        """
        return self._cmd

    @cmd.setter
    def cmd(self, cmd):
        """
        Sets the command
        """
        self._cmd = cmd

    @property
    def args(self):
        """
        Gets the args
        """
        return self._args

    @args.setter
    def args(self, args):
        """
        Sets the args
        """
        self._args = args

    @property
    def nodes(self):
        """
        Returns the number of nodes
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        """
        Sets the number of nodes
        """
        self._nodes = nodes

    @property
    def cpus(self):
        """
        Gets the number of CPUs
        """
        return self._cpus

    @cpus.setter
    def cpus(self, cpus):
        """
        Sets the number of CPUs
        """
        self._cpus = cpus

    @property
    def memory(self):
        """
        Returns the memory in GB
        """
        return self._memory

    @memory.setter
    def memory(self, memory):
        """
        Sets the memory in GB
        """
        self._memory = memory

    @property
    def disk(self):
        """
        Returns the disk size in GB
        """
        return self._disk

    @disk.setter
    def disk(self, disk):
        """
        Sets the disk size in GB
        """
        self._disk = disk

    @property
    def runtime(self):
        """
        Returns the maximum runtime in mins
        """
        return self._runtime

    @runtime.setter
    def runtime(self, runtime):
        """
        Sets the maximum runtime in mins
        """
        self._runtime = runtime

    @property
    def env(self):
        """
        Returns the list of environment variables to be set in the container
        """
        return self._env

    @env.setter
    def env(self, env):
        """
        Sets the list of environment variables to be set in the container
        """
        self._env = env

    @property
    def labels(self):
        """
        Returns the list of labels associated with the job
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """
        Sets the list of labels associated with the job
        """
        self._labels = labels

    @property
    def artifacts(self):
        """
        Returns the list of artifacts to be downloaded before the job starts
        """
        return self._artifacts

    @artifacts.setter
    def artifacts(self, artifacts):
        """
        Sets the list of artifacts to be downloaded before the job starts
        """
        self._artifacts = artifacts

    @property
    def inputs(self):
        """
        Returns the input files
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """
        Sets the list of inputs
        """
        self._inputs = inputs

    @property
    def output_files(self):
        """
        Returns the list of output files to be uploaded to cloud storage
        """
        return self._output_files

    @output_files.setter
    def output_files(self, output_files):
        """
        Sets the list of output files to be uploaded to cloud storage
        """
        self._output_files = output_files

    @property
    def output_dirs(self):
        """
        Returns the list of output directories to be uploaded to cloud storage
        """
        return self._output_dirs

    @output_dirs.setter
    def output_dirs(self, output_dirs):
        """
        Sets the list of output directories to be uploaded to cloud storage
        """
        self._output_dirs = output_dirs

    @property
    def type(self):
        """
        Returns the type of job
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of job ('basic' or 'mpi')
        """
        self._type = type

    @property
    def mpi_version(self):
        """
        Returns the MPI version
        """
        return self._mpi_version

    @mpi_version.setter
    def mpi_version(self, mpi_version):
        """
        Sets the MPI version
        """
        self._mpi_version = mpi_version

    @property
    def constraints(self):
        """
        Returns the placement constraints
        """
        return self._constraints

    @constraints.setter
    def constraints(self, constraints):
        """
        Sets the placement constraints
        """
        self._constraints = constraints

    def to_json(self):
        """
        Returns the job as JSON
        """
        data = {}
        for attr in self.attrs:
            value = getattr(self, attr, None)
            if value is not None:
                data[self.attr_map[attr]] = value
        return data

    def from_json(self, data):
        """
        Initializes job using JSON representation
        """
        for attr in self.attrs:
            attr_json = self.attr_map[attr]
            if attr_json in data:
                setattr(self, attr, data[attr_json])

class ProminenceClient(object):
    """
    PROMINENCE client class
    """

    # Named tuple containing a return code & data object
    Response = namedtuple("Response", ["return_code", "data"])

    def __init__(self, url=None, token=None):
        self._url = url
        self._timeout = 10
        self._headers = {"Authorization":"Bearer %s" % token}

    def list(self, completed, all, num, constraint):
        """
        List running/idle jobs or completed jobs
        """

        params = {}

        if completed:
            params['completed'] = 'true'

        if num:
            params['num'] = num

        if all:
            params['all'] = 'true'

        if constraint:
            params['constraint'] = constraint

        try:
            response = requests.get(self._url + '/jobs', params=params, timeout=self._timeout, headers=self._headers)
        except requests.exceptions.RequestException:
            return self.Response(return_code=1, data={'error': 'cannot connect to PROMINENCE server'})

        if response.status_code == 200:
            return self.Response(return_code=0, data=response.json())
        elif response.status_code < 500:
            if 'error' in response.json():
                return self.Response(return_code=1, data={'error': '%s' % response.json()['error']})
        return self.Response(return_code=1, data={'error': 'unknown'})

    def create(self, job):
        """
        Create a job
        """
        data = job.to_json()
        try:
            response = requests.post(self._url + '/jobs', json=data, timeout=self._timeout, headers=self._headers)
        except requests.exceptions.RequestException:
            return self.Response(return_code=1, data={'error': 'cannot connect to PROMINENCE server'})
        if response.status_code == 201:
            if 'id' in response.json():
                return self.Response(return_code=0, data={'id': response.json()['id']})
        return self.Response(return_code=1, data={'error': 'unknown'})

    def delete(self, job_id):
        """
        Delete the specified job
        """
        try:
            response = requests.delete(self._url + '/jobs/%d' % job_id, timeout=self._timeout, headers=self._headers)
        except requests.exceptions.RequestException:
            return self.Response(return_code=1, data={'error': 'cannot connect to PROMINENCE server'})

        if response.status_code == 200:
            return self.Response(return_code=0, data={})
        else:
            if 'error' in response.json():
                return self.Response(return_code=1, data={'error': '%s' % response.json()['error']})
        return self.Response(return_code=1, data={'error': 'unknown'})

    def describe(self, job_id, completed=False):
        """
        Describe a specific job
        """
        if completed:
            completed = 'true'
        else:
            completed = 'false'
        params = {'completed':completed, 'num':1}

        try:
            response = requests.get(self._url + '/jobs/%d' % job_id, params=params, timeout=self._timeout, headers=self._headers)
        except requests.exceptions.RequestException:
            return self.Response(return_code=1, data={'error': 'cannot connect to PROMINENCE server'})

        if response.status_code == 200:
            return self.Response(return_code=0, data=response.json())
        elif response.status_code < 500:
            if 'error' in response.json():
                return self.Response(return_code=1, data={'error': '%s' % response.json()['error']})
        return self.Response(return_code=1, data={'error': 'unknown'})

    def stdout(self, job_id):
        """
        Get standard output from a job
        """

        try:
            response = requests.get(self._url + '/jobs/%d/0/stdout' % job_id, timeout=self._timeout, headers=self._headers)
        except requests.exceptions.RequestException:
            return self.Response(return_code=1, data={'error': 'cannot connect to PROMINENCE server'})

        if response.status_code == 200:
            return self.Response(return_code=0, data=response.content)
        else:
            if 'error' in response.json():
                return self.Response(return_code=1, data={'error': '%s' % response.json()['error']})
        return self.Response(return_code=1, data={'error': 'unknown'})

    def stderr(self, job_id):
        """
        Get standard error from a job
        """

        try:
            response = requests.get(self._url + '/jobs/%d/0/stderr' % job_id, timeout=self._timeout, headers=self._headers)
        except requests.exceptions.RequestException:
            return self.Response(return_code=1, data={'error': 'cannot connect to PROMINENCE server'})

        if response.status_code == 200:
            return self.Response(return_code=0, data=response.content)
        else:
            if 'error' in response.json():
                return self.Response(return_code=1, data={'error': '%s' % response.json()['error']})
        return self.Response(return_code=1, data={'error': 'unknown'})

