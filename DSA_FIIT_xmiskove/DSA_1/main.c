#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>



unsigned char *memory;

unsigned short getShortIntNumber(unsigned char *ptr){                                                        //pomocna funkcia na zlozenie cisla
    return (unsigned short)((*ptr)*256)+(*(ptr+1));
}

void putNumber(unsigned char *ptr, unsigned short num){                                                      //pomocna funkcia na zapisanie rozlozeneho cisla
    *(unsigned char*)(ptr) = num/256;
    *(unsigned char*)(ptr+1) = num%256;
}

/*int blockIsEmpty(unsigned char *ptr){                                                                        //funkcia zisti, ci je blok pamate volny
    unsigned short size, i;
    size=getShortIntNumber(ptr);
    if(size>getShortIntNumber(memory)){
        return 0;
    }
    if(getShortIntNumber(ptr+2)!=0 && getShortIntNumber(ptr+4)!=0 && getShortIntNumber(ptr+size+2)==size){
        for(i=6;i<size+2;i++){
            if(*(ptr+i)!=0){
                return 0;
            }
        }
        return 1;
    }
    else return 0;
}*/

int checkPreviousForAdjacency(unsigned char *ptr){
    unsigned short prevIndex=getShortIntNumber(ptr+2), prevSize;
    if(prevIndex==1) return 0;
    else{
        prevSize=getShortIntNumber(memory+prevIndex);
        if((memory+prevIndex+prevSize+4)==ptr){
            return 1;
        }
        else return 0;
    }
}

void fixFragments(unsigned char *ptr){
    unsigned short prevIndex=getShortIntNumber(ptr+2), nextIndex=getShortIntNumber(ptr+4), prevSize, nextSize, currentSize, newSize;
    currentSize=getShortIntNumber(ptr);
                                                                                                            //oboje volne su adjacent
    if(prevIndex!=1 && nextIndex!=1){
        if(checkPreviousForAdjacency(ptr)==1 && checkPreviousForAdjacency(memory+nextIndex)==1){
            prevSize=getShortIntNumber(memory+prevIndex);
            nextSize=getShortIntNumber(memory+nextIndex);
            newSize=prevSize+currentSize+nextSize+8;
            putNumber(memory+prevIndex,newSize);                                                        // prepisanie novej hlavicky -> size
                                                                                                            // netreba prepisovat v najprednejsom bloku prevIndex pretoze ten ostava
            putNumber(memory+prevIndex+4,getShortIntNumber(memory+nextIndex+4));               // prepisanie nextIndex v najprednejsom bloku (stale hlavicka)
            putNumber(memory+prevIndex+newSize+2,newSize);                                              // vytvorenie noveho footeru
                                                                                                            // nizsie bude prepisovanie uz irelevantnych informacii
            putNumber(memory+prevIndex+prevSize+2,0);                                              // prepisanie peticky predosleho bloku
            putNumber(ptr,0);                                                                          //    --   --
            putNumber(ptr+2,0);                                                                    //               ---     ---
                                                                                                            //                                          prepisanie vsetkych hlaviciek a piet stredneho bloku
            putNumber(ptr+4,0);                                                                    //               ---     ---
            putNumber(ptr+currentSize+2,0);                                                        //    --   --
            putNumber(memory+nextIndex,0);                                                         // rovnake prepisanie posledneho bloku, lenze neprepisujem peticku, nakolko sa z nej stala nova peticka spojeneho bloku a uz ma v sebe data
            putNumber(memory+nextIndex+2,0);
            putNumber(memory+nextIndex+4,0);
        }
    }
    else if(prevIndex!=1){
        if(checkPreviousForAdjacency(ptr)==1){
            prevSize=getShortIntNumber(memory+prevIndex);
            newSize=prevSize+currentSize+4;
            putNumber(memory+prevIndex,newSize);                                                        //zapisanie novych udajov
            putNumber(memory+prevIndex+4,getShortIntNumber(ptr+4));
            putNumber(memory+prevIndex+newSize+2, newSize);
                                                                                                            //prepisanie starych udajov
            putNumber(memory+prevSize+prevIndex+2,0);
            putNumber(ptr,0);
            putNumber(ptr+2,0);
            putNumber(ptr+4,0);
        }
    }
    else if(nextIndex!=1){
        if(checkPreviousForAdjacency(memory+nextIndex)==1){
            nextSize=getShortIntNumber(memory+nextIndex);
            newSize= currentSize+nextSize+4;
            putNumber(ptr,newSize);                                                                          //zapisanie novych udajov
            putNumber(ptr+4,getShortIntNumber(memory+nextIndex+4));
            putNumber(ptr+newSize+2,newSize);

            putNumber(ptr+currentSize+2,0);                                                         //prepisanie starych udajov
            putNumber(memory+nextIndex,0);
            putNumber(memory+nextIndex+2,0);
            putNumber(memory+nextIndex+4,0);
        }
    }


}

void allocate(unsigned short index, unsigned int size){                                                      //pomocna funkcia k memory_alloc
    unsigned short prevData, nextData, newFooter, newHeader, remainingSize;
    prevData=getShortIntNumber(memory+index+2);
    nextData=getShortIntNumber(memory+index+4);
    if(size==getShortIntNumber(memory+index)){                      //ak sa alokuje cely volny blok
        if(prevData==1 && nextData!=1){
            putNumber(memory+nextData+2,prevData);                  //posun pointerov
            putNumber(memory+2,nextData);
        }
        if(prevData!=1 && nextData==1){
            putNumber(memory+prevData+4,nextData);                  //posun pointerov
        }
        if(prevData!=1 && nextData!=1){
            putNumber(memory+nextData+2,prevData);                  //posun pointerov
            putNumber(memory+prevData+4,nextData);                  //posun pointerov
        }
        if(prevData==1 && nextData==1){
            putNumber(memory+2,1);                             //nastavenie zaciatocneho pointeru na 1 ---> cela pamat je obsadena
        }
        putNumber(memory+index+2,0);                           //vynulovanie byvalych pointerov
        putNumber(memory+index+4,0);
    }
    else{                                                               //ak sa alokuje iba cast volneho bloku
        newFooter=index+2+getShortIntNumber(memory+index);          //vypocet noveho footeru a headeru
        newHeader=index+(size+4);
        remainingSize=getShortIntNumber(memory+index)-(size+4);     //vypocet ostavajucej velkosti bloku pamate
        putNumber(memory+newFooter,remainingSize);                  //zapisanie ostavajucej velkosti do novych headerov a footerov
        putNumber(memory+newHeader,remainingSize);
        putNumber(memory+newHeader+2,getShortIntNumber(memory+index+2));        //presun pointerov na nove miesto
        putNumber(memory+newHeader+4,getShortIntNumber(memory+index+4));
        putNumber(memory+index,size);                                                    //zadanie velkosti alokovanej pamate do noveho bloku
        putNumber(memory+index+(size+2),size);
        putNumber(memory+index+2,0);                                                //prepisanie starych pointerov
        if(size>2)putNumber(memory+index+4,0);
        if(prevData!=1){                                        //vyriesenie pointeru na nasledujuci volny blok, ktory sa nachadza v predoslom volnom bloku (alebo na zaciatku pamate)
            putNumber(memory+prevData,newHeader);
        }
        else{
            putNumber(memory+2,newHeader);
        }

    }


}



void memory_init(void *ptr, unsigned int size){
    for(int i=0;i<size;i++){
        *(unsigned char*)ptr=0;
    }
    memory=ptr;
    putNumber(memory,size);                                     //header

    unsigned int nextFree = 4;
    putNumber(memory+2,nextFree);                           //nextFreeSpace

    putNumber(memory+4,size-8);                        //freeMemorySize  (firstFreeSpace)

    putNumber(memory+6,1);                             //previousPointer

    putNumber(memory+8,1);                             //nextPointer

    putNumber(memory+(size-2),(size-8));               //footer
}

void *memory_alloc(unsigned int size){
    if(getShortIntNumber(memory+2)==1){
        //printf("Neexistuje volny blok pamate!\n");
        return NULL;
    }
    unsigned short currentIndex, /*nextIndex,*/ currentData, nextData;
    if(size<=getShortIntNumber(memory)-8){  //ak mam dostatocne velke cele pole  //1
        //printf("good!!\n");
        currentIndex=getShortIntNumber(memory+2);
            if(size<=getShortIntNumber(memory+currentIndex)){
                if(getShortIntNumber(memory+currentIndex)-size<8){
                    size=getShortIntNumber(memory+currentIndex);
                }
                allocate(currentIndex,size);                                                    //alokujem
                return (memory+currentIndex);
                //printf("alokacia na indexe %u\n",currentIndex);
            }
            else {
                while(1){
                    //nextIndex=4+currentIndex;
                    nextData=getShortIntNumber(memory+4+currentIndex);
                    if(nextData!=1){                               //uz nie je volna pamat
                        currentIndex=nextData;
                        currentData=getShortIntNumber(memory+nextData);
                        if(size<=getShortIntNumber(memory+currentIndex)){
                            if(getShortIntNumber(memory+currentIndex)-size<8){
                                size=getShortIntNumber(memory+currentIndex);
                            }
                            allocate(currentIndex,size);                                        //alokujem
                            return memory+currentIndex;
                            //printf("alokacia na indexe %u\n",currentIndex);
                        }
                        else{
                            continue;
                        }
                    }
                    else{                                           //este je volna pamat
                        //printf("Nedostatocne velka pamat -> %u\n",currentData);
                        return NULL;
                    }
                }
            }
    }
    else{
        //printf("Nedostatocne velka pamat  -> start\n");
        return NULL;
    }
}


int memory_check(void *ptr){
    if(getShortIntNumber(ptr)!=0){
        if(getShortIntNumber(ptr+2)==0 && getShortIntNumber(ptr+4)==0){
            if(getShortIntNumber(ptr+2+getShortIntNumber(ptr))==getShortIntNumber(ptr)){
                return 1;
            }
        }
    }
    return 0;
}

void *findNextEmptyBlock(void *ptr){
    while(1){
        if(memory_check(ptr)==1){
            ptr+=(getShortIntNumber(ptr))+4;
        }
        else{
            return ptr;
        }
        if((unsigned char*)ptr-memory>=getShortIntNumber(memory)){
            return NULL;
        }
    }
}

int memory_free(void *valid_ptr){
    unsigned char *nextEmptyBlock;
    unsigned short nextIndex, findingPrev;
    nextEmptyBlock=findNextEmptyBlock((unsigned char*)valid_ptr);
    if(nextEmptyBlock==NULL){
        if(getShortIntNumber(memory+2)==1){
            putNumber(memory+2,(unsigned short)((unsigned char*)valid_ptr-memory));
            putNumber(valid_ptr+2,1);
            putNumber(valid_ptr+4,1);
            fixFragments(valid_ptr);
            return 0;
        }
        else{
            findingPrev=getShortIntNumber(memory+2);
            while(1){
                if(getShortIntNumber(memory+4+findingPrev)==1){
                    putNumber(findingPrev+memory+4,(unsigned short)((unsigned char*)valid_ptr-memory));
                    putNumber(valid_ptr+2,findingPrev);
                    putNumber(valid_ptr+4,1);
                    break;
                }
                else{
                    findingPrev=getShortIntNumber(memory+4+findingPrev);
                }
            }
            fixFragments(valid_ptr);
            return 0;
        }
    }
    else{
        nextIndex=(unsigned short)(nextEmptyBlock-memory);
        putNumber(valid_ptr+2,getShortIntNumber(memory+nextIndex+2));
        putNumber(valid_ptr+4,nextIndex);
        if(getShortIntNumber(valid_ptr+2)==1){
            putNumber(memory+2,(unsigned short)((unsigned char*)valid_ptr-memory));
        }
        else{
            putNumber(memory+getShortIntNumber(valid_ptr+2)+4,(unsigned short)((unsigned char*)valid_ptr-memory));
        }
        putNumber(memory+nextIndex+2,(unsigned short)((unsigned char*)valid_ptr-memory));
        fixFragments(valid_ptr);
        return 0;
    }


}




int randomNumber(int lower, int upper)                  //pri tejto funkcii som sa inspiroval https://www.geeksforgeeks.org/generating-random-number-range-c/
{

    int num = (rand() % (upper - lower + 1)) + lower;
    return num;
}


void testScenar1(int blockSize, int memorySize, unsigned char *str){
    unsigned char *ptr1 = (unsigned char*)200;          //len nieco aby tam nebol NULL
    float count=0;
    float efficiency;
    memory_init(str, memorySize);
    while(ptr1!=NULL){
        ptr1=memory_alloc(blockSize);
        if(ptr1!=NULL)count+=(float)blockSize;
    }
    for(int i=0;i<memorySize;i++){
        printf("|%5u",*(unsigned char*)(str+i));
    }
    printf("\n");
    for(int i=0;i<memorySize;i++) {
        printf("|%5u", i);
    }
    efficiency=((float)(count/(float)(memorySize))*100);
    printf("\n\nEfektivita tohto testu je: %.2f%%\n",efficiency);
}

void testScenar234(int upper, int lower, int memorySize, unsigned char *str){
    unsigned char *ptr1 = (unsigned char*)200;
    float count=0;
    float efficiency;
    srand(time(0));
    int i=0, zvysok;
    int hodnota[5];    // vygenerujem 5 nahodnych hodnot z nasho intervalu
    for(int j=0;j<5;j++){
        hodnota[j]=randomNumber(lower,upper);
        printf("%d\n",hodnota[j]);
    }
    memory_init(str, memorySize);
    while(ptr1!=NULL){
        zvysok=i%5;
        ptr1=memory_alloc(hodnota[zvysok]);
        if(ptr1!=NULL)count+=(float)hodnota[zvysok];
        i++;
    }
    for(int i=0;i<memorySize;i++){
        printf("|%5u",*(unsigned char*)(str+i));
    }
    printf("\n");
    for(int i=0;i<memorySize;i++) {
        printf("|%5u", i);
    }
    efficiency=((float)(count/(float)(memorySize))*100);
    printf("\n\nEfektivita tohto testu je: %.2f%%\n",efficiency);
}

int main() {
    unsigned char *ptr1, *ptr2, *ptr3;
    int size=50, count=0;
    unsigned char str[55000];
    //testScenar1(15,500,str);
    //testScenar234(5000,500,10000,str);


    return 0;
}










