#!/bin/sh
find . -iname '*.pyc' | xargs -r rm
find . -iname '*~' | xargs -r rm
