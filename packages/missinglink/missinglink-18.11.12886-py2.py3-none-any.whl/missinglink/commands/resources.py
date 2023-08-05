# -*- coding: utf8 -*-
import click

from .utilities import CommonOptions, CloudCredentialsHandler
from .utilities import DockerTools
from missinglink.core.api import ApiCaller
from missinglink.commands.commons import output_result
from colorama import Fore, Style
import six
from collections import defaultdict
from pprint import pformat
from .cloud.aws import BackendContext


class HideAzure(click.Group):
    def list_commands(self, ctx):
        commands = super(HideAzure, self).list_commands(ctx)
        return [c for c in commands if c != 'azure']


@click.group('resources', help='Resource Management', cls=HideAzure)
def resources_commands():
    pass


@resources_commands.group('local-grid')
def local_grid():
    pass


def _trim_value(value, max_chars=30):
    if len(value) > max_chars:
        return value[:max_chars - 4] + ' ...'

    return value


def _with_format(text, fore='', style=''):
    return Style.RESET_ALL + fore + style + text + Style.RESET_ALL


class ArgRow:
    show_score = {
        'std': 1000,
        'adv': 500,
        'internal': 100
    }
    readonly_score = {
        False: 0,
        True: 50
    }
    configured_score = {
        False: 0,
        True: 5000
    }

    @classmethod
    def _values_to_str(cls, v):
        if isinstance(v, six.string_types):
            return v

        return '\n'.join(v if v is not None else '')

    def _active_value(self):
        return self.value if self.configured or self.read_only else self.default_value

    def __eq__(self, other):
        return self.name == other.name and self.arg == other.arg

    def __init__(self, name, arg):
        self.name = name
        self.arg = arg
        self.read_only = self.arg.get('read_only', False)
        self.configured = 'configured' in self.arg and not self.read_only
        self.show_level = self.arg.get('show_level', self.arg.get('edit_level', 'internal'))
        self.score = self.show_score[self.show_level] + self.configured_score[self.configured] + self.readonly_score[self.read_only]

        self.value = self._values_to_str(self.arg.get('configured'))
        self.default_value = self._values_to_str(self.arg.get('default'))
        self.active_value = self._active_value()

    color_legend = '  |  '.join(['Color Legend:', _with_format('read only', Fore.BLUE), _with_format('configured', Fore.GREEN), _with_format('default value', Fore.RESET)])
    param_filed = _with_format('Parameter', Fore.WHITE, Style.BRIGHT)
    value_field = _with_format('Value', Fore.WHITE, Style.BRIGHT)
    default_field = _with_format('Default', Fore.WHITE, Style.DIM)
    description_field = _with_format('Description', Fore.WHITE, Style.DIM)

    def configured_name(self):
        return _with_format(self.name, Fore.GREEN, Style.BRIGHT)

    def default_name(self):
        return _with_format(self.name, Fore.RESET, Style.BRIGHT)

    def row_name(self):
        return self.configured_name() if self.configured else self.default_name()

    def read_only_value(self):
        return _with_format(self.active_value, Fore.BLUE, Style.NORMAL)

    def configured_value(self):
        return _with_format(self.active_value, Fore.GREEN, Style.BRIGHT)

    def un_configured_value(self):
        return _with_format(self.active_value, Fore.RESET, Style.DIM)

    def configured_default_value(self):
        return _with_format(self.default_value, Fore.GREEN, Style.BRIGHT)

    def un_configured_default_value(self):
        return _with_format(self.default_value, Fore.RESET, Style.DIM)

    def row_value(self):
        if self.read_only:
            return self.read_only_value()

        if self.configured:
            return self.configured_value()

        return self.un_configured_value()

    def description_all(self):
        return _with_format(_trim_value(self.arg.get('description'), 60), Style.DIM)

    def row_description(self):
        return self.description_all()

    def row_default(self):
        if self.read_only:
            return ''

        if self.configured:
            return self.un_configured_default_value()

        return self.configured_default_value()

    def to_row(self):
        return {
            self.param_filed: self.row_name(),
            self.value_field: self.row_value(),
            self.default_field: self.row_default(),
            self.description_field: self.row_description(),
        }

    def displayed(self, target_show_levels, configured_only):
        if self.configured:
            return True

        shown = self.show_level in target_show_levels
        return shown and not configured_only

    @classmethod
    def import_and_filter(cls, data, target_show_levels, configured_only):
        res = []
        for k, v in data.items():
            ob = cls(k, v)
            if ob.displayed(target_show_levels, configured_only):
                res.append(ob)

        return res

    @classmethod
    def table_fields(cls, kwargs):
        show_defaults = kwargs.get('show_defaults', False)
        show_description = kwargs.get('show_description', False)

        fields = [cls.param_filed, cls.value_field]
        if show_defaults:
            fields.append(cls.default_field)
        if show_description:
            fields.append(cls.description_field)

        return fields

    @classmethod
    def print_table(cls, ctx, kwargs, data):
        table = [x.to_row() for x in sorted(data, key=lambda x: x.score, reverse=True)]
        fields = cls.table_fields(kwargs)
        click.echo(cls.color_legend)
        click.echo()
        output_result(ctx, table, fields=fields)

    @classmethod
    def parse_user_input(cls, tuples, unset_items):
        res = defaultdict(list)
        for key, value in tuples:
            res[key].append(value)
            if 'None' in res[key]:
                res[key] = ['None']
        for item in unset_items:
            res[item] = ['None']

        return dict(res)


@local_grid.command('init')
@click.pass_context
@CommonOptions.org_option()
@click.option('--ssh-key-path', type=str, help='Path to the private ssh key to be used by the resource manager', default=None)
@click.option('--force/--no-force', default=False, help='Force installation (stops current resource manager if present')
@click.option('--resource-token', default=None, type=str, help='MissingLink resource token. One will be generated if this instance of ml is authorized')
# cloud creds
@click.option('--link-aws/--no-aws-link', required=False, default=True)
@click.option('--env-aws/--no-aws-env', required=False, default=True)
@click.option('--link-gcp/--no-gcp', required=False, default=True)
def install_rm(ctx, org, ssh_key_path, force, resource_token, **kwargs):
    cred_sync = CloudCredentialsHandler(kwargs)
    docker_tools = DockerTools.create(ctx, cloud_credentials=cred_sync)

    docker_tools.pull_rm_image()
    docker_tools.validate_no_running_resource_manager(force)
    docker_tools.validate_local_config(org=org, force=force, ssh_key_path=ssh_key_path, token=resource_token)

    docker_tools.run_resource_manager()
    click.echo('The resource manager is configured and running')


def restore_template_options(func):
    @click.option('--ssh', type=(str, str, str), help='ssh key data', required=True)
    @click.option('ml', '--ml', '--mali', type=(str, str, str), help='mali config data', required=True)
    @click.option('--prefix', type=str, help='ml prefix type', required=False)
    @click.option('--token', type=str, help='ml prefix type', required=True)
    @click.option('--rm-socket-server', type=str, help='web socket server', required=True)
    @click.option('--rm-manager-image', type=str, required=True)
    @click.option('--rm-config-volume', type=str, required=True)
    @click.option('--rm-container-name', type=str, required=True)
    @click.option('--ml-backend', type=str, required=True)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

    return wrapper


@resources_commands.command('restore_aws_template', help="restores predefined cloud configuration")
@click.pass_context
@click.option('--arn', type=str, help='arn of the KMS encryption key', required=True)
@restore_template_options
def apply_aws_template(
        ctx, arn, ssh, ml, prefix, token, rm_socket_server, rm_manager_image,
        rm_config_volume, rm_container_name, ml_backend):
    from .cloud.aws import AwsContext
    if prefix == str(None):
        prefix = None

    click.echo('decrypting data')
    kms = AwsContext.get_kms(arn)
    ssh_key = AwsContext.decrypt(kms, ssh).decode('utf-8')
    ml_data = AwsContext.decrypt(kms, ml).decode('utf-8')
    run_docker(ctx, ml_backend, ml_data, prefix, rm_config_volume, rm_container_name, rm_manager_image,
               rm_socket_server, ssh_key, token)


@resources_commands.command('restore_azure_template', help="restores predefined cloud configuration")
@click.pass_context
@click.option('--key', type=str, help='Key id of Key Vault encryption key', required=True)
@click.option('--role_id', type=str, help='MSI id used to connect ot Key Vault', required=True)
@restore_template_options
def apply_azure_template(
        ctx, key, role_id, ssh, ml, prefix, token, rm_socket_server, rm_manager_image,
        rm_config_volume, rm_container_name, ml_backend):
    from .cloud.azure import AzureContext
    if prefix == str(None):
        prefix = None

    click.echo('decrypting data')
    kms = AzureContext.get_cloud_kms(key, role_id)
    ssh_key = AzureContext.decrypt(kms, ssh).decode('utf-8')
    ml_data = AzureContext.decrypt(kms, ml).decode('utf-8')
    run_docker(ctx, ml_backend, ml_data, prefix, rm_config_volume, rm_container_name, rm_manager_image,
               rm_socket_server, ssh_key, token)


def run_docker(ctx, ml_backend, ml_data, prefix, rm_config_volume, rm_container_name, rm_manager_image,
               rm_socket_server, ssh_key, token):
    click.echo('building installation config')
    docker_tools = DockerTools.create(ctx, rm_socket_server=rm_socket_server, rm_manager_image=rm_manager_image,
                                      rm_config_volume=rm_config_volume, rm_container_name=rm_container_name,
                                      ml_backend=ml_backend)
    click.echo('pulling RM')
    docker_tools.pull_rm_image()

    click.echo('killing RM')
    docker_tools.validate_no_running_resource_manager(True)

    docker_tools.setup_rms_volume(ssh_key, token, prefix=prefix, ml_data=ml_data, force=True)
    docker_tools.remove_current_rm_servers()
    inst = docker_tools.run_resource_manager()
    click.echo('The resource manager is configured and running %s' % inst.id)
    click.echo('docker logs -f %s ' % rm_container_name)


@resources_commands.command('queue', help="manage resource queues")
@CommonOptions.org_option()
@click.argument('name', required=True, nargs=1)
@click.option('--create', is_flag=True, help='Create new resources queue')
@click.option('--new-name', 'display', help='Update name of the given queue to this name')
@click.option('--disable', 'disable', flag_value=str(True), help='Disable existing queue')
@click.option('--enable', 'disable', flag_value=str(False), help='Enable existing queue')
@click.pass_context
def manage_queue(ctx, org=None, disable=None, display=None, create=None, name=None, **kwargs):
    url = '{}/queue/{}'.format(org, name)
    is_update = disable is not None or display is not None
    disabled = None

    if disable is not None:
        disabled = disable == str(True)

    if create:
        result = ApiCaller.call(ctx.obj, ctx.obj.session, 'post', url, {'disabled': disabled, 'display': name})
    elif is_update:
        result = ApiCaller.call(ctx.obj, ctx.obj.session, 'put', url, {'disabled': disabled, 'display': display})
    else:
        result = ApiCaller.call(ctx.obj, ctx.obj.session, 'get', url)
    output_result(ctx, result)


@resources_commands.command('group')
@CommonOptions.org_option()
@click.argument('group', required=True, nargs=1)
@click.option('--json', required=False, default=False, help="output data in json format")
@click.option('--advanced', required=False, default=False, help="show advanced configuration parameters as well")
@click.option('--show-defaults/--no-defaults', required=False, default=False, help="also show default values")
@click.option('--create', required=False, default=None, type=click.Choice(['aws', 'local', 'azure']), help="create new aws/azure/local group")
@click.option('--show-description/--no-description', required=False, default=False, help="also show parameter descriptions")
@click.option('--configured-only/--configured-and-defaults', required=False, default=False, help="show only parameters with configured values")
@click.option('--set', required=False, default=None, type=(str, str), multiple=True, help="Set parameter value. Some parameters can be specified multiple times for arrays")
@click.option('--unset', required=False, default=[], type=str, multiple=True, help="Reset parameter value. If the same paramter is specified as in both `--set` and `--unset`, it will be unset")
@click.pass_context
def resource_group(ctx, **kwargs):
    group_id = kwargs.pop('group')
    json = kwargs.get('json', False)

    configured_only = kwargs.get('configured_only', False)
    target_show_levels = ['std']

    if kwargs['advanced']:
        target_show_levels = ['std', 'adv']
    backend = BackendContext(ctx, kwargs)

    new_values = ArgRow.parse_user_input(kwargs['set'], kwargs['unset'])
    create_cloud_type = kwargs.pop('create')
    if new_values or create_cloud_type is not None:
        response = backend.put_resource_group_parameters(group_id, new_values, new_cloud_type=create_cloud_type)
    else:
        response = backend.resource_group_description(group_id)

    return __print_result(ctx, kwargs, response, json, target_show_levels, configured_only)


def __print_result(ctx, kwargs, response, json, target_show_levels, configured_only):
    data = ArgRow.import_and_filter(response, target_show_levels, configured_only)
    if json:
        click.echo(pformat({v.name: v.arg for v in data}))
    else:
        ArgRow.print_table(ctx, kwargs, data)


@local_grid.command('change-group', help='Change the group a server is assigned to')
@CommonOptions.org_option()
@click.argument('server', type=str, required=True)
@click.option('--new-group', required=True, type=str, help="Change the group the server is assigned to")
@click.pass_context
def change_local_server(ctx, server=None, new_group=None, **kwargs):
    backend = BackendContext(ctx, kwargs)
    response = backend.change_local_server(server, new_group)
    output_result(ctx, response)
