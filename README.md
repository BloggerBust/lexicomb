
# Table of Contents

1.  [Introduction](#orgce23e2d)
2.  [Language Specification](#org3476258)
    1.  [W3C EBNF (Extended Backus-Naur Form) Reference](#org202d8c0)
    2.  [Tag Stream](#org53b0bb5)
    3.  [Tag Statements](#org937a307)
        1.  [EBNF production rules](#orga6d65c4)
    4.  [Lexicon Script](#org15f5699)
        1.  [EBNF production rules](#org66749db)
        2.  [Examples](#org21881a3)
    5.  [Lexicomb Engine](#orgc9c4076)
        1.  [Configuration](#org91211fc)
        2.  [Concurrency](#orgd1c552a)
3.  [How to install it](#orgd48801c)
4.  [Example Usage](#orgceed74d)
5.  [How to contribute](#orgceecf6d)
    1.  [How to setup a developer environment](#orga2f04ef)
    2.  [Where to do your work](#org206dca2)
    3.  [Don't forget unit & integration tests](#org566c37f)
    4.  [Making commits](#orgb5bbc00)
    5.  [Making a pull request](#orgb5941ab)
6.  [Related Projects](#org023ecb0)
    1.  [BbPyP](#org74f2260)
7.  [License](#org56122be)



<a id="orgce23e2d"></a>

# Introduction

Lexicomb is a keyword-driven interpreted programming language. The word *Lexicomb* is the contraction of the word *lexical*, meaning content word, and *combinator*, meaning that which combines. The Lexicomb interpreter is composed of a lexical analyzer and a parser combinator.


<a id="org3476258"></a>

# Language Specification

Lexicomb source code has two representations: [Tag Stream](#org53b0bb5) and [Lexicon script](#org15f5699). Lexicon script is kept in a file with the extension *ls* and saved in a directory that may contain many such files. All such files, taken together, constitute the lexicon. The name of the file becomes the first tag of the tag statement, therefore file names may not contain spaces.


<a id="org202d8c0"></a>

## W3C EBNF (Extended Backus-Naur Form) Reference

I have adopted the use of the [W3C standard notation for EBNF](https://www.w3.org/TR/xml/#sec-notation). Initially, I was using the `ISO/IEC 14977` EBNF standard as described by Wikipedia's [Extended Backus-Naur form](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form) page, but I found the W3C standard notation to be more compact thanks to its use of bracket expressions. Having said that, it is my opinion that Wikipedia did a better job of explaining the `ISO/IEC 14977` notation. I particularly liked that the Wikipedia page organized reserved syntax in [a table of symbols](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form?#Table_of_symbols) for quick reference. 


<a id="org53b0bb5"></a>

## Tag Stream

A Tag stream is a list of [Tag Statements](#org937a307) delimited by line endings.


<a id="org937a307"></a>

## Tag Statements

Tag statements are intended to take on the imperative mood with least verbosity. That is, they should have the form of a terse instruction. Here are some examples:

<p class="verse">
Register John<br />
Register Sally<br />
<br />
Exercise John situps 45 07:05 07:12<br />
Exercise Sally pushups 25 07:05 07:10<br />
</p>

If a single word is not enough to describe the tag, then multiple words may be combined in Pascal case.

    CreateString Combine each tag argument with a single space and return the result


<a id="orga6d65c4"></a>

### EBNF production rules

    tag_statement ::= tag space argument_list
    argument ::= ( char | digit )+ | real
    argument_list ::= argument_list space argument | argument ( delimiter argument )*
    tag ::=  char ( char | digit )*
    real ::= digit+ ( '.' digit+ )?
    char ::= [_a-zA-Z]
    digit ::= [0-9]
    space ::= [ ] =/*a single white space/*=
    delimiter ::= [:]


<a id="org15f5699"></a>

## Lexicon Script

Lexicon script has a simple grammar. The only literal is of type *real* and includes both int and float types. Neither String nor Boolean types can be represented literally, but both may be created indirectly. Hash statements must be declared explicitly, but have no generalized literal representation. In short, the language directly supports basic arithmetic and logical expressions. Control flow is achieved via *`conditional_statement`*, *`conditional_repeat`* and *`tag_statement`*.


<a id="org66749db"></a>

### EBNF production rules

    /* The following identifiers are inherited from the EBNF production rules for Tag Statements:
       - tag_statement
       - char
       - digit
       - real
    */
    
    block ::= { statement_list? }
    
    /* compound statement */
    statement_list ::= statement_list ';' statement | statement
    
    conditional_statement ::= '?' logical_expression block conditional_statement | '?' logical_expression block block | '?' logical_expression block
    
    /* while any logical_expression in the conditional_statement tree is truthy, repeat the evaluation of the conditional_statement */
    conditional_repeat ::= '@' conditional_statement 
    
    statement ::= name ':=' expression ';'
        | name ':=' hash ';'
        | tag_statement ';' /* see EBNF production rules for tag statements */
        | conditional_statement
        | conditional_repeat
    
    logical_expression ::= logical_expression '&&' relational_expression
        | logical_expression '||' relational_expression
        | '!' logical_expression | relational_expression
    
    relational_expression ::= arithmetic_expression '<' arithmetic_expression
        | arithmetic_expression '<=' arithmetic_expression
        | arithmetic_expression '=' arithmetic_expression
        | arithmetic_expression '>' arithmetic_expression
        | arithmetic_expression '>=' arithmetic_expression
    
    arithmetic_expression ::= expression '+' term
        | expression '-' term
        | term
    
    expression ::= logical_expression | arithmetic_expression
    
    term ::= term '*' factor
        | term '/' factor
        | factor
    
    factor ::= name | real | expression
    
    accessor ::= '[' name ']' | '[' real ']'
    access ::= name accessor*
    existence ::= '[' access ']' =/* truthy if access is successful, falsy otherwise /*=
    
    hash ::= '{' '}'
    name ::= char ( char | digit )*


<a id="org21881a3"></a>

### Examples

1.  Accessing arguments

    Arguments that are passed to a tag are named `arg` followed immediately by their 0 based positional value. They may also be collectively accessed via the `args` *name*. For example, if `MyTag` is called with three values.
    
        MyTag First second 3
    
    Then from within the tag definition those arguments may be accessed by their *name* as follows:
    
        {
          first_argument := arg0;
          second_argument := arg1;
          third_argument := arg2;
        }
    
    Or they may be accessed using the `args` *name*:
    
        {
          first_argument := args[0];
          second_argument := args[1];
          third_argument := args[2];
        }
    
    The access operator is safe to use at an arbitrary depth, without having to perform existence checks at each depth.
    
        {
            has_arg0 := [arg0];
            has_arg1 := [arg1];
            is_arg1_undefined := ![arg1];
            does_arg0_have_deep_property := [arg0[property][deep_property]];
        }

2.  Create negative value

    There are no unary operators specified in the EBNF. That does not limit us from creating negative numbers, or from changing the sign of a numeric value.
    
    `ChangeSign.ls:`
    
        {
          return 0 - arg0;
        }
    
        {
          x:= ChangeSign 5;
          y:= ChangeSign x;
          return CreateString first is x and second is y;
        }

3.  Create String

    Strings can be created by concatenating one or more *name* and *real* types.
    
    `CreateString.ls:`
    
        {
          count := 0;
          blank := ReturnNothing _;
          @?[args[count]]{
            ?[words]{
              words := words + blank + args[count];
            }
            {
              words := args[count];
            }
            count := count + 1;
          };
          return words;
        }
    
    The `CreateString` tag may be used to create a string of at least length one with a single space separating each word.
    
        {
          my_string := CreateString This is one way to create a string 1 2 3 4;
          my_string_with_a_single_leading_number := CreateString 1 2 3 leading numbers will be summed;
        }

4.  Create Boolean

    Logical expressions resolve to a `True` or `False` value. If that value is assigned to a *name*, then the result is a named boolean value that can be used in control-flow or returned as a result
    
    `CreateBoolean.ls:`
    
        {
          t := CreateString true;
          return arg0 = t;
        }
    
        {
          true := CreateBoolean true;
          false := CreateBoolean false;
          amount := arg0;
        
          ? arg1 = true {
            amount := ChangeSign amount;
          };
          ? amount <= 0 {
            return false;
          }
          # do stuff...
          return true;
        }

5.  Create hash

    A new and empty *hash* value can be assigned to a *name*.
    
        {
          my_hash := {};
        }
    
    However, as seen in the EBNF, it is not possible to initialize a *hash* value with a set of key value pairs. A `CreateHash` tag can be used to encapsulate *hash* initialization.
    
    `CreateHash.ls:`
    
        {
          hash := {};
          key_index := 0;
          value_index := 1;
        
          key := ReturnNothing _;
          value := ReturnNothing _;
        
          @?[args[key_index]] && [args[value_index]] {
            key := args[key_index];
            hash[key] := args[value_index];
            key_index := value_index + 1;
            value_index := key_index + 1;
          };
        
          return hash;
        }
    
        return CreateHash first_name:John last_name:Doe age:99;


<a id="orgc9c4076"></a>

## Lexicomb Engine


<a id="org91211fc"></a>

### Configuration

Each bbpyp namespace has a [Dependency Injector IoC container](http://python-dependency-injector.ets-labs.org/containers/index.html) that accepts a python dictionary named *config*.

1.  Logging

    **config Key:** logger
    
    **Is Optional:** True
    
    The `logger` configuration key may be set to any valid [logging dictionary configuration](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig). This parameter is entirely optional.
    
    There are two named loggers that can be configured:
    
    1.  `bbpyp.lexicomb`
    2.  `bbpyp.lexicomb_engine`


<a id="orgd1c552a"></a>

### Concurrency

The core of the Lexicomb Engine is the [LexicombPubSubClient](bbpyp/lexicomb_engine/lexicomb_pub_sub_client.py). The `LexicombPubSubClient` relays messages between Lexicomb's [LexicalStateMachine](https://github.com/BloggerBust/bbpyp/blob/master/bbpyp/lexical_state_machine/lexical_state_machine.py) and  [InterpreterStateMachine](https://github.com/BloggerBust/bbpyp/blob/master/bbpyp/interpreter_state_machine/interpreter_state_machine.py) using [TopicChannel](https://github.com/BloggerBust/bbpyp/blob/master/bbpyp/message_bus/model/topic_channel.py)s. The number of concurrent publish and subscribe connections opened per `TopicChannel` is configurable using the [Message Bus `memory_channel_topic` configuration option](https://github.com/BloggerBust/bbpyp#message-bus).

There are four topic names:

1.  `bbpyp.lexical_state_machine.lexical_analyse`
2.  `bbpyp.interpreter_state_machine.parse`
3.  `bbpyp.interpreter_state_machine.evaluate`
4.  `bbpyp.interpreter_state_machine.report`


<a id="orgd48801c"></a>

# How to install it

To do&#x2026;


<a id="orgceed74d"></a>

# Example Usage

To do&#x2026;


<a id="orgceecf6d"></a>

# How to contribute

I am happy to accept pull requests. If you need to get a hold of me you can [create an issue](https://github.com/BloggerBust/lexicomb/issues) or [email me directly](https://bloggerbust.ca/about/).


<a id="orga2f04ef"></a>

## How to setup a developer environment

First, [fork this repository](https://github.com/login?return_to=%2FBloggerBust%2Flexicomb) and clone your fork to a local dev environment.

    git clone https://github.com/<your-username>/lexicomb.git

Next, create a venv and install the latest pip and setuptools.

    cd lexicomb
    python -m venv venv
    source venv/bin/activate
    pip install -q --upgrade pip setuptools

Lastly, install the *dev* requirements declared in [dev-requirements.txt](dev-requirements.txt) and run the unit tests.

    pip install -q -r dev-requirements.txt
    python -m unittest discover

    ......................................................
    ----------------------------------------------------------------------
    Ran 54 tests in 0.716s
    
    OK


<a id="org206dca2"></a>

## Where to do your work

Keep your mainline up to date with upstream.

    git fetch origin --prune
    git checkout master
    git --ff-only origin/master

Make your changes in a feature branch.

    git checkout -b branch_name


<a id="org566c37f"></a>

## Don't forget unit & integration tests

Unit and integration tests are written using python's [unittest framework](https://docs.python.org/3/library/unittest.html). The unittests use the [mock library](https://docs.python.org/3/library/unittest.mock.html). Please do write both unit tests and integration tests to accommodate your contribution, except where existing tests are sufficient to cover the change.


<a id="orgb5bbc00"></a>

## Making commits

Read Chris Beams excellent [article on writing commit messages](https://chris.beams.io/posts/git-commit/) and do your best to follow his advice.


<a id="orgb5941ab"></a>

## Making a pull request

If you feel that your changes would be appreciated upstream, then it is time to create a pull request. Please [write tests](#org566c37f) to validate your code changes and run all the tests again before making a pull request to defend against inadvertently braking something.

    python -m unittest discover

If you have made many intermittent commits in your feature branch, then please make a squash branch and [rebase with a single squashed commit](https://blog.carbonfive.com/2017/08/28/always-squash-and-rebase-your-git-commits/). A squash branch is just a spin-off branch where you can perform the squash and rebase without the fear of corrupting your feature branch. My preference is to perform an interactive rebase. Note, that a squash branch is pointless if you only made a single commit.

First switch to master and fast forward to HEAD. This will reduce the risk of having a merge conflict later.

    git checkout master
    git fetch origin --prune
    git merge --ff-only origin/master

Next, switch back to your feature branch and pull any changes fetched to master. If there are conflicts, then resolve them. Be sure to run all the tests once more if you had to merge with changes from upstream.

    git checkout branch_name
    git pull origin/master
    python -m unittest discover

Determine the first commit of the feature branch which will be needed during interactive rebasing.

    git log master..branch_name | grep -iE '^commit' | tail -n 1

    commit f723dcc2c154662b3d6c366fb5ad923865687796

Then, create a squash branch as a spin-off of the feature branch and begin the interactive rebase following [this guidance](https://blog.carbonfive.com/2017/08/28/always-squash-and-rebase-your-git-commits/).

    git checkout -b branch_name_squash
    git rebase -i f723dcc^

Now, if you make a mistake during the rebase, but don't notice until after you have already committed, all of your precious commit history remains in the feature branch. Simply reset the squash branch back to the feature branch and start again. Once you are happy with your rebase, push the squash branch to remote and [create a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).


<a id="org023ecb0"></a>

# Related Projects


<a id="org74f2260"></a>

## [BbPyP](https://github.com/BloggerBust/bbpyp)

BbPyP (Blogger Bust Python Project) is a collection of python packages that I intend to use to help develop other more interesting python projects.


<a id="org56122be"></a>

# License

[Apache License v2.0](LICENSE-2.0.txt)

