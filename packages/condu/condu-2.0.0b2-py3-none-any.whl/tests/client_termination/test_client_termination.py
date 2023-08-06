from condu.condu import Condu
from condu.objects import TaskDef
from condu.objects import WorkflowDef
from condu.objects import WorkflowTaskDef
import signal
import time


def test_task(task):
    time.sleep(120)
    task.status = 'COMPLETED'


def register_task():
    task = TaskDef('test_task')
    task.description = 'Test task'
    task.retryCount = 3
    task.inputKeys = []
    task.outputKeys = []
    task.responseTimeoutSeconds = 360
    return task


def define_and_start_workflow(cClient):
    def def_workflow():
        wfDef = WorkflowDef("test_wf")
        wfDef.tasks = [WorkflowTaskDef("test_task")]
        return wfDef

    cClient.create_workflow(def_workflow())
    cClient.start_workflow("test_wf")


if __name__ == '__main__':
    cClient = Condu('http://localhost:8080/api', signum=signal.SIGTERM)
    # cClient.create_task(register_task())
    # define_and_start_workflow(cClient)
    cClient.put_task('test_task', test_task)
    cClient.start_tasks()
