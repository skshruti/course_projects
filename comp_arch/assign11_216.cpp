#include <iostream>
#include <vector>
#include <string.h>
#include <sstream>
#include <bits/stdc++.h>
#include <fstream>
using namespace std;

typedef struct floatNum {
    int sign;
    int exponent;
    string fraction;
} floatNum;

typedef struct str_int {
	string value;
	int intValue;
} str_int;

typedef struct output{
	floatNum sum;
	int cycles;
} output;

floatNum normalize(floatNum f);
floatNum addSignificands(floatNum f1, floatNum f2);

void print_floatNum(floatNum val){
	cout<<"sign    :  "<<val.sign<<"\n";
	cout<<"fraction:  "<<val.fraction<<"\n";
	cout<<"exponent:  "<<val.exponent<<"\n";
}

string typeNum(floatNum f){
	size_t found1=(f.fraction.find("1"));
	if(f.exponent+127==255){
		if(found1!=string::npos){
			return "NaN";
		}
		else{
			if(f.sign==0) return "Infinity";
			else return "-Infinity";
		}
	}
	else if(f.exponent+127==0){
		if(found1!=string::npos){
			return "Denormalised";
		}
		else return "Zero";
	}
	else return "FloatingPt";
}

str_int removeDec(string str){
	str_int result;
	int decPlace=0;
	while(str.at(decPlace)!='.'){
		decPlace++;
	}
	result.value=str.substr(0,decPlace)+str.substr(decPlace+1,str.length()-1-decPlace);
	result.intValue=decPlace;
	return result;
}

floatNum shiftRight(floatNum f, int place){
	string temp=removeDec(f.fraction).value;
	int decPlace=removeDec(f.fraction).intValue;
	f.exponent-=place;
	if(temp.length()<decPlace+place){
		while(temp.length()<=decPlace+place) temp=temp+"0";
	}
	f.fraction=temp.substr(0,decPlace+place)+'.'+temp.substr(decPlace+place,23);
	while(f.fraction.length()!=23) f.fraction=f.fraction+"0";
	return f;
}

floatNum shiftLeft(floatNum f, int place){
	string temp=removeDec(f.fraction).value;
	int decPlace=removeDec(f.fraction).intValue;
	f.exponent+=place;
	int i=decPlace-place;
	if(decPlace-place<=0){
		while(decPlace-place!=1){
			temp="0"+temp;
			decPlace++;
		}
	}
	f.fraction=temp.substr(0,decPlace-place)+'.'+temp.substr(decPlace-place,23);
	return f;
}

output roundNum(floatNum f){
	output result;
	result.cycles=0;
	int decPlace=removeDec(f.fraction).intValue;
	if(f.fraction.substr(decPlace+1,f.fraction.length()-1-decPlace).length()>23){
		if(f.fraction.at(decPlace+24)=='1'){
			f.fraction=f.fraction.substr(0,decPlace+24);
			floatNum one;
			one.sign=f.sign;
			one.fraction="0.00000000000000000000001";
			one.exponent=f.exponent;
			f=addSignificands(f,one);
		}
		else f.fraction=f.fraction.substr(0,decPlace+24);
		result.cycles++;
	}
	result.sum=f;
	return result;
}

floatNum binaryToFloat(string binary){
	floatNum value;
	value.sign=stoi(binary.substr(0,1));
	int exponent=0;
	for(int i = 1; i < 9; i++){
		exponent+=stoi(binary.substr(i,1))*pow(2,8-i);
	}
	value.exponent=exponent-127;
	string fraction=binary.substr(9,23);
	value.fraction="1."+fraction;
	if(exponent==0 || exponent==255) 
		value.fraction="0."+fraction;
	return value;
}

string numToBinary(int n, int bits){
    int binaryNum[bits]={0};
    int i = bits-1;
    while (n > 0) {
        binaryNum[i] = n % 2;
        n = n / 2;
        i--;
    }
    string result="";
    for (int j = 0; j <bits ; j++)
        result.append(to_string(binaryNum[j]));
    return result;
}

string floatToBinary(floatNum f){
	if(typeNum(f).compare("NaN")==0) return "01111111100000000000000000000001";
	else if(typeNum(f).compare("Infinity")==0) return "01111111100000000000000000000000";
	else if(typeNum(f).compare("-Infinity")==0) return "11111111100000000000000000000000";
	else if(typeNum(f).compare("Zero")==0) return "00000000000000000000000000000000";
	else{
		string value;
		if(f.sign==1) value=value+'1';
		else value=value+'0';
		value=value+numToBinary(f.exponent+127,8);
		string fraction=f.fraction.substr(2,23);
		while(fraction.length()!=23) fraction=fraction+"0";
		value.append(fraction);
		return value;
	}
}

str_int addBinary(string s1, string s2, int overflow){
	string value;
	for(int i=s1.length()-1; i>=0; i--){
		if(s1.at(i)=='0' && s2.at(i)=='0' && overflow==0){
			value="0"+value;
			overflow=0;
		}
		else if(s1.at(i)=='1' && s2.at(i)=='1' && overflow==1){
			value="1"+value;
			overflow=1;
		}
		else if((s1.at(i)=='0' && s2.at(i)=='0' && overflow==1) || 
				 (overflow==0 && s2.at(i)=='0' && s1.at(i)=='1') || 
				 (s1.at(i)=='0' && overflow==0 && s2.at(i)=='1')){
			value="1"+value;
			overflow=0;
		}
		else{
			value="0"+value;
			overflow=1;
		}
	}
	str_int result;
	result.value=value;
	result.intValue=overflow;
	return result;
}

string subBinary(string str1, string str2){
	int decPlace=0;
	while(str1.at(decPlace)!='.'){
		decPlace++;
	}
	string s1=str1.substr(0,decPlace)+str1.substr(decPlace+1,str1.length()-1-decPlace);
	string s2=str2.substr(0,decPlace)+str2.substr(decPlace+1,str2.length()-1-decPlace);
	string result;
	for(int i=s1.length()-1; i>=0; i--){
		if((s1.at(i)=='0' && s2.at(i)=='0') || (s1.at(i)=='1' && s2.at(i)=='1'))
			result="0"+result;
		else if(s1.at(i)=='1' && s2.at(i)=='0')
			result="1"+result;
		else if(s1.at(i)=='0' && s2.at(i)=='1'){
			int j=i-1;
			while(s1.at(j)!='1' && j>=0){
				j--;
			}
			s1.replace(j,1,"0");
			j++;
			while(j<i){
				s1.replace(j++,1,"1");
			}
			result="1"+result;
		}
	}
	result=result.substr(0,decPlace)+'.'+result.substr(decPlace,result.length()-decPlace);
	return result;
}

floatNum addSignificands(floatNum f1, floatNum f2){
	int decPlace1=0;
	while(f1.fraction.at(decPlace1)!='.'){
		decPlace1++;
	}
	string intf1=f1.fraction.substr(0,decPlace1);
	string decf1=f1.fraction.substr(decPlace1+1,f1.fraction.length()-1-decPlace1);
	int decPlace2=0;
	while(f2.fraction.at(decPlace2)!='.'){
		decPlace2++;
	}
	string intf2=f2.fraction.substr(0,decPlace2);
	string decf2=f2.fraction.substr(decPlace2+1,f2.fraction.length()-1-decPlace2);
	if(decf1.length()!=decf2.length()){
		if(decf1.length()>decf2.length()){
			while(decf1.length()!=decf2.length()){
				decf2.append("0");
			}
		}
		else{
			while(decf1.length()!=decf2.length()){
				decf1.append("0");
			}
		}	
	}

	if(intf1.length()!=intf2.length()){
		if(intf1.length()>intf2.length()){
			while(intf1.length()==intf2.length()){
				intf2="0"+intf2;
			}
		}
		else{
			while(intf1.length()==intf2.length()){
				intf1="0"+intf1;
			}
		}	
	}
	floatNum result;
	result.sign=0;
	result.exponent=f1.exponent;
	if((f1.sign==0 && f2.sign==0) || (f1.sign==1 && f2.sign==1)){
		str_int resDec=addBinary(decf1,decf2,0);
		str_int resInt=addBinary(intf1,intf2,resDec.intValue);
		string val=resInt.value+"."+resDec.value;
		if(resInt.intValue==1) val='1'+val;
		if(f1.sign==1 && f2.sign==1) result.sign=1;
		result.fraction=val;
	}
	else if(f1.fraction.compare(f2.fraction)>0){
		string val=subBinary(intf1+'.'+decf1,intf2+'.'+decf2);
		if(f1.sign==1) result.sign=1;
		result.fraction=val;
	}
	else{
		string val=subBinary(intf2+'.'+decf2,intf1+'.'+decf1);
		if(f2.sign==1) result.sign=1;
		result.fraction=val;
	}

	return result;
}

int isNormalized(floatNum f){
	if(typeNum(f).compare("FloatingPt")==0 || typeNum(f).compare("Denormalised")==0){
		string temp=removeDec(f.fraction).value;
		int decPlace=removeDec(f.fraction).intValue;
		if(decPlace!=1) return 0;
		else{
			if(temp.at(0)=='0' && temp.find("1",decPlace)!=string::npos) return 0;
			else return 1; 
		}
	}
	else return 1;
}

floatNum normalize(floatNum f){
	if(typeNum(f).compare("FloatingPt")==0 || typeNum(f).compare("Denormalised")==0){
		string temp=removeDec(f.fraction).value;
		int decPlace=removeDec(f.fraction).intValue;
		if(decPlace!=1){
			size_t found1=(temp.substr(0,decPlace)).find("1");
			if(found1!=string::npos){
				while(decPlace!=1){
					decPlace--;
					f.exponent++;
				}
				f.fraction=temp.substr(0,decPlace)+'.'+temp.substr(decPlace,temp.length()-decPlace);
				return normalize(f);
			}
			else{
				f.fraction=f.fraction.substr(decPlace-1,f.fraction.length()-decPlace+1);
				return normalize(f);
			}
		}
		else{
			while(temp.at(0)!='1' && temp.length()>0){
				temp=temp.substr(1,temp.length()-1);
				f.exponent--;
			}
			f.fraction=temp.substr(0,1)+'.'+temp.substr(1,temp.length()-1);
		}
		return f;
	}
	else return f;
}

floatNum NaN(){
	floatNum f;
	f.sign=0;
	f.exponent=128;
	f.fraction="1.0011";
	return f;
}

floatNum Zero(){
	floatNum f;
	f.sign=0;
	f.exponent=-127;
	f.fraction="0";
	return f;
}

floatNum Infinity(){
	floatNum f;
	f.sign=0;
	f.exponent=128;
	f.fraction="0";
	return f;
}

floatNum InfinityNeg(){
	floatNum f;
	f.sign=1;
	f.exponent=128;
	f.fraction="0";
	return f;
}

output addFloatNums(string s1, string s2){
	output result;
	if(typeNum(binaryToFloat(s1)).compare("NaN")==0 || typeNum(binaryToFloat(s2)).compare("NaN")==0){
		result.sum=NaN();
		result.cycles=0;
	}
	else if(typeNum(binaryToFloat(s1)).compare("Infinity")==0){
		result.cycles=0;
		if(typeNum(binaryToFloat(s2)).compare("-Infinity")==0) result.sum=NaN();
		else result.sum=Infinity();
	}
	else if(typeNum(binaryToFloat(s1)).compare("-Infinity")==0){
		result.cycles=0;
		if(typeNum(binaryToFloat(s2)).compare("Infinity")==0) result.sum=NaN();
		else result.sum=InfinityNeg();
	}
	else if(typeNum(binaryToFloat(s2)).compare("Infinity")==0){
		result.cycles=0;
		if(typeNum(binaryToFloat(s1)).compare("-Infinity")==0) result.sum=NaN();
		else result.sum=Infinity();
	}
	else if(typeNum(binaryToFloat(s2)).compare("-Infinity")==0){
		result.cycles=0;
		if(typeNum(binaryToFloat(s1)).compare("Infinity")==0) result.sum=NaN();
		else result.sum=InfinityNeg();
	}
	else if(typeNum(binaryToFloat(s1)).compare("Zero")==0 || typeNum(binaryToFloat(s2)).compare("Zero")==0){
		result.cycles=0;
		if(typeNum(binaryToFloat(s1)).compare("Zero")==0 && typeNum(binaryToFloat(s2)).compare("Zero")!=0) 
			result.sum=binaryToFloat(s2);
		else if(typeNum(binaryToFloat(s2)).compare("Zero")==0 && typeNum(binaryToFloat(s1)).compare("Zero")!=0) 
			result.sum=binaryToFloat(s1);
		else result.sum=Zero();
	}
	//CHECK FOR DENORMALIZED
	else{
		floatNum f1=binaryToFloat(s1);
		floatNum f2=binaryToFloat(s2);
		result.cycles=0;
		//STEP 1
		if(f1.exponent<f2.exponent){
			while(f1.exponent!=f2.exponent){
				f1=shiftLeft(f1,1);
			}
			result.cycles++;
		}
		else if(f1.exponent>f2.exponent){
			while(f1.exponent!=f2.exponent){
				f2=shiftLeft(f2,1);
			}
			result.cycles++;
		}
		//STEP 2
		floatNum sum=addSignificands(f1,f2);
		result.cycles++;
		size_t found1=(sum.fraction.find("1"));
		if(found1==string::npos) sum.exponent=-127;
		do{
			//STEP 3
			if(isNormalized(sum)!=1){
				sum=normalize(sum);
				result.cycles++;
			}
			//check overflow/underflow
			try{
				if(sum.exponent+127>254){
					throw "Exception overflow\n";
				}
				if(sum.exponent+127<1){
					throw "Exception underflow\n";
				}
			}
			catch(const char* exp){
				cout<<exp;
				result.sum=sum;
				return result;
			}
			//STEP 4
			output afterRound=roundNum(sum);
			sum=afterRound.sum;
			result.cycles+=afterRound.cycles;
		}while(isNormalized(sum)!=1);
		result.sum=sum;
	}
	return result;
}

std::vector<string> seperateInputs(string s){
	std::vector<string> v;
	string f1;
	int i=0;
	while(s.at(i)!=' ') f1=f1+(s.at(i++));
	string f2;
	for(i=i+1;i<s.length();i++) f2=f2+(s.at(i));
	v.push_back(f1);
	v.push_back(f2);
	return v;
}

int main(){
	ifstream infile;
	infile.open("input");
	string input;
	int noOfIns=0;
	std::vector<std::pair<floatNum,int>> outputs;
	while(getline(infile, input)){
		std::vector<string> v=seperateInputs(input);
		output result=addFloatNums(v.at(0),v.at(1));
		outputs.push_back({result.sum,result.cycles});
	}
	for(auto output: outputs)
		cout<<floatToBinary(output.first)<<" "<<output.second<<"\n";


	return 0;
}
