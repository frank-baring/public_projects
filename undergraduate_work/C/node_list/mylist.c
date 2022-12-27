#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "mylist.h"

struct Node *addFront(struct List *list, void *data)
{
        // Creating node to hold given data pointer
        struct Node *ptr = list->head;
        struct Node *newNode = malloc(sizeof(struct Node));
        if (!newNode) {
        	free(newNode);
        	return NULL;
        } 
        // Assigning data
        newNode->data = data;
        // Adding node to the front of the list
        newNode->next = ptr;
        list->head = newNode;
         
        return newNode;
}

void traverseList(struct List *list, void (*f)(void *))
{
        struct Node *ptr = list->head;
        // Traversing the list
        while(ptr){
        	// Calling f() with each data item
	        f(ptr->data);
        	ptr = ptr->next;
        }
}

void flipSignDouble(void *data)
{
        double tmp = *(double*)data;
        // Taking the value pointed to by 'data'
        // and multiplying it by -1
        tmp = tmp * -1;
        // Putting the result back into the memory location
        *(double*)data = tmp;
}

int compareDouble(const void *data1, const void *data2) 
{
        // Comparing two double values pointed to by the two pointers
        double x = *(double *)data1;
        double y = *(double *)data2;
        // Returning 0 if they are the same value, 1 otherwise
        if (x == y) 
           	return 0; 
        else 
        	return 1;   
}

struct Node *findNode(struct List *list, const void *dataSought,
        int (*compar)(const void *, const void *))
{
        struct Node *nu = list->head;
        // Traversing the list
        // comparing each data item with 'dataSought'
        // using the 'compar' function
        while(nu){
        	if(compar(nu->data, dataSought))
            		nu = nu->next;
        		// This will ensure the first node with matching data is returned
        else 
            break;
        }
        // If no node with matching data can be found, nu will be set
        // to NULL(the stopper value at the end of the list) and then returned,
        // just as requested in the lab instructions. 
        return nu;
}

void *popFront(struct List *list)
{
        // Removing the first node from the list
        if(list->head){
        	struct Node *ptr = list->head;
        	list->head = list->head->next;
        	void *t = ptr->data;
        	// Deallocating the memory for the node
        	free(ptr);
        	// Returning the 'data' pointer that was stored in the node
        	return t;
        }else {
        	// Returning NULL if the list is empty
        	return NULL;
        }        
}

void removeAllNodes(struct List *list)
{
        // Removing all the nodes from the list
        // and deallocating the memory for the nodes
        struct Node *ptr;
        while(list->head){
        	ptr = list->head;
        	list->head = list->head->next;
        	free(ptr); 
        }  
}

struct Node *addAfter(struct List *list,
        struct Node *prevNode, void *data)
{
        // Creating a node that holds the given data pointer
        struct Node *newNode = malloc(sizeof(struct Node));
        // Returning NULL on failure
        if (!newNode) {
        	free(newNode);
            	return NULL;
        }
        // Adding the node right after the node passed in as the
        // 'prevNode' parameter
        newNode->data = data;
        if(prevNode){
        	newNode->next = prevNode->next;
        	prevNode->next = newNode;
        // If 'prevNode' is NULL then this function behaves like
        // addFront()
        }else {
        	newNode->next = NULL;
        	list->head = newNode; 
        } 
        // Returning newly created node on success
        return newNode;
}

void reverseList(struct List *list)
{
        // Creating 3 consecutive pointers to be moved along the list
        struct Node *prv = NULL;
        struct Node *cur = list->head;
        struct Node *nxt;

        // Reversing the list by manipulating the pointers.
        // Essentially reversing the 'direction' of the list
        while (cur) {
	        nxt = cur->next;
       		cur->next = prv;
       		prv = cur;
        	cur = nxt;
        }        
        // Assigning prv to list->head
        list->head = prv;
}
