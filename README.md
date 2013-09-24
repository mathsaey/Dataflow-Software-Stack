# About

This is the repository of the master thesis of Mathijs Saey at the Vrije Universiteit Brussel.
The goal of this project is the creation of a dataflow virtual machine that interprets the IF1 dataflow graph language.

More info about the project can be found on the [documentation](http://mathsaey.github.io/DVM/) pages of this project.

# Context

## [Dataflow](http://en.wikipedia.org/wiki/Dataflow_architecture)

The dataflow architecture is an architecture that differs from the von Neumann architecture seen in most mainstream programming languages these days.
The idea behind dataflow is that instructions are executed when all of the data they depend on is available.

## IF1 and [Sisal](http://en.wikipedia.org/wiki/SISAL)

Sisal (Streams and Iteration in a Single Assignment Language) is a language designed to be a high level variant for languages such as PASCAL that can work on multicore machines.
sisalc, the sisal compiler, is compiled to the IF1 intermediate language, which represents the sisal source code as a dataflow graph. 

## Goal, revisited

> The goal of this project is the creation of a dataflow virtual machine that interprets the IF1 dataflow graph language.

The goal of this project is the creation of a virtual machine that internally works according to the dataflow model. This VM will be able to parse IF1 files. Other languages could be added later, but IF1 was chosen for the goals of this project since it is already represents a dataflow graph.