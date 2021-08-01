import click


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--verbose', '-v', is_flag=True, help="Increase output verbosity level")
def main(ctx, verbose):
    group_commands = ['ls', 'stop']
    if ctx.invoked_subcommand is None:
        click.echo("Specify one of the commands below")
        print(*group_commands, sep='\n')


    ctx.obj['VERBOSE'] = verbose


@main.command('ls')
@click.pass_context
@click.option('--long', '-l', is_flag=True,
              help="Detailed description")
@click.option('--active', '-a', is_flag=True,
              help="Detailed description")
def ls(ctx, long, active=True):
    """ Show existing webhooks

    Args:
        ctx: context
        long: show long description
        active: show only active webhooks
    """
    click.echo('Existing webhooks: To implement')



@main.command('stop')
@click.pass_context
@click.option('--webhook-id', '-i', required=True, type=click.INT,
              help="Stop webhook by the given ID")
def stop(ctx, webhook_id):
    """

    Args:
        ctx: context
        webhook_id: webhook id

    """
    # If webhook_id not found echo an error.
    click.echo(f'Killing the webhook {webhook_id}')


if __name__ == '__main__':
    main(obj={})
