#ifndef queue_h
#define queue_h

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node{
	void *data;
	struct Node *next;
	struct Node *prev;
}Node;

typedef struct Queue
{
	Node *head;
	int size;
}Queue;



Queue* createQueue();

void push(Queue *q, Node* newNode);

Node* pop(Queue *q);

#endif