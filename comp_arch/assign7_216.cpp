#include <iostream>
#include <vector>
#include <string.h>
#include <sstream>  
#include <bits/stdc++.h> 
using namespace std;  

int registers[32]={0};
string memory[4096]={"00000000000000000000000000000000"};
int pc=0;
string TypeofInst(string opcode);


vector<string> getInp(string input){
	vector<string> array;
	stringstream ss(input);
	string tok;
	while(getline(ss,tok,' ')){
		array.push_back(tok);
	}
	return array;
}

vector<string> lbrackSep(string input){
	vector<string> array;
	stringstream ss(input);
	string tok;
	while(getline(ss,tok,'(')){
		array.push_back(tok);
	}
	return array;
}

vector<string> rbrackSep(string input){
	vector<string> array;
	stringstream ss(input);
	string tok;
	while(getline(ss,tok,')')){
		array.push_back(tok);
	}
	return array;
}

string decToBinary(int n) 
{ 
    int binaryNum[32]; 
    int i = 0; 
    while (n > 0) { 
        binaryNum[i] = n % 2; 
        n = n / 2; 
        i++; 
    } 
    string result="";
    for (int j = i - 1; j >= 0; j--) 
        result.append(to_string(binaryNum[j]));
    return result;
}

string decToBinaryReg(int n) 
{ 
    int binaryNum[32]; 
    int i = 0; 
    while (n > 0) { 
        binaryNum[i] = n % 2; 
        n = n / 2; 
        i++; 
    } 
    string result="";
    if(i==4) result="0";
    if(i==3) result="00";
    if(i==2) result="000";
    if(i==1) result="0000";
    if(i==0) result="00000";

    for (int j = i - 1; j >= 0; j--) 
        result.append(to_string(binaryNum[j]));
    return result;
}

string decToBinary16(int n) 
{ 
    int binaryNum[16]={0}; 
    int i = 15; 
    while (n > 0) { 
        binaryNum[i] = n % 2; 
        n = n / 2; 
        i--; 
    } 
    string result="";
    for (int j = 0; j <16 ; j++) 
        result.append(to_string(binaryNum[j]));
    return result;
}

string decToBinary32(int n) 
{ 
    int binaryNum[32]={0}; 
    int i = 31; 
    while (n > 0) { 
        binaryNum[i] = n % 2; 
        n = n / 2; 
        i--; 
    } 
    string result="";
    for (int j = 0; j <31 ; j++) 
        result.append(to_string(binaryNum[j]));
    return result;
}

string decToBinary26(int n) 
{ 
    int binaryNum[26]={0}; 
    int i = 25; 
    while (n > 0) { 
        binaryNum[i] = n % 2; 
        n = n / 2; 
        i--; 
    } 
    string result="";
    for (int j = 0; j <25 ; j++) 
        result.append(to_string(binaryNum[j]));
    return result;
}

int binaryToDec(string n) 
{ 
    string num = n; 
    int dec_value = 0; 
    int base = 1; 
    int len = num.length(); 
    for (int i = len - 1; i >= 0; i--) { 
        if (num[i] == '1') 
            dec_value += base; 
        base = base * 2; 
    } 
    return dec_value; 
}

int mapreg(string name){
	if(name.compare("$zero")==0) return 0;
	else if(name.compare("$at")==0) return 1;
	else if(name.compare("$v0")==0) return 2;
	else if(name.compare("$v1")==0) return 3;
	else if(name.compare("$a0")==0) return 4;
	else if(name.compare("$a1")==0) return 5;
	else if(name.compare("$a2")==0) return 6;
	else if(name.compare("$a3")==0) return 7;
	else if(name.compare("$t0")==0) return 8;
	else if(name.compare("$t1")==0) return 9;
	else if(name.compare("$t2")==0) return 10;
	else if(name.compare("$t3")==0) return 11;
	else if(name.compare("$t4")==0) return 12;
	else if(name.compare("$t5")==0) return 13;
	else if(name.compare("$t6")==0) return 14;
	else if(name.compare("$t7")==0) return 15;
	else if(name.compare("$s0")==0) return 16;
	else if(name.compare("$s1")==0) return 17;
	else if(name.compare("$s2")==0) return 18;
	else if(name.compare("$s3")==0) return 19;
	else if(name.compare("$s4")==0) return 20;
	else if(name.compare("$s5")==0) return 21;
	else if(name.compare("$s6")==0) return 22;
	else if(name.compare("$s7")==0) return 23;
	else if(name.compare("$t8")==0) return 24;
	else if(name.compare("$t9")==0) return 25;
	else if(name.compare("$k0")==0) return 26;
	else if(name.compare("$k1")==0) return 27;
	else if(name.compare("$gp")==0) return 28;
	else if(name.compare("$sp")==0) return 29;
	else if(name.compare("$fp")==0) return 30;
	else if(name.compare("$ra")==0) return 31; 
}

string to_binary(vector<string> instr){
	string temp="";
	if(instr[0].compare("add")==0 || instr[0].compare("sub")==0){
		temp.append("000000");
		string rd=decToBinaryReg(mapreg(instr[1]));
		string rs=decToBinaryReg(mapreg(instr[2]));
		string rt=decToBinaryReg(mapreg(instr[3]));
		temp.append(rs);
		temp.append(rt);
		temp.append(rd);
		temp.append("00000");
		if(instr[0].compare("add")==0) temp.append("100000");
		else temp.append("100010");
		return temp;
	}
	else if(instr[0].compare("sll")==0 || instr[0].compare("srl")==0){
		temp.append("000000");
		string rd=decToBinaryReg(mapreg(instr[1]));
		string rt=decToBinaryReg(mapreg(instr[2]));
		string sa=decToBinaryReg(stoi(instr[3]));
		temp.append("00000");
		temp.append(rt);
		temp.append(rd);
		temp.append(sa);
		if(instr[0].compare("sll")==0) temp.append("000000");
		else temp.append("000010");
		return temp;
	}
	else if(instr[0].compare("lw")==0 || instr[0].compare("sw")==0){
		if(instr[0].compare("lw")==0) temp.append("100011");
		else temp.append("101011");
		vector<string> arr=lbrackSep(instr[2]);
		vector<string> arr2=rbrackSep(arr[1]);
		temp.append(decToBinaryReg(mapreg(arr2[0])));
		temp.append(decToBinaryReg(mapreg(instr[1])));
		temp.append(decToBinary16(stoi(arr[0])));
		return temp;
	}
	else if(instr[0].compare("j")==0){
		temp.append("000010");
		temp.append(decToBinary26(stoi(instr[1])));
		return temp;
	}
	else if(instr[0].compare("jal")==0){
		temp.append("000011");
		temp.append(decToBinary26(stoi(instr[1])));
		return temp;
	}
	else if(instr[0].compare("jr")==0){
		temp.append("00000011111000000000000000001000");
		return temp;
	}

	else return temp;
}

void execute(string instr){
	if(instr.substr(0,6).compare("000000")==0){
		if(instr.substr(26,6).compare("100000")==0){	//add
			int rs=binaryToDec(instr.substr(6,5));
			int rt=binaryToDec(instr.substr(11,5));
			int rd=binaryToDec(instr.substr(16,5));
			registers[rd]=registers[rs]+registers[rt];
			pc++;
		}
		else if(instr.substr(26,6).compare("100010")==0){	//sub
			int rs=binaryToDec(instr.substr(6,5));
			int rt=binaryToDec(instr.substr(11,5));
			int rd=binaryToDec(instr.substr(16,5));
			registers[rd]=registers[rs]-registers[rt];
			pc++;
		}
		else if(instr.substr(26,6).compare("000010")==0){	//srl
			int rd=binaryToDec(instr.substr(6,5));
			int rt=binaryToDec(instr.substr(11,5));
			int sa=binaryToDec(instr.substr(16,5));
			registers[rd]=registers[rt]>>sa;
			pc++;
		}
		else if(instr.substr(26,6).compare("000000")==0){	//sll
			int rd=binaryToDec(instr.substr(6,5));
			int rt=binaryToDec(instr.substr(11,5));
			int sa=binaryToDec(instr.substr(16,5));
			registers[rd]=registers[rt]<<sa;
			pc++;
		}
		else if(instr.substr(26,6).compare("001000")==0){	//jr
			pc=registers[31];
		}
		else return;
	}
	else if(instr.substr(0,6).compare("100011")==0){	//lw
		pc++;
		int base=binaryToDec(instr.substr(6,5));
		int rt=binaryToDec(instr.substr(11,5));
		int offset=binaryToDec(instr.substr(16,31));
		int i=base+offset;
		memory[i]=registers[rt];
	}
	else if(instr.substr(0,6).compare("101011")==0){	//sw
		pc++;
		int base=binaryToDec(instr.substr(6,5));
		int rt=binaryToDec(instr.substr(11,5));
		int offset=binaryToDec(instr.substr(16,31));
		int i=base+offset;
		registers[rt]=binaryToDec(memory[i]);
	}
	else if(instr.substr(0,6).compare("000010")==0){	//j
		int offset=binaryToDec(instr.substr(7,31));
		pc=pc+offset;
	}
	else if(instr.substr(0,6).compare("000010")==0){	//jal
		int offset=binaryToDec(instr.substr(7,31));
		registers[31]=pc+1;
		pc=pc+offset;
	}

}

int main() {  
	string input;    
	cout<<"Enter the string: ";   
	getline(cin, input);
	cout<<input<<'\n';  
	vector<string> instruction=getInp(input);
	string ins=to_binary(instruction);
	memory[0]=ins;
//	cout<<"hi"<<decToBinary32(10);
	cout<<memory[0]<<'\n';
	execute(memory[0]);
  	return 0;  
 } 