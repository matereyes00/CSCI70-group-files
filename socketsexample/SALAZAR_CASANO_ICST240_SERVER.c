/* A simple server in the internet domain using TCP
   The port number is passed as an argument */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

//for formatting text output
#define RESET 0
#define BRIGHT	1
#define DIM	2
#define UNDERLINE	3
#define BLINK 4
#define REVERSE 7
#define HIDDEN 8

#define BLACK 0
#define RED	1
#define GREEN 2
#define YELLOW 3
#define BLUE 4
#define MAGENTA 5
#define CYAN 6
#define WHITE 7

void textcolor(int attr, int fg, int bg)
{	char command[13];

	/* Command is the control command to the terminal */
	sprintf(command, "%c[%d;%d;%dm", 0x1B, attr, fg + 30, bg + 40);
	printf("%s", command);
}


void error(const char *msg)
{
    perror(msg);
    exit(1);
}

void displayBoard(char slot[25])
{
	textcolor(2,5,8);
	printf("\n __1_____2_____3_____4_____5__	\n");
	printf("|__%c__|__%c__|__%c__|__%c__|__%c__|\n", slot[0], slot[1], slot[2], slot[3], slot[4]);
	printf("|__%c__|__%c__|__%c__|__%c__|__%c__|\n", slot[5], slot[6], slot[7], slot[8], slot[9]);
	printf("|__%c__|__%c__|__%c__|__%c__|__%c__|\n", slot[10], slot[11], slot[12], slot[13], slot[14]);
	printf("|__%c__|__%c__|__%c__|__%c__|__%c__|\n", slot[15], slot[16], slot[17], slot[18], slot[19]);
	printf("|__%c__|__%c__|__%c__|__%c__|__%c__|\n\n", slot[20], slot[21], slot[22], slot[23], slot[24]);
	textcolor(0,0,8);
}

void reinitializeEverything(char slot[25], int &ctr1, int &ctr2, int &ctr3, int &ctr4, int &ctr5)
{
	int x = 0;
	for (x = 0; x < 25; x++)
	{
		slot[x]='_';		
	}
	ctr1=4;ctr2=4;ctr3=4;ctr4=4;ctr5=4;;
}

void notifyWin(int &flag)
{
		printf("-game over-\n");
}

void checkWin(char slotCheck[25],int &flag)
{
	textcolor(1,2,8);
	int w = 5;
	int i = 0;
	int j = 0;
	for (i = 0; i < 5; i++)
	{
		for (j = 0; j < 5; j++)
		{
			
			if(slotCheck[i*w+j]=='X' && slotCheck[i*w+j+1]=='X' && slotCheck[i*w+j-1]=='X'){
				printf("Player 1 Wins! \n");
				flag = 1;
	 			notifyWin(flag);

			}
			else if(slotCheck[i*w+j]=='X' && slotCheck[i*w+j-w]=='X' && slotCheck[i*w+j+w]=='X'){
				printf("Player 1 Wins! \n");
				flag = 1;
	 			notifyWin(flag);

			}
			else if(slotCheck[i*w+j]=='X' && slotCheck[i*w+j-w+1]=='X' && slotCheck[i*w+j+w-1]=='X'){
				printf("Player 1 Wins! \n");
				flag = 1;
	 			notifyWin(flag);

			}
			else if(slotCheck[i*w+j]=='X' && slotCheck[i*w+j-w-1]=='X' && slotCheck[i*w+j+w+1]=='X'){
				printf("Player 1 Wins! \n");
				flag = 1;
	 			notifyWin(flag);

			}
			
			if(slotCheck[i*w+j]=='O' && slotCheck[i*w+j+1]=='O' && slotCheck[i*w+j-1]=='O'){
				printf("Player 2 Wins! \n");
				flag = 1;
	 			notifyWin(flag);

			}
			else if(slotCheck[i*w+j]=='O' && slotCheck[i*w+j-w]=='O' && slotCheck[i*w+j+w]=='O'){
				printf("Player 2 Wins! \n");
				flag = 1;
	 			notifyWin(flag);

			}
			else if(slotCheck[i*w+j]=='O' && slotCheck[i*w+j-w+1]=='O' && slotCheck[i*w+j+w-1]=='O'){
				printf("Player 2 Wins! \n");
				flag = 1;
	 			notifyWin(flag);

			}
			else if(slotCheck[i*w+j]=='O' && slotCheck[i*w+j-w-1]=='O' && slotCheck[i*w+j+w+1]=='O'){
				printf("Player 2 Wins! \n");
				flag = 1;
	 			notifyWin(flag);

			}

		}
	}
	textcolor(0,0,8);
}



int main(int argc, char *argv[])
{
     int sockfd, newsockfd, portno;
     socklen_t clilen;
     char buffer[256];
	  char buffer_res[256];
     struct sockaddr_in serv_addr, cli_addr;
     int n; int restart;
     if (argc < 2) {
         fprintf(stderr,"ERROR, no port provided\n");
         exit(1);
     }
     sockfd = socket(AF_INET, SOCK_STREAM, 0);
     if (sockfd < 0) 
        error("ERROR opening socket");
     bzero((char *) &serv_addr, sizeof(serv_addr));
     portno = atoi(argv[1]);
     serv_addr.sin_family = AF_INET;
     serv_addr.sin_addr.s_addr = INADDR_ANY;
     serv_addr.sin_port = htons(portno);
     if (bind(sockfd, (struct sockaddr *) &serv_addr,
              sizeof(serv_addr)) < 0) 
              error("ERROR on binding");
     listen(sockfd,5);
     clilen = sizeof(cli_addr);
     newsockfd = accept(sockfd, 
                 (struct sockaddr *) &cli_addr, 
                 &clilen);

// initializing required components
	char slot[25];
	int x = 0;
	int choice=0;
	int w =5;
	for (; x < 25; x++)
	{
				slot[x]='_';		
	}
		
	char ch[256];
	int ctr1=4,ctr2=4,ctr3=4,ctr4=4,ctr5=4;
	int flag = 0;
	char value;
	int playerWho = 1;
	
	//get name
	printf("please enter your player name: ");
	char server_name[256];
	char opponent_name[256];
	fgets(server_name,255,stdin);
	printf("your name is %s", server_name);

	n = write(newsockfd,server_name,strlen(server_name));
   		if (n < 0) 
         	error("ERROR writing to socket");

	bzero(opponent_name,256);
	n = read(newsockfd,opponent_name,255);
     		if (n < 0)
				error("ERROR reading from socket");

	system("clear");

	printf("your opponent is %s", opponent_name);


	//display board first time
	  displayBoard(slot);

	//first time prompt
			textcolor(2, 2, 8);
			printf(":: %s:: is thinking...\n", opponent_name);
			textcolor(0, 0, 8);

			textcolor(2, 2, 8);
			printf(":: standby...\n");
			textcolor(0, 0, 8);

// passing of data
	while (flag == 0)
	{   
	  
     if (newsockfd < 0) 
          error("ERROR on accept");
     bzero(buffer,256);
     n = read(newsockfd,buffer,255);
     if (n < 0) error("ERROR reading from socket");

	  value = 'O';
     choice = atoi(buffer);

	  switch(choice)
		{	
			case 1: slot[(ctr1*w)+(choice-1)]=value;
				ctr1--;
				break;
			case 2: slot[(ctr2*w)+(choice-1)]=value;
				ctr2--;				
				break;
			case 3:slot[(ctr3*w)+(choice-1)]=value;
				ctr3--;
				break;
			case 4:slot[(ctr4*w)+(choice-1)]=value;
				ctr4--;
				break;
			case 5:slot[(ctr5*w)+(choice-1)]=value;
				ctr5--;
				break;
			default:printf("Wrong choice\n");
		}

	  system("clear");

	  //display board
	  displayBoard(slot);

	 textcolor(1,1,8);
    printf(":: %s:: dropped an 'O' token in column -> %s \n",opponent_name,buffer);
	 textcolor(0,0,8);

	  //check for winner
	  checkWin(slot, flag);

	  //parallel checking of restart game
	  if (flag > 0)
	  {
			textcolor(1,2,8);
			printf("more? [ 1 (yes) / 0 (no) ]: ");
			textcolor(0,0,8);
		
			fgets(buffer_res,255,stdin);
			printf("%s", buffer_res);
			restart = atoi(buffer_res);
			if (restart)
			{
				flag = 0; //printf("restart!%d %s", flag, buffer_res);
				reinitializeEverything(slot, ctr1, ctr2, ctr3, ctr4, ctr5);
				displayBoard(slot);
			}
			else
			{
				printf("please notify your opponent that you already quit: ");
				fgets(buffer, 255, stdin);
				n = write(newsockfd,buffer,strlen(buffer));
    			if (n < 0) 
         	error("ERROR writing to socket");
				break;
			}
	  }


     value = 'X';
	  int repeat = 1;
	
	  while (repeat)
	  {
			textcolor(1, 4, 8);
			printf("\n:: your turn...\n:: Enter token at...: ");
			textcolor(0, 0, 8);

	  		fgets(buffer,255,stdin);
			choice = atoi(buffer);

			textcolor(2,2,8);
			switch(choice)
			{	
			case -1:  exit(1);
			case 1: 	if (ctr1 < 0)
						{
							printf("\n:: invalid move, column already full\n:: try again\n"); break;	
						}
						slot[(ctr1*w)+(choice-1)]=value;
						ctr1--;
						repeat=0;
						break;
			case 2: 	if (ctr2 < 0)
						{
							printf("\n:: invalid move, column already full\n:: try again\n"); break;	
						}
						slot[(ctr2*w)+(choice-1)]=value;
						ctr2--;				
						repeat=0;
						break;
			case 3:	if (ctr3 < 0)
						{
							printf("\n:: invalid move, column already full\n:: try again\n"); break;	
						}
						slot[(ctr3*w)+(choice-1)]=value;
						ctr3--;
						repeat=0;
						break;
			case 4:	if (ctr4 < 0)
						{
							printf("\n:: invalid move, column already full\n:: try again\n"); break;	
						}
						slot[(ctr4*w)+(choice-1)]=value;
						ctr4--;
						repeat=0;
						break;
			case 5:	if (ctr5 < 0)
						{
							printf("\n:: invalid move, column already full\n:: try again\n"); break;	
						}
						slot[(ctr5*w)+(choice-1)]=value;
						ctr5--;
						repeat=0;
						break;
			default: printf("\n:: invalid entry!\n:: input out of range or null\n:: try again\n");
			}
			textcolor(0,0,8);
	  }

	  system("clear");

	  //display board
	  displayBoard(slot);

	  //check for winner
	  checkWin(slot, flag);

     n = write(newsockfd,buffer,strlen(buffer));
     if (n < 0) error("ERROR writing to socket");

	  //parallel checking of restart game
	  if (flag > 0)
	  {
			textcolor(1,2,8);
			printf("more? [ 1 (yes) / 0 (no) ]: ");
			textcolor(0,0,8);

			fgets(buffer_res,255,stdin);
			//printf("%s", buffer_res);
			restart = atoi(buffer_res);
			if (restart)
			{
				flag = 0; //printf("restart!%d %s", flag, buffer_res);
				reinitializeEverything(slot, ctr1, ctr2, ctr3, ctr4, ctr5);
				displayBoard(slot);			
			}
			else
			{
				printf("please notify your opponent that you already quit: ");
				fgets(buffer, 255, stdin);
				n = write(newsockfd,buffer,strlen(buffer));
    			if (n < 0) 
         	error("ERROR writing to socket");
				break;
			}
	  }

			textcolor(2, 2, 8);
			printf(":: %s:: is thinking...\n", opponent_name);
			textcolor(0, 0, 8);

			textcolor(2, 2, 8);
			printf(":: standby...\n");
			textcolor(0, 0, 8);


	}
//
     close(newsockfd);
     close(sockfd);
     return 0; 
}
