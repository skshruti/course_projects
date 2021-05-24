#ifndef myOwnthread_h
#define myOwnthread_h

#include <setjmp.h>     
#include <signal.h>
#include <sys/time.h>
#include "queue.h"

typedef struct TCB{
	int name;
	int status;
	jmp_buf context;
	int flag;
	void *argument;
	void *stackBottom;
	void *stackTop;
	int size;
	void (*entry)(void *);
	//Queue joinlist;
}TCB;

typedef struct TCB * mythread_t;

typedef struct mythread_attr_t{
	int flags;
    size_t size;
    void *stackBottom;
	int status;
}mythread_attr_t;



void *useThread();
mythread_t curThread;
mythread_t mainThread;
jmp_buf schedulerContext;
Queue readyQueue[50];
Queue exited[50];
void (*functionToCall)(void *);
sigset_t old_mask, block_mask;
void myThreadswitch();
struct sigaction sa;
struct itimerval timer_val;
void myThread_yield();
void printQueue(Queue*);


void timer();

int myThread_create(mythread_t thread, mythread_attr_t *attr, void (*start_routine)(void *), void *arg);

//void printQueue(Queue *q);

void myThread_yield();

int myThread_self(void);

void myThread_exit();

void *useThread();

void myThreadswitch();

void myThread_join(int name);

#endif