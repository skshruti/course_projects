#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#include<sys/wait.h>
#include<sys/stat.h>
#include<sys/types.h>
#include<fcntl.h>

char **getInp(char *);
int cd(char *);
int mkdirec(char *);
int rmdirec(char *);
void getCWD();
int execute(char *, char *);
char **getInpPiped(char *);
char **getInpRedirecIn(char *);
char **getInpRedirecOut(char *);
void executePiped(char **, char **);


int main(){
	printf("Welcome to my shell!\n"); //starting of the shell
	char **input;
	char **redirecIn;
	char **redirecOut;
	char **inputPiped;
	char text[20];
	char textcpy[20];
	char textcpyy[20];
	char textcpyyy[20];
	pid_t pid;
	int stat;
	char **cmd;
	char **cmd2;
	while(1){
		printf("shell>>> ");
		fgets(text, 20, stdin);
		strcpy(textcpy, text);
		strcpy(textcpyy, text);
		strcpy(textcpyyy, text);
		input=getInp(text);	
		redirecIn=getInpRedirecIn(textcpy);
		redirecOut=getInpRedirecOut(textcpyy);
		inputPiped=getInpPiped(textcpyyy);
		//command redirected by <
		if(redirecIn!=NULL){
			cmd=getInp(redirecIn[0]);
			cmd2=getInp(redirecIn[1]);
			char *file=cmd2[0];
			int fd[2];
			pid = fork();
			if (pid == -1) {
			    perror("fork");
			} else if(pid==0){
				freopen(file, "r", stdin);
				execvp(cmd[0], cmd);
			    exit(0);
			} else{
				waitpid(pid, &stat, WUNTRACED);
				free(input);
			}
			continue;
		}
		//command redirected by >
		if(redirecOut!=NULL){
			cmd=getInp(redirecOut[0]);
			cmd2=getInp(redirecOut[1]);
			char *file=cmd2[0];	
			int fd[2];
			pid = fork();
			if (pid == -1) {
			    perror("fork");
			} else if(pid==0){
				freopen(file, "w+", stdout);	
				execvp(cmd[0], cmd);
				perror("execvp");
			    	exit(0);
			} else{
				waitpid(pid, &stat, WUNTRACED);
				free(input);
			}
			continue;
		}
		//piped commands
		if(inputPiped!=NULL){
				int fd[2];
				cmd=getInp(inputPiped[0]);
				cmd2=getInp(inputPiped[1]);
				pipe(fd);
				pid = fork();

				if(pid==0)
				{
					dup2(fd[1], STDOUT_FILENO);
					close(fd[0]);
					close(fd[1]);
//					execlp(cmd[0], cmd[0], cmd, (char*) NULL);
					char* path = realpath(cmd[0], NULL);
					if(path == NULL){
						printf("cannot find file with name %s\n", cmd[0]);
						perror("pipe");
					} else{
						system(path);			 
						free(path);
					}
					exit(1);
					fprintf(stderr, "Failed to execute '%s'\n", cmd[0]);
					exit(1);
				}
				else
				{ 
					pid=fork();

					if(pid==0)
					{
						dup2(fd[0], STDIN_FILENO);
						close(fd[1]);
						close(fd[0]);
//						execlp(cmd2[0], cmd2[0], cmd2,(char*) NULL);
						char* path = realpath(cmd2[0], NULL);
						if(path == NULL){
							printf("cannot find file with name %s\n", cmd2[0]);
//							perror("pipe");
						} else{
							system(path);			 
							free(path);
						}
						exit(1);
						fprintf(stderr, "Failed to execute '%s'\n", cmd2[0]);
						exit(1);
					}
					else
					{
						int status;
						close(fd[0]);
						close(fd[1]);
						waitpid(pid, &status, 0);
					}
				}
		}
		//builtin commands
		if(redirecIn==NULL && redirecOut==NULL && inputPiped==NULL){
			if(input[0]==NULL){
				continue;
			}
			if(strcmp(input[0], "exit")==0){
				exit(0);
			}	
			if(execute(input[0], input[1])==0)
				continue;
			pid=fork();
			if(pid==0){
				execvp(input[0], input);
				char* path = realpath(text, NULL);
				if(path == NULL){
				    printf("cannot find file with name %s\n", text);
				} else{
				    system(path);			 
	   			    free(path);
				}
				exit(1);
			}
			else{
				waitpid(pid, &stat, WUNTRACED);}
				free(input);
			}
		}

	return 0;
}
//execution of five builtin commands 
int execute(char *cmd, char *arg){	
		if(strcmp(cmd, "pwd")==0){
			getCWD();
			return 0;
		}
		if(strcmp(cmd, "cd")==0){
			if(cd(arg)<0){
				perror(arg);
				return 0;
			}
			return 0;
		}
		if(strcmp(cmd, "mkdir")==0){
			if(mkdirec(arg)<0){
				perror(arg);
				return 0;			
			}
			return 0;
		}
		if(strcmp(cmd, "rmdir")==0){
			if(rmdirec(arg)<0){
				perror(arg);
				return 0;
			}
			return 0;
		}
		else return 1;
}
//string seperated by space
#define seperate " \n"
char **getInp(char *input){
	char **array=malloc(64 * sizeof(char *));
	char *parsed=strtok(input, seperate);
	int position=0;
	while(parsed!=NULL){
		array[position]=parsed;
		position++;
		parsed=strtok(NULL, seperate);

	}
	array[position]=NULL;
	return array;
}
//string seperated by |
char **getInpPiped(char *input){
	char **array=malloc(64 * sizeof(char *));
	char *parsed=strtok(input, "|");
	int position=0;
	while(parsed!=NULL){
		array[position]=parsed;
		position++;
		parsed=strtok(NULL, "|");
	}
	array[position]=NULL;

	if(array[1]==NULL) return NULL;
	return array;
}
//string seperated by <
char **getInpRedirecIn(char *input){
	char **array=malloc(64 * sizeof(char *));
	char *parsed=strtok(input, "<\n");
	int position=0;
	while(parsed!=NULL){
		array[position]=parsed;
		position++;
		parsed=strtok(NULL, "<\n");
	}
	array[position]=NULL;

	if(array[1]==NULL) return NULL;
	return array;
}
//string seperated by >
char **getInpRedirecOut(char *input){
	char **array=malloc(64 * sizeof(char *));
	char *parsed=strtok(input, ">\n");
	int position=0;
	while(parsed!=NULL){
		array[position]=parsed;
		position++;
		parsed=strtok(NULL, ">\n");
	}
	array[position]=NULL;

	if(array[1]==NULL) return NULL;
	return array;
}
//function for cd
int cd(char *path){
	return chdir(path);
}
//function for mkdir
int mkdirec(char *path){
	return mkdir(path, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
}
//function for rmdir
int rmdirec(char *path){
	return rmdir(path);
}
//function for pwd
void getCWD(){
	char cwd[1024];
	getcwd(cwd, sizeof(cwd));
	printf("The present dir is: %s", cwd);
}


