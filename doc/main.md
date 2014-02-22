<!-- Written by Mathijs Saey at the VUB, all rights reserved -->

[TOC]

# Introduction {#Introduction}

This is the main documentation of DVM, the Dataflow Virtual Machine, created by Mathijs Saey for his thesis at the VUB.

These pages serve a number of purposes:
* [Provide a basic overview about DVM.](#About)
* [Provide a high-level overview of the code base.](#Structure)
* [Collect the documentation about the DVM code base](annotated.html)
* [Collect all the necessary information to get DVM up and running](#Starting)
* [Collect references and examples that are come in handy for working on DVM.](pages.html)

# About DVM {#About}

The goal of DVM is to create a highly parallel virtual machine. In order to do this, we use the [dataflow architecture.](http://en.wikipedia.org/wiki/Dataflow_architecture) 

## Dataflow {#Dataflow}

In short, the general idea behind dataflow is that an instruction in the program is executed once it's inputs are ready. This property allows us to exploit the implicit parallelism of programs.

There are 2 general flavors of dataflow, static and dynamic dataflow. In static dataflow, the program is represented as a graph, and data travels along the edges of this graph. 

An example of such a dataflow graph can be found below, this graph was generated from the following sisal (more on that later) code:

~~~~~~~~~~~
define Main

function main(a, b, c, d : integer returns integer)
	let 
		ab := a + b;
		cd := c + d
	in 
		ab + cd 
	end let
end function
~~~~~~~~~~~

As we can seem this program simply takes 4 inputs, and adds all of these together. The generated dataflow graph shows us that both of the additions could be carried out in parallel.

![A simple dataflow graph](../res/staticSimple.png)

Dynamic dataflow is slightly more tricky, having the entire program in memory causes some issues when dealing with multiple simultaneous calls to the same function or loops. Furthermore, a program graph is not a great internal representation even though it's arguably easier to understand for a human.

Dynamic dataflow works with a static instruction memory instead of a program graph. An instruction in this memory performs roughly the same task as a node in the dataflow graph. The main difference with static dataflow is that program data does not follow predefined edges, instead, all the data travels through the program wrapped in a *tagged token*. Such a token contains not only the actual data being sent, but also the destination of this data and the *context* of this data. Adding this context to program data is what allows the dynamic dataflow model to have multiple simultaneous invocations of the same function.

People looking for a detailed explanation about dynamic dataflow should consider reading: `Executing a Program on the MIT Tagged-Token Dataflow Architecture` (Arvind and RISHIYUR R.S., 1990).

## [Sisal](http://en.wikipedia.org/wiki/SISAL) and IF1 {#IF1}

Sisal (Streams and Iteration in a Single Assignment Language) is a language designed to be a high level variant for languages such as PASCAL that can work on multicore machines. During the first compilation phase sisalc (the sisal compiler) compiles Sisal to IF1, an intermediate language, which represents the sisal source code as a dataflow graph. 

Since DVM is focused on the execution of dataflow programs, and not in it's compilation, we use IF1 as the primary input language of DVM. Internally, we still have our own compiler that converts IF1 into our own intermediate representation (::IGR)


# Getting started

Running DVM should be straightforward if you have the right tools installed. A guide on the command line usage of DVM will be found here once the project reaches that stage.

Code should be manually loaded in the main file for the time being.

## Software 

Due to the academic nature of our work, we decided to write the code in python, favoring rapid development over speed. A [C++ version](https://github.com/mathsaey/DVM/tree/DVM%2B%2B) of DVM is under construction, but the current focus lies on the rapid feature addition that python offers us. 
In order to compensate for this, we decided to use [pypy](http://pypy.org/) to run our python code. As of writing, the code is compatible with pypy 2.2.1 and CPython 2.7.5.

All in all, the following software was used:

Command  | Version | Website | Use
---------|---------|---------|----
`sisalc` | 14.1.0  | http://sourceforge.net/projects/sisal/ | Compile Sisal files to IF1
`python` | 2.7.6   | http://www.python.org/                 | Language of choice
`pypy`   | 2.2.1   | http://pypy.org/                       | Faster python execution 

In order to run DVM, you should at least have python 2.7 installed on your machine, pypy is preferred. You should also install sisalc to avoid writing IF1 code by hand.

# Overall Structure

DVM is split up into a few components:

* The IF1 Parser
* IGR, the Intermediate Graph Representation
* The compiler, which transforms IGR and converts it to work with the runtime
* DVM, the actual execution engine.

The first 3 components of this list are dependent on one another, and on DVM. DVM itself however, is not dependent on any of the other modules.

Information about each of these modules can be found in their documentation.

# Other Information

Check out the [related pages](pages.html) section for some additional information about the project. Especially interesting is the [IF1 overview](md_doc__i_f1.html), which is the only online IF1 reference that I know off.