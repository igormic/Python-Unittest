build_distribution:
    python setup.py sdist bdist_wheel

upload_to_testpypi:
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload_to_pypi:
    twine upload dist/*

