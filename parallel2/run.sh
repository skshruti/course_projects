#!/bin/bash
if [[ $4 -eq 4 ]]
then
	mpiexec -n $3 ./mpi $1 $2
else
	./exec $1 $2 $3 $4
fi
