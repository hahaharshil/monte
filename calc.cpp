#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <random>
#include <algorithm>

using namespace std;

int main() {
    double money = 10000;  // how much we invest
    int sims = 10000;      // how many years we pretend to live
    int days = 252;        // trading days in one year

    // read the prices
    ifstream file("prices.txt");
    vector<double> prices;
    double price;
    while (file >> price) {
        prices.push_back(price);
    }

    // daily returns: how much the price changed each day
    vector<double> returns;
    ofstream returnsFile("returns.txt");
    for (int i = 1; i < prices.size(); i++) {
        double r = log(prices[i] / prices[i - 1]);
        returns.push_back(r);
        returnsFile << r << endl;
    }

    // mu: the average return
    double sum = 0;
    for (int i = 0; i < returns.size(); i++) {
        sum += returns[i];
    }
    double mu = sum / returns.size();

    // sigma: how much the returns jump around
    double total = 0;
    for (int i = 0; i < returns.size(); i++) {
        total += (returns[i] - mu) * (returns[i] - mu);
    }
    double sigma = sqrt(total / (returns.size() - 1));

    // random number maker that gives numbers shaped like a bell curve
    mt19937 rng(42);
    normal_distribution<double> randomReturn(mu, sigma);

    // monte carlo: live the year many times
    vector<double> finals;
    ofstream pathsFile("paths.txt");
    for (int s = 0; s < sims; s++) {
        double value = money;
        for (int d = 0; d < days; d++) {
            value = value * exp(randomReturn(rng));
            if (s < 100) {
                pathsFile << value << " ";  // save 100 years to draw
            }
        }
        if (s < 100) {
            pathsFile << endl;
        }
        finals.push_back(value);
    }

    ofstream finalsFile("finals.txt");
    for (int i = 0; i < finals.size(); i++) {
        finalsFile << finals[i] << endl;
    }

    // sort from worst to best
    sort(finals.begin(), finals.end());

    // the 5% worst year
    double worst5 = finals[sims * 5 / 100];
    double var = money - worst5;

    // how many years lost money
    int losses = 0;
    for (int i = 0; i < sims; i++) {
        if (finals[i] < money) {
            losses++;
        }
    }
    double chanceOfLoss = losses * 100.0 / sims;

    cout << "mu    = " << mu << endl;
    cout << "sigma = " << sigma << endl;
    cout << "middle result  = $" << finals[sims / 2] << endl;
    cout << "chance of loss = " << chanceOfLoss << "%" << endl;
    cout << "VaR 95%        = $" << var << endl;

    ofstream resultsFile("results.txt");
    resultsFile << money << endl;
    resultsFile << var << endl;
    resultsFile << chanceOfLoss << endl;

    return 0;
}
