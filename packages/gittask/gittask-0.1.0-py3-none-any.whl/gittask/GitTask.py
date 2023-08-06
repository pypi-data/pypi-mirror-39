import logging
import os
import random
import shlex
import string
import subprocess

import fire
import yaml


class GitTask:
    """Git-task is a task management system"""

    __TASKS_FILE_NAME = ".tasks.yml"
    __ID_LENGTH = 8

    __task_list = None

    def __init__(self):
        try:
            with(open(self.__TASKS_FILE_NAME, 'r')) as tasks_file:
                self.__task_list = yaml.load(tasks_file)
        except FileNotFoundError:
            logging.info("No " + self.__TASKS_FILE_NAME +
                         " file found. Proceeding with empty task list.")

    def __list_default_tasks(self):
        return self.__task_list or []

    def __gen_id(self):
        return ''.join(random.SystemRandom().choices(
            string.ascii_lowercase + string.digits, k=self.__ID_LENGTH))

    def __convert_item_to_dict(self, item, **kwargs):
        if type(item) is str:
            item = {item: {}}

        if type(item) is not dict:
            raise ValueError("Unexpected item type")

        [(key, details)] = item.items()
        details.setdefault("id", self.__gen_id())
        details.update({k: v for k, v in kwargs.items() if v is not None})

        return {key: {k: v for k, v in details.items() if v is not None}}

    def __convert_task_list_to_item_dict(self, item_list=None):
        return [self.__convert_item_to_dict(item) for item in item_list]

    def __save(self):
        if self.__task_list is not None:
            with(open(self.__TASKS_FILE_NAME, 'w')) as tasks_file:
                yaml.dump(
                    self.__convert_task_list_to_item_dict(self.__task_list),
                    stream=tasks_file,
                    default_flow_style=False)

    def add(self, summary, assignee=None, deadline=None):
        print("Adding new item with summary: \"" + summary + "\"")
        self.__task_list = self.__list_default_tasks() + [
            self.__convert_item_to_dict(summary, assignee=assignee,
                                        deadline=deadline)]
        self.__save()

    def list(self):
        if self.__task_list is None:
            print("No " + self.__TASKS_FILE_NAME
                  + " present  in current directory.")
        if self.__task_list is None or self.__task_list == []:
            print("Hooray, task list is empty!")
            return
        print(
            yaml.dump(self.__convert_task_list_to_item_dict(self.__task_list),
                      default_flow_style=False))

    def reformat(self):
        self.__save()

    def remove(self, id):
        """Removes one task"""

        def __id_matches(item):
            [(key, details)] = item.items()
            return 'id' in details and details['id'].startswith(id)

        id = str(id)

        items = [item for item in self.__list_default_tasks() if
                 __id_matches(item)]
        if len(items) == 0:
            print("Task with id: " + id + " not found")
        elif len(items) > 1:
            print("More than one task with id " + id + " found: \n" +
                  yaml.dump(self.__convert_task_list_to_item_dict(items),
                            default_flow_style=False))
        else:
            print("Removing task with id: " + id)
            self.__task_list.remove(items[0])
            self.__save()

    @staticmethod
    def install_git_alias():
        subprocess.check_call(
            shlex.split(
                "git config --global alias.task '!python3 " + os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "GitTask.py") + "'"))

    @staticmethod
    def uninstall_git_alias():
        subprocess.check_call(
            shlex.split("git config --global --unset-all alias.task"))


def main():
    fire.Fire(GitTask)


if __name__ == '__main__':
    main()
