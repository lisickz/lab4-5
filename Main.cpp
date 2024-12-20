#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include "Task.h"
#include "HR.h"

using namespace std;

enum Action {
    FIRST = 1,
    KNOWN_WORKERS = 1,
    KNOWN_TASKS = 2,
    NEW_WORKER = 3,
    NEW_TASK = 4,
    ASSIGN_TASK = 5,
    WORKER_SALARY = 6,
    COMBINED_SALARIES = 7,
    QUIT = 8,
    LAST = 8
};

bool isNumber(const string& str) {
    for (char c : str) {
        if (!isdigit(c) && c != '.') {
            return false;
        }
    }
    return true;
}

Action menu();
void do_known_workers(HR& hr);
void do_known_tasks(HR& hr);
void do_new_worker(HR& hr);
void do_new_task(HR& hr);
void do_assign_task(HR& hr);
void do_worker_salary(HR& hr);
string read_nonempty_line(istream& str);

void predefined_data(HR& hr) {
    hr.add_task("clean streets", 100);
    hr.add_task("clean windows", 200);
    hr.add_task("harvest apples", 300);

    hr.add_worker("Amanda");
    hr.add_worker("Linda");
    hr.add_worker("Rose");

    hr.add_task_to_worker("Rose", "clean streets");
    hr.add_task_to_worker("Linda", "clean streets");
    hr.add_task_to_worker("Amanda", "clean streets");
    hr.add_task_to_worker("Amand", "harvest apples");
}

int main() {
    HR hr;
    predefined_data(hr);

    for (;;) {
        Action a = menu();
        if (a == Action::QUIT)
            break;

        switch (a) {
        case Action::KNOWN_WORKERS: do_known_workers(hr); break;
        case Action::KNOWN_TASKS: do_known_tasks(hr); break;
        case Action::NEW_WORKER: do_new_worker(hr); break;
        case Action::NEW_TASK: do_new_task(hr); break;
        case Action::ASSIGN_TASK: do_assign_task(hr); break;
        case Action::WORKER_SALARY: do_worker_salary(hr); break;
        case Action::COMBINED_SALARIES:
            cout << hr.get_combines_salaries() << "\n";
            break;
        }
    }
}

Action menu() {
    for (;;) {
        cout << "1. Workers list\n";
        cout << "2. Tasks list\n";
        cout << "3. New worker\n";
        cout << "4. New task\n";
        cout << "5. Assign task\n";
        cout << "6. Worker salary\n";
        cout << "7. Combined salaries\n";
        cout << "8. Quit\n";

        string n;

        cin >> n;

        if (cin.fail() || !isNumber(n)) {
            cout << "Enter number!\n";
            cin.clear();
        }
        else {
            if (stoi(n) >= Action::FIRST && stoi(n) <= Action::LAST)
                return Action(stoi(n));
            cout << "Enter number between " << Action::FIRST << " and " << Action::LAST << "!\n";
        }

        cout << "Try again\n\n";
    }
}

void do_known_workers(HR& hr) {
    auto ws = hr.get_workers();
    for (const auto& w : ws)
        cout << w.name << "\n";
    cout << "\n";
}

void do_known_tasks(HR& hr) {
    auto ts = hr.get_tasks();
    for (const auto t : ts)
        cout << t->name << " for " << t->price << "\n";
    cout << "\n";
}

void do_new_worker(HR& hr) {
    cout << "Enter worker name: ";
    string s;
    cin >> s;
    hr.add_worker(s);
}

void do_new_task(HR& hr) {
    cout << "Enter task name: ";
    string s = read_nonempty_line(cin);
    cout << "Enter task price: ";
    int p;
    cin >> p;
    if (cin.fail()) {
        cout << "Price should be an integer!\n";
        cin.clear();
        string s;
        getline(cin, s);
        return;
    }
    if (p < 0) {
        cout << "Price should be a positive integer!\n";
    }
    hr.add_task(s, p);
}

void do_assign_task(HR& hr) {
    cout << "Enter task name: ";
    string t = read_nonempty_line(cin);
    cout << "Enter worker name: ";
    string w;
    cin >> w;
    if (!hr.add_task_to_worker(w, t)) {
        cout << "There is no such worker or task\n";
    }
}

void do_worker_salary(HR& hr) {
    cout << "Enter worker name: ";
    string w;
    cin >> w;
    int res = hr.get_worker_salary(w);

    if (res < 0) {
        cout << "Unknown worker\n";
    }
    else {
        cout << res << "\n";
    }
}

string read_nonempty_line(istream& str) {
    for (;;) {
        string s;
        getline(str, s);
        if (s.length() > 0)
            return s;
    }
}
