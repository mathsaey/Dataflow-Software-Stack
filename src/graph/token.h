//
//  token.h
//  DataFlow Virtual Machine
//
//  Created by Mathijs Saey on 20/09/13.
//  Copyright (c) 2013 Vrije Universiteit Brussel. All rights reserved.
//

#ifndef __DVM_TOKEN_H__
#define __DVM_TOKEN_H__

#include <iostream>

namespace graph {
    /**
     This class represents a token
     
     @author Mathijs Saey
     */
    class Token {
    public:
        /**
         Default constructor
         */
        explicit Token();
        
        /**
         Copy constructor
         
        @param other
            Token to copy
         @return
            A newly copied token
         */
        explicit Token(const Token& other);
        
        /**
         Assignment operator
         
         @param rhs
            Right hand side of the assignment
         @return
            The new token.
         */
        Token& operator= (const Token& rhs);
    };
}

#endif
