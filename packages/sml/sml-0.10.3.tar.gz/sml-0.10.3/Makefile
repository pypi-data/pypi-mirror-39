.PHONY: release clean

release: lint
	# bdist_wheel requires 'wheel' package from PyPI
	python setup.py sdist bdist_wheel
	twine upload dist/*
	curl -X POST -H 'Content-type: application/json' \
	    --data "{\"text\":\"sml $$(python setup.py --version) released to PyPI by $$(git config --get user.name).\"}"\
	    https://hooks.slack.com/services/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

clean:
	$(RM) -r build dist sml.egg-info

lint:
	python -m compileall sml
	flake8 sml
	mypy sml || true
