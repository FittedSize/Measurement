#! /bin/bash
#
pip install flake8

cat > setup.cfg << eof
[flake8]
extend-ignore = E203
max-line-length = 88
exclude =
	.git,
	__pycache__,
	docs/source/conf.py,old,build,dist,
	manage.py,
	migrations,
	venv,
	local_settings.py,
	settings.py

max-complexity = 10
eof

flake8
