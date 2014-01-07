# IF1 Quick Reference

This page serves as a basic introduction to the IF1 language.
The information on this page is based on the paper: `IF1 - An Intermediate Form for Applicative Languages. (Stephen Skedzielewski 1985)`

On this page, we attempt to create a compact IF1 overview that can serve as a full reference to the language while still being complete.
If you like to look at an example while browsing this page, check out [a sorting algorithm in IF1](@ref SortIF1), generated from [this sisal code](@ref SortSis).

[TOC]

# IF1 Concepts {#Concepts}

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

# IF1 Instructions {#Form}

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
}		  | end compound node 			| `} label operation association_list_length association_list_element_1 association_list_element_2 ...`


The semantics of these instructions are explained below, explanation about *labels* and *types* are presented in the [labels and types](#types) section.

* Simple nodes simply contain a label and an identifier, this identifier represents a native IF1 instruction. 
* Compound nodes contain subgraphs and represent more complex operations, such as a for loop.
* The compound node contains a few subgraphs that represent parts of the compound node, such as the initialization and the condition check, the association list shows which subgraphs represent which action.
* Graph boundaries represent a function and simply contain the type (check out the function type) and name of this function.
* Graph boundaries have a scope associated with them, anything below the boundary declaration is part of the graph's scope until either a "}, G,X or I" is encountered.
* Subgraphs in compound nodes are not required to give a type.
* Edges simply contain the input node, and the port on this node, the destination node, and the port on this node that this edge leads to. Furthermore, the edge also contains the type of it's data.
* Literals contain their destination, the port on this destination, their type and a string version of their counts. [Appendix B](ref #Literal_def) contains an overview of some of the most common literals.

## Labels and Types {#types}

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

#### Basic types

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

#### Array and Streams

Arrays and streams simply point to the *label* of the type they contain.

#### Records and fields, unions and tags. And tuples.

A record can be seen as a pointer to a field. It simply contains it's label, the type_code that indicates it's a record and the *label* of it's first field.

A field contains it's label, it's type_code, the *label* of the type it contains, and the *label* of the next field. The last field contains 0 as the *label* that points to the next field.

Unions and tags work in the same way, the only difference is that unions can be seen as a pointer to a tag. A tag points to the next tag like a field points to the next field.

Tuples follow the same contain your own type, point to the next one convention, but don't require an initial pointer.

#### Functions

A function type simple contains "pointers" to 2 tuples, the first tuple represents the arguments this function accepts while the second tuple represents the result it returns.

In terms of higher level languages, the function type simple declares the function's signature, without the name.


# Appendix A: Comments {#Comments}

2 main types of comments exist in IF1, stamps and pragmas, stamps are comments that occupy an entire line that starts with `C$`, pragmas are comments that are added after the fields of a line.

## Stamps {#Stamps}

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

## Pragmas {#Pragmas}

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

# Appendix C: Nodes {#Nodes}

<!--
arith = integer real double
algeb = arith + bool
atom = algeb + char
T = any
-->

The next section desribes both the simple and compound nodes that IF1 predefines, a few datatype conventions should be established for this.

* *arith* types correspond to any numeric type
* *algeb* types correspond to arith types and booleans
* *atom*  types correspond to algeb types and characters
* *T* corresponds to any type
* `(T)+` Represents one or more occurence of T
* `(T)*` Represents zero or more occurence of T
* `[T]` Represents one or zero occurence of T
* `AS(T)` Represents an array or a stream that contains type T.
* `ASM(T)` Represents an array,stream or multiple that contains type T.


## Simple nodes {#Nodes_Simple}

Label 	| Name 					| Input 						| Output 							| Operation
--------|-----------------------|-------------------------------|-----------------------------------|----------
100 	| AAddH					| `AS(T) x T` 					| 	`AS(T)`							| Add an element to the back of the array/stream
101 	| AAddL					| `AS(T) x T` 					|	`AS(T)`							| Add an element to the front of the array/stream
102 	| AAdjust				| **Unknown**					|	**Unknown**						| **Unknown**
103 	| ABuild				| `Int x (T)*` 					| 	`AS(T)`							| Create an array/stream with a lower bound, following arguments are elements of the array
104 	| ACatenate				| `AS(T) x (AS(T))+` 			| 	`Array(T)`						| Catenate arrays/streams.
105 	| AElement				| `AS(T) x Int` 				| 	`T`								| Returns element at a given index. 
106 	| AFill					| `Int x Int x (T)*` 			| 	`AS(T)`							| Create an array/stream with a lower and upper bound and fill it with the last argument.<br/> An empty array/stream is created if the lower bound > upper bound
107 	| AGather				| `Int x Mult(T) x [Mult(T)]` 	| 	`AS(T)`							| **Only used in return subgraph** <br/>Creates an array or stream with the values of the 2nd argument, <br/>if the corresponding 3rd argument is true (or not given <br/>The first argument represents the lower bound of the array.
108 	| AIsEmpty				| `AS(T)` 						| 	`Bool`							| Returns True if the array/stream is empty
109 	| ALimH					| `AS(T)` 						| 	`Int`							| upper bound of array/stream
110 	| ALimL					| `AS(T)` 						| 	`Int`							| lower bound of array/stream (always 1 in case of a stream)
111 	| ARemH					| `ASM(T)` 						| 	`ASM(T)`						| Remove last element, returns error if empty
112 	| ARemL					| `ASM(T)` 						| 	`ASM(T)`						| Remove first element, returns error if empty
113 	| AReplace				| `Array(T) x Int x (T)+` 		| 	`Array(T)`						| Returns a new array with with the given value at the given idx of the old array. <br/> If multiple values are provided, they are placed consecutively
114 	| AScatter				| `AS(T)` 						| 	`Multiple(T) x Multiple(Int)`	| **Only appears in generator of forall nodes** <br/>Places array at port one, and the indices of this array at port 2.
115 	| ASetL					| `Array(T) x Int` 				| 	`Array(T)`						| Shifts the lower index of the array, all indices are shifted to reflect this
116 	| ASize					| `AS(T)` 						| 	`Int`							| Returns the amount of elements in the highest dimension of the stream/array
117 	| Abs					| `Arith` 						| 	`Arith`							| Absolute value
118 	| BindArguments			| `Func x (T)*` 				| 	`Func`							| Returns a new function with the given arguments bound to it.
119 	| Bool					| `Int` 						| 	`Bool`							| 0 => false, 1 => true, anything else => error
120 	| Call					| `Func x (T)*`  				|	`(T)+`							| Call a function (function is represented as literal)
121 	| Char					| `Int`  						|	`Char`							| Maps to the appropriate error value (or to an error)
122 	| Div					| `Arith x Arith`  				|	`Arith`							| Division, when applied to integer, round to integer.
123 	| Double				| `Real OR Int`  				|	`Double`						| Converts to double, returns an error if the value cannot be represented as a double
124 	| Equal					| `Atom x Atom`  				|	`Boolean`						| `==`
125 	| Exp					| `Arith x Arith`  				|	`Arith`							| `exp(x,y) = x^y` May lead to errors depending on input
126 	| FirstValue			| `Mult(T) x [Mult(Bool)]`  	|	`T`								| **Only used in return subgraph** <br/>Returns the first value for which the corresponding bool is true (if present)
127 	| FinalValue			| `Mult(T) x [Mult(Bool)]`  	|	`T`								| **Only used in return subgraph** <br/>Returns the last value for which the corresponding bool is true (if present)
128 	| Floor					| `Real OR Double`  			|	`Int`							| Rounds down, returns error if the result is not in the integer range.
129 	| Int					| `Atom`  						|	`Int`							| Real or double get rounded (floor after adding 0,5). Charachters returns the matching ASCII code. <br/>False maps to 0, True maps to 1. <br/>Returns an error if the value is out of the integer range.
130 	| IsError				| `T x T`  						|	`Boolean`						| Returns true if the second error has the same value as the first (string literal). <br/>If the first value is the special *error* value, this function should match any error value.
131 	| Less					| `Atom x Atom` 				|	`Boolean`						| `<` Both inputs should be of the same type
132 	| LessEqual				| `Atom x Atom` 				|	`Boolean`						| `=<` Both inputs should be of the same type. Also represents boolean implication
133 	| Max					| `Algeb x Algeb` 				|	`Algeb`							| Maximum when used on *arith* types, *or* when used on boolean types
134 	| Min					| `Algeb x Algeb` 				|	`Algeb`							| Minimum when used on *arith* types, *and* when used on boolean types
135 	| Minus					| `Arith x Arith` 				|	`Arith`							| `-`
136 	| Mod					| `Arith x Arith` 				|	`Arith`							| Modulo
137 	| Neg					| `Arith` 						| 	`Arith`							| Negation
138 	| NoOp					| `(T)+` 						| 	`(T)+`							| Returns the input
139 	| Not					| `Boolean`						| 	`Boolean`						| Not
140 	| NotEqual				| `atom x atom`					| 	`Boolean`						| `!=` Also represents exclusive or when used on boolean types
141 	| Plus					| `Algeb x Algeb`				| 	`Algeb`							| `+` when used on *arith* types, *or* when used on boolean types
142 	| RangeGenerate			| `Int x Int`					| 	`Multiple(Int)`					| **Only appears in forall generator** <br/>Generates an inclusive sequence between the first and second int.
143 	| RBuild				| **Unknown**					|	**Unknown**						| **Unknown**
144 	| RElements				| **Unknown**					|	**Unknown**						| **Unknown**
145 	| RReplace				| **Unknown**					|	**Unknown**						| **Unknown** 
146	<br/>147<br/>148<br/>149| RedLeft<br/>RedRight<br/>RedTree<br/>Reduce | `func x T x Mult(T) x [Mult(Bool)]` | `T` |  **Only used in return subgraph** <br/>Works like foldl, the 3rd argument determines if this element is used. <br/>The suffixes determine if the function is left, right, undetermined or pairwise associative. <br/>func is a string literal representing one of the following functions: <br/> {*sum, product,least, greatest, catenate*}
150 	| RestValues			| **Unknown**					| 	**Unknown**						| **Unknown**
151 	| Single				| `Double OR Int`				| 	`Real`							| Converts to real, error if it's outside the range of real numbers.
152 	| Times					| `Algeb x Algeb`				| 	`Algeb`							| `*` when used on *arith* types, *and* when used on boolean types
153 	| Trunc					| **Unknown**					|	**Unknown**						| **Unknown**
154 	| PrefixSize			| **Unknown**					|	**Unknown**						| **Unknown**
155 	| Error					| **Unknown**					|	**Unknown**						| **Unknown**
156 	| ReplaceMulti			| **Unknown**					|	**Unknown**						| **Unknown**
157 	| Convert				| **Unknown**					|	**Unknown**						| **Unknown**
158 	| CallForeign			| **Unknown**					|	**Unknown**						| **Unknown**
159 	| AElementN				| **Unknown**					|	**Unknown**						| **Unknown**
160 	| AElementP				| **Unknown**					|	**Unknown**						| **Unknown**
161 	| AElementM				| **Unknown**					|	**Unknown**						| **Unknown**
170 	| AAddLAT				| **Unknown**					|	**Unknown**						| **Unknown**
171 	| AAddHAT				| **Unknown**					|	**Unknown**						| **Unknown**
172 	| ABufPartition			| **Unknown**					|	**Unknown**						| **Unknown**
173 	| ABuildAT				| **Unknown**					|	**Unknown**						| **Unknown**
174 	| ABufScatter			| **Unknown**					|	**Unknown**						| **Unknown**
175 	| ACatenateAT			| **Unknown**					|	**Unknown**						| **Unknown**
176 	| AElementAT			| **Unknown**					|	**Unknown**						| **Unknown**
177 	| AExtractAT			| **Unknown**					|	**Unknown**						| **Unknown**
178 	| AFillAT				| **Unknown**					|	**Unknown**						| **Unknown**
179 	| AGatherAT				| **Unknown**					|	**Unknown**						| **Unknown**
180 	| ARemHAT				| **Unknown**					|	**Unknown**						| **Unknown**
181 	| ARemLAT				| **Unknown**					|	**Unknown**						| **Unknown**
182 	| AReplaceAT			| **Unknown**					|	**Unknown**						| **Unknown**
183 	| ArrayToBuf			| **Unknown**					|	**Unknown**						| **Unknown**
184 	| ASetLAT				| **Unknown**					|	**Unknown**						| **Unknown**
185 	| DefArrayBuf			| **Unknown**					|	**Unknown**						| **Unknown**
186 	| DefRecordBuf			| **Unknown**					|	**Unknown**						| **Unknown**
187 	| FinalValueAT			| **Unknown**					|	**Unknown**						| **Unknown**
188 	| MemAlloc				| **Unknown**					|	**Unknown**						| **Unknown**
189 	| BufElements			| **Unknown**					|	**Unknown**						| **Unknown**
190 	| RBuildAT				| **Unknown**					|	**Unknown**						| **Unknown**
191 	| RecordToBuf			| **Unknown**					|	**Unknown**						| **Unknown**
192 	| RElementsAT			| **Unknown**					|	**Unknown**						| **Unknown**
193 	| ReduceAT				| **Unknown**					|	**Unknown**						| **Unknown**
19  	| ShiftBuffer			| **Unknown**					|	**Unknown**						| **Unknown**
195 	| ScatterBufPartitions	| **Unknown**					|	**Unknown**						| **Unknown**
196 	| RedLeftAT				| **Unknown**					|	**Unknown**						| **Unknown**
197 	| RedRightAT			| **Unknown**					|	**Unknown**						| **Unknown**
198 	| RedTreeAT				| **Unknown**					|	**Unknown**						| **Unknown**


## Compound Nodes {#Nodes_Comound}

What follows is a table defining the different compound nodes and their labels, an explanation of every compound node follows afterwards.

Label | Name 
------|------
0  | Forall		
1  | Select		
2  | TagCase	
3  | LoopA		
4  | LoopB		
5  | IfThenElse 
6  | Iterate 	
7  | WhileLoop 	
8  | RepeatLoop 
9  | SeqForall 	
10 | UReduce 

### Select

* Goal: The select node represents a multiway selection. Sisal only supports a 2 way selection, but this compound node could be used to implement different constructs such as a switch too.
* Subnodes: 
	* 1 predicate node that returns a number between 0 and n - 1, n being the amount of subnodes.
	* Every other node is a path that can be followed depending on the result of the predicate.
* Association list:
	* At least 3 associations (predicate, iftrue and iffalse in case of if)
	* First element identifies predicate subgraph
	* Every other element identify the subgraph to use for a given predicate result.
* Signature: `(value)+ -> (value)+`

### Forall

* Goal: Independent execution of multiple instances of an expression
* Subnodes: 
	* **Generator:** Produce values for every instance of the body
	* **Body:** Expression to be evaluated
	* **Results:** Gathers the *ordered* results.
* Association list:
	* Generator
	* Body 
	* Returns
* Signature: `(value)+ -> (value)+`

### LoopA	

* Goal: Iterative looping construct. Stops when the *test* subgraph returns false. The test is executed after the body has executed once.
* Subnodes: 
	* Initialization
	* Test
	* Body
	* Returns
* Association list:
	* Same order as subnodes
* Signature: `(value)+ -> (value)+`

### LoopB	

* Goal: Iterative looping construct. Stops when the *test* subgraph returns false. The test is executed before the body is executed for the first time.
* Subnodes: 
	* Initialization
	* Test
	* Body
	* Returns
* Association list:
	* Same order as subnodes
* Signature: `(value)+ -> (value)+`
 

### TagCase

**Unknown**

### IfThenEl

**Unknown**

### Iterate 

**Unknown**

### WhileLoo

**Unknown**

### RepeatLo

**Unknown**

### SeqForal

**Unknown**

### UReduce 

**Unknown**

\page SortSis Sorting algorithm in Sisal
\include sort.sis

\page SortIF1 Sorting algorithm in IF1
\include sort.if1