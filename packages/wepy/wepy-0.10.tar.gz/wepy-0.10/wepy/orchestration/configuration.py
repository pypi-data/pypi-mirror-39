import os.path as osp
from copy import deepcopy
import logging
import itertools as it

from wepy.work_mapper.mapper import Mapper, WorkerMapper
from wepy.work_mapper.worker import Worker

class Configuration():

    DEFAULT_WORKDIR = osp.realpath(osp.curdir)
    DEFAULT_CONFIG_NAME = "root"
    DEFAULT_NARRATION = ""
    DEFAULT_REPORTER_CLASS = ""
    # if there is to be reporter class in filenames use this template
    # to put it into the filename
    REPORTER_CLASS_SEG_TEMPLATE = ".{}"
    DEFAULT_MODE = 'x'

    def __init__(self,
                 # reporters
                 config_name=None, work_dir=None,
                 mode=None, narration=None,
                 reporter_classes=None,
                 reporter_partial_kwargs=None,
                 # work mappers
                 n_workers=None,
                 worker_type=None,
                 work_mapper_class=None,
                 work_mapper_partial_kwargs=None):

        ## reporter stuff

        # reporters and partial kwargs
        if reporter_classes is not None:
            self._reporter_classes = reporter_classes
        else:
            self._reporter_classes = []

        if reporter_partial_kwargs is not None:
            self._reporter_partial_kwargs = reporter_partial_kwargs
        else:
            self._reporter_partial_kwargs = []

        # file path localization variables

        # config string
        if config_name is not None:
            self._config_name = config_name
        else:
            self._config_name = self.DEFAULT_CONFIG_NAME

        if work_dir is not None:
            self._work_dir = work_dir
        else:
            self._work_dir = self.DEFAULT_WORKDIR

        # narration
        if narration is not None:
            narration = "_{}".format(narration) if len(narration) > 0 else ""
            self._narration = narration
        else:
            self._narration = self.DEFAULT_NARRATION


        # file modes, if none are given we set to the default, this
        # needs to be done before generating the reporters
        if mode is not None:
            self._mode = mode
        else:
            self._mode = self.DEFAULT_MODE

        # generate the reporters for this configuration
        self._reporters = self._gen_reporters()

        ## work mapper

        # the partial kwargs that will be passed for reparametrization
        if work_mapper_partial_kwargs is None:
            self._work_mapper_partial_kwargs = {}
        else:
            self._work_mapper_partial_kwargs = work_mapper_partial_kwargs


        # if the number of workers was sepcified and no work_mapper
        # class was specified default to the WorkerMapper
        if (n_workers is not None) and (work_mapper_class is None):
            self._n_workers = n_workers
            self._work_mapper_class = WorkerMapper

        # if no number of workers was specified and no work_mapper
        # class was specified we default to the serial mapper
        elif (n_workers is None) and (work_mapper_class is None):
            self._n_workers = None
            self._work_mapper_class = Mapper

        # otherwise if the work_mapper class was given we use it and
        # whatever the number of workers was
        else:
            self._n_workers = n_workers
            self._work_mapper_class = work_mapper_class

        # the default worker type if none was given
        if worker_type is None:
            worker_type = Worker

        # set the worker type
        self._worker_type = worker_type

        # then generate a work mapper
        self._work_mapper = self._work_mapper_class(num_workers=self._n_workers,
                                                    worker_type=self._worker_type,
                                                    **self._work_mapper_partial_kwargs)

    @property
    def reporter_classes(self):
        return self._reporter_classes

    @property
    def reporter_partial_kwargs(self):
        return self._reporter_partial_kwargs

    @property
    def config_name(self):
        return self._config_name

    @property
    def work_dir(self):
        return self._work_dir

    @property
    def narration(self):
        return self._narration

    @property
    def mode(self):
        return self._mode

    @property
    def reporters(self):
        return self._reporters

    @property
    def work_mapper_class(self):
        return self._work_mapper_class

    @property
    def work_mapper_partial_kwargs(self):
        return self._work_mapper_partial_kwargs

    @property
    def n_workers(self):
        return self._n_workers

    @property
    def worker_type(self):
        return self._worker_type

    @property
    def work_mapper(self):
        return self._work_mapper

    def _gen_reporters(self):

        # check the extensions of all the reporters. If any of them
        # are the same raise a flag to add the reporter names to the
        # filenames

        # the number of filenames
        all_exts = list(it.chain(*[[ext for ext in rep.SUGGESTED_EXTENSIONS]
                                 for rep in self.reporter_classes]))
        n_exts = len(all_exts)

        # the number of unique ones
        n_unique_exts = len(set(all_exts))

        duplicates = False
        if n_unique_exts < n_exts:
            duplicates = True

        # then go through and make the inputs for each reporter
        reporters = []
        for idx, reporter_class in enumerate(self.reporter_classes):

            # first we have to generate the filenames for all the
            # files this reporter needs. The number of file names the
            # reporter needs is given by the number of suggested
            # extensions it has
            file_paths = []
            for extension in reporter_class.SUGGESTED_EXTENSIONS:


                # if previously found that there are duplicates in the
                # extensions we need to name with the reporter class string
                if duplicates:

                    # use the __name__ attribute of the class and put
                    # it into the template to make a segment out of it
                    reporter_class_seg_str = self.REPORTER_CLASS_SEG_TEMPLATE.format(
                        reporter_class.__name__)

                    # then make the filename with this
                    filename = reporter_class.SUGGESTED_FILENAME_TEMPLATE.format(
                                       narration=self.narration,
                                       config=self.config_name,
                                       reporter_class=reporter_class_seg_str,
                                       ext=extension)

                # otherwise don't use the reporter class names to keep it clean
                else:
                    filename = reporter_class.SUGGESTED_FILENAME_TEMPLATE.format(
                                       narration=self.narration,
                                       config=self.config_name,
                                       reporter_class=self.DEFAULT_REPORTER_CLASS,
                                       ext=extension)


                file_path = osp.join(self.work_dir, filename)

                file_paths.append(file_path)

            modes = [self.mode for i in range(len(file_paths))]

            reporter = reporter_class(file_paths=file_paths, modes=modes,
                                  **self.reporter_partial_kwargs[idx])

            reporters.append(reporter)

        return reporters

    def _gen_work_mapper(self):

        work_mapper = self._work_mapper_class(n_workers=self._n_workers)

        return work_mapper

    @property
    def reporters(self):
        return deepcopy(self._reporters)

    @property
    def work_mapper(self):
        return deepcopy(self._work_mapper)


    def reparametrize(self, **kwargs):

        # dictionary of the possible reparametrizations from the
        # current configuration
        params = {# related to the work mapper
                  'n_workers' : self.n_workers,
                  'work_mapper_class' : self.work_mapper_class,
                  'work_mapper_partial_kwargs' : self.work_mapper_partial_kwargs,
                  # those related to the reporters
                  'mode' : self.mode,
                  'config_name' : self.config_name,
                  'work_dir' : self.work_dir,
                  'narration' : self.narration,
                  'reporter_classes' : self.reporter_classes,
                  'reporter_partial_kwargs' : self.reporter_partial_kwargs}

        for key, value in kwargs.items():
            # if the value is given we replace the old one with it
            if value is not None:
                params[key] = value

        new_configuration = type(self)(**params)

        return new_configuration
