#include<ctype.h>
#include<dirent.h>
#include<math.h>
#include<stdlib.h>
#include<stdio.h>
#include<string.h> 

#define INT_MAX 10000
#define WORD_MAX 100

typedef struct array{
	char** values;
	int size;
}array; 

typedef struct pair{
	char* word;
	float value;
}pair;

typedef struct vecs{
	pair* values;
	int size;
}vecs;

vecs* initialiseVecs(){
	vecs* vec=malloc(100 * sizeof(vecs));;
	vec->size=0;
	vec->values=malloc(INT_MAX * sizeof(pair));
	for(int i=0;i<INT_MAX;i++){
		vec->values[i].word=malloc(INT_MAX*sizeof(char));
		vec->values[i].value=0;
	}
	return vec;
}
char* toLower(char* str){
   for(int i=0;i<strlen(str);i++){
      str[i]=tolower(str[i]);
   }
   return str;
}

int compVecs(const void *p, const void *q)  
{ 
    char* l = ((struct pair *)p)->word; 
    char* r = ((struct pair *)q)->word;  
    int val=strcmp(l,r); 
    return (val); 
} 

int exists2(vecs v, char* str){
	pair *val;
	val=(pair*) bsearch(&str, v.values, v.size, sizeof(v.values[0]), compVecs);
	if(val!=NULL) return (val-v.values);
	return -1;
}


int comparator2(const void *p, const void *q)  
{ 
    char* l = *((char **)p); 
    char* r = *((char **)q); 
    int val=strcmp(l,r); 
    return (val); 
} 

#define seperate " ()-.;:,?/!\r\n"
array getInp(char *input){
	char **values=malloc(INT_MAX * sizeof(char *));
	char *parsed=strtok(input, seperate);
	int position=0;
	while(parsed!=NULL){
		char *parsedLower=toLower(parsed);
		values[position]=parsedLower;
		position++;
		parsed=strtok(NULL, seperate);

	}
	values[position]=NULL;
	array result;
	result.values=malloc(INT_MAX* sizeof(char*));
	result.values=values;
	result.size=position;
	return result;
}

void calcTf(array doc, vecs* result){
	for(int i=0; i<doc.size; i++){
		int occursAt=exists2((*result),doc.values[i]);
		if(occursAt>=0) result->values[occursAt].value++;
		else{
			pair newPair;
			newPair.word=malloc(INT_MAX*sizeof(char));
			strcpy(newPair.word,(doc.values[i]));
			newPair.value=1;
			result->values[result->size]=newPair;
			result->size++;
		} 
	}
	for(int i=0;i<doc.size;i++) result->values[i].value/=doc.size;
}

int calcInDocs(char* word, vecs* v, int size){
	int result=0;
	for(int i=0; i<size; i++){
		int exist=exists2(v[i], word);
		if(exist>=0) result++;
	}
	return result;
}

double simPercent(vecs v1, vecs v2){
	double numerator=0;
	for(int i=0; i<v1.size; i++){
		int exist=exists2(v2, v1.values[i].word);
		if(exist<0) numerator+=0;
		else numerator+=(v1.values[i].value)*(v2.values[exist].value);
	}
	double modV1=0;
	for(int i=0;i<v1.size;i++) {modV1+=(pow(v1.values[i].value,2));}
		modV1=sqrt(modV1);
	double modV2=0;
	for(int i=0;i<v2.size;i++) {modV2+=(pow(v2.values[i].value,2));}
		modV2=sqrt(modV2);
	double denominator=modV1*modV2;
	if(numerator==0) return 0;
	double result=(numerator/denominator)*100;
	return result;
}

//	./a.out testDoc doc (compare testDoc against doc[i])
int main(int argc, char **argv){
	char **input;	
 	FILE *i1;
 	FILE *i2;
 	/*TEST DOCUMENT*/
 	i1=fopen(argv[1], "r");;
	if(i1 == NULL) {
      printf("Error opening file");
      return(-1);
    }
    char testDoc[INT_MAX];
    char* testDocAll=malloc(INT_MAX*sizeof(char));
    while(fgets(testDoc,INT_MAX,i1)!=NULL)
		strcat(testDocAll,testDoc);

	array wordsDoc;
	wordsDoc=getInp(testDocAll);
	qsort((void*)wordsDoc.values,wordsDoc.size, sizeof(wordsDoc.values[0]), comparator2); 
  
	//total no of documents
	int noOfDocs=0;
	//array of file names
	char **files=malloc(INT_MAX*sizeof(char*));	

    DIR *dr = opendir(argv[2]); 
  	struct dirent *de;
    if (dr == NULL)  // opendir returns NULL if couldn't open directory 
    { 
        printf("Could not open current directory" ); 
        return 0; 
    } 
	vecs* tfVectors=malloc(100*sizeof(vecs));
	for(int i=0;i<30;i++) tfVectors[i]=(*initialiseVecs());
    char* dirName=argv[2];
    while ((de = readdir(dr)) != NULL) {
    	if(strcmp(de->d_name,".")!=0 && strcmp(de->d_name,"..")!=0){
	        char* name=malloc(64*sizeof(char));
	    	char fileName[255];
			strcpy( fileName, dirName );
			strcat( fileName, "/");
			strcat( fileName, de->d_name);
			files[noOfDocs]=malloc(INT_MAX*sizeof(char));
	        strcpy(files[noOfDocs],de->d_name);

	        i2=fopen(fileName, "r");;
			if(i2 == NULL) {
		      printf("Error opening file--");
		      return(-1);
		    }

		    char doc[INT_MAX];
    		char* docAll=malloc(5*INT_MAX*sizeof(char));
    		strcpy(docAll,"");
			while(fgets(doc,INT_MAX,i2)!=NULL)
				strcat(docAll,doc);
			array words;
			words=getInp(docAll);
			qsort((void*)words.values,words.size, sizeof(words.values[0]), comparator2); 
			vecs* tfVectorTemp=initialiseVecs();
			calcTf(words, tfVectorTemp);

			for(int i=0;i<tfVectorTemp->size;i++) {
				strcpy(tfVectors[noOfDocs].values[i].word,tfVectorTemp->values[i].word);
				tfVectors[noOfDocs].values[i].value=tfVectorTemp->values[i].value;
			}
			tfVectors[noOfDocs].size=tfVectorTemp->size;
			noOfDocs++;
			free(docAll);
			fclose(i2);
	    }
    }
    closedir(dr);
	vecs* tfVector=initialiseVecs();

	calcTf(wordsDoc, tfVector);

	vecs* tfIdfVector=initialiseVecs();
	for(int i=0; i<tfVector->size; i++){
		strcpy(tfIdfVector->values[i].word,tfVector->values[i].word);
		int inDocs=calcInDocs(tfVector->values[i].word, tfVectors, noOfDocs);
		if(inDocs>0){
			tfIdfVector->values[i].value=((tfVector->values[i].value))*((log(noOfDocs/(double)inDocs)));
		}
		else tfIdfVector->values[i].value=0; 
		tfIdfVector->size++;
	}

	for(int j=0; j<noOfDocs; j++){
		vecs* tfIdfVectorTemp=initialiseVecs();
		for(int i=0; i<tfVectors[j].size; i++){
			strcpy(tfIdfVectorTemp->values[i].word,tfVectors[j].values[i].word);
			int inDocs=calcInDocs(tfVectors[j].values[i].word, tfVectors, noOfDocs);
			if(inDocs>0){
				tfIdfVectorTemp->values[i].value=((tfVectors[j].values[i].value))*((log(noOfDocs/(double)inDocs)));
			}
			else tfIdfVectorTemp->values[i].value=0; 
			tfIdfVectorTemp->size++;
		}
		tfVectors[j]=(*tfIdfVectorTemp);
	}

	for(int i=0; i<noOfDocs; i++){
			float simPercentage=simPercent(*tfIdfVector,tfVectors[i]);
			printf("%s %f\n", files[i], simPercentage);
	}

	return 0;
}	