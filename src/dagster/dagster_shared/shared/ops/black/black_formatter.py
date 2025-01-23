import os
import subprocess

from dagster import (
    Output,
    AssetMaterialization,
    MetadataValue,
    op,
    In,
    AssetExecutionContext,
)


@op(
    ins={
        "BUILD_CWD": In(),
        "BLACK_EXE": In(),
    },
)
def black_formatter(
        context: AssetExecutionContext,
        BUILD_CWD: str,
        BLACK_EXE: str,
) -> bool:
    """
    Black formatting.

    ```
    Args:
        context ():
        BUILD_CWD ():
        BLACK_EXE ():

    Returns:
        Todo

    ```
    """

    # cmd = (f"{BLACK_EXE} "
    #        ".")
    #
    # proc = subprocess.run(
    #     args=cmd,
    #     cwd=BUILD_CWD,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE,
    #     shell=True,
    #     text=True,
    # )
    #
    # context.log.info(proc.stdout)
    # context.log.error(proc.stderr)

    cmd = [
        BLACK_EXE,
        "."
    ]

    proc = subprocess.Popen(
        args=cmd,
        cwd=BUILD_CWD,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    stdout, stderr = proc.communicate()
    return_code = proc.returncode

    context.log.info(stdout)
    context.log.error(stderr)
    context.log.info(return_code)

    yield Output(True)
    # yield Output(dict(os.environ), output_name="env_full")

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            'cmd': MetadataValue.json(cmd),
            'cmd (str)': MetadataValue.path(" ".join(cmd)),
            'environ (full)': MetadataValue.json(dict(os.environ)),
            'stdout': MetadataValue.md(f"```shell\n{stdout}\n```"),
            'stderr': MetadataValue.md(f"```shell\n{stderr}\n```"),
        }
    )
