all: 
	(gcc -pthread -c ./src/static.c -o ./obj/static.o -lm)
	(gcc -pthread -c ./src/dynamic.c -o ./obj/dynamic.o -lm)
	(gcc -pthread obj/static.o -o bin/static -lm)
	(gcc -pthread obj/dynamic.o -o bin/dynamic -lm)
	(./bin/static $(N) $(t))
	(./bin/dynamic $(N) $(t))
	(gcc -c ./src/plot.c -o ./obj/plot.o)
	(gcc obj/plot.o -o bin/plot)
	(cd bin; sudo ./plot)

clean:
	(cd obj; rm *)
	(cd bin; rm *)

