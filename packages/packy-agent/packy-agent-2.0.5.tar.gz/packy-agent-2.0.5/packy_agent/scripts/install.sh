#!/usr/bin/env bash

export VENVS_DIR=$1
export PACKY_TEMP_VENV=$2
export VIRTUALENVWRAPPER_PYTHON=$3
export PACKY_SERVER_BASE_URL=$4

PACKY_TEMP_VENV_DIR=$VENVS_DIR/$PACKY_TEMP_VENV

# Because we are running Ansible we need to install it first. pipenv does not let easily generate
# requirements.txt for `ansible`-only, so we have to install the entire requirements.txt here.
# In order to do so we need to install system dependencies here (mostly lib*-package).
# Therefore we detect OS here not with Ansible (since it is not installed yet).

echo '==> Detecting operating system...'
if [ -f /etc/lsb-release ]; then
    source /etc/lsb-release
    if [ "$DISTRIB_ID" == "Ubuntu" -a "$DISTRIB_RELEASE" == "18.04" -o "$DISTRIB_ID" == "Ubuntu" -a "$DISTRIB_RELEASE" == "16.04" ]; then
        echo "==> Detected supported operating system $DISTRIB_DESCRIPTION (DISTRIB_ID=$DISTRIB_ID, DISTRIB_RELEASE=$DISTRIB_RELEASE)"
        echo '==> Installing system dependencies...'
        if [ "$DISTRIB_ID" == "Ubuntu" ]; then
            add-apt-repository universe
        fi

        apt-get update
        apt-get install -y libcurl4-openssl-dev \
                           libffi-dev \
                           liblz4-dev \
                           libsasl2-dev \
                           libssl-dev \
                           pkg-config

        echo '==> Installing Console dependencies...'
        apt-get install -y nginx
        apt-get install -y git
    else
        echo "Your operating system $DISTRIB_DESCRIPTION (DISTRIB_ID=$DISTRIB_ID, DISTRIB_RELEASE=$DISTRIB_RELEASE) is not supported"
        exit 1
    fi
elif [ -f /etc/alpine-release ]; then
    # TODO(dmu) MEDIUM: Alpine OS detection can be done via /etc/os-release too
    echo '==> Detected supported operating system Alpine '`cat /etc/alpine-release`
    echo '==> Installing system dependencies...'
    export PYCURL_SSL_LIBRARY=openssl

    apk update
    apk add linux-headers build-base pcre-dev libffi-dev libressl-dev curl-dev
    apk add nginx
    apk add git  # to let `pip` install dependencies from git
elif [ -f /etc/os-release ]; then
    source /etc/os-release
    if [ "$ID" == "raspbian" -a "$VERSION_ID" == "9" ]; then
        echo "==> Detected supported operating system \$PRETTY_NAME (ID=\$ID, VERSION_ID=\$VERSION_ID)"
        echo '==> Installing system dependencies...'

        apt-get update
        apt-get install -y libcurl4-openssl-dev \
                           libffi-dev \
                           liblz4-dev \
                           libsasl2-dev \
                           libssl-dev \
                           pkg-config

        echo '==> Installing Console dependencies...'
        apt-get install -y nginx
        apt-get install -y git
    else
        echo "Your operating system \$PRETTY_NAME (ID=\$ID, VERSION_ID=\$VERSION_ID) is not supported"
        exit 1
    fi
else
    echo 'Your operating system is not supported'
    exit 1
fi
set -e
set -x


echo '==> Activating temporary virtualenv...'
source $PACKY_TEMP_VENV_DIR/bin/activate

echo '==> Installing Packy Agent package Python dependencies...'
pip install -r $PACKY_TEMP_VENV_DIR/lib/python3.7/site-packages/packy_agent/requirements.txt

echo '==> Running Ansible playbook...'
export PACKY_VENV=packy-agent
cd $PACKY_TEMP_VENV_DIR/lib/python3.7/site-packages
ANSIBLE_NOCOWS=1 ansible-playbook -e ansible_python_interpreter=`which python` -i localhost, -c local --become-user=root -v packy_agent/scripts/install.yaml; ANSIBLE_RC=$?

# Because we do not want to work in temporary virtualenv any more, permanent virtualenv is ready
deactivate || :
set +x

if [ "$ANSIBLE_RC" == "0" ]; then
    echo '==> Activating permanent virtualenv...'
    source $VENVS_DIR/$PACKY_VENV/bin/activate
    packy-agent-welcome

    set +e
    deactivate
else
    echo 'An error during installation/upgrade'
fi
