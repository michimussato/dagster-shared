import pathlib

from dagster_shared.shared.factories.asset_factory import asset_factory

from dagster import (
    AssetsDefinition,
    MetadataValue,
)


package: str = ""
version: str = "1.1.1"
git_repo: str = ""


package_dict: dict = {
    "package": package,
    "version": version,
    "git_repo": git_repo,
    "group_name": package,
    "assets": [
        {
            # The local folder where the package.py file of this package lives
            "name": "BUILD_CWD",
            "key_prefix": [package],
            "value": f"",
            "type": MetadataValue.path,
            "deps": {},
        },
        {
            # The SSH Git Repo URL
            "name": "GIT_SSH",
            "key_prefix": [package],
            "value": f"git@github.com:....git",
            "type": MetadataValue.path,
            "deps": {},
        },
        {
            "name": "GIT_REPO_NAME",
            "key_prefix": [package],
            "value": git_repo,
            "type": MetadataValue.text,
            "deps": {},
        },
        {
            # The name of the main branch
            "name": "MASTER_BRANCH",
            "key_prefix": [package],
            "value": "master",
            "type": MetadataValue.text,
            "deps": {},
        },
        # {
        #     # The link to th OPEN pull request
        #     "name": "PACKAGE_PR",
        #     "key_prefix": package,
        #     "value": "https://github.com/.../.../pull/1966",
        #     "type": MetadataValue.url,
        #     "deps": {},
        # },
        {
            # The package name as defined in the package.py (can be different
            # from repo name)
            "name": "PACKAGE_NAME",
            "key_prefix": [package],
            "value": package,
            "type": MetadataValue.text,
            "deps": {},
        },
        {
            # The incremented package version (checkout +major/minor/patch)
            "name": "PACKAGE_VERSION",
            "key_prefix": [package],
            "value": version,
            "type": MetadataValue.text,
            "deps": {},
        },
    ],
}


def get_package_assets() -> list[AssetsDefinition]:
    package_assets = [
        asset_factory(
            group_name=f"PACKAGE__{package_dict['group_name']}",
            spec=spec,
        ) for spec in package_dict["assets"]
    ]
    return package_assets


# Creates a group of individual assets for each dict inside the package_dict["assets"] list.
# Works similarly like @multi_asset but seems easier to control.
if __name__ == "__main__":
    get_package_assets()
