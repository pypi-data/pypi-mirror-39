import click
from snark.log import logger
from snark.client.hyper_control import HyperControlClient
from snark.client.store_control import StoreControlClient
import yaml
from os import walk
import pprint
from tabulate import tabulate
import json
import os

def get_all_files(path = "./"):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.append((dirpath, dirnames, filenames))
        #break
    #print(f)
    return f

@click.command()
@click.argument('name_id', default='my_experiment')
@click.option('--file', '-f', default='snark.yml', help='YAML descriptor file for uploading')
@click.pass_context
def up(ctx, file, name_id):
    """ Start experiment """
    get_all_files()
    with open(file, 'r') as stream:
        data_loaded = yaml.load(stream)
    descriptor = open(file,'rb')
    print("Creating Experiments...")
    exp_dict = HyperControlClient().upload(descriptor)
    print("Starting Cluster...")
    show_experiments(exp_dict)

@click.command()
@click.argument('name_id', default='')
@click.option('--file', '-f', default='snark.yml', help='YAML descriptor file for uploading')
@click.pass_context
def down(ctx, file, name_id):
    """ Terminate experiment """
    if name_id == '':
       print('please provide experiment id')
       exit()

    exp = HyperControlClient().list_task(name_id)
    if not 'ID' in exp:
       print('provided experiment id is wrong')
       exit()
    pods_dict = HyperControlClient().down(exp['ID'])


@click.command()
@click.argument('name_id', default='')
@click.option('--all', '-a', flag_value=bool, default=False, help='YAML descriptor file for uploading')
@click.pass_context
def ps(ctx, name_id, all):
   """ List experiments """
   if name_id == "":
        experiments = HyperControlClient().list(all)

        experiments = [[e['ID'][:6], e['Name'], e['State'], e['IPs'], len(e['Tasks'])]
                 for e in experiments]
        print (tabulate(experiments, headers=['ID', 'Name', 'State', 'IPs', 'Tasks']))
   else:
       exp = HyperControlClient().list_experiment(name_id)
       show_tasks(exp)


def show_experiments(experiments):
    experiments = [[e['ID'][:6], e['Name'], e['State'], e['IPs'], len(e['Tasks'])]
                    for e in experiments]
    print (tabulate(experiments, headers=['ID', 'Name', 'State', 'IPs', 'Tasks']))

def show_tasks(exp):
    if 'Tasks' in exp:
        tasks = exp['Tasks']
        task_list = [[t['TaskId'][:6], t['State'], t['AssignedNode']]
                    for t in tasks]
        print (tabulate(task_list, headers=['Name', 'State', 'Node']))
    else:
         print('Task was not found')

@click.command()
@click.argument('name_id', default='')
@click.pass_context
def logs(ctx, name_id):
   """ Get logs of task by task_id"""
   if name_id == '':
       print('please provide task id')
       exit()

   exp = HyperControlClient().list_task(name_id)

   if not 'Tasks' in exp:
       print('No Task found by provided ID')
       return

   tasks = exp['Tasks']

   for task in tasks:
       if task['TaskId'][:6] == name_id:
           if len(task['Logs'])>0:
               log =str(json.loads(task['Logs'][0])['result'])
               log = log.replace('\\r\\n', '\n').replace('\\r','\n')[2:-1]
               print(log)
           else:
               print("No Logs: No task was executed")

@click.command()
@click.argument('source', default='')
@click.argument('target', default='')
@click.pass_context
def sync(ctx, source, target):
    StoreControlClient().s3cmd('sync', source, target)

@click.command()
@click.argument('source', default='')
@click.pass_context
def ls(ctx, source):
    StoreControlClient().s3cmd('ls', source)
