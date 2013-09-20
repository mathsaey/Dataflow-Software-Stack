//
//  node.cpp
//  DataFlow Virtual Machine
//
//  Created by Mathijs Saey on 20/09/13.
//  Copyright (c) 2013 Vrije Universiteit Brussel. All rights reserved.
//

#include "node.h"

using namespace graph;

Node::Node() {};

Node::Node(const Node &other):
    _output(other._output) {};

Node::Node(std::vector<const Node*> &output):
    _output(output) {};

Node& Node::operator= (const Node& rhs) {
    if (this == &rhs) return *this;
    _output = rhs._output;
    return *this;
}

void Node::addOutput(const Node * node) {
    _output.push_back(node);
}

const std::vector<const Node*> Node::getChildren() const {
    return _output;
}
