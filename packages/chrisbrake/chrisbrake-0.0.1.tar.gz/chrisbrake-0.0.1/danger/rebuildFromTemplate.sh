#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

cookiecutter -fo "${DIR}/../../" cookiecutter-python-package