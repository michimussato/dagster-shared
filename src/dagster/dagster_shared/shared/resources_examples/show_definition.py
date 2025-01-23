from dagster_shared.shared.factories.asset_factory import asset_factory

from dagster import (MetadataValue,
                     AssetsDefinition,
                     )


JOB = "show"
SCENE = "scene"
LOCATION = "location"
VERSION = "123"


show_dict = {
    "group_name": f"{LOCATION}_{JOB}_{SCENE}_{VERSION}",
    "assets": [
        # # Template:
        # {
        #     "name": ,
        #     "key_prefix": [],
        #     "value": ,
        #     "type": MetadataValue.,
        #     "deps": {},
        # },
        {
            "name": "JOB",
            "key_prefix": [],
            "value": JOB,
            "type": MetadataValue.text,
            "deps": {},
        },
        {
            "name": "SCENE",
            "key_prefix": [],
            "value": SCENE,
            "type": MetadataValue.text,
            "deps": {},
        },
        {
            "name": "LOCATION",
            "key_prefix": [],
            "value": LOCATION,
            "type": MetadataValue.text,
            "deps": {},
        },
        {
            "name": "INPUT_PATH",
            "key_prefix": [],
            "value": f'/.../{LOCATION}/{JOB}/{SCENE}/.../{SCENE}...v{VERSION}',
            "type": MetadataValue.path,
            "deps": {},
        },
    ]
}


def get_show_assets() -> list[AssetsDefinition]:
    show_assets = [
        asset_factory(
            group_name=f"SHOW__{show_dict['group_name']}",
            spec=spec,
        ) for spec in show_dict["assets"]
    ]
    return show_assets


if __name__ == "__main__":
    get_show_assets()
