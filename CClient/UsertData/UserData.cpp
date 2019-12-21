//
// Created by suvorovm on 18.12.2019.
//

#include "UserData.h"

#include <utility>

UserData::UserData(const string &pid, const string &name, const string &status){
    this->NAME = name;
    this->PID = pid;
    this->STATUS = status;
}
const string &UserData::getPid() const {
    return PID;
}

const string &UserData::getName() const {
    return NAME;
}

const string &UserData::getStatus() const {
    return STATUS;
}

void UserData::setPid(const string &pid) {
    PID = pid;
}

void UserData::setName(const string &name) {
    NAME = name;
}

void UserData::setStatus(const string &status) {
    STATUS = status;
}

UserData::UserData() {
    this->NAME = "NO";
    this->PID = "pid";
    this->STATUS = "status";
}


