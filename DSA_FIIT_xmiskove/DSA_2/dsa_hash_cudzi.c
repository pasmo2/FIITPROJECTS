// kod algoritmu prevzaty z https://github.com/prabaprakash/Data-Structures-and-Algorithms-Programs/blob/master/Hashing%20-%20Linear%20Probing%20(Open%20addressing).c



typedef struct nodeHashCudzi{           //struktura, ktoru v tomto programe pouzivame ako prvok. ostava rovnaka ako pri prvom hashi pre zachovanie porovnatelnosti
    PERSON *pers;
    struct nodeHashCudzi *next;
}NODEHASHCUDZI;


NODEHASHCUDZI *createNewNodeHashCudzi(PERSON *person){              //funkcia alokuje a inicializuje prvok pre tento program
    NODEHASHCUDZI *newNode = (NODEHASHCUDZI*) malloc(sizeof(NODEHASHCUDZI));
    newNode->pers = person;
    newNode->next = NULL;
    return newNode;
}

char *randomStringHashCudzi(int size){            //funkcia vygeneruje random string pismen
    char pismena[] = "abcdefghijklmnopqrstuvwxyz";
    char *str = NULL;
    str = (char*)malloc(sizeof(char)*(size+1));
    for(int i=0; i<size; i++){
        str[i]=pismena[rand()%(26)];
        if(i==size-1) str[i+1]='\0';
    }
    return str;
}

int randomNumberHashCudzi(int max){         //funkcia vygeneruje random cislo
    int num;
    num = rand() % max;
    return num;
}

PERSON *createPersonHashCudzi(char *inputName, int inputAge){       //funkcia alokuje a inicializuje noveho cloveka
    PERSON *newPerson = (PERSON*) malloc(sizeof(PERSON));
    strcpy(newPerson->name,inputName);
    newPerson->age = inputAge;
    return newPerson;
}

long int createHashHashCudzi(PERSON *pers, long int tableSize){     //inspirovane prastarou hashovacou funkciou djb2 od Dana Bernsteina, popisana v dokumentacii
    long int hash = 5381;
    int i = 0;
    while(pers->name[i] != '\0'){
        hash = (hash * (long)pow(2,5)) + hash + pers->name[i];
        i++;
    }
    hash += pers->age;
    return (hash%tableSize);
}

void InsertHashCudzi(NODEHASHCUDZI *element, long int hashSize, long int *countHash, NODEHASHCUDZI **arr)           //funkcia vklada prvok do tabulky
{
    if(*countHash==hashSize){
        printf("Error.\nTable is FULL\n");
        return;
    }
    long int probe=createHashHashCudzi(element->pers, hashSize);
    while(arr[probe]!=NULL)
    {
        probe=(probe+1)%hashSize;
    }
    arr[probe]=element;
    (*countHash)++;
}

long int searchElementHashCudzi(char *inputName, int inputAge, long int hashSize, long int *countHash, NODEHASHCUDZI **arr)     //funkcia vyhladava prvok v tabulke
{
    if(*countHash==0){
        printf("Error.\nTable is EMPTY\n");
        exit(EXIT_FAILURE);
    }
    long int probe=createHashHashCudzi(createPersonHashCudzi(inputName,inputAge), hashSize);
    while(arr[probe]!=NULL)
    {
        if(probe == hashSize - 1) return 0;
        if(arr[probe]->pers->age==inputAge && strcmp(arr[probe]->pers->name,inputName)==0){
            return probe;
        }
        probe=(probe+1)%hashSize;
    }
    return -1;
}


void testInsertHashCudzi(long int num, long int hashSize, long int *countHash, NODEHASHCUDZI **arr){        //funkcia testuje vkladanie prvkov do tabulky
    clock_t start = clock();
    for(long int i=0;i<num;i++){
        if(i>=hashSize){
            printf("max size reached\n");
            return;
        }
        NODEHASHCUDZI *newNode = createNewNodeHashCudzi(createPersonHashCudzi(randomStringHashCudzi(5),randomNumberHashCudzi(50)));
        InsertHashCudzi(newNode,hashSize,countHash, arr);
    }
    clock_t end = clock();
    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    printf("the insertion of %li nodes(without rehashing) took %f seconds\n",num,seconds);
}

void testSearchHashCudzi(long int num, long int hashSize, long int *countHash, NODEHASHCUDZI **arr){        //funkcia testuje vyhladavanie prvkov v tabulke
    clock_t start = clock();
    for(long int i=0;i<num;i++){
        searchElementHashCudzi(randomStringHashCudzi(5),randomNumberHashCudzi(50),hashSize,countHash, arr);
    }
    clock_t end = clock();
    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    printf("the search of %li nodes took %f seconds\n",num,seconds);
    for(long int i=0;i<hashSize;i++){
        free(arr[i]);
    }
}

void fullTestHashCudzi(long int iterations){                //funkcia sluzi na spojenie testov dokopy a inicializaciu testu
    long int countHash= 0;
    long int hashSize = 3*iterations;
    NODEHASHCUDZI *arr[hashSize];
    for(long int i=0;i<hashSize;i++){
        arr[i] =(NODEHASHCUDZI*)malloc(sizeof(NODEHASHCUDZI));
        arr[i] = NULL;
    }
    testInsertHashCudzi(iterations,hashSize,&countHash,arr);
    testSearchHashCudzi(iterations,hashSize,&countHash,arr);
    printf("\n");
}


