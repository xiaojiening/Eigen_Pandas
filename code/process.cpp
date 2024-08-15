#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <chrono>
#include <iomanip> // for setprecision
#include <utility>
#include <sys/ioctl.h>
#include <unistd.h>
#include "../eigen-3.4.0/Eigen/Dense"

using namespace Eigen;
using namespace std;
using namespace std::chrono;

// typedef Eigen::Matrix< long double, Eigen::Dynamic, 1> Vec;
// using Vec = Eigen::VectorXd;
using Vec = Eigen::ArrayXd;

// 读取 csv 文件
vector<vector<string>> readCSV(const string& filename) {
    vector<vector<string>> data;
    ifstream file(filename);
    
    if (!file.is_open()) {
        cerr << "Unable to open file: " << filename << endl;
        return data;
    }

    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string field;
        vector<string> row;

        while (getline(ss, field, ',')) {
            row.push_back(field);
        }

        data.push_back(row);
    }

    file.close();
    return data;
}

// Debug：打印 csv 数据
void printCSV(const vector<vector<string>>& data) {
    for (const auto& row : data) {
        for (const auto& field : row) {
            cout << field << " ";
        }
        cout << endl;
    }
}

// 从 csv 数据中提取指定列并转换为 Eigen 向量
Vec getColumnAsVector(const vector<vector<string>>& data, const string& col_name) {
    Vec columnVector;
    if (data.empty()) return columnVector;

    // 找到指定名称的列的索引
    vector<string> header = data.front();
    auto it = find(header.begin(), header.end(), col_name);
    if (it == header.end()) {
        cerr << "Column name not found: " << col_name << endl;
        return columnVector; // Return empty vector if column not found
    }
    size_t col_index = distance(header.begin(), it);

    // 重置 Eigen 向量的大小为行数（不包括标题）
    columnVector.resize(data.size() - 1);

    // 从指定列中提取数据并保存为 Eigen 向量
    for (size_t i = 1; i < data.size(); ++i) {
        try {
            columnVector(i - 1) = stold(data[i][col_index]);
        } catch (const invalid_argument& e) {
            cerr << "Invalid data in column " << col_name << ": " << e.what() << endl;
            columnVector(i - 1) = 0; // 非法数据将被替换为 0
        }
    }

    return columnVector;
}

// 从 csv 数据中提取指定列并转换为普通 vector<string>
vector<string> getColumnAsVectorString(const vector<vector<string>>& data, const string& col_name) {
    vector<string> columnVector;
    if (data.empty()) return columnVector;

    // 找到指定名称的列的索引
    const vector<string>& header = data.front();
    auto it = find(header.begin(), header.end(), col_name);
    if (it == header.end()) {
        cerr << "Column name not found: " << col_name << endl;
        return columnVector; // Return empty vector if column not found
    }
    size_t col_index = distance(header.begin(), it);

    // 重置 Eigen 向量的大小为行数（不包括标题）
    columnVector.resize(data.size() - 1);

    // 从指定列中提取数据并保存为普通向量
    for (size_t i = 1; i < data.size(); ++i) {
        columnVector[i - 1] = data[i][col_index];
    }

    return columnVector;
}

// 计算加权收益
std::unordered_map<std::string, long double> calculateWeightedProfit(const Vec& profit, const Vec& weight, const std::vector<std::string>& date) {
    auto weighted_profit = profit * weight;
    // auto weighted_profit = profit.cwiseProduct(weight);
    
    // 使用 unordered_map 按日期分组并计算加权利润总和
    std::unordered_map<std::string, long double> date_to_weighted_profit;
    date_to_weighted_profit.reserve(date.size());  

    for (int i = 0; i < date.size(); ++i) {
        date_to_weighted_profit[date[i]] += weighted_profit(i);
    }

    return date_to_weighted_profit;
}

// Debug：进度条
void print_progress(int progress, int total) {
    struct winsize ws;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws);
    int width = ws.ws_col - 50;  // 进度条的宽度
    float ratio = static_cast<float>(progress) / total;
    int pos = static_cast<int>(width * ratio);

    cout << "Processing: " << setw(3) << static_cast<int>(ratio * 100) << "%|";
    for (int i = 0; i < width; ++i) {
        if (i < pos)
            cout << "█";
        else
            cout << " ";
    }
    cout << "| " << progress << "/" << total << "\r";
    cout.flush();
}

int main() {
    vector<string> nums = {"500", "1000", "1500", "2000", "2500", "3000", "3500", "4000", "4500", "5000"};
    vector<pair<string, string>> years = {{"1", "2020"}, {"2", "2021"}, {"3", "2022"}, {"4", "2023"}, {"5", "2024"}};
    int total_tasks = nums.size() * years.size();
    int current_task = 0;
    ofstream results_file("../result/eigen_analysis.csv");
    results_file << "stocks,years,time\n";

    for (const auto& num : nums) {
        for (const auto& year_pair : years) {
            auto data = readCSV("../data/stocks_n" + num + "_y" + year_pair.first + ".csv");
            auto profit = getColumnAsVector(data, "profit");
            auto weight = getColumnAsVector(data, "weight");
            auto date = getColumnAsVectorString(data, "date");

            auto start_time = high_resolution_clock::now();
            auto weighted_profit = calculateWeightedProfit(profit, weight, date);
            auto end_time = high_resolution_clock::now();
            duration<double> elapsed = end_time - start_time;

            // 将结果写入 CSV 文件
            ofstream file("../data/e_weighted_profit_n" + num + "_y" + year_pair.first + ".csv");
            file << fixed << setprecision(16); 
            file << "date,weighted_profit\n";
            for (const auto& entry : weighted_profit) {
                file << entry.first << "," << entry.second << "\n";
            }
            file.close();

            // 记录耗时
            results_file << num << "," << year_pair.first << "," << elapsed.count() << endl;
            
            // 更新进度条
            ++current_task;
            print_progress(current_task, total_tasks);
        }
    }
    cout << endl;

    return 0;
}