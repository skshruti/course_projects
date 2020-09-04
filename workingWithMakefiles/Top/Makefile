run: exe/final
	./exe/final

exe/final: obj/evenodd.o obj/cube.o obj/add.o obj/max.o obj/final.o
	gcc obj/evenodd.o obj/cube.o obj/add.o obj/max.o obj/final.o -o exe/final


directories:
	mkdir -p exe
	mkdir -p obj

obj/final.o: final.c
	gcc -c final.c -o ./obj/final.o

obj/evenodd.o: 1/evenodd.c
	(cd 1; make)

obj/cube.o: 2/cube.c
	(cd 2; make)

obj/add.o: 3/add.c
	(cd 3; make)

obj/max.o: 4/max.c
	(cd 4; make)

clean:
	(cd obj; rm *)
	(cd exe; rm *)

