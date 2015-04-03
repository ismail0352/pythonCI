#!/bin/bash

[ -s src/config/build.default.json ] || {
	echo "This script must be run from the root of the iris repository." >&2
	exit 1
}

git log -1 --pretty=format:%ct_%h
