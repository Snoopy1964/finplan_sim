#!/bin/bash

pwd

cd docs
sphinx-apidoc -o source ../models
sphinx-apidoc -o source ../utils
make html
if [ $? -eq 0 ]; then
    echo "Documentation built successfully."
else
    echo "Error building documentation."
    exit 1
fi
