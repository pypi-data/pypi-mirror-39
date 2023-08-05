.PHONY: test_dependencies tests build_dependencies build clean_build_dir

test_dependencies:
	python -m pip install -r test-requirements.in .

tests: test_dependencies
	python -m pytest --cov=actorio ./tests

build_dependencies:
	python -m pip install -U wheel setuptools_scm twine readme_renderer[md]

clean_build_dir:
	rm -r ./dist 2>/dev/null || true

build: build_dependencies
	python setup.py sdist bdist_wheel

publish: clean_build_dir build
	python -m twine upload dist/*

publish_on_test_pypi: clean_build_dir build
	python -m twine upload -u ${TWINE_TEST_USERNAME} -p ${TWINE_TEST_PASSWORD} --repository-url https://test.pypi.org/legacy/ dist/*

publish_on_pypi: clean_build_dir build
	python -m twine upload -u ${TWINE_PROD_USERNAME} -p ${TWINE_PROD_PASSWORD} --repository-url https://pypi.org/legacy/ dist/*