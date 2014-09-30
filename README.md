# About

This is the repository of the master's thesis of Mathijs Saey at the Vrije Universiteit Brussel. The goal of this thesis was the creation of a dataflow software stack on modern hardware. Concretely, this repo contains a prototypical Dataflow Virtual Machine (DVM), alongside a compiler (DISc), which can transform a subset of (Sisal/IF1) programs into valid DVM programs. 

## [Dataflow](http://en.wikipedia.org/wiki/Dataflow_architecture)

The dataflow architecture is a computer architecture which differs from the more traditional von Neumann architecture. 
The idea behind dataflow is that instructions are executed when all of the data they depend on is available.

## IF1 and [Sisal](http://en.wikipedia.org/wiki/SISAL)

Sisal (Streams and Iteration in a Single Assignment Language) is an implicitly parallel language designed to be a high level variant for languages such as PASCAL that can work on multicore machines. During the first compilation phase sisalc (the sisal compiler) compiles Sisal to IF1, an intermediate language, which represents the sisal source code as a dataflow graph. We can utilize IF1 as an input to our software stack.

# Getting Started.

If you are interested in working with or using DVM or DISc, you should look at the [documentation](http://mathsaey.github.io/Dataflow-Software-Stack/index.html). It contains the complete DVM and DISc documentation, a detailed IF1 overview and a guide to get DVM and DISc up and running.