//
//  edge.h
//  DataFlow Virtual Machine
//
//  Created by Mathijs Saey on 20/09/13.
//  Copyright (c) 2013 Vrije Universiteit Brussel. All rights reserved.
//

#ifndef __DVM_EDGE_H__
#define __DVM_EDGE_H__

#include <iostream>
#include "token.h"

namespace graph {
    class Node;

    /**
     This class represents an edge in a graph
     
     @author Mathijs Saey
     */
    class Edge {
    private:
        const Token   * _token;     /**< A token to be sent to the _to node.*/
        const Node    * _from;      /**< The source node */
        const Node    * _to;        /**< The destination node */
        
    public:
        /**
         Copy constructor
         
         @param other
            The Edge to copy
         */
        explicit Edge(const Edge& other);
        /**
         Initialise an Edge with a from and to node.
         
         @param from
            The from node
         @param to
            The to node
         */
        explicit Edge(const Node* from, const Node* to);
        
        /**
         Initialise an edge with from and to nodes, and a token.
         
         @param from
            The from node
         @param to
            The node.
         @param token
            The token.
         */
        explicit Edge(const Node* from, const Node* to, const Token* _token);
        
        /**
         Assignmen operator
         
         @param rhs
            The right hand side of the assignment
         @return
            A newly initialised edge
         */
        Edge& operator= (const Edge& rhs);
        
    private:
        /**
         Private constructor to avoid autogenerating the default constructor.
         Don't use this.
         */
        explicit Edge();
        
    public:
        
        /**
         Checks if this edge received input
         
         @return
            true if this edge has received
            the token needed to proceed.
            False otherwise.
         */
        inline const bool inputReady();
        
        /** Getter for _token */
        inline const Token* getToken();
        /** Getter for _from */
        inline const Node* getFrom();
        /** Getter for _to */
        inline const Node* getTo();
    };
}

#endif
