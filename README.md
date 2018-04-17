# GOL

Exploration of a Python implementation of Conway´s Game Of Life

This is not hashlife, but is intended to be a lot more powerful and faster than the typical brute force nested loop generaration calculation.

This is very incomplete.  It is/was being used to learn about various things.  A little work with the unittest Library.  Creating and validating xml with xsd files.  Working with xml in python.  Using tkinter.  Everything should run, though with minimal functionality.

## work in progress

* [data storage](data-storage.md)
  * xml structure
    * generalize to support other cellular automaton universes
      *
    * validation
      * [dtd](https://www.w3.org/TR/xml11/)
        * [info](https://en.wikipedia.org/wiki/Document_type_definition)
        * [doc](http://www.xmlfiles.com/dtd/dtd_elements.asp)
          * incorrectly? shows empty element as type (EMPTY) when EMPTY seems right
      * [xml schema](https://www.w3.org/TR/xmlschema11-1/)
        * [reference](http://www.xmlschemareference.com/)
        * [build in datatypes](https://www.w3.org/TR/xmlschema-2/#built-in-datatypes)
        * [attribute to attribute validdation](https://stackoverflow.com/questions/20904083/how-can-i-restrict-the-values-of-an-xml-attribute-based-on-attribute-values-in-o)
        * [key,keyref](http://markchensblog.blogspot.ca/2012/11/key-keyref-and-unique-in-xsd.html)
        * [key,keyref constraints](http://www.datypic.com/books/defxmlschema/chapter17.html)
      * ISO RELAX NG
  * support load from / save to simple text version of board

* parse board (in memory) configuration to extract distinct groups
* analyze group to match to known templates

## Expanded Notes

### blocks / groups, and neighbourhood of interest

A living cell has a normal neighbourhood where it can influence, and be influenced by cell states in the next generation.  An *empty* cell has the same neighbourhood.  When generating an area of interest based on the neighbourhoods of living cells with overlapping neighbourhoods, the outer edge of combined neighbourhoods will all be empty cells.  However, the next generation of those empty cells will also be influenced by the cells one more *radius* out from generated area of interest.

That should be handled by setting the (collision) bounding box to be the simple area of interest, instead of only the area containing the living cells.  If 2 of the expanded bounding boxes overlap, they have (at least) an empty cell in common that can (potentially) be influenced in the next generation by both blocks.  Second check is if the actual living cell neighbourhoods of the 2 groups intersect.

Expanding the bounding box does not require storing the outer ring of empty cells that it encloses.  For a «standardized¦reduced» block, the bounding box will be from [-radius,-radius] to [maxColum + radius, maxRow+radius].  IE:
with radius 1, block = [1, 0, 1], bounding box [-1, -1], [3, 1], giving a bounding box 5 columns wide, by 3 high, but only storing 3 columns in 1 row.

The bounding box will be relative to whatever offset exists for the block.

This will create the smallest blocks, but can also have block collisions (real, not just bounding box) in the very first generation.

### alternate neighbourhood of interest

The neighbourhood of interest could be expanded one extra radius.  That is, include in the expanded neighbourhood, the neighbourhoods of all empty cells that can be influenced by the living cells being processed.  This will make sure that 2 disjoint blocks will not really be in collision for the next generation.  The bounding boxes might be, but the (real) neighbourhoods will not.

This will tend to create fewer and larger groups, since fewer cases will be detected as disjoint.

### isolating groups

A group is any set of cells that interact with (are neighbours of) each other, but do not interact with other cells.  At least for the next generation.

Start from any single unprocess living cell.
* generate the neighbourhood for the cell
* generate a second neighbourhood for all of the empty cells in the first neighbourhood
* until no unprocessed living cells in either neighbourhood
  * repeat above

Create block from the living cells in the neighbourhood.
* Set bounding box as limits of the neighbourhood around of the living cells (not including the neighbourhood for the empty cells.)

* Generate a 'neighbourhood' for a group by starting from any unprocessed living cell.
* create the neighbourhood for that cell
* expand the neighbourhood with the neighbourhoods of any other living cell that is included in the neighbourhood
* repeat until no more unprocessed living cells covered by the neighbourhood.

This is the neighbourhood where the introduction of a living cell could affect the next generation of the the group.  It can be used to generate a bounding box for initial group collision detection.  The block/group origin will be at position 1,1 of the neighbourhood.  The outer row of the neighbourhood will be empty.  If it wasn't, the group detection logic would have expanded it further.

* Create a block from the processed cells and neighbourhood
* add the block to the (closest/smallest) existing block that the bounding box is in
* if no existing block, create or expand the outermost wrapper block

Repeat until no unprocessed living cells left.

Watch out for, and handle

* voids that contain other blocks
* "C" OR "L" shaped neighbourhoods with overlap in the open side/corner
* enclosed blocks become children of the enclosing block
* overlapping blocks are both children or an outer block

Add «?¦2 * radius» extra empty rows and columns to the initial configuration, to make sure that cells on the edge of the processing space have valid (and empty) neighbours.

Using python, the empty rows and cells only need to be added at the end.  The row/column before zero will be -1, which is a valid index, and will wrap to the end.  Where the empty cells were added.  The same cells will be used on the maximum edges of the starting processing space, and there will not be any overlap, at least during group detection and creation.

### transformations (rotation and mirror)

There are simple transformation matricies for rotation by multiples of 90 degrees, and for mirror about x and y axis.  This use sin and cos, but at multiples of 90 degrees, the numbers all come out as 0 or 1.  However, in this case it is even simpler to directly manipulate the lists and elements.  A rotate by +90 degrees simply turns rows into columns.  The bottom row becomes the leftmost column.  The second row from the bottom becomes the second column, etc., until the top row becomes the last (right) column.

Similar operations will rotate by 180 degrees, and mirror vetically and horizontally

## Setup

Local Environment: Fedora 27 x86_64

```sh
sudo dnf install python3-virtualenv
sudo dnf install python3-tkinter
virtualenv-3 gol
cd gol
git init .
. bin/activate
pip install lxml
pip install defusedxml
```

* uses "xmllint" program

.gitignore file
```
bin
include
lib
lib64
pip-selfcheck.json
__pycache__
```


## IDEAs

* Create common CellualarAutomaton class to inherit custom versions from

* hash managment class HashTracker
* non displaying memory/process efficent, dynamic memory block processor
  * history
  * toXml
  * load from file
  * constructor
  * step
    * when oscillator, just count, mark bounding box static
      * will only need to compare against changing boundary boxes
        * ?quad tree? to minimize number of compares needed?
  * clone, rotateFlip, hash, set NoFlipRotate0 case
  * multiple vector offsets and cycle offsets
* toXml
  * current generation: specified, all
