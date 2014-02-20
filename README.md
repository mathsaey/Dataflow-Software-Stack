# About

This is the repository of the master's thesis of Mathijs Saey at the Vrije Universiteit Brussel.
The goal of DVM is the creation of a dataflow virtual machine, along with a compiler that allows it to
run IF1 programs.

## [Dataflow](http://en.wikipedia.org/wiki/Dataflow_architecture)

The dataflow architecture is an architecture that differs from the von Neumann architecture seen in most mainstream programming languages these days.
The idea behind dataflow is that instructions are executed when all of the data they depend on is available.

## IF1 and [Sisal](http://en.wikipedia.org/wiki/SISAL)

Sisal (Streams and Iteration in a Single Assignment Language) is a language designed to be a high level variant for languages such as PASCAL that can work on multicore machines. During the first compilation phase sisalc (the sisal compiler) compiles Sisal to IF1, an intermediate language, which represents the sisal source code as a dataflow graph. 

We use IF1 due to it's dataflow semantics. These semantics allow us to easily map IF1 to IGR, our own intermediate representation.

# Getting Started.

If you are interested in working with or using DVM, you should look at the [documentation](http://mathsaey.github.io/DVM/index.html). It contains the complete DVM documentation, a detailed IF1 overview and a guide to get DVM up and running. It also contains an overview of the tools that were used to run and create dvm.