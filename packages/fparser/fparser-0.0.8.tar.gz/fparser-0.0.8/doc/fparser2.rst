..  Copyright (c) 2017-2018 Science and Technology Facilities Council.

    All rights reserved.

    Modifications made as part of the fparser project are distributed
    under the following license:

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

    1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

.. _fparser2 :

fparser2
========

Fparser2 provides support for parsing Fortran up to and including
Fortran 2003. This is implemented in
the Fortran2003.py `file`__ and contains an entirely separate parser
that includes rules for Fortran 2003 syntax. Support for Fortran 2008
is being added in the Fortran2008.py `file`__ which extends the
Fortran2003 rules appropriately. At this time Fortran2008 support is
limited to submodules.

__ https://github.com/stfc/fparser/blob/master/src/fparser/two/Fortran2003.py
__ https://github.com/stfc/fparser/blob/master/src/fparser/two/Fortran2008.py


Getting Going : Script
----------------------

fparser2 can be run from the command line by using the `fparser2.py`
script located in the `scripts` directory. One or more input files can
be provided. These files are parsed in turn and the parsed Fortran is output
to the screen (most likely with a different formatting to the input as
fparser2 does not preserve format), or an appropriate error is ouput.
::

   >>> cat simple.f90
   program simple
   end
   >>> src/fparser/scripts/fparser2.py simple.f90
   PROGRAM simple
   END PROGRAM simple
   >>> cat error.f90
   prog error
   end
   >>> src/fparser/scripts/fparser2.py error.f90
   Syntax error: at line 1
   >>>prog error

   parsing 'src/error.f90' failed at line #1'prog error'
   started at line #1'prog error'


Getting Going : Python
----------------------

As with the other parser (:ref:`fparser`), the source code to parse
must be provided via a Fortran reader which is an instance of either
`FortranFileReader` or `FortranStringReader` (see
:ref:`readfortran`).

The required parser is then created using an instance of the
`ParserFactory` class. `ParserFactory` either returns a
Fortran2003-compliant parser or a Fortran2008-compliant parser
depending on the `std` argument provided to its create method.

Finally the parser is provided with the Fortran reader and returns an
abstract representation (an abstract syntax tree - AST) of the code,
if the code is valid Fortran. This AST can be output as Fortran by
printing it. The AST hierarchy can also be output in textual form by
executing the AST. For example:

::
   
    >>> from fparser.two.parser import ParserFactory
    >>> from fparser.common.readfortran import FortranFileReader
    >>> reader = FortranFileReader("compute_unew_mod.f90",
                                   ignore_comments=False)
    >>> f2008_parser = ParserFactory().create(std="f2008")
    >>> ast = f2008_parser(reader)
    >>> print ast
    MODULE compute_unew_mod
      USE :: kind_params_mod
      USE :: kernel_mod
      USE :: argument_mod
      USE :: grid_mod
      USE :: field_mod
      IMPLICIT NONE
      PRIVATE
      PUBLIC :: invoke_compute_unew
      PUBLIC :: compute_unew, compute_unew_code
      TYPE, EXTENDS(kernel_type) :: compute_unew
      ...
    >>> ast
    Program(Module(Module_Stmt('MODULE', Name('compute_unew_mod')),Spec
    ification_Part(Use_Stmt(None, Name('kind_params_mod'), '', None),Us
    e_Stmt(None, Name('kernel_mod'), '', None),Use_Stmt(None, Name('arg
    ument_mod'), '', None),Use_Stmt(None, Name('grid_mod'), '', None),U
    se_Stmt(None, Name('field_mod'), '', None),Implicit_Part(Implicit_S
    tmt('NONE')), Access_Stmt('PRIVATE', None),Access_Stmt('PUBLIC', Na
    me('invoke_compute_unew')),Access_Stmt('PUBLIC', Access_Id_List(','
    , (Name('compute_unew'),Name('compute_unew_code')))),Derived_Type_D
    ef(Derived_Type_Stmt(Type_Attr_Spec('EXTENDS',Name('kernel_type')),
    Type_Name('compute_unew'), None), ...

Note that the two readers will ignore (and dispose of) comments by
default. If you wish comments to be retained then you must set
`ignore_comments=False` when creating the reader. The AST created by
fparser2 will then have `Comment` nodes representing any comments
found in the code. Nodes representing in-line comments will be added
immediately following the node representing the code in which they
were encountered.

Note that empty input, or input that consists of purely white space
and/or newlines, is not treated as invalid Fortran and an empty AST is
returned. Whilst this is not strictly valid, most compilers have this
behaviour so we follow their lead.

If the code is invalid Fortran then a `FortranSyntaxError` exception
will be raised which indicates the offending line of code and its line
number. For example:

::
   
   >>> from fparser.common.readfortran import FortranStringReader
   >>> code = "program test\nen"
   >>> reader = FortranStringReader(code)
   >>> from fparser.two.parser import ParserFactory
   >>> f2008_parser = ParserFactory().create(std="f2008")
   >>> ast = f2008_parser(reader)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "fparser/two/Fortran2003.py", line 1300, in __new__
       raise FortranSyntaxError(error)
   fparser.two.Fortran2003.FortranSyntaxError: at line 2
   >>>en


Classes
-------

.. autoclass:: fparser.common.readfortran.FortranFileReader
    :members:


.. autoclass:: fparser.common.readfortran.FortranStringReader
    :members:


.. autoclass:: fparser.two.parser.ParserFactory
    :members:


Data Model
----------

The module provides the classes; `Comment`, `Main_Program`,
`Subroutine_Subprogram`, `Function_Subprogram`, `Program_Stmt`,
`Function_Stmt`, `Subroutine_Stmt`, `Block_Do_Construct`,
`Block_Label_Do_Construct`, `Block_Nonlabel_Do_Construct`,
`Execution_Part`, `Name` and `Constant`, amongst others.  Nodes in the
tree representing the parsed code are instances of either `BlockBase`
or `SequenceBase`. Child nodes are then stored in the `.content`
attribute of `BlockBase` objects or the `.items` attribute of
`SequenceBase` objects. Both of these attributes are Tuple instances.


Walking the AST
---------------

fparser2 provides two functions to support the traversal of the
AST that it constructs:

.. automethod:: fparser.two.utils.walk_ast

.. automethod:: fparser.two.utils.get_child

