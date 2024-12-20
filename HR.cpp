#include "HR.h"
#include <algorithm>

Task::Task(const std::string& n, int p) : name(n), price(p) {}

int Worker::salary() const {
    int s = 0;
    for (int i = 0; i < tasks.size(); i++) {
        s += tasks[i]->price;
    }
    return s;
}

HR::~HR() {
    for (int i = 0; i < tasks.size(); i++) {
        delete tasks[i];
    }
}

void HR::add_task(const std::string& name, int price) {
    tasks.push_back(new Task(name, price));
}

void HR::add_worker(const std::string& name) {
    workers.push_back(Worker{ name });
}

bool HR::add_task_to_worker(const std::string& name, const std::string& task) {
    auto w = std::find_if(workers.begin(), workers.end(),
        [name](const Worker& w) {return w.name == name; });
    if (w == workers.end()) return false;

    auto t = std::find_if(tasks.begin(), tasks.end(),
        [task](const Task* t) {return t->name == task; });
    if (t == tasks.end()) return false;

    w->tasks.push_back(*t);
    return true;
}

void HR::fire_worker(const std::string& name) {
    auto w = std::find_if(workers.begin(), workers.end(),
        [name](const Worker& w) {return w.name == name; });
    if (w == workers.end()) return;
    workers.erase(w);
}

const std::vector<Task*>& HR::get_tasks() const {
    return tasks;
}

const std::vector<Worker>& HR::get_workers() const {
    return workers;
}

int HR::get_worker_salary(const std::string& name) const {
    auto w = std::find_if(workers.begin(), workers.end(),
        [name](const Worker& w) {return w.name == name; });
    if (w == workers.end()) return -1;
    return w->salary();
}

int HR::get_combines_salaries() const {
    int s = 0;
    for (const auto& w : workers) {
        s += w.salary();
    }
    return s;
}