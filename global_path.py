# -*- coding:utf8 -*-
import os


def get_data_path():
    project_path = get_project_path()
    return os.path.join(project_path, 'data')


def get_project_path():
    return os.path.dirname(os.path.realpath(__file__))

# if __name__ == '__main__':
#     print(get_project_path())
#     print(get_data_path())