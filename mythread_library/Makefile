all:	 
	gcc -Wall -fpic -o obj/queue.o -c src/queue.c 
	gcc -Wall -fpic -o obj/myOwnThread.o -c src/userthread.c
	gcc -o obj/libmyOwnThread.so obj/queue.o obj/myOwnThread.o -shared

test1:
	gcc -Wall -fpic -o obj/queue.o -c src/queue.c 
	gcc -Wall -fpic -o obj/myOwnThread.o -c src/userthread.c
	gcc -o obj/libmyOwnThread.so obj/queue.o obj/myOwnThread.o -shared
	gcc -Wall -fpic ./src/test1.c ./src/userthread.c ./src/queue.c -o ./bin/test
	(cd bin; ./test)

test2:	 
	gcc -Wall -fpic -o obj/queue.o -c src/queue.c 
	gcc -Wall -fpic -o obj/myOwnThread.o -c src/userthread.c
	gcc -o obj/libmyOwnThread.so obj/queue.o obj/myOwnThread.o -shared
	gcc -Wall -fpic ./src/test2.c ./src/userthread.c ./src/queue.c -o ./bin/test
	(cd bin; ./test $(N))

clean:
	(cd obj; rm *)
	(cd bin; rm *)