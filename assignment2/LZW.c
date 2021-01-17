#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define TRUE 1
#define FALSE 0

#define DICTSIZE 4096                     /* allow 4096 entries in the dict  */
#define ENTRYSIZE 32

unsigned char dict[DICTSIZE][ENTRYSIZE];  /* of 30 chars max; the first byte */
                                          /* is string length; index 0xFFF   */
                                          /* will be reserved for padding    */
                                          /* the last byte (if necessary)    */ 



// These are provided below
int read12(FILE *infil);
int write12(FILE *outfil, int int12);
void strip_lzw_ext(char *fname);
void flush12(FILE *outfil); 





int search_dictionary(unsigned char char_array[], int len){ 
    int index; 
    int index_length; 
    int char_counter = 0;  
    int index_of_found = -1;
    
    for(index=0;index<DICTSIZE;index++){  
        if(dict[index][0] == len){ 
            for(index_length=0;index_length<ENTRYSIZE;index_length++){ 
                if(dict[index][index_length] == char_array[index_length+1]){ 
                    char_counter++;  
                if(char_counter == len){ 
                    index_of_found = index; 
                    printf("%d\n",index);
                }  
            } 
        }
    } 
   
    }  
    
  return index_of_found;   
}

int encode(FILE *in, FILE *out) { 
    // TODO implement   
    
    // Initilize the dictionary  
    int i;  
    for (i=0;i<256;i++){ 
        dict[i][0] = 1;  
        dict[i][1] = i;    
    }    
    //for(i=0;i<256;i++){ 
    //   printf("%c",dict[i][1]); 
     //  printf("%d\n",i);
    //}
    
    int offset = 1; // How far ahead we are of the first 256 entries 
    int length = 0; // The length of our current string  
    
    unsigned char w[ENTRYSIZE]="";  
    
    int c; //The character that we will read from the file one bit at a time 
    
    unsigned char w_c[ENTRYSIZE]="";    
    
    
    int done_reading = FALSE; // Determines when we have reached the EOF 
    
    int index_of_w; 
    int index_of_w_c;
    int counter_input = 0;
   
    w_c[0] = w[0];
    
    while(done_reading != TRUE){  
        c = fgetc(in); 
        if (c == EOF){ 
            done_reading = TRUE;
        } else { 
          
          
        
        w_c[length] = c;   
      //  printf("%s",w_c); 
       // length++;
       
        index_of_w_c = search_dictionary(w_c,length);  
        printf("%d\n",index_of_w_c); 
        length++;
        
        if(index_of_w_c != -1){ 
        
            int i;
            for(i=1;i<ENTRYSIZE;i++){ 
                w[i] = w_c[i];
           }  
            index_of_w = index_of_w_c; 
            
        
           
        // Need to search our dictionary   
     //   int n; 
     //   int i;
    //    for (n=0;n<DICTSIZE;n++){   
    //        if(dict[n][0] == length){ 
    //            for(i=0;i<ENTRYSIZE;i++){ 
    //                if(dict[n][i] == w_c[i+1]){ 
     //                   char_counter++; 
     //                   if(char_counter == length){  
                            // get the indice 
     //                       index_of_w_c = n; 
    //                        found = TRUE; 
    //                       char_counter = 0;
     //                   }
     //               } 
     //           }
     //       }
            
          
        } else { 
          
            if(offset>=3840){ 
            
                offset = 1;   
            }  
                
                index_of_w = search_dictionary(w,length); 
                write12(out,index_of_w);
                dict[255+offset][0] = length;  
                int count; 
                for(count=0;i<length;count++){ 
                   dict[255+offset][count+1] = w_c[count];
               }
                offset++;
             
            w[0] = c;
            length = 1;  
            int n; 
            for(n=0;i<ENTRYSIZE;i++){ 
                w_c[n] = w[n];
            }
        }  
        
       }
            
    }  
  
    flush12(out);
    return(0);
}
 

int decode(FILE *in, FILE *out) {
    // TODO implement  
    
    // Initiliaze the dictionary  
    int i;  
    for (i = 0;i < 256;i++){ 
        dict[i][0] = 1;  
        dict[i][1] = i;    
    }   
    
    return(0);
}

int main(int argc, char *argv[]) {
    // TODO implement 
    // Lets start with error checking  
    if(argc<2){    
        fprintf(stderr,"You must provide a filename\n");  
        exit(1);
    } 
    
    char *mode = argv[2]; 
    
    if(argc<3 ||((strcmp(mode,"e")!=0 && strcmp(mode,"d"))!=0)){ 
        fprintf(stderr,"Invalid Usage,expected:LZW{filename}[e|d]\n");  
        exit(4);
    } 
    FILE *data = fopen(argv[1],"rb");  
    
    if(data == NULL){ 
        fprintf(stderr,"Read error:File cannot be read or open\n"); 
        exit(2);
        
    } 
    if(strcmp(mode,"e")==0){ 
        char output_name[strlen(argv[1])+4]; 
        strcpy(output_name,argv[1]); 
        strcat(output_name,".LZW"); 
        
        FILE *output = fopen(output_name,"wb"); 
        encode(data,output); 
    }else{  
        char *output_name = argv[1]; 
        strip_lzw_ext(output_name); 
        
        FILE *output = fopen(argv[1],"wb");
           decode(data,output); 
        }
    
}

/*****************************************************************************/
/* encode() performs the Lempel Ziv Welch compression from the algorithm in  */
/* the assignment specification. The strings in the dictionary have to be    */
/* handled carefully since 0 may be a valid character in a string (we can't  */
/* use the standard C string handling functions, since they will interpret   */
/* the 0 as the end of string marker). Again, writing the codes is handled   */
/* by a separate function, just so I don't have to worry about writing 12    */
/* bit numbers inside this algorithm.                                        */
//int encode(FILE *in, FILE *out) { 
    // TODO implement  
    
   
   // return(0);
//}

/*****************************************************************************/
/* decode() performs the Lempel Ziv Welch decompression from the algorithm   */
/* in the assignment specification.                                          */
//int decode(FILE *in, FILE *out) {
    // TODO implement 
    
   // return(0);
//}


/*****************************************************************************/
/* read12() handles the complexities of reading 12 bit numbers from a file.  */
/* It is the simple counterpart of write12(). Like write12(), read12() uses  */
/* static variables. The function reads two 12 bit numbers at a time, but    */
/* only returns one of them. It stores the second in a static variable to be */
/* returned the next time read12() is called.                                */
int read12(FILE *infil)
{
 static int number1 = -1, number2 = -1;
 unsigned char hi8, lo4hi4, lo8;
 int retval;

 if(number2 != -1)                        /* there is a stored number from   */
    {                                     /* last call to read12() so just   */
     retval = number2;                    /* return the number without doing */
     number2 = -1;                        /* any reading                     */
    }
 else                                     /* if there is no number stored    */
    {
     if(fread(&hi8, 1, 1, infil) != 1)    /* read three bytes (2 12 bit nums)*/
        return(-1);
     if(fread(&lo4hi4, 1, 1, infil) != 1)
        return(-1);
     if(fread(&lo8, 1, 1, infil) != 1)
        return(-1);

     number1 = hi8 * 0x10;                /* move hi8 4 bits left            */
     number1 = number1 + (lo4hi4 / 0x10); /* add hi 4 bits of middle byte    */

     number2 = (lo4hi4 % 0x10) * 0x0100;  /* move lo 4 bits of middle byte   */
                                          /* 8 bits to the left              */
     number2 = number2 + lo8;             /* add lo byte                     */

     retval = number1;
    }

 return(retval);
}

/*****************************************************************************/
/* write12() handles the complexities of writing 12 bit numbers to file so I */
/* don't have to mess up the LZW algorithm. It uses "static" variables. In a */
/* C function, if a variable is declared static, it remembers its value from */
/* one call to the next. You could use global variables to do the same thing */
/* but it wouldn't be quite as clean. Here's how the function works: it has  */
/* two static integers: number1 and number2 which are set to -1 if they do   */
/* not contain a number waiting to be written. When the function is called   */
/* with an integer to write, if there are no numbers already waiting to be   */
/* written, it simply stores the number in number1 and returns. If there is  */
/* a number waiting to be written, the function writes out the number that   */
/* is waiting and the new number as two 12 bit numbers (3 bytes total).      */
int write12(FILE *outfil, int int12)
{
 static int number1 = -1, number2 = -1;
 unsigned char hi8, lo4hi4, lo8;
 unsigned long bignum;

 if(number1 == -1)                         /* no numbers waiting             */
    {
     number1 = int12;                      /* save the number for next time  */
     return(0);                            /* actually wrote 0 bytes         */
    }

 if(int12 == -1)                           /* flush the last number and put  */
    number2 = 0x0FFF;                      /* padding at end                 */
 else
    number2 = int12;

 bignum = number1 * 0x1000;                /* move number1 12 bits left      */
 bignum = bignum + number2;                /* put number2 in lower 12 bits   */

 hi8 = (unsigned char) (bignum / 0x10000);                     /* bits 16-23 */
 lo4hi4 = (unsigned char) ((bignum % 0x10000) / 0x0100);       /* bits  8-15 */
 lo8 = (unsigned char) (bignum % 0x0100);                      /* bits  0-7  */

 fwrite(&hi8, 1, 1, outfil);               /* write the bytes one at a time  */
 fwrite(&lo4hi4, 1, 1, outfil);
 fwrite(&lo8, 1, 1, outfil);

 number1 = -1;                             /* no bytes waiting any more      */
 number2 = -1;

 return(3);                                /* wrote 3 bytes                  */
}

/** Write out the remaining partial codes */
void flush12(FILE *outfil)
{
 write12(outfil, -1);                      /* -1 tells write12() to write    */
}                                          /* the number in waiting          */

/** Remove the ".LZW" extension from a filename */
void strip_lzw_ext(char *fname)
{
    char *end = fname + strlen(fname);

    while (end > fname && *end != '.' && *end != '\\' && *end != '/') {
        --end;
    }
    if ((end > fname && *end == '.') &&
        (*(end - 1) != '\\' && *(end - 1) != '/')) {
        *end = '\0';
    }
}










