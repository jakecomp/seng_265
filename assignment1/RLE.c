

/* 
 * File:   RLE.c
 * Author: jakobvalen
 *  
 * Created on October 2, 2019, 11:44 AM
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>   

#define MAX 41
/* 
 * The function encode takes a C-string as an input
 * We will first ensure the input is valid for the encode function
 * Once the input is validated we will print the result of our function
 */
int encode(char* input){ 
    // DNA_counter will be used to count repeating chars in our input
    int DNA_counter = 0;
    
    char previous_char;  
 
    char *current_char = input;  
    
    // Check that the input file is valid for encoding 
    for(;*current_char != '\0';current_char++){ 
        if(((*current_char !='A')&&(*current_char != 'G')&&(*current_char != 'T')&&(*current_char != 'C'))){ 
            fprintf(stderr,"Error:String cannot be encoded\n"); 
            exit(5);
        }  
        
    }   
    // DNA will be our variable to store the chars A,G,C or T
    char *DNA = &input[0]; 
    
    // Now iterate through the input and perform encode algorithm
    int i;  
    previous_char = *DNA;
    for(i = 0;i <= strlen(input); i++){  
       
        if(*DNA == previous_char){ 
          DNA_counter++;  
          DNA++;
        } 
        else { 
          printf("%c",previous_char); 
          printf("%d",DNA_counter); 
          previous_char = *DNA;
          DNA_counter =1; 
          DNA++;
        }
       
    }
        
      
    return(0);
} 

/* 
 * The function decode takes a C - string as an input 
 * We will first ensure the input is valid for the decode function
 * After the input is validated we will print out the result of our function
 */
int decode(char* input){  
    
    char *current_char = input; 
    
    // Check that the chars are valid and are in the correct location
    for(;*current_char != '\0';current_char = current_char+2){ 
        
        if(((*current_char !='A')&&(*current_char != 'G')&&(*current_char != 'T')&&(*current_char != 'C'))){  
           fprintf(stderr,"Error:String cannot be decoded\n"); 
           exit(5); 
            
        }
    }  
    // Now check that the integers are valid and are in the correct location
    int current_num = atoi(&input[1]);  
    int n;
    for(n = 1;n <= strlen(input);n = n+2){ 
        if(current_num > 9 || current_num < 1){ 
           fprintf(stderr,"Error:String cannot be decoded\n"); 
           exit(5); 
        } 
        current_num = atoi(&input[n+2]);
    } 
    // Now that the input is valid for decode get the first char and integer
    char *DNA_type = &input[0]; 
    int DNA_number = atoi(&input[1]); 
    
    // Perform decode algorithm and print the output
    int i; 
    for(i = 1;i <= strlen(input);i = i+2){ 
        
        while(DNA_number > 0){ 
            printf("%c",*DNA_type); 
            DNA_number = DNA_number-1;
        } 
        DNA_number = atoi(&input[i+2]); 
        DNA_type = DNA_type+2;
        
    }
    
    return(0);
    
}



int main(int argc, char *argv[]) { 
    
    /* 
     When our main RLE function is called we will first check 
     * that the number of arguments match the expected number
     */ 
    
    // Check if a file name was inputed
    if(argc<2){    
        fprintf(stderr,"You must provide a filename\n");  
        exit(1);
    } 
    // Check the second argument for encode or decode mode
    char *mode = argv[2]; 
    
    if (argc<3||(strcmp(mode,"e")!= 0 && strcmp(mode,"d")!= 0)){
        fprintf(stderr,"Invalid Usage,expected:RLE{filename}[e|d]\n");  
        exit(4);
               
    }   
    // Read the inputed file
    FILE *data = fopen(argv[1],"r"); 
    
    // If the file cannot be open/read for any reason print an error message
    if(data == NULL){ 
        fprintf(stderr,"Read error:File cannot be read or open\n"); 
        exit(2);
    }  
    // Here we are going to check for whitespace between any 
    // digits or characters in the text file
    char buf[MAX];  
    fgets(buf,MAX,data); 
    char *current_char = buf; 
    
    //Check if there is an immediate whitespace or if the file is empty
    if(*current_char == ' ' || *current_char == '\0'){ 
        fprintf(stderr,"Error:Invalid Format\n"); 
        exit(3); 
    }
    
    char previous_char  = *current_char; 
    // Check for trailing whitespaces 
    for(;*current_char != '\0';current_char++){ 
        if(previous_char == ' ' && *current_char !=' '){ 
           fprintf(stderr,"Error:Invalid Format\n"); 
           exit(3); 
        
    } 
    }  
    //Now trim off any extra whitespace at the end of the text file 
    int i;
    for(i = 0;i <strlen(buf); i++){  
        if(buf[i] == ' '){ 
            buf[i] = '\0'; 
            break;
        } 
        
    } 
   
    // Now call the encode or decode functions based off inputed char
    if(strcmp(mode,"e") == 0 ){
        encode(buf);
    } else{ 
        
        decode(buf);
    } 
        return (EXIT_SUCCESS);
    } 










    
    


