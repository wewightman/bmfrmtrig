# `bmfrmtrig`
C-based trigonometric engines used in delay and sum beamforming

## Compilation and Instalation
In order to use these functions directly in python, one must clone the source code, compile it, and install it into their virtual python environment.

*Linux*

```
git clone https://github.com/wewightman/bmfrmtrig.git
cd bmfrmtrig
source compileengines.sh
pip install .
```

## Testing
To directly test the C functions, run the following command

```
source runtests.sh
```

## Cleaning up a messy repo
To clean the messy repo, simply run `source cleanup.sh' on linux and './cleanup.sh' on windows.

