#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <cmath>

using namespace std;
vector<string>columnNames;


vector<string> split(const string& str, char delimiter) {
  vector<string> tokens;
  string token;
  istringstream stream(str);
  while (getline(stream, token, delimiter)) {
    tokens.push_back(token);
  }
  return tokens;
}

bool readMatrix(const string& filename, unordered_map<string, int>& colIndex, vector<vector<double>>& matrix) {
  ifstream file(filename);
  if (!file.is_open()) {
    cerr << "Error: Could not open file " << filename << endl;
    return false;
  }

  string line;
  getline(file, line); 

  columnNames = split(line, ' ');
  for (int i = 0; i < columnNames.size(); ++i) {
    colIndex[columnNames[i]] = i;
  }

  while (getline(file, line)) {
    vector<double> row;
    vector<string> values = split(line, ' ');
    if (values.size() != columnNames.size()) {
      cerr << "Error: Inconsistent number of values in a line" << endl;
      return false;
    }
    for (const string& value : values) {
      try {
        row.push_back(stod(value));
      } catch (const invalid_argument& e) {
        cerr << "Error: Invalid value encountered in the file" << endl;
        return false;
      }
    }
    matrix.push_back(row);
  }

  file.close();
  return true;
}

pair<double, double> calculateMeanVariance(const vector<double>& data, int n) {
  double sum = 0.0;
  for (double value : data) {
    sum += value;
  }
  double mean = sum / (data.size() - n);

  double variance = 0.0;
  for (double value : data) {
    variance += pow(value - mean, 2);
  }
  variance /= data.size();

  return make_pair(mean, variance);
}

void buildAdjacencyList(const vector<vector<double>>& matrix, unordered_map<string, int>& colIndex, vector<vector<int>>& adjList, double threshold) {
  int n = matrix.size();
  for(int i = 1; i <= n; i++)
  {
        adjList.push_back(vector<int>());
  }
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      if (matrix[i][j] > threshold || matrix[j][i] > threshold) {
        adjList[i].push_back(j);
        adjList[j].push_back(i);
        // cout << columnNames[i] << " " << columnNames[j] << " " << max(matrix[i][j], matrix[j][i]) << endl;
      }
    }
  }
}

void writeAdjVectorsToFile(const string& filename, const vector<vector<int>>& adjAns) {
    ofstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: Could not open file " << filename << endl;
        return;
    }

    file << adjAns.size() << endl;

    int i = 0;
    for (const vector<int>& neighbors : adjAns) {
        file << columnNames[i] << ": ";
        for (int neighbor : neighbors) {
            file << columnNames[neighbor] << " ";
        }
        file << endl; 
        ++i;
    }

    file.close();
    // cout << "Adjacency vectors written to file: " << filename << endl;
}


int main() {

//   cout << "Please write the name of the matrix file: ";
  string filename;
  cin >> filename; 
  unordered_map<string, int> colIndex; 
  vector<vector<double>> matrix; 
  vector<vector<int>> adjList;


  if (!readMatrix(filename, colIndex, matrix)) {
    return 1; 
  }

  int n = matrix.size(); 

  vector<double> allElements;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      allElements.push_back(matrix[i][j]);
    }
  }
  pair<double, double> meanVar = calculateMeanVariance(allElements, n);
  buildAdjacencyList(matrix, colIndex, adjList, 0.75);

  vector<vector<int> > adjAns;
  vector<bool> mark;
  vector<int>sz;
  for(int i = 1; i <= n; i++)
  {
    adjAns.push_back(vector<int>());
    mark.push_back(false);
    sz.push_back(adjList[i].size());
  }
  for(int i = 1; i < n; i++)
  {
    int mn = n + 1;
    int ind = 0;
    for(int j = 0; j < n; j++)
    {
        if(!mark[j] && sz[j] < mn)
        {
            mn = adjList[j].size();
            ind = j;
        }
    }
    sz[ind] = 0;
    for(int k = 0; k < adjList[ind].size(); k++)
    {
        int u = adjList[ind][k];
        if(mark[u])
            continue;
        // cout << columnNames[u] << " " << columnNames[ind] << endl;
        if(sz[u] == 1 && matrix[ind][u] > 0.75)
        {
            adjAns[ind].push_back(u);
            // cout << columnNames[ind] << " " << columnNames[u] << endl;
        }
        if(matrix[u][ind] > 0.75)
        {
            sz[u] --;
            adjAns[u].push_back(ind);
        }
    }
    mark[ind] = true;
  }
//   cout << "Please write the name of the output path: ";
  string file_out;
  cin >> file_out; 
  writeAdjVectorsToFile(file_out, adjAns);
}
  