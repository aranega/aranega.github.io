EXE=myprog
SOURCE=myprog.c
TEST_SRC=myprog_test.c
TEST_EXE=myprog_test


test:
	gcc -o $(TEST_EXE) $(TEST_SRC) -lcheck -L ~/usr/check/lib -I ~/usr/check/include
	LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/usr/check/lib/ ./$(TEST_EXE)
