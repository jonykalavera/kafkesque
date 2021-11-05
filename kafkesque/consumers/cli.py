import click


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--verbose', '-v', is_flag=True, help="Increase output verbosity level")
def main(ctx, verbose):
    """ CLI root
    """
    group_commands = ['register', 'delete', 'ls', 'stop', 'start']
    if ctx.invoked_subcommand is None:
        click.echo("Specify one of the commands below")
        print(*group_commands, sep='\n')


    ctx.obj['VERBOSE'] = verbose


@main.command('register')
@click.pass_context
@click.option('--url', '-u', click.STRING,
              help="Webhook URL", required=True)
@click.option('--topic', '-t', click.STRING, # Should we allow to subscribe to multiple topics? In that case it should be "--topics".
              help="Kafka topic to subscribe to", required=True)
# TODO: add more
def register_webhook(ctx, long, active=True):
    """ Register new webhook for kafka topic.

    Args:
        ctx: context
        long: show long description
        active: show only active webhooks
    """
    click.echo('Existing webhooks: To implement')


@main.command('delete')
@click.pass_context
@click.option('--id', '-i', click.INT,
              help="Webhook id")
def delete_webhook(ctx, long, active=True):
    """ Delete webhook

    Args:
        ctx: context
        long: show long description
        active: show only active webhooks
    """
    click.echo('Existing webhooks: To implement')

@main.command('ls')
@click.pass_context
@click.option('--long', '-l', is_flag=True,
              help="Show in long format")
@click.option('--active', '-a', is_flag=True,
              help="Show only active webhooks")
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
