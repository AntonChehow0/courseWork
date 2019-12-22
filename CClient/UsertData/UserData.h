//
// Created by suvorovm on 18.12.2019.
//

#ifndef CCLIENT_USERDATA_H
#define CCLIENT_USERDATA_H

#include <string>

using namespace  std;
class UserData {
private:
     string PID;
     string NAME;
     string STATUS;
public:
    UserData(const string &pid, const string &name, const string &status);

    const string &getPid() const;

    const string &getName() const;

    const string &getStatus() const;



    void setPid(const string &pid);

    void setName(const string &name);

    void setStatus(const string &status);

    UserData();
};


#endif //CCLIENT_USERDATA_H
