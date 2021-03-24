#include "lib.h"

using namespace std;
int main(int argc, char *argv[]){
  if (argc==1){
    cout << "Need Some Argument, Type with -h or help bfx\n";
}
  int arg;
  while ((arg = getopt(argc, argv, "x:e:c:h"))!=-1 ){
  switch (arg){
   case 'x':
     GetHexOrder(argv[2]);
     break;
   case 'e':
     printf ("Calling Code...\n");
     esc(argv[2]);
     break;
   case 'c':
     printf ("Calling Module...\n");
     sleep(1);
     printf("%sTesting%s Program...\n", KGRN,KNRM);
     int bak, ne;

     fflush(stdout);
     bak = dup(1);
     ne = open("/dev/null", O_WRONLY);
     dup2(ne, 1);
     close(ne);

     int r; r=check(argv[2]);

     fflush(stdout);
     dup2(bak, 1);
     close(bak);
     dup2(1,1);
     if (r!=0){
        printf ("%sBuffer OverFlow%s Crash Detected, Occured After %d Bytes, %sSIGSEGV%s Received\n", KRED, KNRM, r,KGRN, KNRM);
     }
     else{
        printf("%sTested%s, %sBuffer Overflow%s Not Detected, Normal Exit Signal Recevied\n",KGRN,KNRM,KRED,KNRM);
     }
     break;
   case 'h':
     help();
   default:
     usage(argv[0]);
  }


  }

}
