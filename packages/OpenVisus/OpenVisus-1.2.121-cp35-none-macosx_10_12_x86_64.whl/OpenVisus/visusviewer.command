#!/bin/bash

export PYTHON_VERSION=3.5

this_dir=$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)
cd ${this_dir}

export PATH=${this_dir}/bin:$PATH
export PYTHONPATH=${this_dir}:${this_dir}/bin:$(python$PYTHON_VERSION -c "import sys; print(':'.join(sys.path))")

export QT_PLUGIN_PATH=${this_dir}/bin/plugins



./bin/visusviewer.app/Contents/MacOS/visusviewer
