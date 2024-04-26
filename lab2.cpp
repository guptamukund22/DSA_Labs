#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#include<cassert>
//#include"interface_template.h"
using namespace std;

class StudentRecord {
private:
    string studentName;
    string rollNumber;

public:
    string get_studentName() {
        return studentName;
    }
    void set_studentName(string Name) {
        studentName = Name;
    }
    string get_rollNumber() {
        return rollNumber;
    }
    void set_rollNumber(string rollnum) {
        rollNumber = rollnum;
    }
};

class Node {
private:
    Node* next;
    StudentRecord* element;

public:
    Node() {
        this->next = nullptr;
        this->element = nullptr;
    }
    Node* get_next() {
        return next;
    }
    StudentRecord* get_element() {
        return element;
    }
    void set_next(Node* value) {
        next = value;
    }
    void set_element(StudentRecord* student) {
        element = student;
    }
};

class Entity {
private:
    string name;
    Node* iterator;

public:
    Entity() {
        iterator = nullptr;
    }
    string get_name() {
        return name;
    }
    void set_name(string Name) {
        name = Name;
    }
    Node* get_iterator() {
        return iterator;
    }
    void set_iterator(Node* iter) {
        iterator = iter;
    }
};

class LinkedList : public Entity {
public:
    void add_student(StudentRecord student) {
        Node* newStudentNode = new Node();
        newStudentNode->set_element(new StudentRecord(student));
        newStudentNode->set_next(nullptr);

        if (!get_iterator()) {
            set_iterator(newStudentNode);
        } else {
            Node* temp = get_iterator();
            while (temp->get_next()) {
                temp = temp->get_next();
            }
            temp->set_next(newStudentNode);
        }
    }

    void delete_student(string studentName) {
        Node* itr = get_iterator();
        Node* prev = nullptr;

        while (itr != nullptr) {
            if (itr->get_element()->get_studentName() == studentName) {
                if (prev != nullptr) {
                    prev->set_next(itr->get_next());
                    delete itr->get_element();
                    delete itr;
                } else {
                    Node* temp = itr->get_next();
                    delete itr->get_element();
                    delete itr;
                    set_iterator(temp);
                }
                break;
            }
            prev = itr;
            itr = itr->get_next();
        }
    }
};

vector<StudentRecord> students;
vector<LinkedList> EntityArray;

bool containStudent(StudentRecord& obj) {
    for (auto& i : students) {
        if (i.get_rollNumber() == obj.get_rollNumber() && i.get_studentName()==obj.get_studentName()) {
            return true;
        }
    }
    return false;
}

void checkLL(string& name, StudentRecord& student) {
    for (auto& i : EntityArray) {
        if (i.get_name() == name) {
            i.add_student(student);
            return;
        }
    }
    LinkedList obj;
    obj.set_name(name);
    obj.set_iterator(nullptr);
    obj.add_student(student);
    EntityArray.push_back(obj);
}

void read_input_file(string file_path) {
    ifstream tempfile(file_path);
    if (!tempfile.is_open()) {
        cerr << "Error: Could not open file." << endl;
        return;
    }

    string line;
    string name, roll, branch, course, hostel, hobby;
    string word;
    while (getline(tempfile, line)) {
        stringstream s(line);
        getline(s, name, ',');
        getline(s, roll, ',');
        StudentRecord obj;
        obj.set_studentName(name);
        obj.set_rollNumber(roll);

        if (!containStudent(obj)) {
            students.push_back(obj);
            getline(s, branch, ',');
            checkLL(branch, obj);
            getline(s,word,'[');
            getline(s,word,']');
            stringstream ss(word);
            while(getline(ss,course,',')){
                checkLL(course,obj);
            }
            getline(s,word,',');
            getline(s,hostel,',');
            checkLL(hostel,obj);
            getline(s,word,'[');
            getline(s,word,']');
            stringstream sm(word);
            while(getline(sm,hobby,',')){
                checkLL(hobby,obj);
            }
        }
    }

    tempfile.close();
}