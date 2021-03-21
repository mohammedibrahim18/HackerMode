#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

int main(int argc, char *argv[]){
  int sfd=socket(AF_INET, SOCK_STREAM, 0);
  if (argc < 4){
     printf("Error, Usage: %s <ip> <port> <output_file>\n",argv[0]);
     exit(1);
  }
  int ofd=open(argv[3],O_CREAT|O_WRONLY|O_APPEND,S_IREAD|S_IWRITE);
  if (ofd==-1){printf("Error Opening Output File\n");exit(1);}
  struct sockaddr_in server;
  struct sockaddr_in client;
  server.sin_port=htons(atoi(argv[2]));
  server.sin_family=AF_INET;
  inet_pton(AF_INET, argv[1], &server.sin_addr.s_addr);
  int bd=bind(sfd,(struct sockaddr*)&server, sizeof(server));
  int lstr=listen(sfd, 1);
  socklen_t clntlen=sizeof(client);
  int newfd=accept(sfd, (struct sockaddr*)&client, &clntlen);
  char recvbfr[5000];
  while (recv(newfd,recvbfr,sizeof(recvbfr),0)){
  printf("%s",recvbfr);
  strcat(recvbfr,"\0");
  write(ofd, recvbfr, strlen(recvbfr));
  bzero(&recvbfr, sizeof(recvbfr));
  }
  close(newfd);
  close(sfd);
  close(ofd);
}





