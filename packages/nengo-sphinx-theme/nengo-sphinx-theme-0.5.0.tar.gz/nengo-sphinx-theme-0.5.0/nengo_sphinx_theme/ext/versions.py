import warnings

from sphinx.errors import ConfigError


def validate_config(app, config):
    html_context = getattr(config, "html_context", {})
    releases = html_context.get("releases", "").split(",")
    building = html_context.get("building_version", "")

    if "latest" in releases:
        raise ConfigError(
            "nengo_sphinx_theme.ext.versions: 'latest' cannot be a release "
            "name (link to the most up-to-date version of the docs will be "
            "added automatically)")

    if building == "":
        warnings.warn(
            "'building_version' not set, versions will not be rendered")


def setup(app):
    app.connect("config-inited", validate_config)
