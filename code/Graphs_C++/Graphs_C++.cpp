﻿#include <iostream>
#include <vector>
#include <bitset>
#include <string>
#include <queue>
#include <set>
#include <unordered_set>

using namespace std;

const int INF = 1e9;

void print2d(vector <vector <int>> vect)
{
    for (auto u : vect)
    {
        for (auto v : u)
        {
            cout << v << " ";
        }
        cout << endl;
    }
}

void print1d(vector <int> vect)
{
    for (auto u : vect)
    {
        cout << u << " ";
    }
    cout << endl;
}

class Graph {
public:
    int num_vertices;
    vector<vector<int>> adj;
    vector<int> nodes;

    Graph(int n) {
        num_vertices = n;
        adj = vector<vector<int>>(num_vertices);
        for (int i = 0; i < n; i++)
        {
            nodes.push_back(i);
        }
    }

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    void printGraph() {
        for (int i = 0; i < num_vertices; i++) {
            cout << "Vertex " << i + 1 << ": ";
            for (int j = 0; j < adj[i].size(); j++) {
                cout << adj[i][j] + 1 << " ";
            }
            cout << endl;
        }
    }

};

Graph parse_graph6(const string& graph6) {
    int vertices = static_cast<int>(graph6[0]) - 63;
    string bin_list = "";

    for (char c : graph6.substr(1)) {
        bin_list += bitset<6>(static_cast<int>(c) - 63).to_string();
    }

    vector<vector<int>> adjMatrix(vertices, vector<int>(vertices, 0));

    int num_in_bot_left_diag = 0;
    for (int i = 1; i < vertices; ++i) {
        num_in_bot_left_diag += i;
    }
    string bot_left_diag = bin_list.substr(0, num_in_bot_left_diag);

    Graph g(vertices);
    int index = 0;
    for (int i = 0; i < vertices; ++i) {
        for (int j = 0; j < i; ++j) {
            if (bot_left_diag[index++] - '0' == 1)
            {
                g.addEdge(i, j);
            }
        }
    }

    return g;
}

void dijkstra(vector<vector<int>>& graph, int n, int start, vector<vector<int>>& paths) {
    vector<int> dist;
    dist.resize(n, INF);
    dist[start] = 0;

    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    pq.push({ 0, start });

    paths.resize(n);

    while (!pq.empty()) {
        int v = pq.top().second;
        int cur_dist = pq.top().first;
        pq.pop();

        if (cur_dist > dist[v]) continue;

        for (int u : graph[v]) {
            if (dist[u] > dist[v] + 1) {
                dist[u] = dist[v] + 1;
                pq.push({ dist[u], u });
                paths[u].push_back(v);
            }
            else if (dist[u] == dist[v] + 1) {
                paths[u].push_back(v);
            }
        }
    }
}

void printPaths(vector<vector<int>> paths, int start, int end, vector<int>& curr_path, vector<int>& all_paths) {
    curr_path.push_back(end);
    if (end == start) {
        // Убрал вершины start и end
        for (int i = curr_path.size() - 2; i > 0; --i) {
            all_paths.push_back(curr_path[i]);
            //cout << curr_path[i] << " ";
        }
        cout << endl;
    }
    else {
        for (int p : paths[end]) {
            printPaths(paths, start, p, curr_path, all_paths);
        }
    }

    curr_path.pop_back();
}

// Куда элементы девают эу
bool nextComb(unordered_set<int>& a, int n, int m)
{
    vector<int> temp(a.begin(), a.end());
    int k = m;
    for (int i = k - 1; i >= 0; --i)
        if (temp[i] < n - k + i + 1)
        {
            ++temp[i];
            for (int j = i + 1; j < k; ++j)
                temp[j] = temp[j - 1] + 1;
            a.clear();
            for (int val : temp)
                a.insert(val);
            return true;
        }
    return false;
}


void find_perfect_geodominating_sets(Graph g)
{
    int n = g.num_vertices;
    vector <vector <vector <int>>> all_paths(n, vector<vector<int>>(n, vector<int>(n)));
    vector <vector <vector <int>>> all_paths_dijkstra(n);

    for (size_t i = 0; i < n; i++)
    {
        vector<int> dist;
        vector<vector<int>> paths;
        dijkstra(g.adj, n, i, paths);
        all_paths_dijkstra[i] = paths;
    }

    for (size_t k = 2; k < n; k++)
    {
        unordered_set <int> s;
        copy(g.nodes.begin(),
            g.nodes.begin() + k,
            inserter(s, s.end()));
         
        while (nextComb(s, n, k))
        {
            vector <int> paths;
        }
    }


    //for (size_t i = 0; i < n; i++)
    //{
    //    for (size_t j = 0; j < n; j++)
    //    {
    //        if (i != j) 
    //        {
    //            vector<int> paths_between;
    //            vector<int> cur_path;
    //            printPaths(all_paths_dijkstra[i], i, j, cur_path, paths_between);



}


int main()
{
    string g6 = "F?`fw";
    //string g6;

    //while (getline(cin, g6))
    //{
    //    if (g6.empty()) {
    //        break;
    //    }

        Graph g = parse_graph6(g6);
        unordered_set <int> s = { 1, 2, 3, 4, 5, 6, 7 };
        while (nextComb(s, g.num_vertices, 3))
        {
            for (auto v : s)
            {
                cout << v << " ";
            }
            cout << endl;
        }
        //g.printGraph();
        //find_perfect_geodominating_sets(g);

        //vector<vector<int>> paths;
        //int start = 0;
        //int end = 1;
        //dijkstra(g.adj, g.num_vertices, start, paths);
        //vector<int> curr_path;
        //vector<int> all_paths;
        //printPaths(paths, start, end, curr_path, all_paths);
        //cout << "Paths:" << endl;
        //for (auto v : all_paths)
        //{
        //    cout << v << " ";
        //}
        //print2d(paths);

    //}

    
    return 0;
}
