#include<stdlib.h>
#include<string.h>
#include<stdbool.h>
#include<stdio.h>
#include<math.h>

typedef struct nodeFlt{
	float data;
	struct nodeFlt* next;
	struct nodeFlt* prev;
}nodeFlt; 

typedef struct list{
	nodeFlt* head;
	int size;
}list;

typedef struct customers
{
	float time;
	bool serviced;
}cust;

typedef struct nodeC{
	cust data;
	struct nodeC* next;
	struct nodeC* prev;
}nodeC;  

typedef struct tellerQueue{
	nodeC* head;
	int size;
}tellerQueue;

typedef struct teller
{
	float time;
	bool serviced;
	tellerQueue* tQ;
}teller;

typedef struct events
{	
	char* type;
	cust cEve;
	teller tEve;
}event;

typedef struct node{
	event data;
	struct node* next;
	struct node* prev;
}node; 

typedef struct eventQueue{
	node* head;
	int size;
	int custServed;
	float curTime;
	float timeSpent;
	float maxWaitTime;
	float totServiceTime;
	float totIdleTime;
	list* dataList;
}eventQueue;

typedef struct nodeTQ{
	tellerQueue* data;
	struct nodeTQ* next;
	struct nodeTQ* prev;
}nodeTQ; 

typedef struct tellerQueueList{
	nodeTQ* head;
	int size;
}tellerQueueList;



event createEvent(char* type, cust cEve, teller tEve);
cust createCust(float time);
teller createTeller(float time);
node* createNode(event e);

cust createCust(float time){
	cust nc;
	nc.time=time;
	nc.serviced=false;
	return nc;
}

event createEvent(char* type, cust cEve, teller tEve){
	event nEve;
	nEve.type=type;
	nEve.tEve=tEve;
	nEve.cEve=cEve;
	return nEve;
}

node* pNull=NULL;
node* createNode(event e){
	node* newnode=(node*)malloc(sizeof(node));
	newnode->data=e;
	newnode->next=pNull;
	newnode->prev=pNull;
	return newnode;
}

nodeC* pNullC=NULL;
nodeC* createNodeC(cust e){
	nodeC* newnode=(nodeC*)malloc(sizeof(nodeC));
	newnode->data=e;
	newnode->next=pNullC;
	newnode->prev=pNullC;
	return newnode;
}

nodeTQ* pNullTQ=NULL;
nodeTQ* createNodeTQ(tellerQueue* e){
	nodeTQ* newnode=(nodeTQ*)malloc(sizeof(nodeTQ));
	newnode->data=e;
	newnode->next=pNullTQ;
	newnode->prev=pNullTQ;
	return newnode;
}

nodeFlt* pNullFlt=NULL;
nodeFlt* createNodeFlt(float f){
	nodeFlt* newnode=(nodeFlt*)malloc(sizeof(nodeFlt));
	newnode->data=f;
	newnode->next=pNullFlt;
	newnode->prev=pNullFlt;
	return newnode;
}

list* createList(){
	list* l=(list*)malloc(sizeof(list));
	l->size=0;
	return l;
}

eventQueue* createQueue(){
	eventQueue* eQ=(eventQueue*)malloc(sizeof(eventQueue));
	eQ->size=0;
	eQ->custServed=0;
	eQ->curTime=0;
	eQ->timeSpent=0;
	eQ->maxWaitTime=0;
	eQ->totServiceTime=0;
	eQ->totIdleTime=0;
	eQ->dataList=createList();
	return eQ;
}

tellerQueue* createTellerQ(){
	tellerQueue* tQ=(tellerQueue*)malloc(sizeof(tellerQueue));
	tQ->size=0;
	return tQ;
}

tellerQueueList* createTQL(){
	tellerQueueList* tQL=(tellerQueueList*)malloc(sizeof(tellerQueueList));
	tQL->size=0;
	return tQL;
}

teller createTeller(float time){
	teller nt;
	nt.time=time;
	nt.serviced=false;	
	tellerQueue* tQueue=createTellerQ();
	nt.tQ=tQueue;
	return nt;
}


void addtQ(cust c,tellerQueue *eQ){
	nodeC* newnode=createNodeC(c);
	if((*eQ).size==0){
		(*eQ).head=newnode;
		(*eQ).size++;
		return;
	}
	else{
		nodeC* temp=(*eQ).head;
		while(temp != pNullC){
			if(temp->next==pNullC){
				temp->next=newnode;
				newnode->prev=temp;
				(*eQ).size++;
				return;
			}
			temp=temp->next;
		}
	}
}

void deletetQ(tellerQueue *eQ){
	if((*eQ).size>1){
		(*eQ).head=(*eQ).head->next;
		(*eQ).head->prev=pNullC;
	}
	else{
		(*eQ).head=pNullC;
	}
	(*eQ).size--;
}

void addtQL(tellerQueue* tQ,tellerQueueList *eQ){
	nodeTQ* newnode=createNodeTQ(tQ);
	if((*eQ).size==0){
		(*eQ).head=newnode;
		(*eQ).size++;
		return;
	}
	else{
		nodeTQ* temp=(*eQ).head;
		while(temp != pNullTQ){
			if(temp->next==pNullTQ){
				temp->next=newnode;
				newnode->prev=temp;
				(*eQ).size++;
				return;
			}
			temp=temp->next;
		}
	}
}

tellerQueue* shortestTQ(tellerQueueList *tQL){
	if((*tQL).size==1) return (*tQL).head->data;
	else{
		nodeTQ* temp=(*tQL).head;
		tellerQueue* res=(*tQL).head->data;
		while(temp!=pNullTQ){
			if((*res).size==(*(temp->data)).size){
				int random=rand()%2;
				if(random==1) res=temp->data;
			}
	 		if((*res).size>(*(temp->data)).size) res=temp->data;
	 		temp=temp->next;
	 	}
	 	return res;
	}
}

tellerQueueList* custExist(tellerQueueList *tQL){
	tellerQueueList* result=createTQL();
	nodeTQ* temp=(*tQL).head;
	while(temp!=pNullTQ){
		if((*(temp->data)).size>0) addtQL(temp->data,result);
		temp=temp->next;
	}
	return result; 
}

tellerQueue* select_random(tellerQueueList *tQL){
	int i=rand()%((*tQL).size);
//	printf("get_i: %d size: %d\n",i,(*tQL).size);
	int counter=0;
	nodeTQ* temp=(*tQL).head;
	while(counter<i){
		temp=temp->next;
		counter++;
	}
	return temp->data;
}

void addList(float f,list *eQ){
	nodeFlt* newnode=createNodeFlt(f);
	if((*eQ).size==0){
		(*eQ).head=newnode;
		(*eQ).size++;
		return;
	}
	else{
		nodeFlt* temp=(*eQ).head;
		while(temp != pNullFlt){
			if(temp->next==pNullFlt){
				temp->next=newnode;
				newnode->prev=temp;
				(*eQ).size++;
				return;
			}
			temp=temp->next;
		}
	}
}

void print_queue(eventQueue *eQ){
	printf("started\n");
	printf("qSize=%d\n", eQ->size);
	node* temp=(*eQ).head;
	if((*eQ).size==0) {
		printf("NULL\n");
	}
	else{
	 	while(temp!=pNull){
	 		if(strcmp(temp->data.type,"cust")==0) 
	 			printf("cust:%f\n",temp->data.cEve.time);
	 		else
	 			printf("teller:%f\n",temp->data.tEve.time);
	 		temp=temp->next;
	 	}
	}
	printf("printed\n");
}

float* calculateStd(list* list, float avg, float* result){
	nodeFlt* temp=(*list).head;
	if((*list).size==0) {
		return result;
	}
	else{
	 	while(temp!=pNullFlt){
	 		(*result) += pow(temp->data - avg, 2);
	 		temp=temp->next;
	 	}
	}
	(*result)/=((*list).size);
	return result;
}

void print_teller_queue(tellerQueue *eQ){
	printf("startedTellerQueue\n");
	printf("qSize=%d\n", eQ->size);
	nodeC* temp=(*eQ).head;
	if((*eQ).size==0) {
		printf("NULL\n");
	}
	else{
	 	while(temp!=pNullC){
	 		printf("cust:%f\n",temp->data.time);
	 		temp=temp->next;
	 	}
	}
	printf("printed\n");
}

void print_tqueueList(tellerQueueList *eQ){
	printf("startedTQueueList\n");
	printf("qSize=%d\n", eQ->size);
	nodeTQ* temp=(*eQ).head;
	if((*eQ).size==0) {
		printf("NULL\n");
	}
	else{
	 	while(temp!=pNullTQ){
	 		printf("size:%d\n",(*(temp->data)).size);
	 		temp=temp->next;
	 	}
	}
	printf("printed\n");
}

void print_dataList(list *eQ){
	printf("startedDataList\n");
	printf("qSize=%d\n", eQ->size);
	nodeFlt* temp=(*eQ).head;
	if((*eQ).size==0) {
		printf("NULL\n");
	}
	else{
	 	while(temp!=pNullFlt){
	 		printf("time taken:%f\n",(temp->data));
	 		temp=temp->next;
	 	}
	}
	printf("printed\n");
}