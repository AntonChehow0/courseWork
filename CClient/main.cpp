#include <fcntl.h>
#include <iostream>
#include <sys/stat.h>
#include <unistd.h>
#include <string>
#include <fstream>
#include <signal.h>
#include <cstring>
#include "UsertData/UserData.h"

using namespace std;
int const STRING_LENGTH = 100;
string managerPID;


void InitPips(string &generalPipeName);

void NotifyNotifyParent(const string &generalPipeName, const string &info);
string ManagerPidPath;
UserData userData;
int main() {
    chdir("..");
    chdir("..");

    setlocale(LC_CTYPE,"");
    userData = UserData(to_string((int)getpid()), "No name", "1");
    string generalPipeName;
    string targetPipeName;
    __pid_t myPid = getpid();
    cout<<"\nLOG_CLIENT: My PID is " <<userData.getPid() << endl;
    ManagerPidPath = get_current_dir_name() ;
    ManagerPidPath += + "/Pipe/PidFile.txt";
    ifstream rdl(ManagerPidPath);
    getline(rdl, managerPID);
    InitPips(generalPipeName);
    NotifyNotifyParent(generalPipeName, targetPipeName);

    while (true){

    }
    return 0;
}

void NotifyNotifyParent(const string &generalPipeName, const string &info) {
    __pid_t parentPid = getppid();
    kill(stoi(managerPID), SIGUSR1);
    cout<<"LOG_CLIENT :PArent PID is "<< parentPid<<endl;
    cout<< "\nLOG_CLIENT: start writing ..... \n";
    int fdGeneralPipeName = open(generalPipeName.c_str(), O_WRONLY );
    if(fdGeneralPipeName<0){
        cout << "Info:  " << info.c_str() << "\n";
        cout<<"\nLOG_CLIENT: ERROR HIRE\n";
         perror("LOG: CAN'T write to pipe");
         exit(0);
    }

    string formatingMes = "messageType:1,PID:"+ userData.getPid() +",status:"+ userData.getStatus()+",userName:"+userData.getName()+",msg:ps -e.";
    int response = write(fdGeneralPipeName,formatingMes.c_str(), formatingMes.size());
    cout<< "Writed = "<<response<<endl;
    close(fdGeneralPipeName);
    cout<<"LOG_CLIENT : Writed to Pipe";
}

void InitPips(string &generalPipeName) {
    generalPipeName= get_current_dir_name();
    generalPipeName +=  "/Pipe/GeneralPipe.p";
}