#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

using namespace std;

int main(){
    ifstream file("prices.txt");
    if(!file){
        cout << "wtf dude no prices.txt found" << endl;
        return 1;
    }

    vector<double> p;
    double x;
    while(file >> x){
        p.push_back(x);
    }

    ofstream returns("returns.txt");
    
    int n = p.size();
    vector<double> r(n);
    for(int i = 1; i < p.size(); i++){
        r[i] = log(p[i] /p[i-1]);
        returns << r[i] << endl;
    }
    cout << endl;

    


    double mu;
    double sum = 0;
    for(int i = 0; i < n; i++){
        sum += r[i];
    }
    mu = sum / (n - 1); 

    double summation = 0;
    for(int i = 0; i < n; i++){
        double a = (r[i] - mu) * (r[i] - mu);
        
        summation += a;
    }
    double sigma = sqrt(summation / (n - 2));

    cout << n << endl;
    cout << mu << endl;
    cout << sum << endl;
    cout << sigma << endl;
}



