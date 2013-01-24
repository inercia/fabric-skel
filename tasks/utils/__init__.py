
__all__ = [
    'config',
    'decorators',
    'install',
    ]

from config                     import load_cfg

from fabric.api                 import run, sudo
from fabric.context_managers    import settings
from fabric.tasks               import Task
from fabric.api                 import env



class WrappedCallableTask(Task):
    """
    Wraps a given callable transparently, while marking it as a valid Task.

    Generally used via `@task <~fabric.decorators.task>` and not directly.

    .. versionadded:: 1.1
    """
    def __init__(self, callable, *args, **kwargs):
        super(WrappedCallableTask, self).__init__(*args, **kwargs)
        self.wrapped = callable
        # Don't use getattr() here -- we want to avoid touching self.name
        # entirely so the superclass' value remains default.
        if hasattr(callable, '__name__'):
            self.__name__ = self.name = callable.__name__
        if hasattr(callable, '__doc__'):
            self.__doc__ = callable.__doc__

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        try:
            over_env = env.machines[env.host_string]
        except KeyError:
            pass
        else:
            env.update(over_env)

        return self.wrapped(*args, **kwargs)

    def __getattr__(self, k):
        return getattr(self.wrapped, k)


def manager_task(*args, **kwargs):
    """
    Decorator declaring the wrapped function to be a new-style task.

    May be invoked as a simple, argument-less decorator (i.e. ``@task``) or
    with arguments customizing its behavior (e.g. ``@task(alias='myalias')``).

    Please see the :ref:`new-style task <task-decorator>` documentation for
    details on how to use this decorator.

    .. versionchanged:: 1.2
        Added the ``alias``, ``aliases``, ``task_class`` and ``default``
        keyword arguments. See :ref:`task-decorator-arguments` for details.
    """
    invoked = bool(not args or kwargs)
    task_class = kwargs.pop("task_class", WrappedCallableTask)
    if not invoked:
        func, args = args[0], ()

    def wrapper(func):
        return task_class(func, *args, **kwargs)

    return wrapper if invoked else wrapper(func)





def run_bg (command, out_file = "/dev/null", err_file = None, shell = True, pty = False ):
    run('nohup %s >%s 2>%s </dev/null &' % (command, out_file, err_file or '&1'), shell, pty)

def sudo_bg (command, out_file = "/dev/null", err_file = None, shell = True, pty = False ):
    sudo('nohup %s >%s 2>%s </dev/null &' % (command, out_file, err_file or '&1'), shell, pty)



def ping():
    """
    Return True if we cold run a command in this machine
    """
    with settings(warn_only = True):
        try:
            return bool(int(run('echo 1')))
        except ValueError:
            return False


