#!/usr/bin/env python3
import argparse
from cli.commands import handle_command

def main():
    parser = argparse.ArgumentParser(description='Project Manager CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)


    parser_add_user = subparsers.add_parser('add-user')
    parser_add_user.add_argument('--name', required=True)
    parser_add_user.add_argument('--email')

    
    parser_add_project = subparsers.add_parser('add-project')
    parser_add_project.add_argument('--user', required=True)
    parser_add_project.add_argument('--title', required=True)
    parser_add_project.add_argument('--description')
    parser_add_project.add_argument('--due')

    parser_add_task = subparsers.add_parser('add-task')
    parser_add_task.add_argument('--project', required=True)
    parser_add_task.add_argument('--title', required=True)
    parser_add_task.add_argument('--status', default='pending',
                                 choices=['pending', 'in_progress', 'completed'])
    parser_add_task.add_argument('--assigned-to')

    
    subparsers.add_parser('list-users')  

    
    parser_list_projects = subparsers.add_parser('list-projects')
    parser_list_projects.add_argument('--user')

    
    parser_list_tasks = subparsers.add_parser('list-tasks')
    parser_list_tasks.add_argument('--project')
    parser_list_tasks.add_argument('--user')

    
    parser_update_task = subparsers.add_parser('update-task')
    parser_update_task.add_argument('--id', required=True, type=int)
    parser_update_task.add_argument('--status', required=True,
                                    choices=['pending', 'in_progress', 'completed'])

    parser_complete_task = subparsers.add_parser('complete-task')
    parser_complete_task.add_argument('--id', required=True, type=int)

    args = parser.parse_args()
    handle_command(args)

if __name__ == '__main__':
    main()