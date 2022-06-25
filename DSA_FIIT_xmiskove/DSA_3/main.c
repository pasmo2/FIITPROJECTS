#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>


typedef struct bf{                  //struktura, v ktorej drzim booleovsku funkciu v podobe vektora v stringu a pocet premennych
    char *vectorFunction;
    int numOfVariables;
}BF;


typedef struct uzol{                //struktura uzlov, ktore tvoria diagram
    int terminal;                   //terminal je "list" diagramu, ktory drzi iba hodnotu 1 alebo 0. Ak uzol nie je terminal, jeho hodnota premennej terminal je 2
    int skipLeft;                   //skipLeft/skipRight sluzia na preskakovanie premennych v BDD_use, tieto hodnoty sa menia v tretej faze BDD_reduce
    int skipRight;
    BF *function;
    struct uzol *left;              //klasicky lavy a pravy child daneho uzla
    struct uzol *right;
}UZOL;

typedef struct bdd{                 //struktura BDD obsahuje pocet premennych, pre ktory je vytvorena, pocet uzlov, ktore obsahuje, a pointer na svoj koren v podobe uzla
    int globalNumberOfVariables;
    int sizeOfDiagram;
    UZOL *root;
}BDD;



char *createNewRandomVector(int numOfVariables){            //vygeneruje nahodnu funkciu pre dany pocet premennych (string nul a jednotiek)
    long int size = (long int)pow(2,numOfVariables);        //2^x, pricom x je pocet premennych, je dlzka stringu(vektoru)
    char *vector = (char*)malloc(sizeof(char)*(size+1));
    for(long int i=0; i<size;i++){
        vector[i] = (char)(48+(rand()%2));
        if(i==size-1) vector[i+1] = '\0';
    }
    return vector;
}

/*char *createNewVectorFromInput(){
    char *vector = (char*)malloc(sizeof(char));
    scanf("%s",vector);
    return vector;
}*/

BF *createNewBF(char *vector, int numOfVariables){      //vytvori a alokuje novu BF z vektoru a poctu premennych
    BF* newBF = (BF*)malloc(sizeof(BF));
    newBF->numOfVariables = numOfVariables;
    newBF->vectorFunction = vector;
    return newBF;
}

UZOL *createNewElement(BF *function){                   //vytvori a alokuje novy uzol (terminal=2 takze nie je list(terminal))
    UZOL *newElement = (UZOL*) malloc(sizeof(UZOL));
    newElement->function = function;
    newElement->left = NULL;
    newElement->right = NULL;
    newElement->terminal = 2;
    newElement->skipLeft = 0;
    newElement->skipRight = 0;
    return newElement;
}

UZOL *createNewTerminal(int terminalNumber){            //vytvori a alokuje novy list(terminal)
    UZOL *newElement = (UZOL*) malloc(sizeof(UZOL));
    newElement->left = NULL;
    newElement->right = NULL;
    newElement->terminal = terminalNumber;
    return newElement;
}

BF *createLeftBF(BF *oldBF){                            //pri rozpolovani vektoru vytvori lavu stranu
    long int newSize = (long int)(pow(2,oldBF->numOfVariables))/2;
    char *firstHalfOfFunction = (char*)malloc(sizeof(char)*(newSize+1));
    for(long int i=0;i<newSize;i++){
        firstHalfOfFunction[i] = oldBF->vectorFunction[i];
        if(i==newSize-1) firstHalfOfFunction[i+1]='\0';
    }
    BF *halvedBF = createNewBF(firstHalfOfFunction,((oldBF->numOfVariables)-1));
    return halvedBF;
}

BF *createRightBF(BF *oldBF){                              //pri rozpolovani vektoru vytvori pravu stranu
    long int newSize = (long int)(pow(2,oldBF->numOfVariables))/2;
    char *firstHalfOfFunction = (char*)malloc(sizeof(char)*(newSize+1));
    for(long int i=newSize;i<(newSize*2);i++){
        firstHalfOfFunction[i-newSize] = oldBF->vectorFunction[i];
        if(i==(newSize*2)-1) firstHalfOfFunction[i+1-newSize]='\0';
    }
    BF *halvedBF = createNewBF(firstHalfOfFunction,((oldBF->numOfVariables)-1));
    return halvedBF;
}

char *createRandomStringOfVariables(int numOfVariables){
    int size = numOfVariables;
    char *str = (char*)malloc(sizeof(char)*(size+1));
    for(long int i=0; i<size;i++){
        str[i] = (char)(48+(rand()%2));
        if(i==size-1) str[i+1] = '\0';
    }
    return str;
}

void splitElements(UZOL *element, BDD *newBDD){             //tato funkcia porozdeluje vektor na polovice dokym sa to da, cize vytvori skoro cely bdd
    if(element==NULL){
        printf("element==NULL\n");
        return;
    }
    else{
        if(element->function->numOfVariables>1 && element->terminal==2){
            element->left = createNewElement(createLeftBF(element->function));
            splitElements(element->left, newBDD);       //splitne nalavo
            element->right = createNewElement(createRightBF(element->function));
            splitElements(element->right, newBDD);      //splitne napravo
            newBDD->sizeOfDiagram+=2;
        }
        else if (element->function->numOfVariables==1){                     //vytvori terminaly a prestane sa rozdelovat
            int leftNumber = (int)element->function->vectorFunction[0];
            int rightNumber = (int)element->function->vectorFunction[1];
            element->left = createNewTerminal(leftNumber-48);
            element->right = createNewTerminal(rightNumber-48);
            newBDD->sizeOfDiagram+=2;
        }
    }
}

int isBFRedundant(BF* function){            //zisti, ci je BF cisto z jednotiek alebo nul
    int size = (int)strlen(function->vectorFunction);
    for(int i=0;i<size;i++){
        if(function->vectorFunction[0]==function->vectorFunction[i]){
            //everything is fine
        }
        else return 0;
    }
    return 1;
}

void traverseAllTerminals(UZOL *uzol, UZOL *terminal0, UZOL *terminal1, int *count){            //uvolni vsetky terminaly a napoji ich na dva predvytvorene
    if (uzol!=NULL) {
        if(uzol->left->terminal==0){
            (*count)--;
            free(uzol->left);
            uzol->left = terminal0;
        }
        if(uzol->right->terminal==0){
            (*count)--;
            free(uzol->right);
            uzol->right = terminal0;
        }
        if (uzol->left->terminal==1){
            (*count)--;
            free(uzol->left);
            uzol->left = terminal1;
        }
        if (uzol->right->terminal==1){
            (*count)--;
            free(uzol->right);
            uzol->right = terminal1;
        }
        if (uzol->left!=NULL && uzol->left->terminal == 2) {                //rekurzivne prebehne cely bdd
            traverseAllTerminals(uzol->left, terminal0, terminal1, count);
        }


        if (uzol->right!=NULL && uzol->right->terminal == 2) {
            traverseAllTerminals(uzol->right, terminal0, terminal1, count);
        }
    }
}

void mergeTerminals(BDD *bdd){                                      //vytvori terminaly, ktore sa budu pouzivat a zavola funkciu ktora ich ponapaja
    UZOL *singleTerminal0 = createNewTerminal(0);
    UZOL *singleTerminal1 = createNewTerminal(1);
    traverseAllTerminals(bdd->root,singleTerminal0,singleTerminal1, &bdd->sizeOfDiagram);
}

int isBFDuplicateNoTerminal(UZOL *uzol){                            //zisti, ci je vektor v uzle z rovnakych polovic
    if(uzol->left->terminal!=2 || uzol->right->terminal!=2){
        return 0;
    }
    if(strcmp(uzol->left->function->vectorFunction,uzol->right->function->vectorFunction)==0){
        return 1;
    }
    else return 0;
}

int checkHalves(UZOL *uzol){                                    //zisti, ci ma vektor rovnake polovice
    int half = (int)strlen(uzol->function->vectorFunction)/2;
    if(strlen(uzol->function->vectorFunction)%2==1){
        return 0;
    }
    for(int i=0;i<half;i++){
        if(uzol->function->vectorFunction[i]!=uzol->function->vectorFunction[i+half]){
            return 0;
        }
    }
    return 1;

}

void freeSubtree(UZOL *uzol){                           //uvolni cely podstrom
    if(uzol->left!=NULL && uzol->left->terminal==2){
        freeSubtree(uzol->left);
    }
    if(uzol->right!=NULL && uzol->right->terminal==2){
        freeSubtree(uzol->right);
    }
    if(uzol->terminal==2){
        free(uzol);
    }
}

void freeBDD(BDD *bdd){                             //uvolni bdd
    freeSubtree(bdd->root);
    free(bdd);
}

void traverseSubtree(UZOL *uzol, int *count){               //prejde strom pri redukcii a spocita uzly, ktore sa redukuju
    if(uzol->left!=NULL && uzol->left->terminal==2){
        traverseSubtree(uzol->left, count);
    }
    if(uzol->right!=NULL && uzol->right->terminal==2){
        traverseSubtree(uzol->right, count);
    }
    if(uzol->terminal==2){
        (*count)--;
    }
}

void mergeDuplicates(UZOL *uzol, int *count){                   //druha faza redukcie, TYP S v prezentacii pana prednasajuceho
    if(uzol!=NULL){
        if(isBFDuplicateNoTerminal(uzol)==1){
            //printf("2. phase, %s\n",uzol->function->vectorFunction);
            traverseSubtree(uzol->right, count);
            uzol->right=uzol->left;
        }
        if (uzol->left!=NULL && uzol->left->terminal == 2) {
            mergeDuplicates(uzol->left, count);
        }


        if (uzol->right!=NULL && uzol->right->terminal == 2) {
            mergeDuplicates(uzol->right, count);
        }
    }
}

void removeRedundantElements(UZOL *uzol, int *count){                   //tretia faza redukcie, TYP I v prezentacii pana prednasajuceho
    if(uzol!=NULL){
        while(uzol->left->terminal==2 && checkHalves(uzol->left)==1){
            UZOL *temp = uzol->left->left;
            //printf("3. phase, %s\n",uzol->left->function->vectorFunction);
            free(uzol->left);
            uzol->left = temp;
            uzol->skipLeft++;
            (*count)--;
        }
        while(uzol->right->terminal==2 && checkHalves(uzol->right)==1){
            UZOL *temp = uzol->right->right;
            //printf("3. phase, %s\n",uzol->right->function->vectorFunction);
            free(uzol->right);
            uzol->right = temp;
            uzol->skipRight++;
            (*count)--;
        }
        if (uzol->left!=NULL && uzol->left->terminal == 2) {
            removeRedundantElements(uzol->left, count);
        }


        if (uzol->right!=NULL && uzol->right->terminal == 2) {
            removeRedundantElements(uzol->right, count);
        }
    }
}

int BDD_reduce(BDD *bdd){                       //redukcia je rozdelena na tri fazy: terminaly, TYP S, a TYP I
    if(bdd->root->terminal==1 || bdd->root->terminal==0){       //vynimka pre cisto nulovu/jednotkovu funkciu
        return 0;
    }
    int oldSize = bdd->sizeOfDiagram;
    int newSize;
    if(bdd->root==NULL){
        return -1;
    }
    mergeTerminals(bdd);                                                                //zredukuje pocet terminalov na 2
    bdd->sizeOfDiagram+=2;
    //printf("post terminal reduction number of things: %d\n",bdd->sizeOfDiagram);
    mergeDuplicates(bdd->root,&bdd->sizeOfDiagram);                                     //odstrani jeden z dvoch childov ak ma parent vektor s rovnakymi polovicami
    //printf("post duplicate merge reduction number of things: %d\n",bdd->sizeOfDiagram);
    removeRedundantElements(bdd->root, &bdd->sizeOfDiagram);                            //preskoci/skipne nepotrebny uzol, ktory ukazuje obomi pointermi na rovnaky uzol
    //printf("post duplicate removal number of things: %d\n",bdd->sizeOfDiagram);
    newSize=bdd->sizeOfDiagram;
    return (oldSize-newSize);
}

BDD *BDD_create(BF *bfunkcia){                      //vytvori bdd pre danu funkciu
    if(isBFRedundant(bfunkcia)==1){     //vynimka pre funkciu cisto nulovu/jednotkovu funkciu
        UZOL *root;
        if(bfunkcia->vectorFunction[0]=='0'){
            root = createNewTerminal(0);
        }
        else if(bfunkcia->vectorFunction[0]=='1'){
            root = createNewTerminal(1);
        }
        else{
            printf("error create redundant root\n");
            return NULL;
        }
        BDD *newBDD = (BDD*) malloc(sizeof(BDD));
        newBDD->root = root;
        newBDD->globalNumberOfVariables = 0;
        newBDD->sizeOfDiagram = 1;
        return newBDD;
    }
    UZOL *root = createNewElement(bfunkcia);                //alokuje a napoji root do bdd, zavola funkciu spliElements, ktora porozdeluje a vytvori uzly
    BDD *newBDD = (BDD*) malloc(sizeof(BDD));
    newBDD->root = root;
    newBDD->globalNumberOfVariables = newBDD->root->function->numOfVariables;
    newBDD->sizeOfDiagram = 1;
    splitElements(root, newBDD);
    return newBDD;
}

char BDD_use(BDD *bdd, char *vstupy){                       //vyhlada alebo pouzije dany vstup pre dany bdd, najde vystupny char
    if(bdd->root->terminal==1 || bdd->root->terminal==0){       //vynimka pre cisto nulovu/jednotkovu funkciu
        if(bdd->root->terminal==1) return '1';
        else if(bdd->root->terminal==0) return '0';
    }
    if(strlen(vstupy)>bdd->globalNumberOfVariables){        //nespravny vstup
        return '9';
    }
    UZOL *pomocnik = bdd->root;
    int i = 0;
    while(pomocnik!=NULL && pomocnik->terminal==2){         //prejde vstupy dokym nenarazi na terminal
            if(vstupy[i]=='0'){
                i+=pomocnik->skipLeft;          //ak skipujem premennu
                pomocnik = pomocnik->left;
            }
            else if(vstupy[i]=='1'){
                i+=pomocnik->skipRight;         //ak skipujem premennu
                pomocnik = pomocnik->right;
            }
            else{
                printf("nespravny vstup!\n");
                return '9';
            }
        i++;
    }
    if(pomocnik->terminal!= 1 && pomocnik->terminal!=0){
        printf("chyba\n");
    }
    if(pomocnik->terminal==1){
        return '1';
    }
    else if(pomocnik->terminal==0){
        return '0';
    }
}

char *createStringOfVariables(long int number, int numOfVariables){         //vytvori string premennych pre testovaciu funkciu
    char *str = (char*) malloc(sizeof (char)*(numOfVariables+1));
    for(int i=0;i<numOfVariables;i++){
        long int temp = (long int)pow(2,numOfVariables-i-1);
        if(number>=temp){
            number-=temp;
            str[i]='1';
        }
        else{
            str[i]='0';
        }
    }
    str[numOfVariables] = '\0';
    return str;
}

void testEverything(int iterations, int numOfVariables){            //pre pocet iteracii a pocet premennych spravi BDD_create a BDD_reduce, a pre vsetky kombinacie vstupov pouzije BDD_use(samozrejme aj porovna, ci vracia spravny vysledok)
    clock_t start = clock();
    float reduction, avgReduction = 0;
    for(int i=0;i<iterations;i++){
        BF *testFunction = createNewBF(createNewRandomVector(numOfVariables),numOfVariables);
        BDD *bdd = BDD_create(testFunction);
        int oldSize = bdd->sizeOfDiagram;
        reduction = (float)BDD_reduce(bdd)/(float)oldSize;
        avgReduction += reduction;
        long int size = (long int)pow(2,numOfVariables);
        for(long int j=0;j<size;j++){
            char *str = createStringOfVariables(j, numOfVariables);
            char testReduced = BDD_use(bdd,str);
            if(testReduced!=testFunction->vectorFunction[j]){
                printf("problem right: %c   found: %c\n", testFunction->vectorFunction[j], testReduced);
            }
        }
        freeBDD(bdd);
    }
    clock_t end = clock();
    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    printf("test took %f seconds\n",seconds);
    printf("average reduction: %.3f%%",(avgReduction/(float)iterations)*100);
}

int main() {
    srand(time(0));
    testEverything(2000,13);

    return 0;
}




