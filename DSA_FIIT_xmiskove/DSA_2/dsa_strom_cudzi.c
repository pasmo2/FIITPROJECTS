//kod zo stranky https://www.codesdope.com/course/data-structures-red-black-trees-insertion/

enum COLOR {Red, Black};

typedef struct tree_node {          //struktura prvku ktory sa tu bude pouzivat
    int age;
    char name[50];
    struct tree_node *right;
    struct tree_node *left;
    struct tree_node *parent;
    enum COLOR color;
}tree_node;

typedef struct red_black_tree {         //struktura zaciatku stromu
    tree_node *root;
    tree_node *NIL;
}red_black_tree;

char *randomStringStromCudzi(int size){            //vygeneruje random string pismen
    char pismena[] = "abcdefghijklmnopqrstuvwxyz";
    char *str = NULL;
    str = (char*)malloc(sizeof(char)*(size+1));
    for(int i=0; i<size; i++){
        str[i]=pismena[rand()%(26)];
        if(i==size-1) str[i+1]='\0';
    }
    return str;
}

int randomNumberStromCudzi(int max){            //vygeneruje random cislo
    return (rand() % max);
}

int determinePlaceStromCudzi(tree_node *tree, tree_node *myNode){       //funkcia zisti, na ktoru stranu nas prvok patri
    if(strcmp(myNode->name,tree->name)>0){
        return 1;
    }
    else if(strcmp(myNode->name,tree->name)<0){
        return 0;
    }
    else if(myNode->age>tree->age){
        return 1;
    }
    else if(myNode->age<tree->age){
        return 0;
    }
    else return 1;
}

tree_node* new_tree_node(int age) {             //funkcia inicializuje a vytvori novy prvok
    tree_node* n = malloc(sizeof(tree_node));
    n->left = NULL;
    n->right = NULL;
    n->parent = NULL;
    n->age = age;
    n->color = Red;
    strcpy(n->name,randomStringStromCudzi(5));
    return n;
}

red_black_tree* new_red_black_tree() {          //funkcia inicializuje a vytvory novy strom
    red_black_tree *t = malloc(sizeof(red_black_tree));
    tree_node *nil_node = malloc(sizeof(tree_node));
    nil_node->left = NULL;
    nil_node->right = NULL;
    nil_node->parent = NULL;
    nil_node->color = Black;
    nil_node->age = 0;
    t->NIL = nil_node;
    t->root = t->NIL;

    return t;
}

void left_rotate(red_black_tree *t, tree_node *x) {         //rotacia vlavo, rovnaky princip ako pri avl strome
    tree_node *y = x->right;
    x->right = y->left;
    if(y->left != t->NIL) {
        y->left->parent = x;
    }
    y->parent = x->parent;
    if(x->parent == t->NIL) { //x is root
        t->root = y;
    }
    else if(x == x->parent->left) { //x is left child
        x->parent->left = y;
    }
    else { //x is right child
        x->parent->right = y;
    }
    y->left = x;
    x->parent = y;
}

void right_rotate(red_black_tree *t, tree_node *x) {            //rotacia vpravo, rovnaky princip ako pri avl strome
    tree_node *y = x->left;
    x->left = y->right;
    if(y->right != t->NIL) {
        y->right->parent = x;
    }
    y->parent = x->parent;
    if(x->parent == t->NIL) { //x is root
        t->root = y;
    }
    else if(x == x->parent->right) { //x is left child
        x->parent->right = y;
    }
    else { //x is right child
        x->parent->left = y;
    }
    y->right = x;
    x->parent = y;
}

void insertion_fixup(red_black_tree *t, tree_node *z) {             //funkcia na napravenie porusenych pravidiel Red Black stromu, ako je opisane v dokumentacii
    while(z->parent->color == Red) {
        if(z->parent == z->parent->parent->left) { //z.parent is the left child

            tree_node *y = z->parent->parent->right; //uncle of z

            if(y->color == Red) { //case 1
                z->parent->color = Black;
                y->color = Black;
                z->parent->parent->color = Red;
                z = z->parent->parent;
            }
            else { //case2 or case3
                if(z == z->parent->right) { //case2
                    z = z->parent; //marked z.parent as new z
                    left_rotate(t, z);
                }
                //case3
                z->parent->color = Black; //made parent black
                z->parent->parent->color = Red; //made parent red
                right_rotate(t, z->parent->parent);
            }
        }
        else { //z.parent is the right child
            tree_node *y = z->parent->parent->left; //uncle of z

            if(y->color == Red) {
                z->parent->color = Black;
                y->color = Black;
                z->parent->parent->color = Red;
                z = z->parent->parent;
            }
            else {
                if(z == z->parent->left) {
                    z = z->parent; //marked z.parent as new z
                    right_rotate(t, z);
                }
                z->parent->color = Black; //made parent black
                z->parent->parent->color = Red; //made parent red
                left_rotate(t, z->parent->parent);
            }
        }
    }
    t->root->color = Black;
}

void insertStromCudzi(red_black_tree *t, tree_node *z) {                    //funkcia na vlozenie prvku do stromu, je dost mozne ze porusi pravidla ktore opravi insertion_fixup()
    tree_node* y = t->NIL; //variable for the parent of the added node
    tree_node* temp = t->root;
    while(temp != t->NIL) {
        y = temp;
        if(determinePlaceStromCudzi(temp,z)==0){
            temp = temp->left;
        }
        else{
            temp = temp->right;
        }
    }
    z->parent = y;

    if(y == t->NIL) { //newly added node is root
        t->root = z;
    }
    else if(z->age < y->age) //age of child is less than its parent, left child
        y->left = z;
    else
        y->right = z;

    z->right = t->NIL;
    z->left = t->NIL;

    insertion_fixup(t, z);
}

void inorderStromCudzi(red_black_tree *t, tree_node *n) {           //pomocna funkcia pre vypis stromu
    if(n != t->NIL) {
        inorderStromCudzi(t, n->left);
        printf("%d\n", n->age);
        inorderStromCudzi(t, n->right);
    }
}

tree_node* searchStromCudzi(tree_node *t,char *name, int age){          //funkcia na vyhladanie prvku v strome, rovnaky princip ako pri normalnych binarnych stromoch
    tree_node* temp = t;
    if(temp==NULL){
        return NULL;
    }
    else if(strcmp(name,temp->name)<0){     //patri vlavo
        searchStromCudzi(temp->left,name,age);
    }
    else if(strcmp(name,temp->name)>0){         //patri vpravo
        searchStromCudzi(temp->right,name,age);
    }
    else if(age<temp->age){             //patri vlavo
        searchStromCudzi(temp->left,name,age);
    }
    else if(age>temp->age){             //patri vpravo
        searchStromCudzi(temp->right,name,age);
    }
    else if(age == temp->age && strcmp(name,temp->name) == 0){
        //printf("\nnasiel sa %s,  %d\n",temp->name, temp->age);
        return temp;
    }
    return NULL;
}

void testSearchStromCudzi(long int num, red_black_tree *t){     //testovacia funkcia pre vyhladavanie
    clock_t start = clock();
    for(long int i=0;i<num;i++){
        searchStromCudzi(t->root,randomStringStromCudzi(5),randomNumberStromCudzi(50));
    }
    clock_t end = clock();
    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    printf("the search of %li nodes took %f seconds\n",num,seconds);
}

void testInsertStromCudzi(long int num, red_black_tree *t){         //testovacia funkcia pre vkladanie prvkov
    clock_t start = clock();
    for(long int i=0;i<num;i++){
        tree_node *newNode = new_tree_node(randomNumberStromCudzi(50));
        insertStromCudzi(t, newNode);
    }
    clock_t end = clock();
    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    printf("the insertion of %li nodes took %f seconds\n",num,seconds);
}

void fullTestStromCudzi(long int iterations){           //testovacia funkcia, ktora spaja vkladanie a vyhladavanie
    red_black_tree *t = new_red_black_tree();
    testInsertStromCudzi(iterations,t);
    testSearchStromCudzi(iterations,t);
    printf("\n");
}

