from unittest import mock

import luigi


def mock_run(self):

    with self.output().open('w') as file:
        file.write('test')


def mock_up_task(luigi_task, temp_dir, mock_func=mock_run):
    """
    Recursively combs luigi task tree and replaces run and output def with mocks

    luigi_task: The wrapper task being patched
    temp_dir: Directory that output files are written to
    mock_func: The function replacing the task's run method,
    needs to exist if there should be side effects for the run.
    There should at least be something that writes to the task output 

    """

    required = luigi_task.requires()

    # If the task has any requirements, recurse through them
    if required:

        if type(required) == dict:
            for child_task in required.values():
                mock_up_task(child_task, temp_dir)
        else:
            try:
                for child_task in list(luigi_task.requires()):
                    mock_up_task(child_task, temp_dir)
            except TypeError:
                mock_up_task(luigi_task.requires(), temp_dir)

    # Get the class of the task
    task_class = luigi_task.__class__

    # Mock the method on the class in the module

    mock_string = "{}.{}".format(task_class.__module__, task_class.__name__)

    run_patch = mock.patch(target="{}.run".format(mock_string), new=mock_func)
    run_patch.start()
    output_patch = mock.patch(target="{}.output".format(mock_string)).start()

    output_patch.return_value = luigi.LocalTarget(path='{}/{}.txt'.format(
        temp_dir, luigi_task
    ))
