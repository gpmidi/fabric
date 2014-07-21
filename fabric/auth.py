"""
Common authentication subroutines. Primarily for internal use.
"""


def get_password(user, host, port):
    from fabric.state import env
    from fabric.network import join_host_strings
    host_string = join_host_strings(user, host, port)
    passCall = env.passwords.get(host_string, env.password)
    if callable(passCall):
        return passCall(user, host, port)
    return passCall


def set_password(user, host, port, password):
    from fabric.state import env
    from fabric.network import join_host_strings
    host_string = join_host_strings(user, host, port)
    env.password = env.passwords[host_string] = password
