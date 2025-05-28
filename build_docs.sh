#!/bin/bash
cd docs


pwd


make clean
# sphinx-apidoc --module-first -o source ../models/*.py 
# sphinx-apidoc --module-first -o source ../utils/*.py 

echo "Building HTML documentation..."
make html
if [ $? -eq 0 ]; then
    echo "Documentation built successfully."
else
    echo "Error building documentation."
    exit 1
fi
