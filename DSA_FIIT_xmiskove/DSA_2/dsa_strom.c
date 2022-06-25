#define MAXNAME 50          //max velkost pola pre meno
typedef struct person{      //struktura, ktoru pouzivam vo viacerych programoch, obsahuje meno a vek cloveka
    char name[MAXNAME];
    int age;
}PERSON;

typedef struct nodeStrom{           //struktura, s ktorou budem v tomto programe pracovat
    PERSON *pers;
    int depth;
    struct nodeStrom *left;
    struct nodeStrom *right;
}NODESTROM;

NODESTROM *createNode(char *inputName, int inputAge){                            //funkcia vytvori novy prvok, inicializuje ho
    NODESTROM *newNode = (NODESTROM*)malloc(sizeof(NODESTROM));            //alokujem miesto pre cely prvok
    PERSON *newPerson = (PERSON*)malloc(sizeof(PERSON));    //alokujem miesto pre cloveka
    newNode->pers= newPerson;
    strcpy(newNode->pers->name,inputName);
    newNode->pers->age=inputAge;
    newNode->left=NULL;
    newNode->right=NULL;
    newNode->depth=1;
    return (newNode);
}

int max(int x, int y){              //funkcia vrati maximum z danych hodnot
    if(x>y) return x;
    else return y;
}

int determinePlace(NODESTROM *tree, NODESTROM *myNode){         //funkcia nam povie, na ktoru stranu nas prvok patri (voci prvku kde sa bude vkladat)
    if(strcmp(myNode->pers->name,tree->pers->name)>0){
        return 1;       //napravo
    }
    else if(strcmp(myNode->pers->name,tree->pers->name)<0){
        return 0;       //nalavo
    }
    else if(myNode->pers->age>tree->pers->age){
        return 1;       //napravo
    }
    else if(myNode->pers->age<tree->pers->age){
        return 0;       //nalavo
    }
    else return 2;
}



void printInOrder(struct nodeStrom* root)                                                     //touto pomocnou funkciou si vypisujem
{
    if (root != NULL) {
        printInOrder(root->left);
        printf("%s   %d \n", root->pers->name, root->pers->age);
        printInOrder(root->right);
    }
}

char *randomString(int size){            //vygenerujem random string
    char pismena[] = "abcdefghijklmnopqrstuvwxyz";
    char *str = NULL;
    str = (char*)malloc(sizeof(char)*(size+1));
    for(int i=0; i<size; i++){
        str[i]=pismena[rand()%(26)];
        if(i==size-1) str[i+1]='\0';
    }
    return str;
}

NODESTROM *createRandomPerson(){             //funkcia vytvori osobu s nahodnym menom a vekom, |meno|==5, vek<50
    int age = rand()%50;
    char *name = randomString(5);
    //printf("new person %s\n", name);
    NODESTROM *randomPerson = createNode(name,age);
    return randomPerson;
}

int findDepth(NODESTROM *tree){         //funkcia vráti hodnotu hlbky stromu (niekde sa hovori aj o vyske). Je potrebne, aby pri NULL vracala 0
    if(tree == NULL){
        return 0;
    }
    return tree->depth;
}

int findBalance(NODESTROM *tree){                   //funkcia vrati balance/vyrovnanost stromu. toto je opisane v dokumentacii
    if(tree==NULL){
        return 0;
    }
    return findDepth(tree->left)-findDepth(tree->right);
}

int updateDepth(NODESTROM *tree){                   //funkcia sa vola pri zvysovani hlbky stromu, pricom sa mohli zmenit hlbky jeho vetiev
    int newDepth;
    newDepth = max(findDepth(tree->left),findDepth(tree->right)) + 1;
    return newDepth;
}

NODESTROM *rotateRight(NODESTROM *top){
    NODESTROM *node = top->left;                 //node bude presunuta na horne miesto a top bude presunuta
    NODESTROM *temp = node->right;

    node->right = top;                  //vykonanie rotacie
    top->left = temp;

    top->depth = updateDepth(top);          //sviezo vyratana hlbka prvku, pricom teba najprv top, ktory je pod node, pretoze ovlplyvnuje novu hlbku node taktiez ako svoju
    node->depth = updateDepth(node);

    return node;
}

NODESTROM *rotateLeft(NODESTROM *top){                //rovnake ako rotateRight, pricom sa rotacia vykona do opacneho smeru
    NODESTROM *node = top->right;
    NODESTROM *temp = node->left;

    node->left = top;                   //vykonanie rotacie
    top->right = temp;

    top->depth = updateDepth(top);
    node->depth = updateDepth(node);

    return node;
}

NODESTROM *avlInsertNode(NODESTROM *tree,NODESTROM *myNode){
    int balance;
    if(tree==NULL){                                         //klasicky insert do stromu
        return myNode;
    }
    if (determinePlace(tree, myNode)==1){                   //ak patri napravo
        tree->right = avlInsertNode(tree->right, myNode);
    }
    else if (determinePlace(tree, myNode)==0){                  //ak patri nalavo
        tree->left = avlInsertNode(tree->left, myNode);
    }
    else return tree;
    tree->depth = updateDepth(tree);                            //aktualizujem hlbku prvku
    balance = findBalance(tree);                                //zistim ci je strom v rovnovahe
    //printf("balance tree name: %s   balance: %d    \n", tree->pers->name, balance);

        //rotacie su podrobne opisane v dokumentacii
    if(balance > 1 && (strcmp(myNode->pers->name,tree->left->pers->name)<0)){                                    // left left rotacia
        //printf("LL rotate\n");
        return rotateRight(tree);
    }
    if(balance > 1 && (strcmp(myNode->pers->name,tree->left->pers->name)>0)){                                    // left right rotacia
        //printf("LR rotate!!!!!!!!!!!!!!\n");
        tree->left = rotateLeft(tree->left);
        return rotateRight(tree);
    }
    if(balance < -1 && (strcmp(myNode->pers->name,tree->right->pers->name)>0)){                                    // right right rotacia
        //printf("RR rotate\n");
        return rotateLeft(tree);
    }
    if(balance < -1 && (strcmp(myNode->pers->name,tree->right->pers->name)<0)){                                    // right left rotacia
        //printf("RL rotate!!!!!!!!!!!!!!!!\n");
        tree->right = rotateRight(tree->right);
        return rotateLeft(tree);
    }

    return tree;
}

NODESTROM* avlSearch(NODESTROM *tree, char *name, int age){     //klasicke vyhladavanie v binarnom strome rekurziou
    if(tree==NULL){
        return NULL;
    }
    else if(strcmp(name,tree->pers->name)<0){
        avlSearch(tree->left,name,age);
    }
    else if(strcmp(name,tree->pers->name)>0){
        avlSearch(tree->right,name,age);
    }
    else if(age<tree->pers->age){
        avlSearch(tree->left,name,age);
    }
    else if(age>tree->pers->age){
        avlSearch(tree->right,name,age);
    }
    else if(age == tree->pers->age && strcmp(name,tree->pers->name) == 0){
        //printf("\nnasiel sa %s,  %d\n",tree->pers->name, tree->pers->age);
        return tree;
    }
    //printf("\nnebolo najdene\n");
    return NULL;
}

int findMaxPossibleDepth(int n){                 //vrati najvyssiu moznu hlbku AVL stromu s danym n prvkov
    float multi = 1.44;
    float myLog = log(n)/log(2);
    return (int)(1.44*myLog);
}

NODESTROM *testInsertStrom(long int num, NODESTROM *root){          //testovacia funkcia pre vkladanie
    clock_t start = clock();
    for(long int i=0;i<num;i++){
        root = avlInsertNode(root,createRandomPerson());
    }
    clock_t end = clock();
    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    printf("the insertion of %li nodes took %f seconds\n",num,seconds);
    return root;
}

void testSearchStrom(long int num, NODESTROM *root){                //testovacia funkcia pre vyhladavanie
    clock_t start = clock();
    for(long int i=0;i<num;i++){
        avlSearch(root, randomString(5), (rand()%50));
    }
    clock_t end = clock();
    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    printf("the search of %li nodes took %f seconds\n",num,seconds);
}

void fullTestStrom(long int iterations){                        //spojenie testovacich funkcii do jednej
    NODESTROM *root = createNode("havko",10);
    root = testInsertStrom(iterations,root);
    testSearchStrom(iterations,root);
    printf("\n");
}

