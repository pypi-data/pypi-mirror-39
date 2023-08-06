import os
import shutil

from lightflow.queue import JobType
from lightflow.logger import get_logger
from lightflow.models import BaseTask, Action, TaskParameters
from .exceptions import LightflowFilesystemPathError, LightflowFilesystemCopyError

logger = get_logger(__name__)


class CopyTask(BaseTask):
    """ Copies files or directories from a source to a destination. """
    def __init__(self, name, sources, destination, *, queue=JobType.Task,
                 callback_init=None, callback_finally=None,
                 force_run=False, propagate_skip=True):
        """ Initialize the Copy task.

        All task parameters except the name, queue, force_run and propagate_skip
        can either be their native type or a callable returning the native type.

        Args:
            name (str): The name of the task.
            sources (str/list/callable): A single file or directory path or a list of
                                         file or directory paths that should be copied.
                                         This parameter can either be a string, a list of
                                         strings or a callable that returns a string or a
                                         list of strings. The paths have to be absolute
                                         paths, otherwise an exception is thrown.
            destination: The destination file or folder the source should be
                         copied to. This parameter can either be a string or a
                         callable returning a string.
            queue (str): Name of the queue the task should be scheduled to. Defaults to
                         the general task queue.
            callback_init (callable): A callable that is called shortly before the task
                                      is run. The definition is:
                                        def (data, store, signal, context)
                                      where data the task data, store the workflow
                                      data store, signal the task signal and
                                      context the task context.
            callback_finally (callable): A callable that is always called at the end of
                                         a task, regardless whether it completed
                                         successfully, was stopped or was aborted.
                                         The definition is:
                                           def (status, data, store, signal, context)
                                         where status specifies whether the task was
                                           success: TaskStatus.Success
                                           stopped: TaskStatus.Stopped
                                           aborted: TaskStatus.Aborted
                                           raised exception: TaskStatus.Error
                                         data the task data, store the workflow
                                         data store, signal the task signal and
                                         context the task context.
            force_run (bool): Run the task even if it is flagged to be skipped.
            propagate_skip (bool): Propagate the skip flag to the next task.
        """
        super().__init__(name, queue=queue,
                         callback_init=callback_init, callback_finally=callback_finally,
                         force_run=force_run, propagate_skip=propagate_skip)

        self.params = TaskParameters(
            sources=sources,
            destination=destination
        )

    def run(self, data, store, signal, context, **kwargs):
        """ The main run method of the CopyTask task.

        Args:
            data (MultiTaskData): The data object that has been passed from the
                                  predecessor task.
            store (DataStoreDocument): The persistent data store object that allows the
                                       task to store data for access across the current
                                       workflow run.
            signal (TaskSignal): The signal object for tasks. It wraps the construction
                                 and sending of signals into easy to use methods.
            context (TaskContext): The context in which the tasks runs.

        Raises:
            LightflowFilesystemPathError: If the source is a directory
                                          but the target is not.
            LightflowFilesystemCopyError: If the copy process failed.

        Returns:
            Action: An Action object containing the data that should be passed on
                    to the next task and optionally a list of successor tasks that
                    should be executed.
        """
        params = self.params.eval(data, store)
        sources = [params.sources] if isinstance(params.sources, str) else params.sources

        for source in sources:
            logger.info('Copy {} to {}'.format(source, params.destination))

            if os.path.isdir(source):
                if not os.path.isdir(params.destination):
                    raise LightflowFilesystemPathError(
                        'The destination is not a valid directory')

                try:
                    shutil.copytree(source, params.destination)
                except OSError as e:
                    raise LightflowFilesystemCopyError(e)
            else:
                try:
                    shutil.copy2(source, params.destination)
                except OSError as e:
                    raise LightflowFilesystemCopyError(e)

        return Action(data)
