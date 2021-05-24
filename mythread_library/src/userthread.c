#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <setjmp.h>     
#include <unistd.h>   
#include <signal.h>
#include <sys/time.h>
#include "../include/myOwnthread.h"

#define EXITED 2
#define RUNNING 1
#define NOT_STARTED 0

int newName=0;

int firstRun=1;

int createMain=1;
void timer(){
	sa.sa_handler=myThread_yield;
	sa.sa_flags=SA_NODEFER;
	if (sigaction(SIGALRM,&sa,NULL) < 0) { 
        printf("Unable to catch SIGALRM\n");
        exit(1);
    }
	timer_val.it_value.tv_sec=0;
	timer_val.it_value.tv_usec=50000;
	timer_val.it_interval=timer_val.it_value;
	if (setitimer(ITIMER_REAL, &timer_val, NULL) == -1) { 
	    printf("error calling setitimer()\n");
        exit(1);
    }
    // while ( 1 ) {
    //     pause();
    //     printf("haan?");
    // }
}

int myThread_create(mythread_t thread, mythread_attr_t *attr, void (*start_routine)(void *), void *arg){
	thread->name=newName++;
	thread->entry=start_routine;
	thread->argument=arg;
	thread->status=NOT_STARTED;
	thread->flag=0;
	thread->size = 100000;
    thread->stackBottom = malloc(thread->size);
    thread->stackTop = thread->stackBottom + thread->size;

    Node* newNode=(Node*)malloc(sizeof(Node));
	newNode->data=(void*)thread;
	newNode->next=NULL;
	newNode->prev=NULL;
	push(readyQueue,newNode);
	printf("creating thread: %d\n", thread->name);	

	if(createMain==1){
		createMain=0;
		mainThread=malloc(sizeof(TCB));
		mainThread->name=-1;
		mainThread->entry=NULL;
		mainThread->argument=NULL;
		mainThread->status=NOT_STARTED;
		mainThread->flag=1;
		mainThread->size = 100000;
	    mainThread->stackBottom = malloc(mainThread->size);
	    mainThread->stackTop = mainThread->stackBottom + mainThread->size;
		setjmp(mainThread->context);
		curThread=mainThread;
		timer();
	}


	return thread->name;
}


void myThread_yield(){
	printf("enter yield\n");
	Node* newNode=(Node*)malloc(sizeof(Node));
	newNode->data=(void*)curThread;
	newNode->next=NULL;
	newNode->prev=NULL;
	push(readyQueue,newNode);
	if(setjmp(curThread->context)==0){
		if(firstRun==1){
			myThreadswitch();
		}
		else {
			longjmp(schedulerContext,1);
		}
	}
	else{
		printf(".");
	}
}

int myThread_self(void){
	return curThread->name;
}

void myThread_exit(){
	curThread->status=EXITED;
	longjmp(schedulerContext,1);
}

void *useThread(){
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

void myThreadswitch(){
	sigprocmask(SIG_BLOCK, &block_mask, NULL);
		setjmp(schedulerContext);	
		Node* temp=pop(readyQueue);
		curThread=(mythread_t)(temp->data);
		sigprocmask(SIG_UNBLOCK, &block_mask, NULL);
		if(curThread->flag==1){
			longjmp(curThread->context,1);
		}
		else{
			register void *top = curThread->stackTop;
		       asm volatile(
		           "mov %[rs], %%rsp \n"
		           : [ rs ] "+r" (top) ::
	       );
			curThread->flag=1;
			curThread->status=RUNNING;
			functionToCall=curThread->entry;
			functionToCall(curThread->argument);
		}
}

void myThread_join(int name){
	Node* temp=(*exited).head;
	int toJoin=1;
	while(temp != NULL){
		mythread_t tempThread=(mythread_t)(temp->data);
		if(tempThread->name==name) toJoin=0;
		temp=temp->next;
	}
	if(toJoin==1){
		mythread_t waitingFor;
		temp=(*readyQueue).head;
		while(temp != NULL){
			mythread_t tempThread=(mythread_t)(temp->data);
			if(tempThread->name==name) {
				waitingFor=tempThread;
				break;
			}
			temp=temp->next;
		}
		while(waitingFor->status != EXITED){
			myThread_yield();
		}
	}
}

// int main(int argc, char** argv)
// {
// 	//printQueue(readyQueue);
// 	mythread_t *threads=malloc(5*sizeof(mythread_t));
// 	for (int i = 0; i < 5; i++)
// 	{
// 		threads[i]=malloc(sizeof(TCB));
// 	}
// 	for (int i = 0; i < 5; i++)
// 	{
// 		myThread_create(threads[i],NULL,(void*)useThread,(void*)NULL);
// 	}
// 	printQueue(readyQueue);
// 	for (int i = 0; i < 5; i++)
// 	{
// 		myThread_join(threads[i]->name);
// 	}
// 	printf("%d\n", (*exited).size);
// 	printf("HELLO, LOVE!");
// 	return 0;
// }

// gcc -Wall -fpic -o obj/queue.o -c src/queue.c 
// 	gcc -Wall -fpic -o obj/myOwnThread.o -c src/userthread.c
// 	gcc -o lib/libmyOwnThread.so obj/queue.o obj/myOwnThread.o -shared