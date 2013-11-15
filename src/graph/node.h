//
//  node.h
//  DataFlow Virtual Machine
//
//  Created by Mathijs Saey on 20/09/13.
//  Copyright (c) 2013 Vrije Universiteit Brussel. All rights reserved.
//

#ifndef __DVM_NODE_H__
#define __DVM_NODE_H__

#import <vector>
#import "token.h"

namespace core {
    /**
     This class represents a node in a dataflow graph.
     A node represents a single operation on an arbitrary
     amount of input data.
     
     This input data is provided by other elements in the form
     of a Token. Once the node received all of the input tokens it
     needs, it executes it's operation and sends the results to 
     other nodes that are waiting for this data.
     
     @author Mathijs Saey
     */
    class Node {
    private:
        int _treshold;                      /**< Amount of tokens the node needs to activate */
        bool _executed;                     /**< Keeps track of wether this node executed */
        
        std::vector<Token *> _input;  /**< Collection of input tokens */
        std::vector<Node *> _output;  /**< Nodes that are connected to this node */
  
    public:
        /**
         Copy constructor of a node
         
         @param other
            The node to copy
         */
        explicit Node(const Node &other);
        
        /**
         Create a node with a given treshold.
         
         @param treshold
            The amount of tokens the
            node needs to activate.
         */
        explicit Node(int treshold);
        
        /**
         Create a node with a given set of output nodes
         
         @param treshold
            The amount of tokens the
            node needs to activate.
         
         @param output
            A reference to a vector that contains
            the output nodes of this node.
         */
        explicit Node(int treshold, std::vector<Node *> &output);
        
        /**
         Assignment operator
         
         @param rhs
            Right hand side of the assignment
         @return
            A newly created node.
         */
        Node& operator= (const Node& rhs);
        
        /**
         Adds an output node
         
         @param node
            The new output node.
         */
        void addOutput(Node * node);
        
        /**
         Accept a token.
         If the node has more tokens than the treshold after adding this token,
         the node's operation is executed.
         
         @param token
            The token to accept.
         */
        void acceptToken(Token * token);
        
        /**
         Gets all the children of this node.
         
         @return
            The children of this node.
         */
        const std::vector<Node *> getChildren();
        
    private:
        /**
         Default constructor.
         Declared private to avoid default implementation.
         */
        explicit Node();
        
        /**
         Consume all the input tokens, execute the operation
         and send the result to the output.
         */
        void execute();
    };
}

#endif
