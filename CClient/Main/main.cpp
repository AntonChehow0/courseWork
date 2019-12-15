#include <fcntl.h>
#include <iostream>
#include <sys/stat.h>
#include <unistd.h>
#include <string>

#include <signal.h>
#include <cstring>

using namespace std;
int const STRING_LENGTH = 100;

void InitPips(string &generalPipeName, string &targetPipeName);

void NotifyNotifyParent(const string &generalPipeName, const string &targetPipeName);

int main() {
    chdir("..");
    chdir("..");

    setlocale(LC_CTYPE,"");
    string generalPipeName;
    string targetPipeName;
    __pid_t myPid = getpid();
    cout<<"\nMy PID is " <<myPid << endl;
    InitPips(generalPipeName, targetPipeName);
    NotifyNotifyParent(generalPipeName, targetPipeName);

    while (true){

    }
    return 0;
}

void NotifyNotifyParent(const string &generalPipeName, const string &targetPipeName) {
    __pid_t parentPid = getppid();
    cout<<"PArent PID is "<< parentPid<<endl;
    int fdGeneralPipeName = open(generalPipeName.c_str(), O_RDWR );
    if(fdGeneralPipeName<0){
        cout<< "File:  "<<targetPipeName.c_str()<<"\n";
        cout<<"\nERROR HIRE\n";
      //  perror("CAN'T write to pipe");
       // return;
    }

    char char_array[100];
    strcpy(char_array, targetPipeName.c_str());
    int response = write(fdGeneralPipeName,char_array,sizeof(char_array));

    close(fdGeneralPipeName);
    cout<<"\n writed to FIFO "<< targetPipeName.c_str()<<endl;
    kill(parentPid,SIGUSR1);
}

void InitPips(string &generalPipeName, string &targetPipeName) {
    generalPipeName= get_current_dir_name();
    targetPipeName+=get_current_dir_name();
    generalPipeName +=  "/Pipe/GeneralPipe.p";
    targetPipeName.append("/Pipe/" + to_string(getpid()) + "." + to_string(random() % 100).c_str());

}
