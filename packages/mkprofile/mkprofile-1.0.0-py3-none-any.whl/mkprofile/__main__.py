import sys
from collections import defaultdict

import click
import yaml

from .mobileconfig import Configuration, MCXPayload, Payload, toxml


def _extend_dict(a, b):
    for k, v in b.items():
        if k in a and v != a[k]:
            raise Exception()
        a[k] = v


def _create_configuration_payloads(reqs, scope="system"):
    def merged(prop):
        out = defaultdict(lambda: defaultdict(dict))
        for req in reqs:
            for scope, domains in req.get(prop, {}).items():
                for domain, keys in domains.items():
                    _extend_dict(out[scope][domain], keys)
        return out

    profiles = merged("profiles")
    defaults = merged("defaults")
    payloads = []
    for domain, keys in profiles[scope].items():
        payloads.append(Payload(domain, **keys))
    for domain, keys in defaults[scope].items():
        payloads.append(MCXPayload(domain, **keys))
    return payloads


def _write_output(output, s):
    if isinstance(s, str):
        s = s.encode()
    if output is None:
        sys.stdout.buffer.write(s)
    else:
        with open(output, "wb") as fp:
            fp.write(s)


@click.command()
@click.option("-i", "--input", "input_", type=str)
@click.option("-id", "--identifier", type=str, required=True)
@click.option("-n", "--display-name", type=str)
@click.option("-s", "--scope", type=str, default="system")
@click.option("-o", "--output", type=str)
def cli(input_, identifier, display_name, scope, output):
    kwargs = {}
    if display_name is not None:
        kwargs["PayloadDisplayName"] = display_name
    if input_ is None:
        reqs = yaml.load(sys.stdin.read())
    else:
        with open(input_, "rt") as fp:
            reqs = yaml.load(fp.read())
    payloads = _create_configuration_payloads(reqs, scope)
    conf = Configuration(
        PayloadIdentifier=identifier, PayloadContent=payloads, **kwargs
    )
    _write_output(output, toxml(conf))


if __name__ == "__main__":
    cli()
