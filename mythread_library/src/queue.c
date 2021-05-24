#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "../include/queue.h"

Queue* createQueue(){
	Queue* q=(Queue*)malloc(sizeof(Queue));
	q->size=0;
	return q;
}

void push(Queue *q, Node* newNode){
	if((*q).size==0){
		(*q).head=newNode;
		(*q).size++;
		return;
	}
	else{
		Node* temp=(*q).head;
		while(temp != NULL){
			if(temp->next==NULL){
				temp->next=newNode;
				newNode->prev=temp;
				(*q).size++;
				return;
			}
			temp=temp->next;
		}
	}
}


Node* pop(Queue *q){
	if((*q).size==0){
		printf("Sorry, queue is empty\n");
	}
	Node* temp=(*q).head;
	Node* newHead=temp->next;
	(*q).head=newHead;
	(*q).size--;
	return temp;
}