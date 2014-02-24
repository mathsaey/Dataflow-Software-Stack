<!-- Written by Mathijs Saey at the VUB, all rights reserved -->

[TOC]

# Introduction {#Introduction}

This is the main documentation of DVM, the Dataflow Virtual Machine, created by Mathijs Saey for his thesis at the VUB.

These pages serve a number of purposes:
* [Provide a basic overview about DVM.](#About)
* [Provide a high-level overview of the code base.](#Structure)
* [Collect the documentation about the DVM code base](files.html)
* [Collect all the necessary information to get DVM up and running](#Start)
* [Collect references and examples that can come in handy while working on DVM.](pages.html)

It should be noted that the version string next to the project name in the header of any page of this documentation corresponds to a commit hash. This hash can be used to find the exact codebase that was used to generate the docs.

Finally, the main repository of this project can be found [on github](https://github.com/mathsaey/DVM).

# About DVM {#About}

The goal of DVM is to create a highly parallel virtual machine. This machine will use the [dataflow architecture](http://en.wikipedia.org/wiki/Dataflow_architecture) to achieve a high amount of concurrency.

## Dataflow {#Dataflow}
<img style="float: right" src="../res/simpleStatic.png" />

In short, the general idea behind [dataflow](http://en.wikipedia.org/wiki/Dataflow_architecture) is that an instruction in the program is executed once it's inputs are ready. This property allows us to exploit the implicit parallelism of programs.

There are 2 general flavors of dataflow, static and dynamic. In static dataflow, the program is represented as a graph, and data travels along the edges of this graph. Each node of the graph represents an operation on this data.

A visual representation of such a dataflow graph can be seen right of this section. This graph was generated from the following Sisal code.

~~~
function main(a, b, c, d : integer returns integer)
	let 
		ab := a + b;
		cd := c + d
	in 
		ab + cd 
	end let
end function
~~~

As we can see, this program simply takes 4 inputs, and adds all of these together. The generated dataflow graph shows us that both of the additions could be carried out in parallel.

The second flavor, dynamic dataflow, is a less intuitive representation, which is better suited to parallel execution. Dynamic dataflow is the model of dataflow that is generally used in practice.
This is because static dataflow is very poor at running the same piece of code without internally copying it. 

In dynamic dataflow, the program is not represented as a graph, instead, the program is represented as a set of instructions kept in the instruction memory. Providing these instructions with data is done through using tagged tokens. 

These tokens consists of 2 pieces, a datum and a tag. The datum is simply the piece of data that we want to transport to some instruction, while the tag contains all the information that the program needs to get this token to it's destination. Furthermore, this tag contains some additional information that allows us to have multiple invocations of the same piece of code without causing concurrency issues. 

Executing the program is now done by sending these tagged tokens to their destinations. These destination instructions will in turn return new tokens, which can be added to the program again, continuing the cycle until we reach the end of our program.

The exact details of a dynamic dataflow architecture are not presented here for the sake of brevity, people looking for a more detailed explanation should consider reading: `Executing a Program on the MIT Tagged-Token Dataflow Architecture` (Arvind and RISHIYUR R.S., 1990).

## Sisal and IF1 {#IF1}

[Sisal](http://en.wikipedia.org/wiki/SISAL) is a language designed to be a high level variant for languages such as PASCAL that can work on multicore machines. During the first compilation phase sisalc (the sisal compiler) compiles Sisal to IF1, an intermediate language, which represents the sisal source code as a dataflow graph. 

The focus of DVM lies on the optimization and execution of dataflow programs, and not on the language or compiler design. For this reason, we decided to use IF1 as the primary input language of DVM. Using DVM in combination with [sisalc](http://sourceforge.net/projects/sisal/) offers us a good language for writing dataflow program, along with a compiler that removes the complexity of the language for us.

More information about IF1 along with some sisal and IF1 code samples can be found in the [IF1 overview](md_doc__i_f1.html). 

## In General {#General}

To recap, DVM is a virtual machine that attempts to achieve high levels of parallelism. In order to do this, DVM utilizes a dynamic dataflow architecture. DVM uses IF1 as an input language, as generated by sisalc, the Sisal compiler. 

# Getting started {#Start}

Running DVM is quite trivial at the moment. All you need is a working [python](http://www.python.org/) interpreter. We recommend using [pypy](http://pypy.org/) if you want to benchmark DVM or test it for speed. However, wherever possible, compatibility is maintained with CPython, the default python interpreter.

You need to install [sisalc](http://sourceforge.net/projects/sisal/), the sisal C compiler if you want to produce your own IF1 files from sisal source code.

For the time being, input files are manually added in the source code. A decent way to invoke DVM from the command line is planned for the future.

The sites of all these tools and the used versions can be found below:

Command  | Version | Website
---------|---------|--------
`sisalc` | 14.1.0  | http://sourceforge.net/projects/sisal/
`python` | 2.7.6   | http://www.python.org/
`pypy`   | 2.2.1   | http://pypy.org/

## On Python and speed {#Performance}

Running a virtual machine on an interpreted language seems like a pretty bad idea. Python performance is pretty slow, even with the speedup that using pypy nets us. So why did we opt to use python instead of going for a fast language, such as C++?

The use of python can be explained by a number of reasons. First of all, using python significantly speeds up development time, which is important in a project with a limited amount of time. Secondly, rapid prototyping and testing multiple approaches to a single problem is quite important due to the academic nature of our work. Initially, we only wanted to use python for a prototyping stage, but time constraints led us to using python as our primary language. A [C++ version](https://github.com/mathsaey/DVM/tree/DVM%2B%2B) of DVM is in the works, but no progress should be expected anytime soon, or even at all.

# Overall Structure {#Structure}

DVM is split up into a few components:

* [The IF1 Parser](\ref if1parser)
* IGR, the Intermediate Graph Representation
* The ::compiler, which transforms IGR and converts it to work with the runtime
* DVM, the actual execution engine.

The first 3 components of this list are dependent on one another, and on DVM. DVM itself however, is not dependent on any of the other modules.