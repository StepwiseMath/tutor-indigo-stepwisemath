from __future__ import annotations

import os
import typing as t

import importlib_resources
from tutor import hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

# Handle version suffix in nightly mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__


################# Configuration
config: t.Dict[str, t.Dict[str, t.Any]] = {
    # Add here your new settings
    "defaults": {
        "VERSION": __version__,
        "WELCOME_MESSAGE": "The place for all your online learning",
        "ENABLE_DARK_THEME": False,
        "PRIMARY_COLOR": "#15376D",  # Indigo
        # Footer links are dictionaries with a "title" and "url"
        # To remove all links, run:
        # tutor config save --set INDIGO_FOOTER_NAV_LINKS=[]
        "FOOTER_NAV_LINKS": [
            {"title": "About Us", "url": "/about"},
            {"title": "Blog", "url": "/blog"},
            {"title": "Donate", "url": "/donate"},
            {"title": "Terms of Service", "url": "/tos"},
            {"title": "Privacy Policy", "url": "/privacy"},
            {"title": "Help", "url": "/help"},
            {"title": "Contact Us", "url": "/contact"},
        ],
    },
    "unique": {},
    "overrides": {},
}

# Theme templates
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    str(importlib_resources.files("tutorindigo") / "templates")
)
# This is where the theme is rendered in the openedx build directory
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("indigo", "build/openedx/themes"),
        ("indigo/env.config.jsx", "plugins/mfe/build/mfe"),
    ],
)

# Force the rendering of scss files, even though they are included in a "partials" directory
hooks.Filters.ENV_PATTERNS_INCLUDE.add_items(
    [
        r"indigo/lms/static/sass/partials/lms/theme/",
        r"indigo/cms/static/sass/partials/cms/theme/",
    ]
)


# init script: set theme automatically
with open(
    os.path.join(
        str(importlib_resources.files("tutorindigo") / "templates"),
        "indigo",
        "tasks",
        "init.sh",
    ),
    encoding="utf-8",
) as task_file:
    hooks.Filters.CLI_DO_INIT_TASKS.add_item(("lms", task_file.read()))


# Override openedx & mfe docker image names
@hooks.Filters.CONFIG_DEFAULTS.add(priority=hooks.priorities.LOW)
def _override_openedx_docker_image(
    items: list[tuple[str, t.Any]]
) -> list[tuple[str, t.Any]]:
    openedx_image = ""
    mfe_image = ""
    for k, v in items:
        if k == "DOCKER_IMAGE_OPENEDX":
            openedx_image = v
        elif k == "MFE_DOCKER_IMAGE":
            mfe_image = v
    if openedx_image:
        items.append(("DOCKER_IMAGE_OPENEDX", f"{openedx_image}-indigo"))
    if mfe_image:
        items.append(("MFE_DOCKER_IMAGE", f"{mfe_image}-indigo"))
    return items


# Load all configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"INDIGO_{key}", value) for key, value in config["defaults"].items()]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"INDIGO_{key}", value) for key, value in config["unique"].items()]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))


hooks.Filters.ENV_PATCHES.add_items(
    [
        # MFE will install header version 3.0.x and will include indigo-footer as a
        # separate package for use in env.config.jsx
        (
            "mfe-dockerfile-post-npm-install-learning",
            """
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install '@edx/brand@git+https://github.com/StepwiseMath/brand-openedx.git#open-release/redwood.master'

RUN git clone -b open-release/redwood.master https://github.com/StepwiseMath/frontend-component-header.git /openedx/app/frontend-component-header
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm install && npm run build
RUN cd /openedx/app/frontend-component-header && npm link
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm link @edx/frontend-component-header

RUN npm install @edly-io/indigo-frontend-component-footer@^2.0.0
COPY indigo/env.config.jsx /openedx/app/
""",
        ),
        (
            "mfe-dockerfile-post-npm-install-authn",
            """
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install --save '@edx/brand@git+https://github.com/StepwiseMath/brand-openedx.git#open-release/redwood.master'
""",
        ),
        # Tutor-Indigo v2.1 targets the styling updates in discussions and learner-dashboard MFE
        # brand-openedx is related to styling updates while others are for header and footer updates
        (
            "mfe-dockerfile-post-npm-install-discussions",
            """
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install '@edx/brand@git+https://github.com/StepwiseMath/brand-openedx.git#open-release/redwood.master'

RUN git clone -b open-release/redwood.master https://github.com/StepwiseMath/frontend-component-header.git /openedx/app/frontend-component-header
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm install && npm run build
RUN cd /openedx/app/frontend-component-header && npm link
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm link @edx/frontend-component-header

RUN npm install @edly-io/indigo-frontend-component-footer@^2.0.0
COPY indigo/env.config.jsx /openedx/app/
""",
        ),
        (
            "mfe-dockerfile-post-npm-install-learner-dashboard",
            """
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install '@edx/brand@git+https://github.com/StepwiseMath/brand-openedx.git#open-release/redwood.master'

RUN git clone -b open-release/redwood.master https://github.com/StepwiseMath/frontend-component-header.git /openedx/app/frontend-component-header
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm install && npm run build
RUN cd /openedx/app/frontend-component-header && npm link
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm link @edx/frontend-component-header

RUN npm install @edly-io/indigo-frontend-component-footer@^2.0.0
COPY indigo/env.config.jsx /openedx/app/
""",
        ),
        (
            "mfe-dockerfile-post-npm-install-profile",
            """
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install '@edx/brand@git+https://github.com/StepwiseMath/brand-openedx.git#open-release/redwood.master'

RUN git clone -b open-release/redwood.master https://github.com/StepwiseMath/frontend-component-header.git /openedx/app/frontend-component-header
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm install && npm run build
RUN cd /openedx/app/frontend-component-header && npm link
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm link @edx/frontend-component-header

RUN npm install @edly-io/indigo-frontend-component-footer@^2.0.0
COPY indigo/env.config.jsx /openedx/app/
""",
        ),
        (
            "mfe-dockerfile-post-npm-install-account",
            """
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install '@edx/brand@git+https://github.com/StepwiseMath/brand-openedx.git#open-release/redwood.master'

RUN git clone -b open-release/redwood.master https://github.com/StepwiseMath/frontend-component-header.git /openedx/app/frontend-component-header
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm install && npm run build
RUN cd /openedx/app/frontend-component-header && npm link
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm link @edx/frontend-component-header

RUN npm install @edly-io/indigo-frontend-component-footer@^2.0.0
COPY indigo/env.config.jsx /openedx/app/
""",
        ),
    ]
)

# Include js file in lms main.html, main_django.html, and certificate.html

hooks.Filters.ENV_PATCHES.add_items(
    [
        # for production
        (
            "openedx-common-assets-settings",
            """
javascript_files = ['base_application', 'application', 'certificates_wv']
dark_theme_filepath = ['indigo/js/dark-theme.js']

for filename in javascript_files:
    if filename in PIPELINE['JAVASCRIPT']:
        PIPELINE['JAVASCRIPT'][filename]['source_filenames'] += dark_theme_filepath
  
""",
        ),
        # for development
        (
            "openedx-lms-development-settings",
            """
javascript_files = ['base_application', 'application', 'certificates_wv']
dark_theme_filepath = ['indigo/js/dark-theme.js']

for filename in javascript_files:
    if filename in PIPELINE['JAVASCRIPT']:
        PIPELINE['JAVASCRIPT'][filename]['source_filenames'] += dark_theme_filepath
""",
        ),
    ]
)
