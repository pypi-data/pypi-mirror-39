#!/bin/bash

export PYTHON_VERSION=3.5

this_dir=$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)
cd ${this_dir}

export PATH=${this_dir}/bin:$PATH
export PYTHONPATH=${this_dir}:${this_dir}/bin:$(python$PYTHON_VERSION -c "import sys; print(':'.join(sys.path))")



./bin/visus.app/Contents/MacOS/visus
