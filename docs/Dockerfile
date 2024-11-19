# syntax=docker/dockerfile:1
# https://hub.docker.com/_/node/tags
FROM docker.io/node:18.19.0-bullseye-slim AS base

RUN apt update \
  && apt install -y git \
    # required for cwebp-bin
    gcc libgl1 libxi6 make \
    # required for gifsicle, mozjpeg, and optipng (on arm)
    autoconf libtool pkg-config zlib1g-dev \
    # required for node-sass (on arm)
    python g++ \
    # required for image-webpack-loader (on arm)
    libpng-dev \
    # required for building node-canvas (on arm, for course-authoring)
    # https://www.npmjs.com/package/canvas
    libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev

RUN mkdir -p /openedx/app /openedx/env
WORKDIR /openedx/app
ENV PATH=/openedx/app/node_modules/.bin:${PATH}




####################### authn MFE
######## authn (git)
FROM base AS authn-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-authn.git#open-release/redwood.2 .

######## authn (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch AS authn-src
COPY --from=authn-git /openedx/app /

######## authn (common)
FROM base AS authn-common
COPY --from=authn-src /package.json /openedx/app/package.json
COPY --from=authn-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install --save '@edx/brand@git+https://github.com/StepwiseMath/brand-openedx.git#open-release/redwood.master'
COPY --from=authn-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository=openedx/openedx-translations --revision=open-release/redwood.2 " pull_translations

EXPOSE 1999

# Configuration needed at build time
ENV APP_ID=authn
ENV PUBLIC_PATH='/authn/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## authn (dev)
FROM authn-common AS authn-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### account MFE
######## account (git)
FROM base AS account-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-account.git#open-release/redwood.2 .

######## account (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch AS account-src
COPY --from=account-git /openedx/app /

######## account (common)
FROM base AS account-common
COPY --from=account-src /package.json /openedx/app/package.json
COPY --from=account-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=account-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository=openedx/openedx-translations --revision=open-release/redwood.2 " pull_translations

EXPOSE 1997

# Configuration needed at build time
ENV APP_ID=account
ENV PUBLIC_PATH='/account/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## account (dev)
FROM account-common AS account-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### communications MFE
######## communications (git)
FROM base AS communications-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-communications.git#open-release/redwood.2 .

######## communications (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch AS communications-src
COPY --from=communications-git /openedx/app /

######## communications (common)
FROM base AS communications-common
COPY --from=communications-src /package.json /openedx/app/package.json
COPY --from=communications-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=communications-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository=openedx/openedx-translations --revision=open-release/redwood.2 " pull_translations

EXPOSE 1984

# Configuration needed at build time
ENV APP_ID=communications
ENV PUBLIC_PATH='/communications/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## communications (dev)
FROM communications-common AS communications-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### course-authoring MFE
######## course-authoring (git)
FROM base AS course-authoring-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-course-authoring.git#open-release/redwood.2 .

######## course-authoring (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch AS course-authoring-src
COPY --from=course-authoring-git /openedx/app /

######## course-authoring (common)
FROM base AS course-authoring-common
COPY --from=course-authoring-src /package.json /openedx/app/package.json
COPY --from=course-authoring-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=course-authoring-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository=openedx/openedx-translations --revision=open-release/redwood.2 " pull_translations

EXPOSE 2001

# Configuration needed at build time
ENV APP_ID=course-authoring
ENV PUBLIC_PATH='/course-authoring/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## course-authoring (dev)
FROM course-authoring-common AS course-authoring-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### discussions MFE
######## discussions (git)
FROM base AS discussions-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-discussions.git#open-release/redwood.2 .

######## discussions (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch AS discussions-src
COPY --from=discussions-git /openedx/app /

######## discussions (common)
FROM base AS discussions-common
COPY --from=discussions-src /package.json /openedx/app/package.json
COPY --from=discussions-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=discussions-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository=openedx/openedx-translations --revision=open-release/redwood.2 " pull_translations

EXPOSE 2002

# Configuration needed at build time
ENV APP_ID=discussions
ENV PUBLIC_PATH='/discussions/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## discussions (dev)
FROM discussions-common AS discussions-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### gradebook MFE
######## gradebook (git)
FROM base AS gradebook-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-gradebook.git#open-release/redwood.2 .

######## gradebook (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch AS gradebook-src
COPY --from=gradebook-git /openedx/app /

######## gradebook (common)
FROM base AS gradebook-common
COPY --from=gradebook-src /package.json /openedx/app/package.json
COPY --from=gradebook-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=gradebook-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository=openedx/openedx-translations --revision=open-release/redwood.2 " pull_translations

EXPOSE 1994

# Configuration needed at build time
ENV APP_ID=gradebook
ENV PUBLIC_PATH='/gradebook/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## gradebook (dev)
FROM gradebook-common AS gradebook-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### learner-dashboard MFE
######## learner-dashboard (git)
FROM base AS learner-dashboard-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-learner-dashboard.git#open-release/redwood.2 .

######## learner-dashboard (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch AS learner-dashboard-src
COPY --from=learner-dashboard-git /openedx/app /

######## learner-dashboard (common)
FROM base AS learner-dashboard-common
COPY --from=learner-dashboard-src /package.json /openedx/app/package.json
COPY --from=learner-dashboard-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=learner-dashboard-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository=openedx/openedx-translations --revision=open-release/redwood.2 " pull_translations

EXPOSE 1996

# Configuration needed at build time
ENV APP_ID=learner-dashboard
ENV PUBLIC_PATH='/learner-dashboard/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## learner-dashboard (dev)
FROM learner-dashboard-common AS learner-dashboard-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### learning MFE
######## learning (git)
FROM base AS learning-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-learning.git#open-release/redwood.2 .

######## learning (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch AS learning-src
COPY --from=learning-git /openedx/app /

######## learning (common)
FROM base AS learning-common
COPY --from=learning-src /package.json /openedx/app/package.json
COPY --from=learning-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


# =============================================================================            
# begin patch: mfe-dockerfile-post-npm-install-learning
# -----------------------------------------------------------------------------

# 1.) install the branding package
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install '@edx/brand@git+https://github.com/StepwiseMath/brand-openedx.git#open-release/redwood.master'

# 2.a) clone frontend-component-header source
RUN git clone -b open-release/redwood.master https://github.com/StepwiseMath/frontend-component-header.git /openedx/app/frontend-component-header

# 2.b) install and build the header component from source
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/frontend-component-header && npm ci && npm run i18n_extract && npm run build

# 2.c) link frontend-component-header to the openedx/app directory
RUN cd /openedx/app/frontend-component-header && npm link
RUN --mount=type=cache,target=/root/.npm,sharing=shared cd /openedx/app/ && npm link @edx/frontend-component-header

# 2.d) install into the @edx/frontend-component-header package
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install '@edx/frontend-component-header@/openedx/app/frontend-component-header/'

# 4.) install the footer component
RUN npm install @edly-io/indigo-frontend-component-footer@^2.0.0
COPY indigo/env.config.jsx /openedx/app/

RUN --mount=type=cache,target=/root/.npm,sharing=shared npm install

# -----------------------------------------------------------------------------
# end patch mfe-dockerfile-post-npm-install-learning
# =============================================================================            
COPY --from=learning-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository=openedx/openedx-translations --revision=open-release/redwood.2 " pull_translations

EXPOSE 2000

# Configuration needed at build time
ENV APP_ID=learning
ENV PUBLIC_PATH='/learning/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## learning (dev)
FROM learning-common AS learning-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### ora-grading MFE
######## ora-grading (git)
FROM base AS ora-grading-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-ora-grading.git#open-release/redwood.2 .

######## ora-grading (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch AS ora-grading-src
COPY --from=ora-grading-git /openedx/app /

######## ora-grading (common)
FROM base AS ora-grading-common
COPY --from=ora-grading-src /package.json /openedx/app/package.json
COPY --from=ora-grading-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=ora-grading-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository=openedx/openedx-translations --revision=open-release/redwood.2 " pull_translations

EXPOSE 1993

# Configuration needed at build time
ENV APP_ID=ora-grading
ENV PUBLIC_PATH='/ora-grading/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## ora-grading (dev)
FROM ora-grading-common AS ora-grading-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]

####################### profile MFE
######## profile (git)
FROM base AS profile-git
ADD --keep-git-dir=true https://github.com/openedx/frontend-app-profile.git#open-release/redwood.2 .

######## profile (src)
# Empty layer with just the repo at the root, for build-time bind-mounts
FROM scratch AS profile-src
COPY --from=profile-git /openedx/app /

######## profile (common)
FROM base AS profile-common
COPY --from=profile-src /package.json /openedx/app/package.json
COPY --from=profile-src /package-lock.json /openedx/app/package-lock.json
ARG NPM_REGISTRY=https://registry.npmjs.org/


ENV CPPFLAGS=-DPNG_ARM_NEON_OPT=0
ENV PACT_SKIP_BINARY_INSTALL=true
RUN --mount=type=cache,target=/root/.npm,sharing=shared npm clean-install --no-audit --no-fund --registry=$NPM_REGISTRY


COPY --from=profile-src / /openedx/app

RUN make OPENEDX_ATLAS_PULL=true ATLAS_OPTIONS="--repository=openedx/openedx-translations --revision=open-release/redwood.2 " pull_translations

EXPOSE 1995

# Configuration needed at build time
ENV APP_ID=profile
ENV PUBLIC_PATH='/profile/'
# We could in theory point the mfe_config API directly to the LMS. But for that we would
# have to code the LMS url into the mfe image, and this configuration is user-dependent.
# So we point to a relative url that will be a proxy for the LMS.
ENV MFE_CONFIG_API_URL=/api/mfe_config/v1
ARG ENABLE_NEW_RELIC=false



######## profile (dev)
FROM profile-common AS profile-dev
ENV NODE_ENV=development
CMD ["/bin/bash", "-c", "npm run start --- --config ./webpack.dev-tutor.config.js"]


# Production images are last to accelerate dev image building
######## authn (production)
FROM authn-common AS authn-prod
ENV NODE_ENV=production
RUN npm run build



######## account (production)
FROM account-common AS account-prod
ENV NODE_ENV=production
RUN npm run build



######## communications (production)
FROM communications-common AS communications-prod
ENV NODE_ENV=production
RUN npm run build



######## course-authoring (production)
FROM course-authoring-common AS course-authoring-prod
ENV NODE_ENV=production
RUN npm run build



######## discussions (production)
FROM discussions-common AS discussions-prod
ENV NODE_ENV=production
RUN npm run build



######## gradebook (production)
FROM gradebook-common AS gradebook-prod
ENV NODE_ENV=production
RUN npm run build



######## learner-dashboard (production)
FROM learner-dashboard-common AS learner-dashboard-prod
ENV NODE_ENV=production
RUN npm run build



######## learning (production)
FROM learning-common AS learning-prod
ENV NODE_ENV=production
RUN npm run build



######## ora-grading (production)
FROM ora-grading-common AS ora-grading-prod
ENV NODE_ENV=production
RUN npm run build



######## profile (production)
FROM profile-common AS profile-prod
ENV NODE_ENV=production
RUN npm run build




####### final production image with all static assets
FROM docker.io/caddy:2.7.4 AS production

RUN mkdir -p /openedx/dist

# Copy static assets

COPY --from=authn-prod /openedx/app/dist /openedx/dist/authn

COPY --from=account-prod /openedx/app/dist /openedx/dist/account

COPY --from=communications-prod /openedx/app/dist /openedx/dist/communications

COPY --from=course-authoring-prod /openedx/app/dist /openedx/dist/course-authoring

COPY --from=discussions-prod /openedx/app/dist /openedx/dist/discussions

COPY --from=gradebook-prod /openedx/app/dist /openedx/dist/gradebook

COPY --from=learner-dashboard-prod /openedx/app/dist /openedx/dist/learner-dashboard

COPY --from=learning-prod /openedx/app/dist /openedx/dist/learning

COPY --from=ora-grading-prod /openedx/app/dist /openedx/dist/ora-grading

COPY --from=profile-prod /openedx/app/dist /openedx/dist/profile

