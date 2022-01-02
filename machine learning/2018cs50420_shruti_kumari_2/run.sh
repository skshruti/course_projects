#!/bin/bash

if [[ $1 -eq 1 ]]
then
    python q1.py $2 $3 $4 
else
    python q2.py $2 $3 $4 $5
fi