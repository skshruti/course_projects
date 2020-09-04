#include"event.h"
#include<stdlib.h>
#include<stdio.h>
#define ID_MAX 150

void delete(eventQueue *eQ);

bool custExistEQ(eventQueue *eQ){
	node* temp=(*eQ).head;
	while(temp != pNull){
		if(strcmp(temp->data.type,"cust")==0) return true;
		temp=temp->next;
	}
	return false; 
}

void add(event e,eventQueue *eQ){
	float compareWith=0;
		if(strcmp(e.type,"cust")==0) compareWith=e.cEve.time;
		else compareWith=e.tEve.time;
	node* newnode=createNode(e);
	if((*eQ).size==0){
		(*eQ).head=newnode;
		(*eQ).size++;
		return;
	}
	else{
		node* temp=(*eQ).head;
		float compTemp=0;
		if(strcmp(temp->data.type,"cust")==0) compTemp=temp->data.cEve.time;
		else compTemp=temp->data.tEve.time;
		if(compTemp>compareWith){
		    (*eQ).head=newnode;
			temp->prev=newnode;
			newnode->next=temp;
			(*eQ).size++;
			return;
		}
		while(temp != pNull){
			if(compTemp>compareWith){
				temp->prev->next=newnode;
				newnode->prev=temp->prev;
				temp->prev=newnode;
				newnode->next=temp;
				(*eQ).size++;
				return;
			}
			if(temp->next==pNull){
				temp->next=newnode;
				newnode->prev=temp;
				(*eQ).size++;
				return;
			}
			temp=temp->next;
			if(strcmp(temp->data.type,"cust")==0) compTemp=temp->data.cEve.time;
			else compTemp=temp->data.tEve.time;
		}
	}
}

void actionMulti(event e, eventQueue *eQ, tellerQueueList *tQL, float time){
	if(strcmp(e.type,"cust")==0){
		 if(e.cEve.serviced==true){
		 	(*eQ).custServed++;
		 	delete(eQ);
		 }
		 else {
			(*eQ).curTime=e.cEve.time;
		 	tellerQueue* temp=shortestTQ(tQL);
			addtQ(e.cEve,temp);
			delete(eQ);
		}
	}
	else{
	 	(*eQ).curTime=e.tEve.time;
	 	if(e.tEve.tQ->size>0){
	 		cust newCust=createCust(e.tEve.tQ->head->data.time);
	 		float serviceTime = 2*time*rand()/(float)(RAND_MAX);
	 		float waitTime=(*eQ).curTime-e.tEve.tQ->head->data.time;
	 		if(waitTime>(*eQ).maxWaitTime) (*eQ).maxWaitTime=waitTime;
	 		addList((*eQ).curTime+serviceTime-e.tEve.tQ->head->data.time,(*eQ).dataList);
	 		(*eQ).timeSpent+=(*eQ).curTime+serviceTime-e.tEve.tQ->head->data.time;
	 		(*eQ).totServiceTime+=serviceTime;
	 		newCust.time=(*eQ).curTime+serviceTime;
	 		newCust.serviced=true;
	 		cust cnull=createCust(0);
			teller tnull=createTeller(0);
	 		event newEvent=createEvent("cust",newCust,tnull);
	 		deletetQ(e.tEve.tQ);
	 		e.tEve.time=(*eQ).curTime+serviceTime;
	 		delete(eQ);
	 		add(newEvent,eQ);
	 		add(e,eQ);
	 	}
	 	else{
	 		if((*custExist(tQL)).size>0){
	 			tellerQueue* randomTeller=select_random(custExist(tQL));
	 			cust newCust=createCust(randomTeller->head->data.time);
		 		float serviceTime = 2*time*rand()/(float)(RAND_MAX);
		 		float waitTime=(*eQ).curTime-randomTeller->head->data.time;
		 		if(waitTime>(*eQ).maxWaitTime) (*eQ).maxWaitTime=waitTime;
		 		addList((*eQ).curTime+serviceTime-randomTeller->head->data.time,(*eQ).dataList);
		 		(*eQ).timeSpent+=(*eQ).curTime+serviceTime-randomTeller->head->data.time;
		 		(*eQ).totServiceTime+=serviceTime;
		 		newCust.time=(*eQ).curTime+serviceTime;
		 		newCust.serviced=true;
		 		cust cnull=createCust(0);
				teller tnull=createTeller(0);
		 		event newEvent=createEvent("cust",newCust,tnull);
		 		deletetQ(randomTeller);
		 		e.tEve.time=(*eQ).curTime+serviceTime;
		 		delete(eQ);
		 		add(newEvent,eQ);
		 		add(e,eQ);
	 		}
	 		else if(custExistEQ(eQ)==true){
	 			float random=rand()%150;
		 		float idTime = random/60;
		 		e.tEve.time+=idTime;
		 		(*eQ).totIdleTime+=idTime;
		 		add(e,eQ);
		 		delete(eQ);
	 		}
	 		else {
	 			delete(eQ);
	 		}
	 	}
	}
}

void actionSingle(event e,eventQueue *eQ,tellerQueue *tQ,float time){
	if(strcmp(e.type,"cust")==0){
		 if(e.cEve.serviced==true){
		 	(*eQ).custServed++;
		 	delete(eQ);
		 }
		 else {
			(*eQ).curTime=e.cEve.time;
			addtQ(e.cEve,tQ);
			delete(eQ);
		}
	}
	else{
	 	(*eQ).curTime=e.tEve.time;
	 	if((*tQ).size>0){
	 		if((*tQ).head->data.time>(*eQ).curTime){
	 			float random=rand()%150;
		 		float idTime = random/60;
		 		e.tEve.time+=idTime;
		 		(*eQ).totIdleTime+=idTime;
		 		add(e,eQ);
	 		}
	 		else{
		 		cust newCust=createCust((*tQ).head->data.time);
		 		float serviceTime = 2*time*rand()/(float)(RAND_MAX);
		 		float waitTime=(*eQ).curTime-(*tQ).head->data.time;
		 		if(waitTime>(*eQ).maxWaitTime) (*eQ).maxWaitTime=waitTime;
		 		addList((*eQ).curTime+serviceTime-(*tQ).head->data.time,(*eQ).dataList);
		 		(*eQ).timeSpent+=(*eQ).curTime+serviceTime-(*tQ).head->data.time;
		 		(*eQ).totServiceTime+=serviceTime;
		 		newCust.time=(*eQ).curTime+serviceTime;
		 		newCust.serviced=true;
		 		cust cnull=createCust(0);
				teller tnull=createTeller(0);
		 		event newEvent=createEvent("cust",newCust,tnull);
		 		deletetQ(tQ);
		 		e.tEve.time=(*eQ).curTime+serviceTime;
		 		delete(eQ);
		 		add(newEvent,eQ);
		 		add(e,eQ);
		 	}
	 	}
	 	else{
	 		delete(eQ);
	 	}
	}
}

void delete(eventQueue *eQ){
	if((*eQ).size>1){
		(*eQ).head=(*eQ).head->next;
		(*eQ).head->prev=pNull;
	}
	else{
		(*eQ).head=pNull;
	}
	(*eQ).size--;
}
