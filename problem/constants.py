# FILES AND DIRECTORIES
CODES_DIR = 'session/'
# temporary dir within the container
TMP_DIR = '/'
# name of file

# Extentions
PY = 'py'
C = 'c'
CPP = 'cpp'

# CONTAINER NAMES
CONTAINER_NAME = {
    PY: 'pycon',
    C: 'ccon',
    CPP: 'cppcon'
}

DOCKER_IMAGE = {
    PY: 'python:3',
    C: 'gcc:4.9',
    CPP: 'gcc:4.9'
}

# SEPARATORS
INPUT_SEP = 'INPUT'