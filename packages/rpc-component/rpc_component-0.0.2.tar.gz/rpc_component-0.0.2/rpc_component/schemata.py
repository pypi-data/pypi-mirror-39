from collections import ChainMap
from functools import partial
import re

from schema import And, Optional, Or, Regex, Schema


def sorted_versions(versions):
    return sorted(
        versions,
        key=lambda v: version_key(v["version"]),
        reverse=True,
    )


def is_sorted_versions(versions):
    return versions == sorted_versions(versions)


def is_value_unique(key):
    def fn(data):
        values = [v[key] for v in data]
        return len(values) == len(set(values))
    fn.__name__ = "is_{value}_unique".format(value=key)
    return fn


def is_version_ids_unique(releases):
    is_version_unique = is_value_unique("version")
    return is_version_unique((v for r in releases for v in r["versions"]))


sha_regex = r"^[0-9a-f]{40}$"
version_regex = (
    r"^(?P<version>r?"
    r"(?P<major>[0-9]+)\."
    r"(?P<minor>[0-9]+)\."
    r"(?P<patch>[0-9]+)"
    r"(-(?P<prerelease>alpha|beta|rc)\."
    r"(?P<prerelease_version>[0-9]+))?)$"
)

version_id_schema = Regex(version_regex)
version_sha_schema = Regex(sha_regex)
version_schema = Schema(
    {
        "version": version_id_schema,
        "sha": version_sha_schema,
    },
)

comparison_added_version_schema = Schema(
    And(
        {
            And(str, len): {
                "added": {
                    "releases": And(
                        [
                            {
                                Optional("series"): And(str, len),
                                "versions": And(
                                    [version_schema],
                                    lambda vs: len(vs) == 1,
                                ),
                            }
                        ],
                        lambda rs: len(rs) == 1,
                    )
                },
                "deleted": {},
            }
        },
        lambda cs: len(cs) == 1,
    )
)

repo_url_schema = Regex(r"^https://github.com/.+")

comparison_operator_regex = r"(?P<comparison_operator>(=|!)=|(<|>)=?)"
constraint_regex = (
    r"(?P<version>r?(?P<major>[0-9]+)"
    r"(\.(?P<minor>[0-9]+)"
    r"(\.(?P<patch>[0-9]+)"
    r"(-(?P<prerelease>alpha|beta|rc)\."
    r"(?P<prerelease_version>[0-9]+))?)?)?)"
)
version_constraint_regex = r"^version{op}{version}$".format(
    op=comparison_operator_regex,
    version=constraint_regex,
)
branch_constraint_regex = r"^branch==(?P<branch_name>.+)$"
branch_constraints_schema = And(
    [Regex(branch_constraint_regex)],
    lambda cs: len(cs) == 1,
)

constraints_schema = Or(
    [Regex(version_constraint_regex)],
    branch_constraints_schema,
)

component_single_version_schema = Schema(
    {
        "name": And(str, len),
        "repo_url": repo_url_schema,
        "is_product": bool,
        "release": {
            "series": And(str, len),
            "version": version_id_schema,
            "sha": version_sha_schema,
        },
        Optional("artifact_stores", default=[]): And(
            [
                {
                    "description": Or(str, None),
                    "name": And(str, len),
                    "public_url": And(str, len),
                    "type": And(str, len),
                },
            ],
            is_value_unique("name"),
        ),
    }
)

component_schema = Schema(
    {
        "name": And(str, len),
        "repo_url": repo_url_schema,
        "is_product": bool,
        "releases": And(
            [
                {
                    "series": And(str, len),
                    "versions": And(
                        [
                            version_schema,
                        ],
                        is_sorted_versions,
                    ),
                },
            ],
            is_value_unique("series"),
            is_version_ids_unique,
        ),
        Optional("artifact_stores", default=[]): And(
            [
                {
                    "description": Or(str, None),
                    "name": And(str, len),
                    "public_url": And(str, len),
                    "type": And(str, len),
                },
            ],
            is_value_unique("name"),
        ),
    }
)

dependencies_schema = Schema(
    {
        Optional("dependencies"): And(
            [
                {
                    "name": And(str, len),
                    "constraints": constraints_schema,
                },
            ],
            is_value_unique("name"),
        )
    }
)

artifacts_file_schema = Schema(
    {
        "type": "file",
        "source": And(str, len),
        Optional("dest"): And(str, len),
        Optional("expire_after"): And(int, lambda n: n > 0)
    }
)

artifacts_log_schema = Schema(
    {
        "type": "log",
        "source": And(str, len)
    }
)

artifacts_schema = Schema(
    {
        Optional("artifacts"):
            [
                Or(artifacts_file_schema, artifacts_log_schema)
            ]
    }
)

jenkins_schema = Schema(
    {
        Optional("jenkins"): {
            Optional("jjb_paths"): [And(str, len)],
        }
    }
)

component_metadata_schema = Schema(
    dict(
        ChainMap(
            *(s._schema for s in
                (
                    dependencies_schema,
                    artifacts_schema,
                    jenkins_schema,
                )
              )
        )
    )
)

component_requirements_schema = Schema(
    {
        "dependencies": And(
            [
                {
                    "name": And(str, len),
                    "ref": Or(And(str, len), None),
                    "ref_type": Or(lambda r: r in ("branch", "tag"), None),
                    "repo_url": repo_url_schema,
                    "sha": version_sha_schema,
                    "version": Or(version_id_schema, None),
                }
            ],
            is_value_unique("name"),
        ),
    }
)

comparison_added_component_schema = Schema(
    And(
        {
            And(str, len): {
                "added": And(component_schema),
                "deleted": {},
            }
        },
        lambda cs: len(cs) == 1,
    )
)

comparison_added_artifact_stores_schema = Schema(
    And(
        {
            And(str, len): {
                "added": {
                    "artifact_stores": And(
                        [
                            {
                                "description": Or(str, None),
                                "name": And(str, len),
                                "public_url": And(str, len),
                                "type": And(str, len),
                            },
                        ],
                        is_value_unique("name"),
                    ),
                },
                "deleted": {},
            }
        },
        lambda s: len(s) == 1,
    )
)


def _version_key(version_id, regex=None):
    prerelease_map = {
        "alpha": 0,
        "beta": 1,
        "rc": 2,
        None: 3,
    }

    def int_or_none(x): return x if x is None else int(x)

    v = re.match(regex, version_id)
    major = int(v.group("major"))
    minor = int_or_none(v.group("minor"))
    patch = int_or_none(v.group("patch"))
    prerelease = prerelease_map[v.group("prerelease")]
    prerelease_version = int(v.group("prerelease_version") or 0)

    return (major, minor, patch, prerelease, prerelease_version)


version_key = partial(_version_key, regex=version_regex)
constraint_key = partial(_version_key, regex=constraint_regex)
