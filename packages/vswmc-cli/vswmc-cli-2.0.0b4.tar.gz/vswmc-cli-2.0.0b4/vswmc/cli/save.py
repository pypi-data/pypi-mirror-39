from __future__ import print_function

from vswmc.cli import utils


def do_save(args):
    client = utils.create_client(args)

    for task in client.get_run(args.run)['tasks']:
        content = client.download_task_results(args.run, task['model_id'])

        target_file = task['model_id'] + '.zip'
        print('Saving {}'.format(target_file))
        with open(target_file, 'wb') as f:
            f.write(content)


def configure_parser(parser):
    parser.set_defaults(func=do_save)
    parser.add_argument('run', metavar='RUN', help='The run to save')
