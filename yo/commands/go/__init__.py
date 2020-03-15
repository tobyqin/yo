import click
from yo import pass_environment

from yo import cli


@cli.group(invoke_without_command=True)
@pass_environment
@click.argument('destination', default='')
def go(env, destination="baidu"):
    """commands to check now."""
    ctx = click.get_current_context()
    assert isinstance(ctx, click.core.Context)

    if not destination:
        env.log(f"Yo~ you should tell me where to go!")
        return

    env.log(f"Yo~ go {destination}")
    found = get_dest(destination)
    if found:
        env.log(f"OK, it is {found}")
        click.launch(found)
    else:
        env.log(f"No result found.")


def get_dest(val: str):
    destinations = {
        "baidu": "http://www.baidu.com",
        "google": "http://www.google.com"
    }
    for k, v in destinations.items():
        if val in k or val in v:
            return v

    return f"http://www.baidu.com/s?wd={val}"
