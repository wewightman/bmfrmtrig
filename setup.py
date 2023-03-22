from setuptools import Extension, setup

trig = Extension(
    name="bmfrmtrig.trig._trig",
    include_dirs=["bmfrmtrig/trig"],
    sources=["bmfrmtrig/trig/trigengines.c"]
)

setup(
    name='bmfrmtrig',
    description="C-Backed beamforming engines",
    author_email="wew12@duke.edu",
    packages=['bmfrmtrig', 'bmfrmtrig.trig'],
    ext_modules=[trig]
)