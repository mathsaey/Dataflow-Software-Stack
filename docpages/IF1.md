# IF1 Quick Reference

This page serves as a basic introduction to the IF1 language.
The information on this page is based on the paper: `IF1 - An Intermediate Form for Applicative Languages. (Stephen Skedzielewski 1985)`

On this page, we attempt to create a compact IF1 overview that can serve as a full reference to the language while still being complete.
If you like to look at an example while browsing this page, check out [Quicksort in IF1](@ref QSIF1), generated from [this sisal code](@ref QSSis).

[TOC]

# IF1 Concepts # {#Concepts}

IF1 represents directed, acyclic graphs, these graphs have a few components.

* IF1 nodes are operations.
	* a node can have an arbitrary amount of in -and outputs.
	* IF1 defines over 50 nodes, that is, "native" operations.
	* The in -and output of a node happens through **ports**, which are numbered indicators of in and output locations
	* Not every node has a predefined amount of ports.
* Edges represent data paths between nodes.
	* Edges carry **type information**
		* Not mandatory
		* Can describe user-defined types and built-in types.
	* A special edge exists to describe literal constants.
		* Don't contain a source port
		* Contain the text of a literal as a string.
* Graph boundaries surround groups of nodes and edges.

# IF1 Instructions # {#Form}

IF1 instructions are delimited by newlines. The first character after a newline determines the type of instruction the line represents, the rest of the line consists of a number of whitespace separated fields, the amount of which depends on that specific instruction. Any extra text listed after the fields is considered to be a comment, so are lines that start with C. For more information about comments, look into [appendix A](#Comments).

The following table lists the different instructions types.

Character | Represents | Syntax 
----------| -----------|-------
T         | type   						| `T label type_code arg_1 arg_2 `
E 		  | edge 						| `E source_node port destination_node port type `
L 		  | literal						| `L destination_node port type string `
G 		  | subgraph of a compound node | `G type_reference `
G 		  | local function graph 		| `G type_reference "name" `
X 		  | global function graph 		| `X type_reference "name" `
I 		  | imported function   		| `I type_reference "name" `
N 		  | simple node   				| `N label operation `
{		  | start compound node 		| `{ `
}		  | end compound node 			| `} label operation integers 


The semantics of these instructions are explained below, explanation about *labels* and *types* are presented in the [labels and types](#types) section.

* Graph boundaries represent a function and simply contain the type (check out the function type) and name of this function.
* Graph boundaries have a scope associated with them, anything below the boundary declaration is part of the graph's scope until either a "}, G,X or I" is encountered.
* Subgraphs in compound nodes are not required to give a type.
* Edges simply contain the input node, and the port on this node, the destination node, and the port on this node that this edge leads to. Furthermore, the edge also contains the type of it's data.
* Literals contain their destination, the port on this destination, their type and a string version of their counts. [Appendix B](ref #Literal_def) contains an overview of some of the most common literals.

## Labels and Types ## {#types}

IF1 instructions commonly contain a type identifier, the purpose of this section is to explain IF1 type definitions, any defined type is referred to by it's *label*.

Labels are represented by integers, and are used to identify nodes and types. Nodes and types do not share labels, that is, a node and a type may have the same integer as label without being related in any way. Type labels share a global scope, while Node labels only have to be unique within their enclosing graph. It's also worth noting that a missing or unknown type is referred to by using the label 0.

With that being said, we can look at the type definitions:

    T label type_code arg_1 arg_2

* Label can be used to refer to the type later on.
* The type code can be considers to be an argument that indicates what type of type we are dealing with, based on this information, the basic_type is used as another argument to construct the actual type.
* The exact use of the other codes depends on the type_code.

To clarify this, let's look at a  basic sisal types. In this case, the boolean.

`T 1 1 0    %na=Boolean`

* T implies that we are declaring a type
* 1 is the *label* of the type, it will be used to refer to the type we are constructing from now on.
* 1 is the *type_code* of the type. This particular type code tells us that we are dealing with a *basic code*.
* From the information of the type_code, we know that 0 is a basic code, in this case the basic code 0 represents a boolean.
* The rest of the line is a comment, it tells us we are dealing with a boolean.

What follows is a table of the possible type codes and their meaning.

Code | Type 	| Argument 1 | Argument 2  
-----|----------|------------|-----------
0 	 | Array 		| Base type 		| ` none `
1 	 | Basic code 	| Basic code 		| ` none `
2 	 | Field 		| Field type 		| Next field
3 	 | Function 	| Argument type 	| Result type
4 	 | Multiple 	| Base type 		| ` none `
5 	 | Record 		| First field 		| ` none `
6 	 | Stream 		| Base type 		| ` none `
7 	 | Tag			| Tag type 			| Next tag
8 	 | Tuple		| Type 				| Next in tuple
9 	 | Union 		| First Tag 		| ` none `

In the following section, the different types are described.

#### Basic types ####

As the example in the parent section indicates, basic types simply indicate a standard type, the argument is simply a code that tells us which type we are dealing with. A table with the basic types and their code can be found below.

Code | Type
-----|-----
0 	 |	Boolean
1 	 |	Character
2 	 |	Double
3 	 |	Integer
4 	 |	Null
5 	 |	Real
6 	 |	WildBasic*

`* This type does not appear in the official reference, but is generated by sisalc 14.1.

#### Array and Streams ####

Arrays and streams simply point to the *label* of the type they contain.

#### Records and fields, unions and tags. And tuples. ####

A record can be seen as a pointer to a field. It simply contains it's label, the type_code that indicates it's a record and the *label* of it's first field.

A field contains it's label, it's type_code, the *label* of the type it contains, and the *label* of the next field. The last field contains 0 as the *label* that points to the next field.

Unions and tags work in the same way, the only difference is that unions can be seen as a pointer to a tag. A tag points to the next tag like a field points to the next field.

Tuples follow the same contain your own type, point to the next one convention, but don't require an initial pointer.

#### Functions ####

A function type simple contains "pointers" to 2 tuples, the first tuple represents the arguments this function accepts while the second tuple represents the result it returns.

In terms of higher level languages, the function type simple declares the function's signature, without the name.


# Appendix A: Comments {#Comments}

2 main types of comments exist in IF1, stamps and pragmas, stamps are comments that occupy an entire line that starts with `C$`, pragmas are comments that are added after the fields of a line.

## Stamps ## {#Stamps}

Stamps are used to mark some processing that has been done to a file, a few stamp type exists. A stamp line has the following syntax: `C$ stamp_type info`.
The following table provides an overview of the different stamp types.

Character | Meaning
----------|--------
A | Array update analysis
C | Structure checker
D | Order nodes using data dependencies
E | Common subexpression information 
F | Frontend
L | Loop invariant removal
O | Add offsets for use by the interpreter
P | Partitioning analysis
S | Stream analysis
V | Vector analysis

## Pragmas ## {#Pragmas}

Pragmas are used to add additional information to an instruction. Currently, 2 types of pragmas exist, pragmas that are generated by the compiler, and pragmas that are added after analyzing. Multiple pragmas can be added after a single instruction. Pragmas are terminated by a whitespace character. 

Pragmas have the following syntax: `%<id>=<anything>,<otheranything> %<otherid>=<anything>`

The following table provides an overview of the meaning of different pragmas. The type column indicates the type of pragma; C indicates a compiler-generated pragma, while A indicates a pragma generated by analyzing.

Character | Type | Meaning
----------|------|---------
bd | C | bounds
na | C | name
sl | C | source line
op | C | op number with line of source
ar | A | size of activation record needed
lz | A | edge carries a value that must be demanded
mk | A | mark this edge by reference (%mk=r) or by value (%mk=v)
of | A | offset in activation record
st | A | style of memory allocation (%st=p for pointer, %st=c for contiguous)
xy | A | position for node in graphic output

# Appendix B: Literal Definitions {#Literal_def}

Type | String
-----|-------
Function names | "someName"
Boolean values | "T" or "F"
Integer values | "03349"
Characters 	   | "'\n'" or "'x'"
Null value 	   | nil
Single-precision floating point value | "3.503" or "5e3" or ".503"
Double-precision floating point value | "6.626198d-34" ".056D24"

\page QSSis Quicksort in Sisal
\include quicksort.sis

\page QSIF1 Quicksort in IF1
\include quicksort.if1
