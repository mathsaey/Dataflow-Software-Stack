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

namespace graph {
    /**
     This class represents a node in a graph
     
     @author Mathijs Saey
     */
    class Node {
    private:
        std::vector<const Node *> _output;   /**< Nodes that are connected to this node */
  
    public:
        /**
         Create a node with no output nodes
         */
        explicit Node();
        
        /**
         Copy constructor of a node
         
         @param other
            The node to copy
         */
        explicit Node(const Node &other);
        
        /**
         Create a node with a given set of 
         output nodes
         
         @param output
            A reference to a vector that contains
            the output nodes of this node.
         */
        explicit Node(std::vector<const Node*> &output);
        
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
        void addOutput(const Node * node);
        
        /**
         Gets all the children of this node.
         
         @return
            The children of this node.
         */
        const std::vector<const Node*> getChildren() const;
    };
}

#endif
