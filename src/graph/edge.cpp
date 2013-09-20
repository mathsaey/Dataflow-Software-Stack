//
//  edge.cpp
//  DataFlow Virtual Machine
//
//  Created by Mathijs Saey on 20/09/13.
//  Copyright (c) 2013 Vrije Universiteit Brussel. All rights reserved.
//

#include "edge.h"
#include "node.h"

using namespace graph;

Edge::Edge(const Edge& other):
    _to(other._to),
    _from(other._from),
    _token(other._token) {};

Edge::Edge(const Node* from,const Node* to):
    _to(to),
    _from(from),
    _token(NULL){};

Edge& Edge::operator= (const Edge& rhs) {
    // Check for self assignment
    if (this == &rhs) return *this;

    _to     = rhs._to;
    _from   = rhs._from;
    _token  = rhs._token;
    return *this;
}

const Token* Edge::getToken() {
	return _token;
}
const Node* Edge::getFrom() {
	return _from;
}
const Node* Edge::getTo() {
	return _to;
}

const bool Edge::inputReady() {
    return _token != NULL;
}