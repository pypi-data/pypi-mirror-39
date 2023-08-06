
**Note**: If you are reading this description on PyPI, some of the
formatting is unclear (particularly LaTeX and code examples). Instead
read [this](https://gitlab.com/apgoucher/lifelib/blob/master/README.md)
documentation, which is correctly rendered and updated more frequently.

![](images/screenshot.png)

Quick start
-----------

Make sure your machine has the correct system requirements before commencing.
This essentially boils down to you having an **x86-64 processor** (likely to
be the case unless you're using a smartphone, tablet, or Raspberry Pi). Then
getting started with `lifelib` is straightforward.

 - Install Python with the `numpy` and `jupyter` packages and the 'pip'
   package manager. The [Anaconda](https://www.anaconda.com/download)
   distribution contains those packages and many more, and is available
   on Windows, Mac OS X, and Linux. You can use either Python 2 or 3.

 - If on Mac OS X, make sure you have the **command-line developer tools**
   installed. You can test this by opening a terminal and running the
   command `g++ --version`.

 - Download and run the [installation script][1] to install or upgrade
   `lifelib`. Internally, this uses the pip package manager and installs
   `lifelib` into a user-local directory.

 - Open a Jupyter notebook (e.g. by opening Anaconda Prompt and typing
   `jupyter notebook`) and execute the following commands. They are explained
   in the 'example usage' section later in this document:

        import lifelib
        sess = lifelib.load_rules("b3s23")
        lt = sess.lifetree()
        lidka = lt.pattern("bo7b$obo6b$bo7b8$8bo$6bobo$5b2obo2$4b3o!")
        print("Initial population: %d" % lidka.population)
        lidka_30k = lidka[30000]
        print("Final population: %d" % lidka_30k.population)
        lidka.viewer()

 - Try some of the [example notebooks][2] to familiarise yourself with
   `lifelib` usage. Other features are documented in this README file.

[1]: https://gitlab.com/apgoucher/python-lifelib/blob/master/install/install.py
[2]: https://gitlab.com/apgoucher/python-lifelib/tree/master/notebooks

What is lifelib?
----------------

`lifelib` is a collection of algorithms for simulating and manipulating
patterns in cellular automata. It can be included in your project in
either of two ways:

 - **Python package**: `lifelib` can be imported as a Python package,
   and is compatible with both Python 2.7 and Python 3.5 (and beyond).
   We recommend this for everyday use, as the Python bindings are more
   user-friendly.

 - **C++ header files**: if you have a project written in C++11 or above,
   specific components of `lifelib` may be included. This approach is
   used by the [apgsearch](https://gitlab.com/apgoucher/apgmera) soup
   searcher and the [slmake](https://gitlab.com/apgoucher/slmake) glider
   synthesis compiler. Note that `lifelib` is header-only owing to the
   use of templates.

How is lifelib structured?
--------------------------

The idea behind `lifelib` is a universal framework in which different
high-level **algorithms** such as Bill Gosper's Hashlife can seamlessly
integrate with different low-level **iterators** for running specific
rules on various architectures. There are currently three algorithms
supported by `lifelib`:

 - **Hashlife**: This is the celebrated algorithm by Bill Gosper used
   to gain exponential speedups by exploiting repeated structure in both
   space and time. It operates directly on a compressed representation
   called a 'hashed quadtree'. Due to its efficiency, simplicity and
   generality, this is recommended as the default algorithm.

 - **Streamlife**: This is a new (2018) modification of Hashlife designed
   to work efficiently on patterns containing antiparallel streams of
   information-carrying gliders, such as certain self-replicating
   machines. Streamlife works by disentangling a pattern into provably
   non-interacting parts which can be run in separate 'universes'. This
   algorithm is inspired by China Mieville's novel, 'The City and The
   City', and borrows much of its terminology.

 - **Tile-based**: Whereas the other algorithms are best for patterns
   exhibiting regular behaviour, this is well-suited for running random
   patterns. It is only available in the C++ version of `lifelib` and
   is aimed at [apgsearch](https://gitlab.com/apgoucher/apgmera), which
   runs random soups in a Monte Carlo fashion and logs their eventual
   decay products. The tile-based algorithm optimises for areas of the
   universe that do not change, excluding them from future calculations
   until necessary.

Whereas the Streamlife implementation is only suited to Conway's Game of
Life and close variants thereof, the other two algorithms (Hashlife and
tile-based) are fully compatible with every `lifelib` iterator.

In `lifelib`, an **iterator** is an efficient low-level implementation of
a cellular automaton, which runs on a $`32 \times 32`$ grid and returns
the central $`16 \times 16`$ subgrid after one or more generations. The
philosophy behind `lifelib` is that any of these iterators can seamlessly
plug into either the Hashlife or tile-based algorithm, 'upgrading' it
from a small $`32 \times 32`$ universe to an unbounded universe.

The iterators themselves are written mostly in C and inline assembly
language, specifically tailored to your machine's instruction set and to
the cellular automaton being simulated. Iterators are generated by Python
modules called **genera** (singular: genus), each one of which targets a
specific family of related rules. At the moment, `lifelib` contains nine
different genera, but there is nothing to prevent you from adding more
of your own:

 - **b3s23life**: This genus supports only one rule, namely Conway's Game
   of Life, and produces iterators with remarkably low instruction counts
   (and concomitantly high speed!). It can yield iterators compatible with
   either AVX-512, AVX2, AVX, or SSE, and chooses the most advanced
   instruction set supported by your processor.

 - **lifelike**: This genus is more general, and supports any 2-state
   outer-totalistic cellular automaton on the Moore neighbourhood. It can
   produce optimised code for either AVX2, AVX, or SSE. As with b3s23life,
   this genus uses bitwise parallelism and vectorisation to compute many
   cells simultaneously.

 - **isotropic**: This is again more general, supporting any isotropic
   2-state Moore-neighbourhood cellular automaton. It is not as fast as
   the lifelike genus, as it is not vectorised and instead computes 8 cells
   at a time using a lookup table.

 - **ltl**: A SSSE3-based byte-parallel implementation of Kellie Evans'
   'Larger than Life' cellular automata. It supports square neighbourhoods
   with a radius up to 7 (i.e. $`15 \times 15`$).

 - **generations**: A multistate generalisation of lifelike. Internally, it
   uses the vectorised lifelike iterator as a subroutine.

 - **isogeny**: A multistate generalisation of isotropic.

 - **gltl**: A multistate generalisation of Larger than Life.

 - **bsfkl**: Brian Prentice's 3-state BSFKL rules generalise both 3-state
   Generations rules and outer-totalistic cellular automata.

 - **hrot**: Higher-range outer-totalistic rules, a common generalisation of
   Lifelike and 'Larger than Life' rulesets. This genus supports square
   neighbourhoods with a radius up to 5 (i.e. $`11 \times 11`$).

The design of `lifelib` restricts iterators to have a maximum neighbourhood
radius of 8 and a maximum of $`2^{64}`$ states. (Note that this is a proper
superset of the custom rules supported by Golly's RuleLoader, which are
restricted to a radius of 1 and a maximum of 256 states.)

System requirements
-------------------

For `lifelib` to work, you need a computer with an **x86-64 processor**.
This includes most personal computers, but not smartphones, tablets, or the
Raspberry Pi.

It runs easily in a POSIX environment, such as:

 - Linux / Unix;
 - Mac OS X;
 - Windows (using Cygwin);
 - Windows 10 (using WSL);

and requires a C++ compiler (gcc or clang) and Python (ideally with numpy).

The Python version of `lifelib` can actually run in Windows' native Python
(e.g. Anaconda). A suitable Cygwin installation still needs to exist on the
machine and be locatable by `lifelib`; the Python package contains a function
(`lifelib.install_cygwin()`) to automatically and painlessly handle this.

Installation
------------

If you are including `lifelib` as part of a project, it does not necessarily
need 'installing' per se. Instead, you can clone `lifelib` into your
project's directory:

    cd path/containing/your/project
    git clone https://gitlab.com/apgoucher/lifelib.git

It can be accessed from with a Python script using:

    import lifelib

or from within a C++11 program using (for example):

    #include "lifelib/pattern2.h"

If you want to install `lifelib` so that it's available on your system for
you to access anywhere (such as from a Python script, module, or even a
Jupyter notebook), then run:

    pip install --user --upgrade python-lifelib

to download the latest source distribution from PyPI. The --user argument is
to ensure that it is installed under your home directory, rather than system
wide, because `lifelib` relies on the ability to create and compile its own
source code.

Using lifelib in Windows Python
-------------------------------

If you install `lifelib` into a native Windows Python distribution, such as
Anaconda, then you need to run the following line of code. (If you used the
installation script in the 'quick start' section, then this will have already
been done for you.)

    import lifelib
    lifelib.install_cygwin()

This ensures that Cygwin and all required packages are installed into a
subtree of the `lifelib` package directory (within your user site-packages
directory). Approximately one gigabyte of disk space will be consumed when
you run this for the first time.

Apart from requiring this one-time command, there is no difference between
running `lifelib` in Windows or POSIX.

Example usage (Python)
----------------------

This is essentially the 'Hello World' of `lifelib`, and takes a small chaotic
pattern (called Lidka) and runs it 30000 generations in Conway's Game of Life.
It prints both the initial and final populations.

    import lifelib
    sess = lifelib.load_rules("b3s23")
    lt = sess.lifetree()
    lidka = lt.pattern("bo7b$obo6b$bo7b8$8bo$6bobo$5b2obo2$4b3o!")
    print("Initial population: %d" % lidka.population)
    lidka_30k = lidka[30000]
    print("Final population: %d" % lidka_30k.population)

This should print 13 as the initial population and 1623 as the final
population.

Now, let us walk through what happens in the code.

 - The first line imports the Python package. This is a lightweight operation
   so does not take a perceptible amount of time.

 - The second line is by far the most subtle. It takes in one or more rules
   (in this case, "b3s23" is the systematic name for Conway's Game of Life:
   birth on three neighbours and survival on two or three neighbours) and
   creates a lifelib 'session' capable of running those rules. This is a
   healthy abstraction designed to obscure what `load_rules()` _really_ does,
   which is the following:

    - Checks to see whether there is already a compiled `lifelib` shared
      library with the desired ruleset. If so, it checks its version against
      the Python package's version to ensure that it's current, and otherwise
      ignores it and proceeds:

    - Finds the highest-priority genus which supports the rule. In this case,
      it is the **b3s23life** genus, which can generate optimised C and
      assembly code to take advantage of instruction sets up to AVX-512. The
      genus is then invoked to create the rule. (If multiple rules have been
      specified, this step is repeated for each rule.)

    - Generates some extra 'glue code' to include all of the rule iterators
      into the `lifelib` source code.

    - Compiles the file `lifelib.cpp` using a C++ compiler (g++ or clang)
      into a shared library called `lifelib_b3s23.so` (even though if this
      is Windows, it's actually a DLL masquerading under the extension .so).
      This step is the most time-consuming, because the C++ compiler must
      compile tens of thousands of lines of code (C++11, C, and assembly)
      and optimise it for your machine. Typically this will take 10 or 20
      seconds to complete.

    - Dynamically loads the `lifelib_b3s23.so` shared library into the
      running process. (If you are on Windows and running outside Cygwin,
      this is loaded into a Cygwin subprocess instead, with interprocess
      communication pipes used to bridge the rift. Fortunately, this
      indirection is invisible to you, provided everything is configured
      correctly.)

 - The third line now creates a **lifetree** (hashed quadtree) in the
   session, allowed to use up to 1000 megabytes of memory before garbage
   collecting. All of our patterns reside in this lifetree, and they
   automatically take advantage of mutual compression. This means that
   if a structure occurs many times in many patterns, it will only be
   stored once in the compressed container.

 - The fourth line creates a pattern (finitely-supported configuration of
   cells inside an unbounded plane universe) called Lidka, which has 13
   live cells. The pattern is specified in a format called Run Length
   Encoded (or RLE), which is the standard for sharing patterns in cellular
   automata.

 - The fifth line reports the population of Lidka, and should print 13. The
   .population property calls lifelib code to compute the population of the
   pattern by recursively walking the quadtree.

 - The sixth line runs Lidka 30000 generations in Bill Gosper's Hashlife
   algorithm. On a modern machine, this should take less than 100 milliseconds
   owing to the speed of the b3s23life iterator. This is not done in-place,
   so a new object `lidka_30k` is returned without modifying the original
   `lidka` object.

 - The seventh line reports the population of the pattern `lidka_30k`. This
   should be exactly 1623.

That's it! You've now simulated your very first pattern in Hashlife!

The `python-lifelib` repository, along with packaging tools, contains several
[examples](https://gitlab.com/apgoucher/python-lifelib/tree/master/notebooks)
of more complex and interesting applications of `lifelib`.

Editing features
----------------

In addition to running patterns, `lifelib` has extensive support for editing
patterns. In particular, the following operations are included:

 - Shifting, rotating, and reflecting patterns.
 - Boolean set operations such as union, intersection, difference, symmetric
   difference.
 - Slicing rectangular subregions.
 - Convolutions (either using inclusive or exclusive disjunction).
 - Getting and setting individual cells or arrays thereof.
 - Pattern-matching capabilities such as find and replace.
 - Kronecker products.

The Python interface allows arbitrarily large integers to be used for shifts
and getting/setting coordinates of individual cells. Manipulating arrays of
cells is restricted to 64-bit integers, and requires `numpy` to be installed,
but is much faster.

Both the Python and C++ versions of `lifelib` use operator overloading for
editing patterns, and are consistent with each other:

 - Two patterns can be added (elementwise bitwise OR) by using `|` or `+`.
   The in-place assignment operators `|=` and `+=` also work. For two-state
   patterns viewed as sets of cells, this coincides with union / disjunction.

 - Patterns can be subtracted (elementwise bitwise AND-NOT) by using `-` or
   its in-place form `-=`.

 - The intersection / conjunction (elementwise bitwise AND) is exposed
   through the operator `&` and its in-place form `&=`.

 - Exclusive disjunction can be performed using the caret operator `^` and
   its in-place form `^=`.

 - The Kronecker product of two patterns can be perfomred using `*`.

 - A pattern may be shifted using either `pattern.shift(30, -20)` or the
   more concise `pattern(30, -20)`. The latter syntax can have a third
   parameter prepended to allow transformations, such as counter-clockwise
   rotation using `pattern("rccw", 0, 0)`.

 - The square brackets operator advances a pattern in the current rule for
   the specified number of generations.

In Python, a pattern can also be viewed as an associative array mapping
coordinate pairs to the state, and manipulated as such. The `__getitem__`
and `__setitem__` methods (square brackets operator as an rvalue and lvalue
respectively) support the following:

    lidka[-3:5, 8:20] # for specifying an 8-by-12 rectangular region
    lidka[7893, -462] # for specifying an individual cell
    lidka[np.array([[3, 4], [2, 1], [69, -42]])] = np.array([1, 0, 1])

The first of these returns a pattern and supports assignment from either a
pattern or an int (in which case it block-fills the rectangle with that
state). If you provide a dictionary such as `{0: 0.60, 1: 0.20, 2: 0.20}`,
then it will fill the rectangle randomly with cells of states given by the
keys in the dictionary, and values in the proportions in the dictionary.
For two-state random fill, you can use:

    pat[0:100, 0:100] = 0.3

to fill that rectangle with 30-percent density.

The second notation returns an int and supports assignment from an int. The
third returns and supports assignment from a numpy array of the same length.
The numpy array syntax can only specify 64-bit signed coordinates (each
coordinate is limited to the interval $`\pm 9 \times 10^{18}`$ ), whereas
the other two syntaxes allow pairs of arbitrarily large ints to be used.

Querying patterns
-----------------

As well as editing functionality, patterns in `lifelib` have various
properties that give basic information:

    lidka.population # returns population count
    lidka.bounding_box # returns bounding box

If a pattern is periodic (an oscillator or spaceship), you can additionally
use the following further properties:

    pattern.period
    pattern.displacement
    pattern.apgcode

Loading/saving files
--------------------

Both the macrocell and RLE file formats from Golly are supported by `lifelib`
for both reading and writing files; moreover, they have been generalised to
support up to $`2^{64}`$ states. The Python version of `lifelib` also allows
the reading and writing of compressed files (.rle.gz and .mc.gz). The easiest
way to use this is:

    lidka.save('lidka.rle')
    lidka_reloaded = lt.load('lidka.rle')

Unless otherwise specified, file format is inferred from the extension.

Jupyter notebook support and LifeViewer integration
---------------------------------------------------

If you are running `lifelib` in Python from a Jupyter notebook, you can view
a pattern in Chris Rowett's LifeViewer by calling the pattern's `.viewer()`
method:

    lidka.viewer()

Note that, for this to work, you need to be viewing the notebook from a
browser with Internet access; the LifeViewer JavaScript plugin is sourced
from `conwaylife.com`.

In Internet Explorer, the lack of support for data URIs means that you need
to use the antiquated option:

    lidka.viewer(base64=False)

which is worse because 'downloading' the notebook as HTML does not preserve
the embedded LifeViewers in the latter case.

Future directions
-----------------

 - Currently lifelib is specific to 64-bit x86 architecture; ideally
   support for other architectures will be introduced.
