#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <set>
#include <fstream>
#include <sstream>
#include <map>
#include<cassert>
using namespace std;

class PhoneRecord {
private:
    string name;
    string organisation;
    vector<string> phoneNumbers;
public:
    int count;
public:
    PhoneRecord(const string& n, const string& org, const vector<string>& numbers)
        : name(n), organisation(org), phoneNumbers(numbers) , count(0){}

    string getName() const {
        return name;
    }

    string getOrganisation() const {
        return organisation;
    }

    vector<string> getPhoneNumbers() const {
        return phoneNumbers;
    }
};

class HashTableRecord {
private:
    int key;
    PhoneRecord* element; 
    HashTableRecord* next;

public:
    HashTableRecord(int k, PhoneRecord* rec)
        : key(k), element(rec), next(nullptr) {}

    int getKey() const {
        return key;
    }

    PhoneRecord* getRecord() const {
        return element;
    }

    HashTableRecord* getNext() const {
        return next;
    }

    void setNext(HashTableRecord* nxt) {
        next = nxt;
    }
};

long long power(int x,int i){
        if(i==1 || i==0){
            return 1;
        }

        long long temp=power(x,i/2);

        if(i%2==0){
            return (temp*temp)%1000000007;
        }
        else{
            return (temp*temp*x)%1000000007;
        }
}

class PhoneBook {
private:
    static const int HASH_TABLE_SIZE = 263;
    HashTableRecord* hashTable[HASH_TABLE_SIZE];

public:
    PhoneBook() {
        for (int i = 0; i < HASH_TABLE_SIZE; ++i) {
            hashTable[i] = nullptr;
        }
    }

    long long computeHash(const string& str){
        int length=str.length();
        long long ans=0;
        for(int i=0;i<length;i++){
            ans=(ans%263 + (((str[i]%1000000007) * power(263,i))%1000000007)%263)%263;
        }
        return ans;
    }

    void addContact(PhoneRecord* record){
        string name=record->getName();
        stringstream s(name);
        string part;
        while(getline(s,part,' ')){
            long long index = computeHash(part);
            HashTableRecord *ob = new HashTableRecord(index,record);
            if(hashTable[index] == nullptr){
                hashTable[index] = ob;
                (record->count)++;
            }
            else{
                HashTableRecord *temp = hashTable[index];
                while(temp->getNext()!=nullptr){
                        temp=temp->getNext();
                }
                temp->setNext(new HashTableRecord(int(index),record));
                record->count+=1;
            }
        }
    }


    vector<PhoneRecord*> fetchContacts(string* query) {
    map<PhoneRecord*, int> recordCount;
    stringstream s(*query);
    string word;
    while (getline(s, word, ' ')) {
        long long index = computeHash(word);
        HashTableRecord* record = hashTable[index];
        while (record != nullptr) {
            PhoneRecord* phoneRecord = record->getRecord();
            string recordName = phoneRecord->getName();
            if(recordName == * query){
                recordCount[phoneRecord] +=100;
            }
            else if (recordName.find(word) != string::npos) {
                recordCount[phoneRecord]++;
            }

            record = record->getNext();
        }
    }

    vector<pair<PhoneRecord*, int>> recordsWithCount;
    
    for (const auto& entry : recordCount) {
        recordsWithCount.push_back(entry);
    }

    sort(recordsWithCount.begin(), recordsWithCount.end(),
         [](const pair<PhoneRecord*, int>& a, const pair<PhoneRecord*, int>& b) {
             return a.second > b.second;
         });

    vector<PhoneRecord*> result;

    for (const auto& entry : recordsWithCount) {
        PhoneRecord* phoneRecord = entry.first;
        result.push_back(phoneRecord);
    }
    return result;
}

    bool deleteContact(const string* searchName) {
       
        string str  = *searchName;
        vector<PhoneRecord*> contact = fetchContacts(&str);
        string name = contact[0] -> getName() + " ";
        
        if(contact.empty())
         return false;
        else{
        PhoneRecord *ob = contact[0];
        string word = "";
        for(int i  = 0;i<name.size();i++){
            if(name[i] == ' ')
             {
                
                int KEY = computeHash(word);
                
                HashTableRecord *current = hashTable[KEY];            
               if (current && (current -> getRecord() -> getName()) == ob -> getName()) {
                   
                   HashTableRecord *node = current;
                   current = current -> getNext();
                 hashTable[KEY] = current;
                   delete node;
                   word  = "";
                   continue;
                   
               }
               
               HashTableRecord* prev = nullptr;
               
               while (current && (current->getRecord() -> getName()) != ob -> getName()) {
               
                   prev = current;
                   
                   current = current->getNext();
               }
               if (current == nullptr) {
                   return false;
               }
               //cout << current -> getRecord() -> getName() << " ";
               prev -> setNext(current -> getNext());
               //cout << prev -> getNext() -> getRecord() -> getName();

               delete current;
             //deletion complete
               word  = "";
                
 }

             else{
                word = word + name[i];
             }
        }

      return true;

        }
     return true;
        
    }


    int countRecordsPointingTo(PhoneRecord* record){
        return record->count;
    };

    void readRecordsFromFile(const string& filename){
        ifstream tempfile(filename);
        
        if(!tempfile.is_open()){
            cerr<<"Error: Could not open file"<<endl;
            return;
        }
        string line;
        string name,organization;
        vector<string> number;
        string word;
        while(getline(tempfile,line)){
            stringstream s(line);
            getline(s,name,',');
            while(getline(s,word,',')){
                if(word[0]>='a' && word[0]<='z' || word[0]>='A' && word[0]<='Z' ){
                    break;
                }
                number.push_back(word);
            }
            organization=word;
            PhoneRecord * temp = new PhoneRecord(name,organization,number);
            addContact(temp);
        }
       
    }

    // ~PhoneBook(){
    //     ;
    // }

};