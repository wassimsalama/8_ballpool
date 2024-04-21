CC=gcc
SWIG=swig
CFLAGS=-std=c99 -Wall -pedantic -fpic
LDFLAGS=-shared
PYTHON_INCLUDE=$(shell python3-config --includes)
PYTHON_LIB=$(shell python3-config --ldflags)

# Source and target files
SRC_C=phylib.c
SRC_I=phylib.i
OBJ_C=phylib.o
OBJ_WRAP=phylib_wrap.o
TARGET_LIB=libphylib.so
TARGET_SWIG=_phylib.so

# First target: all
all: $(TARGET_LIB) $(TARGET_SWIG)

# Compile phylib.c to phylib.o
$(OBJ_C): $(SRC_C)
	$(CC) $(CFLAGS) -c $< -o $@

# Create libphylib.so from phylib.o
$(TARGET_LIB): $(OBJ_C)
	$(CC) $(LDFLAGS) -o $@ $^

# Use SWIG to generate phylib_wrap.c and phylib.py
phylib_wrap.c:
	$(SWIG) -python $(SRC_I)

# Compile phylib_wrap.c to phylib_wrap.o
$(OBJ_WRAP): phylib_wrap.c
	$(CC) $(CFLAGS) $(PYTHON_INCLUDE) -c $< -o $@

# Create _phylib.so from phylib_wrap.o and phylib.o
$(TARGET_SWIG): $(OBJ_WRAP) $(OBJ_C)
	$(CC) $(LDFLAGS) $(PYTHON_LIB) -o $@ $^

# Clean target
clean:
	rm -f *.o *.so phylib.py phylib_wrap.c

.PHONY: all clean

