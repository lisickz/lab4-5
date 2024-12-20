#pragma once
#ifndef HR_H
#define HR_H

#include <vector>
#include <string>
#include "Task.h"

class Worker {
public:
    Worker(const std::string& n) : name(n) {}

    int salary() const;

    std::string name;
    std::vector<Task*> tasks;
};
class HR {
public:
    ~HR();
    void add_task(const std::string& name, int price);
    void add_worker(const std::string& name);
    bool add_task_to_worker(const std::string& name, const std::string& task);
    void fire_worker(const std::string& name);
    const std::vector<Task*>& get_tasks() const;
    const std::vector<Worker>& get_workers() const;
    int get_worker_salary(const std::string& name) const;
    int get_combines_salaries() const;

private:
    std::vector<Task*> tasks;
    std::vector<Worker> workers;
};


#endif 
