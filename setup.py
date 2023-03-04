from setuptools import Extension, setup

setup(
    name="trigengines",
    ext_modules=[
        Extension(
            name="_trigengines",  # as it would be imported

            sources=["trigengines.c", "trigengines.i"], # all sources are compiled into a single binary file
        ),
    ]
)
