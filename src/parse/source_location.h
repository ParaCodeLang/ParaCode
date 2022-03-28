#pragma once

#include <tuple>

class SourceLocation
{
public:
    std::string filename;
    int col = 1;
    int row = 1;

    SourceLocation(std::string filename, int col = 1, int row = 1) {
        this->filename = filename;
        this->col = col;
        this->row = row;
    }

    std::tuple<int, int> colRow() {
        return std::make_tuple(this->col, this->row);
    }
};
