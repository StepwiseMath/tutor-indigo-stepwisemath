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
# =============================================================================            
# begin patch: mfe-dockerfile-post-npm-install-learning
# -----------------------------------------------------------------------------

# 1.) install the branding package
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install '@edx/brand@git+https://github.com/StepwiseMath/brand-openedx.git#open-release/redwood.master'

# 2.) install the header component
# note: this is the original code, that works perfectly.
# -------------------------------------
# RUN npm install '@edx/frontend-component-header@npm:@edly-io/indigo-frontend-component-header@~3.0.0'
# note: the source for the npm package is https://github.com/edly-io/frontend-component-header
# note: the Docker build and resulting deployment work as expected.
# -------------------------------------

# new replacement code. this is a fork of https://github.com/edly-io/frontend-component-header
# -------------------------------------
# 2.a) install frontend-component-header from source
RUN git clone -b open-release/redwood.master https://github.com/StepwiseMath/frontend-component-header.git /openedx/app/frontend-component-header

# 2.b) install peer dependencies
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm install -g install-peerdeps
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && install-peerdeps --dev -Y


# 2.c) install and build the header component
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm ci && npm run i18n_extract && npm run build
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/ && npm install

# 2.d) link frontend-component-header to the openedx/app directory
RUN cd /openedx/app/frontend-component-header && npm link
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/ && npm link @edx/frontend-component-header

# note: the Docker build works, but the resulting deployment raises this js console browser error:
# TypeError: Cannot read properties of undefined (reading 'getLoginRedirectUrl')
#
# the error is raised by the following ReactJS module -- src/learning-header/AnonymousUserMenu.jsx -- 
# in the forked header component https://github.com/StepwiseMath/frontend-component-header.git:
#     import React from 'react';

#     import { getConfig } from '@edx/frontend-platform';
#     import { getLoginRedirectUrl } from '@edx/frontend-platform/auth';
#     import { injectIntl, intlShape } from '@edx/frontend-platform/i18n';
#     import { Button } from '@openedx/paragon';

#     import genericMessages from '../generic/messages';

#     const AnonymousUserMenu = ({ intl }) => (
#       <div>
#         <Button
#           className="mr-3"
#           variant="outline-primary"
#           href={`${getConfig().LMS_BASE_URL}/register?next=${encodeURIComponent(global.location.href)}`}
#         >
#           {intl.formatMessage(genericMessages.registerSentenceCase)}
#         </Button>
#         <Button
#           variant="primary"
#           href={`${getLoginRedirectUrl(global.location.href)}`}
#         >
#           {intl.formatMessage(genericMessages.signInSentenceCase)}
#         </Button>
#       </div>
#     );

#     AnonymousUserMenu.propTypes = {
#       intl: intlShape.isRequired,
#     };

#     export default injectIntl(AnonymousUserMenu);

# -------------------------------------

# note: the broken import getLoginRedirectUrl from the frontend-platform/auth module is installed during the 'npm clean-install' step
# in 'FROM base AS learning-common'. It appears that npm is able to automatically link the frontend-platform/auth module to the header component when 
# installing from the npm registry, but not when installing from a local directory. My commandds above that include 'npm link' are intended to mitigate
# this issue, but they do not work as expected. I will need to investigate further.


# 3.) install the footer component
RUN npm install @edly-io/indigo-frontend-component-footer@^2.0.0
COPY indigo/env.config.jsx /openedx/app/

# -----------------------------------------------------------------------------
# end patch mfe-dockerfile-post-npm-install-learning
# =============================================================================            
""",
        ),
        (
            "mfe-dockerfile-post-npm-install-authn",
            """
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install --save '@edx/brand@git+https://github.com/StepwiseMath/brand-openedx.git#open-release/redwood.master'
""",
        ),
        # copy node_modules to the openedx build directory
        (
            "mfe-dockerfile-production-final",
            """
# mcdaniel: Copy node_modules to the final container so that we can audit the final results.
COPY --from=learning-prod /openedx/app/node_modules/ /openedx/app/node_modules/
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
