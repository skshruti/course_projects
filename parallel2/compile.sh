#!/bin/bash
gcc -fopenmp main.c -o exec
mpicc -fopenmp mpi.c -o mpi