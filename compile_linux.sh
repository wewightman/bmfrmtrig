# compile trig engines
gcc -c -Wall -Werror -fpic trigengines.c -o trig.o
gcc -shared -o _trig.so trig.o
rm *.o