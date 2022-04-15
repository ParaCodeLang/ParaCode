#pragma once

class Stack {
public:
    std::vector<BasicValue*> stack;
    
    Stack() {
        this->stack = {};
    }

    void push(BasicValue* value) {
        this->stack.push_back(value);
    }

    BasicValue* pop(std::string expectedType = "") {
        BasicValue* val = this->stack.back()->clone();
        this->stack.pop_back();
        if (expectedType != "" && expectedType.c_str() != typeid(val).name()) {
            throw std::runtime_error(Util::format("Stack value(%s) != expected value(%s)", typeid(val).name(), expectedType.c_str()));
        }
        return val;
    }
};
