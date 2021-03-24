#include <stdio.h>
#include <iostream>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <sys/types.h>
#include <fcntl.h>
#include <string>
#include <limits.h>
#include "colors.h"

using namespace std;

typedef struct{
  string name;
  int    size;
}reg;


reg regs[]={
{.size=8},
{.size=4},
{.size=2},
{.size=1}};

const char *names[]={"rbx", "ebx", "bx", "bl"};
void usage(char *prgname){
     cout << "Usage: bfx <Option> <Argument> "<< endl;
}
void GetHexOrder(const char *data){
    int l=strlen(data);l--;
    int len=0;
    printf ("Starting Stack Order Hex Calculation.....\n Hex Value -> ");
    for (int i=0; i<= l;l--){
       printf ("%x",(int)data[l]);
       len++;
    }
    printf (" <-\nHex Digits: %d | Bytes: %d\n", len*2,len);
    printf ("====================================\n");
    for (int i=0; i<4; i++){
       printf (".\n");
       if (len==regs[i].size){
       printf ("- Recommented execve path Register: %s%s%s\n",KYEL, names[i],KNRM);
       }
    }
}
void help(){
   printf ("bfx, Buffer OverFLow Toolkit (Detection, Stack Order Hex Calculator, Executor)\n");
   printf ("Arguments:\n");
   printf ("  -h: This Message\n  -c: Test A Command Line Program To Automatically Detect Overflow\n  -x: Generate A Stack Hex Order String\n  -e  Execute a ShellCode\n");
}
void esc(char *fname){
     int fd=open(fname, O_RDONLY);
     if (fd==-1){
       printf ("Error Reading File %s\n");
       exit(1);
     }
     void (*fptr)(void);
     struct stat file;
     stat(fname, &file);
     void *data;
     data=malloc(file.st_size);
     read (fd,data,sizeof(data));
     int (*exeshell)();
     exeshell = (int (*)()) data;
     (int)(*exeshell)();
     close(fd);
}

int check(char *prgname){
  close(1);close(2);
  int ret=0;
  strcat (prgname, " A");
  for (int i=0; i<=1030; i++){
    ret=system(prgname);
    if (WEXITSTATUS(ret)==139){
       return i;
    }
    strcat (prgname, "A");
  }
  return 0;
}
