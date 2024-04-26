#include<iostream>
using namespace std;

class Stack{
    private:
    int array[10000];
    int size=0;
    public:
    void isempty(){
        if(size==0){
            std::cout<<"1\n";
        }
        else{
            std::cout<<"0\n";
        }
    }
    
    void Size(){
        std::cout<<this->size<<"\n";
    }
    
    void peek(){
        if(size==0){
            std::cout<<"-1\n";
        }
        else{
            std::cout<<this->array[size]<<"\n";
        }
    }
    
    void Pop(){
        if(size==0){
            std::cout<<"stack is empty\n";
        }
        else{
            this->array[size--]=0;
        }
    }
    
    void Push(){
        int value;
        std::cin>>value;
        this->array[++size]=value;
    }
    
    
};

int main(){
    int n;
    std::cin>>n;
    std::string s;
    Stack stack;
    while(n--){
        std::cin>>s;
        if(s=="push"){
            stack.Push();
        }
        else if(s=="pop"){
            stack.Pop();
        }
        else if(s=="peek"){
            stack.peek();
        }
        else if(s=="size"){
            stack.Size();
        }
        else if(s=="isempty"){
            stack.isempty();
        }
        
        
    }
    return 0;
}