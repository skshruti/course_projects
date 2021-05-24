#include "../include/myOwnthread.h"

void *test1(){
	int i=0;
	while(1){
		printf("Thread number %d is running for %dth time\n",curThread->name,i);
		i++;
		if(i==1000){
			printf("EXITING\n");
			myThread_exit();
		}
		// if(i%200==0){
		// 	printf("uh oh\n");
		// 	i++;
		// 	myThread_yield();
		// }
	}
}
int main(int argc, char** argv)
{
	//printQueue(readyQueue);
	int n=atoi(argv[1]);
	mythread_t *threads=malloc(n*sizeof(mythread_t));
	for (int i = 0; i < n; i++)
	{
		threads[i]=malloc(sizeof(TCB));
	}
	for (int i = 0; i < n; i++)
	{
		myThread_create(threads[i],NULL,(void*)test1,(void*)NULL);
	}
	//printQueue(readyQueue);
	for (int i = 0; i < n; i++)
	{
		myThread_join(threads[i]->name);
	}
	//printf("%d\n", (*exited).size);
	printf("DONE!");
	return 0;
}
