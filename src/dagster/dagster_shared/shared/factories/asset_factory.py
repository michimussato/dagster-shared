import typing

from dagster import (
    asset,
    Output,
    AssetMaterialization,
    AssetsDefinition,
    # RetryPolicy,
    # Backoff,
    # Jitter,
)


# Further Readings:
# - https://dagster.io/blog/unlocking-flexible-pipelines-customizing-asset-decorator


def asset_factory(
        group_name: str,
        spec: dict[
            str, typing.Union[str, callable],
        ],
) -> AssetsDefinition:

    @asset(
        group_name=group_name,
        compute_kind="python",
        key_prefix=spec["key_prefix"],
        name=spec["name"],
        deps=spec["deps"],
        # retry_policy=RetryPolicy(
        #     max_retries=5,
        #     delay=2,
        #     backoff=Backoff.EXPONENTIAL,
        #     jitter=Jitter.FULL,
        # ),
    )
    def _asset() -> typing.Union[Output, AssetMaterialization]:

        yield Output(spec["value"])

        yield AssetMaterialization(
            asset_key=[
                *spec["key_prefix"],
                spec["name"],
            ],
            metadata={
                spec["name"]: spec["type"](spec["value"]),
            },
        )

    return _asset
