

typedef struct nodeHash{            //struktura pre nas prvok v tomto programe
    PERSON *pers;
    struct nodeHash *next;
}NODEHASH;

NODEHASH *createNewNodeHash(PERSON *person){            //funkcia alokuje a inicializuje prvok
    NODEHASH *newNode = (NODEHASH*) malloc(sizeof(NODEHASH));
    newNode->pers = person;
    newNode->next = NULL;
    return newNode;
}

void appendToListHash(NODEHASH *newNode, NODEHASH **table, unsigned long int hash){                 //podla hashu zisti kde v tabulke je dany zoznam, a potom prvok prideli na jeho koniec
    NODEHASH *pomocnik = table[hash];
    if(pomocnik == NULL){
        table[hash] = newNode;
    }
    else{
        while(pomocnik->next!=NULL){
            pomocnik = pomocnik->next;
        }
        if(pomocnik->next == NULL){
            pomocnik->next = newNode;
        }
    }
}

void printListHash(NODEHASH *rootNode){
    NODEHASH *start = rootNode;
        while(rootNode!=NULL){
            printf("%s,   %d\n", rootNode->pers->name, rootNode->pers->age);
            rootNode = rootNode->next;
        }
    rootNode = start;
}

NODEHASH* findInListHash(PERSON *subject, NODEHASH* list){          //funkcia prechadza zoznam do konca/dokym najde subjekt
    if(list==NULL){
        return NULL;
    }
    else{
        NODEHASH *pomocnik = list;
        while(pomocnik!=NULL){
            if(strcmp(subject->name,pomocnik->pers->name)==0){
                if(subject->age == pomocnik->pers->age){
                    return pomocnik;
                }
            }
            pomocnik = pomocnik->next;
        }
    }
    return NULL;
}

char *randomStringHash(int size){            //funkcia vygeneruje random string malych pismen
    char pismena[] = "abcdefghijklmnopqrstuvwxyz";
    char *str = NULL;
    str = (char*)malloc(sizeof(char)*(size+1));
    for(int i=0; i<size; i++){
        str[i]=pismena[rand()%(26)];
        if(i==size-1) str[i+1]='\0';
    }
    return str;
}

int randomNumberHash(int max){          //funkcia vygeneruje random cislo s maximom
    int num;
    num = rand() % max;
    return num;
}

PERSON *createPersonHash(char *inputName, int inputAge){            //funkcia vytvori/inicializuje struct person
    PERSON *newPerson = (PERSON*) malloc(sizeof(PERSON));
    strcpy(newPerson->name,inputName);
    newPerson->age = inputAge;
    return newPerson;
}

unsigned long int createHashHash(PERSON *pers, long int tableSize){     //inspirovane prastarou hashovacou funkciou djb2 od Dana Bernsteina, opisane hlbsie v dokumentacii
    unsigned long int hash = 5381;
    int i = 0;
    while(pers->name[i] != '\0'){
        hash = (hash * (unsigned long)pow(2,5)) + hash + pers->name[i];
        i++;
    }
    hash += pers->age;
    return (hash%tableSize);
}

NODEHASH *searchHash(char *inputName, int inputAge,NODEHASH **table , int tableSize){   //sluzi na sprostredkovanie medzi testovacou funkciou a funkciou findInList
    PERSON *pers = createPersonHash(inputName, inputAge);
    unsigned long int hash = createHashHash(pers,tableSize);

    return findInListHash(pers, table[hash]);
}

NODEHASH **rehashHash(NODEHASH **table, long int tableSize){            //funkcia vytvori novu vacsiu tabulku a prehashuje vsetky prvky zo starej do novej
    NODEHASH *pomoc = table[0], *rakety;
    long int newSize = tableSize * 5;
    NODEHASH **newTable = (NODEHASH**)malloc(sizeof(NODEHASH*)*(newSize));
    for(long int i=0;i<newSize;i++){
        newTable[i] = NULL;
    }

    for(long int i=0; i<tableSize;i++){
        pomoc = table[i];
        while(pomoc!=NULL){
            unsigned long int hash = createHashHash(pomoc->pers,newSize);
            rakety = createNewNodeHash(createPersonHash(pomoc->pers->name,pomoc->pers->age));
            appendToListHash(rakety,newTable,hash);
            pomoc = pomoc->next;

        }
    }
    for(long int i = 0;i<tableSize;i++){
        free(table[i]);
    }
    free(table);

    return newTable;
}

NODEHASH **testInsertHash(NODEHASH **table, long int *tableSize, int num){          //test pre vkladanie prvkov
    clock_t start = clock();
    for(long int i=0; i<num;i++){
        NODEHASH *haha = createNewNodeHash(createPersonHash(randomStringHash(5),randomNumberHash(50)));
        unsigned long int hash = createHashHash(haha->pers,*tableSize);
        appendToListHash(haha,table,hash);

        if(i>=(*tableSize)){
            table = rehashHash(table,(*tableSize));
            *tableSize = (*tableSize)*5;
        }
    }
    clock_t end = clock();
    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    printf("The insertion of %d nodes with rehashing took %f seconds\n",num,seconds);
    return table;
}

void testSearchHash(NODEHASH **table, long int tableSize, int num){         //test pre vyhladavanie prvkov
    long int finds= 0;
    clock_t start2 = clock();
    for(long int i=0; i<num;i++){
        if(searchHash(randomStringHash(5),randomNumberHash(50),table,tableSize)!=NULL){
            finds++;
        }
    }
    clock_t end2 = clock();
    float seconds2 = (float)(end2 - start2) / CLOCKS_PER_SEC;
    printf("The search of %d nodes took %f seconds\n",num,seconds2);
    for(long int i=0;i<tableSize;i++){
        free(table[i]);
    }
    free(table);
}
NODEHASH **initializeTestHash(long int size){           //funkcia sluzi na inicializaciu testu
    long int tableSize = size;
    NODEHASH **table = (NODEHASH**)malloc(sizeof(NODEHASH*)*tableSize);
    for(long int i=0;i<tableSize;i++){
        table[i] = NULL;
    }
    return table;
}
void fullTestHash(long int size){           //funkcia sluzi na spojenie testov dokopy
    long int tableSize = size/10;
    NODEHASH** table;
    table = initializeTestHash(tableSize);
    table = testInsertHash(table,&tableSize,size);
    testSearchHash(table,tableSize,size);
    printf("\n");
}

