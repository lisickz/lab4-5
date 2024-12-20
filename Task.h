#pragma once
#ifndef TASK_H
#define TASK_H

#include <string>

class Task {
public:
    Task(const std::string& n, int p);
    std::string name;
    int price;
};

#endif // CLASS_H
