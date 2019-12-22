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
string ManagerPidPath;
int Ppid;
UserData userData;
string generalPipeName;

void InitPips(string &generalPipeName);

void NotifyNotifyParent(const string &generalPipeName, const string &info);
void InitSignals();
void HandleUserSignal(int n){
    cout.flush();
    cout.clear();
    cout<<"\nWork with SIGUSER1";
    ifstream fifo {generalPipeName};
    string line;
    getline(fifo, line);
    cout<<"LOG_CLIENT: Recived" <<line;


}

void SignalQuitHandler(int n){

    cout<<"\nWork with SIGQUIt";
    exit(0);
}
int main(int argc, char *argv[]) {

    cout<<"Process name = "<< argv[1];
    setlocale(LC_CTYPE,"");
    string processName(argv[1]);
    userData = UserData(to_string((int)getpid()), processName, "1");
    ;
    string targetPipeName;
    __pid_t myPid = getpid();
    cout<<"\nLOG_CLIENT: My PID is " <<userData.getPid() << endl;

    if(argc==3){
        Ppid = (int)getppid();
    }else{
        chdir("..");
        chdir("..");
        ManagerPidPath = get_current_dir_name() ;
        ManagerPidPath += + "/Pipe/PidFile.txt";
        ifstream rdl(ManagerPidPath);
        getline(rdl, managerPID);
        Ppid = stoi(managerPID);
    }
    InitPips(generalPipeName);
    NotifyNotifyParent(generalPipeName, targetPipeName);
    InitSignals();
    while (true){
    }
    return 0;
}

void InitSignals() {
    struct sigaction act,outI;
    act.sa_handler = SignalQuitHandler;
    sigemptyset(&act.sa_mask);
    act.sa_flags = SA_NODEFER;
    sigaction(9, &act, &outI);

    struct sigaction sa;
    sigemptyset(&sa.sa_mask);
    sa.sa_handler = HandleUserSignal;
    sa.sa_flags = SA_NODEFER;
    sigaction(SIGUSR1, &sa, NULL);
}

void NotifyNotifyParent(const string &generalPipeName, const string &info) {
    __pid_t parentPid = getppid();
    kill(Ppid, SIGUSR1);
    cout<<"LOG_CLIENT :PArent PID is "<< parentPid<<endl;
    cout<< "\nLOG_CLIENT: start writing ..... \n";
    cout<<generalPipeName;
    int fdGeneralPipeName = open(generalPipeName.c_str(), O_WRONLY );
    if(fdGeneralPipeName<0){
        cout<<"\nLOG_CLIENT: ERROR HIRE\n";
         perror("LOG: CAN'T write to pipe");
         exit(0);
    }

    string formatingMes = "messageType:1,PID:"+ userData.getPid() +",status:"+ userData.getStatus()+",userName:"+userData.getName()+",msg:ps -e.";
    int response = write(fdGeneralPipeName,formatingMes.c_str(), formatingMes.size());
    close(fdGeneralPipeName);
    cout<< "Writed = "<<response<<endl;
    cout<<"LOG_CLIENT : Writed to Pipe";
    cout.flush();
}

void InitPips(string &generalPipeName) {
    generalPipeName= get_current_dir_name();
    generalPipeName +=  "/Pipe/GeneralPipe.p";
}