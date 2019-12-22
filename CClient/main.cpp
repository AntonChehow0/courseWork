#include <fcntl.h>
#include <iostream>
#include <sys/stat.h>
#include <unistd.h>
#include <string>
#include <fstream>
#include <signal.h>
#include <cstring>
#include "UsertData/UserData.h"
#include <vector>
#include <algorithm>

using namespace std;
int const STRING_LENGTH = 100;
string managerPID;
string ManagerPidPath;
int Ppid;
UserData userData;
string generalPipeName;

bool is_number(const std::string& s);
void InitPips(string &generalPipeName);
vector<string> splitStrings(string str, char dl);
void NotifyNotifyParent();
void InitSignals();

void ChooseTypeMsg(vector<string> msgData);

void SetNewName(vector<string> vector);

void SetStatus(vector<string> vector);

void HandleUserSignal(int n){
    cout.flush();
    cout.clear();
    cout<<"\nWork with SIGUSER1";
    ifstream fifo {generalPipeName};
    string line;
    getline(fifo, line);
    fifo.close();
    cout<<"\nLOG_CLIENT: Recived\n" <<line;
    char lineSpliter = ',';
    vector<string> blocks = splitStrings(line, lineSpliter);
    ChooseTypeMsg(blocks);
    NotifyNotifyParent();
}

void ChooseTypeMsg(vector<string> msgData) {
    char lineSpliter = ':';
    string  msgType = splitStrings(msgData[0], lineSpliter)[1];
    if (!is_number(msgType)){
        cout<< "\nCLIENT_LOG: ERROR unavailable type msg\n ";
        return;
    }
    int type = stoi(msgType);
    switch (type){
        case 1:
            SetNewName(msgData);
            break;
        case 2:
            SetStatus(msgData);
            break;
        default:
            cout<<"\nCLIENT_LOG: ERROR unavailable type msg \n";
    }

}

void SetStatus(vector<string> vector) {

}

void SetNewName(vector<string> vector) {
    char lineSpliter = ':';
    string newName = splitStrings(vector[4],lineSpliter)[1];
    userData.setName(newName);
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
    NotifyNotifyParent();
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

void NotifyNotifyParent() {
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

vector<string> splitStrings(string str, char dl)
{
    string word = "";

    int num = 0;

    str = str + dl;

    int l = str.size();

    vector<string> substr_list;
    for (int i = 0; i < l; i++) {

        if (str[i] != dl)
            word = word + str[i];

        else {
            if ((int)word.size() != 0)
                substr_list.push_back(word);

            word = "";
        }
    }
    return substr_list;
}

bool is_number(const std::string& s)
{
    return !s.empty() && std::find_if(s.begin(),
                                      s.end(), [](char c) { return !std::isdigit(c); }) == s.end();
}