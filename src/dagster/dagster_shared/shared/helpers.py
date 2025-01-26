import select
import typing


__all__ = [
    "iterate_fds",
]


def iterate_fds(
        *,
        handles: tuple[
            typing.Optional[typing.IO[bytes]],
            typing.Optional[typing.IO[bytes]],
        ],
        labels: tuple[str, str],
        functions: tuple[
            callable, callable,
        ],
        do_print: bool = True,
        live_print=False,
) -> dict[str, bytes]:
    """
    Can be used to live-feed stdout and stderr of a
    subprocess.Popen.stdout/stderr stream to an
    appropriate logging stream like info and warning.
    stdout -> logging.info
    stderr -> logging.warning

    Usage:

    ```
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    handles = (proc.stdout, proc.stderr)
    labels = ("stdout", "stderr")
    functions = (context.log.info, context.log.warning)
    logs = helpers.iterate_fds(
        handles=handles,
        labels=labels,
        functions=functions,
        live_print=False,
    )

    for _label, _function in zip(labels, functions):
        if bool(logs[_label]):
            _function(logs[_label].decode("utf-8"))
    ```

    Reference:

    https://alexandre.deverteuil.net/post/monitor-python-subprocess-output-streams-real-time/

    Args:
        handles (tuple[
                typing.Optional[typing.IO[bytes]],
                typing.Optional[typing.IO[bytes]],
            ]): io.BufferedReader
        labels (tuple[str, str]):
        functions (tuple[
                callable, callable,
            ]): bound method (Logger.info, Logger.warning)
        live_print (bool): Do you want to live_print? (False is equivalent to "summarize")

    Returns: dict[callable, bytes]

    """

    ret = dict()

    for label in labels:
        ret[label] = bytes()

    methods = dict(zip(handles, zip(labels, functions)))

    while methods:
        for handle in select.select(methods.keys(), tuple(), tuple())[0]:

            label = methods[handle][0]
            function = methods[handle][1]
            line = handle.readline()

            if line:
                # Todo
                #  - [ ] what does live_print do?
                if live_print:
                    function(line.decode("utf-8"))

                if do_print:
                    print(line.decode("utf-8"))
                ret[label] += line

                # This is from the reference, but can't
                # tell the difference so far other than
                # not cutting off the last character in
                # a line without \n
                # methods[handle](line[:-1].decode("utf-8"))
            else:
                methods.pop(handle)

    return ret
