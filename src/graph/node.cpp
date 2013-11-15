//
//  node.cpp
//  DataFlow Virtual Machine
//
//  Created by Mathijs Saey on 20/09/13.
//  Copyright (c) 2013 Vrije Universiteit Brussel. All rights reserved.
//

#include "node.h"

using namespace core;

Node::Node(const Node &other):
    _output(std::vector<Node *>(other._output)),
    _input(std::vector<Token *>(other._input)),
    _treshold(other._treshold)
    {};

Node& Node::operator= (const Node& rhs) {
    if (this == &rhs) return *this;
    _treshold = rhs._treshold;
    _output = std::vector<Node *>(rhs._output);
    _input = std::vector<Token *>(rhs._input);
    return *this;
}

Node::Node(int treshold):
    _input(std::vector<Token *>(treshold)),
    _treshold(treshold)
    {_input.reserve(_treshold);};

Node::Node(int treshold, std::vector<Node*> &output):
    _output(output),
    _input(std::vector<Token *>(treshold)),
    _treshold(treshold)
    {_input.reserve(_treshold);};


void Node::addOutput(Node * node) {
    _output.push_back(node);
}

const std::vector<Node*> Node::getChildren() {
    return _output;
}

void Node::acceptToken(Token * token) {
    _input.push_back(token);
    
    if (_input.size() >= _treshold) {
        execute();
    }
}

void Node::execute() {
    for (auto i:_output) {
        i->acceptToken(new Token());
    }
}