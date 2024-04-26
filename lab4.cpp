#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <cassert>
#include <bits/stdc++.h> 
#include <algorithm>
using namespace std;
class Vehicle;

class Trip {
public:
    Trip(Vehicle* vehicle, std::string pick_up_location, std::string drop_location, int departure_time)
        : vehicle(vehicle), pick_up_location(pick_up_location), drop_location(drop_location), departure_time(departure_time), booked_seats(0) {}

    // Getter functions
    Vehicle* getVehicle() const {
        return vehicle;
    }

    std::string getPickUpLocation() const {
        return pick_up_location;
    }

    std::string getDropLocation() const {
        return drop_location;
    }

    int getDepartureTime() const {
        return departure_time;
    }

    int getBookedSeats() const {
        return booked_seats;
    }

    // Setter functions
    void setVehicle(Vehicle* v) {
        vehicle = v;
    }

    void setPickUpLocation(std::string location) {
        pick_up_location = location;
    }

    void setDropLocation(std::string location) {
        drop_location = location;
    }

    void setDepartureTime(int time) {
        departure_time = time;
    }

    void setBookedSeats(int seats) {
        booked_seats = seats;
    }

private:
    Vehicle* vehicle;
    std::string pick_up_location;
    std::string drop_location;
    int departure_time;
    int booked_seats;
};


class BinaryTreeNode {
public:
    BinaryTreeNode(int departuretime = 0, Trip* tripenodeptr = nullptr, BinaryTreeNode* parentptr = nullptr)
        : leftptr(nullptr), rightptr(nullptr), parentptr(parentptr), departuretime(departuretime), tripnodeptr(tripenodeptr) {}

    // Getter functions
    BinaryTreeNode* getLeftPtr() const {
        return leftptr;
    }

    BinaryTreeNode* getRightPtr() const {
        return rightptr;
    }

    BinaryTreeNode* getParentPtr() const {
        return parentptr;
    }

    int getDepartureTime() const {
        return departuretime;
    }

    Trip* getTripNodePtr() const {
        return tripnodeptr;
    }

    void setLeftPtr(BinaryTreeNode* left) {
        leftptr = left;
    }

    void setRightPtr(BinaryTreeNode* right) {
        rightptr = right;
    }

    void setParentPtr(BinaryTreeNode* parent) {
        parentptr = parent;
    }

    void setDepartureTime(int time) {
        departuretime = time;
    }

    void setTripNodePtr(Trip* trip) {
        tripnodeptr = trip;
    }

    void addTripNodePtr(Trip * trip){
        if(departuretime>trip->getDepartureTime()){
            if(leftptr==nullptr){
                leftptr=new BinaryTreeNode(trip->getDepartureTime(),trip,this);
                return;
            }
            else{
            leftptr->addTripNodePtr(trip);
            }
        }
        else{
            if(rightptr==nullptr){
                rightptr = new BinaryTreeNode(trip->getDepartureTime(),trip,this);
                return;
            }
            else{
                rightptr->addTripNodePtr(trip);
            }
        }
    }


    vector<Trip*> showTrip(int after,int before,vector<Trip *>&ans){
        if(after<this->departuretime && this->departuretime<before && this!=nullptr){
            ans.push_back(this->tripnodeptr);
        }
        if(this->rightptr!=nullptr && after<this->rightptr->departuretime<before){
            this->rightptr->showTrip(after,before,ans);
        }
        if(this->leftptr!=nullptr && after<this->leftptr->departuretime<before){
            this->leftptr->showTrip(after,before,ans);
        }
        return ans;
    }

    BinaryTreeNode * findNode(int departure){
        if(this==nullptr){
            return nullptr;
        }
        if(this->departuretime==departure){
            return this;
        }
        else if(this->departuretime>departure){
            this->leftptr->findNode(departure);
        }
        else if(this->departuretime<departure){
            this->rightptr->findNode(departure);
        }
        return nullptr;
    }


private:
    BinaryTreeNode* leftptr;
    BinaryTreeNode* rightptr;
    BinaryTreeNode* parentptr;
    int departuretime;
    Trip* tripnodeptr;
};

class Vehicle {
public:
    Vehicle(std::string vehicle_number, int seating_capacity)
        : vehicle_number(vehicle_number), seating_capacity(seating_capacity) {}

    std::string getVehicleNumber() {
        return vehicle_number;
    }

    int getSeatingCapacity() const {
        return seating_capacity;
    }

    // Setter functions
    void setVehicleNumber(std::string number) {
        vehicle_number = number;
    }

    void setSeatingCapacity(int capacity) {
        seating_capacity = capacity;
    }

    void addTrip(Trip* trip) {
        trips.push_back(trip);
    }

    vector<Trip *> getTrips(){
        return trips;
    }

private:
    std::string vehicle_number;
    int seating_capacity;
    std::vector<Trip*> trips;
};

class TransportService {
public:
    TransportService(std::string name) : name(name), BSThead(nullptr) {}

    std::string getName() const {
        return name;
    }

    BinaryTreeNode* getBSTHead() const {
        return BSThead;
    }

    void setName(std::string service_name) {
        name = service_name;
    }

    void setBSTHead(BinaryTreeNode* node) {
        BSThead = node;
    }
    
    void addTrip(int key, Trip* trip){
        if(BSThead==nullptr){
            BSThead = new BinaryTreeNode(key,trip);
        }
        else{
            BSThead->addTripNodePtr(trip);
        }
    }

    BinaryTreeNode* getSuccessorNode(BinaryTreeNode *bt) {
    if (bt->getRightPtr() != nullptr) {
        BinaryTreeNode* successor = bt->getRightPtr();
        while (successor->getLeftPtr() != nullptr) {
            successor = successor->getLeftPtr();
        }
        return successor;
    }
    BinaryTreeNode* current = bt;
    BinaryTreeNode* parent =bt->getParentPtr();

    while (parent != nullptr && current == parent->getRightPtr()) {
        current = parent;
        parent = parent->getParentPtr();
    }

    return parent;
}

    void deleteNode(BinaryTreeNode * bt) {
    if (bt->getRightPtr() == nullptr && bt->getLeftPtr() == nullptr) {
        delete bt->getTripNodePtr()->getVehicle();
        delete bt->getTripNodePtr();
        delete bt;
    } else if (bt->getRightPtr() == nullptr || bt->getLeftPtr() == nullptr) {
        BinaryTreeNode* nonNullChild = (bt->getLeftPtr()!= nullptr) ? bt->getLeftPtr() : bt->getRightPtr();
        if (bt->getParentPtr() != nullptr) {
            if (bt->getParentPtr()->getLeftPtr() == bt) {
                bt->getParentPtr()->setLeftPtr(nonNullChild);
            } else {
                bt->getParentPtr()->setRightPtr(nonNullChild);
            }
            nonNullChild->setParentPtr(bt->getParentPtr());
        } else {
             this->setBSTHead(nonNullChild);
        }
        delete bt->getTripNodePtr()->getVehicle();
        delete bt->getTripNodePtr();
        delete bt;
    } else {
        BinaryTreeNode* successor = this->getSuccessorNode(bt);
        bt->setTripNodePtr(successor->getTripNodePtr());
        this->deleteNode(successor);
    }
}
   
private:
    std::string name;
    BinaryTreeNode* BSThead;
};


class Location {
public:
    Location(std::string name) : name(name) {}

    std::string getName() const {
        return name;
    }

    TransportService* getServicePtr(std::string droplocation) const {
            if(serviceptrs.empty()){
                return nullptr;
            }
            for(int i=0;i<serviceptrs.size();i++){
                if((serviceptrs.at(i)->getName()==droplocation)){
                    return (serviceptrs.at(i));
                }
            }
            return nullptr;
    }

    void setName(std::string location_name) {
        name = location_name;
    }

    TransportService* setServicePtr(std::string droplocation) {
        TransportService * ts = new TransportService(droplocation);
        serviceptrs.push_back(ts);
        return serviceptrs.back();
    }

    void addTrip(Trip* trip) {
        trips.push_back(trip);
    }

    vector<Trip *> showTrip(int after,int before){
        vector<Trip *> ans;
        for(int i=0;i<serviceptrs.size();i++){
            ans=serviceptrs.at(i)->getBSTHead()->showTrip(after,before,ans);
        }
        return ans;
    }


private:
    std::string name;
    std::vector<TransportService* >serviceptrs;
    std::vector<Trip*> trips;
};

int height(BinaryTreeNode *bt){
    if(bt==nullptr){
        return -1;
    }
    else{
        int l=height(bt->getLeftPtr());
        int r=height(bt->getRightPtr());
        return 1+max(l,r);
    }
}

int countNodes(BinaryTreeNode* node) {
    if (node == nullptr) {
        return 0;
    } else {
        int leftCount = countNodes(node->getLeftPtr());
        int rightCount = countNodes(node->getRightPtr());
        return 1 + leftCount + rightCount;
    }
}


class BinaryTree {
protected:
    BinaryTreeNode* root;

public:
    BinaryTree() : root(nullptr) {}

    int getHeight() const {
        return height(root);
    }

    int getNumberOfNodes() const {
        return countNodes(root);
    }
};

class BinarySearchTree : public BinaryTree {
public:
    BinarySearchTree() {}

    BinaryTreeNode* getElementWithMinimumKey() const {
        BinaryTreeNode * ans=root;
        while(ans->getLeftPtr()!=nullptr && root!=nullptr){
            ans = ans->getLeftPtr();
        }
        return ans;
    }

    BinaryTreeNode* getElementWithMaximumKey() const {
         BinaryTreeNode * ans=root;
        while(ans->getRightPtr()!=nullptr && root!=nullptr){
            ans = ans->getRightPtr();
        }
        return ans;
    }

    BinaryTreeNode* searchNodeWithKey(int key) const {
    BinaryTreeNode* current = root;
    BinaryTreeNode* successor = nullptr;

    while (current != nullptr) {
        if (key == current->getDepartureTime()) {
            return current; 
        } else if (key < current->getDepartureTime()) {
            successor = current; 
            current = current->getLeftPtr();
        } else {
            current = current->getRightPtr(); 
        }
    }

    return successor;
}


    BinaryTreeNode* getSuccessorNode(BinaryTreeNode* node) const {
    if (node == nullptr) {
        return nullptr;
    }

    if (node->getRightPtr() != nullptr) {
        BinaryTreeNode * ans=node;
        while(ans->getRightPtr()!=nullptr && node!=nullptr){
            ans = ans->getRightPtr();
        }
        return ans;
    }

    BinaryTreeNode* successor = nullptr;
    BinaryTreeNode* current = root;

    while (current != nullptr) {
        if (node->getDepartureTime() < current->getDepartureTime()) {
            successor = current;
            current = current->getLeftPtr();
        } else if (node->getDepartureTime() > current->getDepartureTime()) {
            current = current->getRightPtr();
        } else {
            break;
        }
    }

    return successor;
}


    BinaryTreeNode* getSuccessorNodeByKey(int key) const {
    BinaryTreeNode* node = searchNodeWithKey(key);
    return getSuccessorNode(node);
}


    BinaryTreeNode* getPredecessorNode(BinaryTreeNode* node) const {
    if (node == nullptr) {
        return nullptr;
    }

    if (node->getLeftPtr() != nullptr) {
        BinaryTreeNode* predecessor = node->getLeftPtr();
        while (predecessor->getRightPtr() != nullptr) {
            predecessor = predecessor->getRightPtr();
        }
        return predecessor;
    }

    BinaryTreeNode* predecessor = nullptr;
    BinaryTreeNode* current = root;

    while (current != nullptr) {
        if (node->getDepartureTime() > current->getDepartureTime()) {
            predecessor = current;
            current = current->getRightPtr();
        } else if (node->getDepartureTime() < current->getDepartureTime()) {
            current = current->getLeftPtr();
        } else {
            break;
        }
    }

    return predecessor;
}
    BinaryTreeNode* getPredecessorNodeByKey(int key) const {
    BinaryTreeNode* node = searchNodeWithKey(key);
    return getPredecessorNode(node);
}

};

class TravelDesk {
public:
    void add_trip(std::string vehicle_number, int seating_capacity, std::string pick_up_location, std::string drop_location, int departure_time) {
        vector<Vehicle *>::iterator itv;
        for(itv=vehicles.begin();itv!=vehicles.end();itv++){
            if((*itv)->getVehicleNumber()==vehicle_number){
                break;
            }
        }
        if(itv==vehicles.end()){
            Vehicle * v = new Vehicle(vehicle_number,seating_capacity);
            vehicles.push_back(v);
            itv=vehicles.end()-1;
        }
        Trip * t = new Trip(*itv,pick_up_location,drop_location,departure_time);
        (*itv)->addTrip(t); 
        vector<Location *>::iterator itl;
        for(itl=locations.begin();itl!=locations.end();itl++){
            if((*itl)->getName()==pick_up_location){
                break;
            }
        }
        if(itl==locations.end()){
            Location * l = new Location(pick_up_location);
            locations.push_back(l);
            itl=locations.end()-1;
        }
        (*itl)->addTrip(t);
        TransportService * ts;
        ts=(*itl)->getServicePtr(drop_location);
        if(ts==nullptr){
            ts=(*itl)->setServicePtr(drop_location);
        }
        ts->addTrip(departure_time,t);
    }

    std::vector<Trip*> show_trips(std::string pick_up_location, int after_time, int before_time) {
        vector<Location *>::iterator itl;
        if(after_time>before_time){
            int temp=after_time;
            after_time=before_time;
            before_time=temp;
        }
        for(itl=locations.begin();itl!=locations.end();itl++){
            if((*itl)->getName()==pick_up_location){
                break;
            }
        }
        return (*itl)->showTrip(after_time,before_time);
    }

    std::vector<Trip*> showTripsbydestination(std::string pick_up_location, std::string destination,int after_time, int before_time) {
        if(after_time>before_time){
            int temp=after_time;
            after_time=before_time;
            before_time=temp;
        }
        vector<Location *>::iterator itl;
        for(itl=locations.begin();itl!=locations.end();itl++){
            if((*itl)->getName()==pick_up_location){
                break;
            }
        }
        vector<Trip *> ans;
        TransportService * ts = (*itl)->getServicePtr(destination);
        ans=ts->getBSTHead()->showTrip(after_time,before_time,ans);
        return ans;
    }

    Trip* book_trip(std::string pick_up_location, std::string drop_location, std::string vehicle_number, int departure_time) {
        vector<Location *>::iterator itl;
        for(itl=locations.begin();itl!=locations.end();itl++){
            if((*itl)->getName()==pick_up_location){
                break;
            }
        }
        BinaryTreeNode * bt = (*itl)->getServicePtr(drop_location)->getBSTHead()->findNode(departure_time);
        if(bt->getTripNodePtr()->getBookedSeats()<bt->getTripNodePtr()->getVehicle()->getSeatingCapacity()){
            int temp = bt->getTripNodePtr()->getBookedSeats();
            bt->getTripNodePtr()->setBookedSeats(++temp);
            return bt->getTripNodePtr();
        }
        else{
            
        }

        
    }
    Location* getLocation(std::string location){
        vector<Location *>::iterator itl;
        for(itl=locations.begin();itl!=locations.end();itl++){
            if((*itl)->getName()==location){
                break;
            }
        }
        return *itl;
    }

private:
    std::vector<Vehicle*> vehicles;
    std::vector<Location*> locations;
};
