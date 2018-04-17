# Cellular Automaton data storage

## General

* automa rules
  * number of neighbours
  * live to next generation
  * birth new
  * number of cell states
  * number of dimensions

* object
  * cellular Automaton
    * eg: gol ¦ conway
  * base configuration
    * dimension sizes
    * cell states
    * hash
  * name, id
  * cycle
    * oscillator (boolean)
    * generations until 'stable' (int)
    * pattern offset after cycles
      * to extents of (new) stable state
    * maximum extent for
  * type (enum)
    * unknown
    * oscillator
  * rotations
    * condition (enum) for gol, 90, 180, 270, + flip (horizontal, vertical)
      * hash
* group ¦ set
  * reference object
    * instance
      * position
      * rotation, flip
      * generation offset

## Conway´s Game of Life

* [Cellular Automaton](http://www.conwaylife.com/wiki/Cellular_automaton)

## Cellular Automaton

* [Cellular Automaton](http://www.conwaylife.com/wiki/Cellular_automaton)
* [Cellular Automaton](https://en.wikipedia.org/wiki/Cellular_automaton)

Neighborhood«s», Transitions, System«s», Universe«?», Template«s»

* «neighbourhood» family
  * id, «minimum¦maxium» «radius¦dimensions»
  * generic description, history, math expression representing generic neighbourhood
* neighbourhood
  * id, family id, radius, dimensions
  * description of specific neighbourhood «case¦instance¦implementation»
    * this does NOT include the generation transition rules (only the neighbourhood «bounds¦set»)
* system
  * id, neighbourhood id, transition rule(s)
* Universe
  * dimension extents
* Template «state»
  * id, dimension extents «bounding box», starting cell states,
  * normalized (bool), created by «name¦program»
  * ?suggested? system id
  * system*
    * system id, classification «enum», «cycle¦series» length, cycle offset «vector»
    * generation*
      * sequence
      * rotationflip*
        * hash
      * becomes
        * template id, generation offset, rotationflip state, [hash]
* log (as template, single system, single rotationflip)
  * [name], system id
  * generation*
    * cell states
      * concatenation of objects
        *
    * [hash]

Fragments

* object
  * [system id], reference coordinates «vector»
  * fragment*
* fragment
  * [system id], [reference coordinates «vector»]
  * (raw cell states «N dimensional array» ¦ sparse array, rle?)
  * template reference*
    * template id, rotationflip, generation offset, hash
  * object*


* Neighborhoods
  * [Neighborhood](https://en.wikibooks.org/wiki/Cellular_Automata/Neighborhood)
  * [Neighborhood](http://www.conwaylife.com/wiki/Neighbourhood#Common_dimensions_and_neighborhoods)
  * [gallery](http://www.conwaylife.com/wiki/Gallery_of_neighbourhoods)
  * [Moore](http://www.conwaylife.com/wiki/Moore_neighbourhood)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<cellular-automaton semVersion="«Semantic Version»" «1» xmlns='http://www.cellularautomaton.org/ca'> «?»
  <url>http://semver.org/</url>
  <url>http://www.michaelfcollins3.me/blog/2013/01/23/semantic_versioning_dotnet.html</url>
  <description>Above url has a regex to match a semantice version string, but it shows a "\." after the patch number, which should not exsit"</description>
  <version>«nonnegint:autoincrement»</version> «1»
  <description>The above version is for the file, and should auto increment each time it is saved. The caVersion attribute is the data file structure version.</description>
  <url>http://www.conwaylife.com/wiki/Cellular_automaton</url>
  <purpose>«text description of the reason this file exists»</purpose> «?»
  <neighbourhoods> «?»
    <description>
      library of neighbourhoods to use for included¦external system specifications
    </description>
    <neighbourhood id=«name» dimensions="«posint»"> «+»
      <description>
        A more formal definition of neighbourhood is needed.  Something that a program can parse reliably.
      </description>
      <description>«text description of neighborhood»</description>
      <url>https://en.wikibooks.org/wiki/Cellular_Automata/Neighborhood</url>
      <symmetry rotation="4" «?» reflection="yes" «?»/> «?»
    </neighbourhood>
  </neighbourhoods>
  <systems> «?»
    <system id="«unique»" states="«2+»" dimensions="«posint»" neighbourhood="«neighbourhoodId»"> «+»
      <description>
        The Cellular Automaton system: what about same 'system' with different extents / wrap?
        What makes a 'system'? ¦ number of dimensions, neighbourhood, transitions, state count
      </description>
      <name>«label»</name> «?»
      <states>
        <state id="«nonnegint:unique@system»" name="«unique@system»"/> «+»
      </states>
      <dimensions>
        <description>need a way to describe closed geometries</description>
        <extent id="0">
          <limit min="«»" max="«»">
            <wrap>
              <description>specifiying general case wrapping could be hard</description>
            </wrap>
          </limit>
        </extent>
        <extent id="1">
        </extent>
      </dimensions>

      <transitions alias="B3S23">
        <transition cellstate-n="«list of states»" cellstate-n1="«state»">
          <description>
            This needs to describe the conditions need to do the state transition.  For the general case, that could be complex.  For GOL it is straight forward.  Though general case optimization is more problematic.
          </description>
          <neighborhoodstate count="«n»"/>
          <neighborhoodstate/>
        </transition>
      </transitions>
    </system>
  </systems>
  <templates>
    <description>
      A library of predefined / named patterns.  These are more constrained than general configurations.  Each template must have at least one 'living' cell on every edge of declared spaces.  That is, the space dimension sizes are shrunk until every edge (surface) of the bounding box contacts a live cell.
    </description>
    <template>
      <name id="«unique template id»">«label»/>

    </template>
  </template>
  <configuration>
  </configuration>
</cellular-automaton>
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<cellular-automaton semVersion="0.1.0-dev+build.2017.10.26" xmlns='http://www.cellularautomaton.org/'>
  <version>0</version>
  <purpose>Sample Cellluar Automaton systems</purpose>

  <neighbourhoods>
    <neighbourhood id="Moore3x3" group="Moore" dimensions="2" range="1">
      <description>A simple 3 x 3 square with the output cell in the centre</description>
      <generalized>{x∈ℤn|(Σ0≤i≤n-1|xi|)<r}</generalized>
      <symmetry rotation="4" reflection="yes"/>
      <neighbours N="{{-1,-1},{0,-1},{1,-1},{-1,0},{1,0},{-1,1},{0,1},{1,1}}" target="false" radius="«posint»" aligned="true">
        <neighbour>«label»</neighbour> «…»
      </neighbours>
    </neighbourhood>
  </neighbourhoods>

  <systems>
    <system id="conway-B3S23" states="2" dimensions="2" neighbourhood="Moore">

      <name>Game of Life</name>

      <states>
        <state id="0" name="dead"/>
        <state id="1" name="living"/>
      </states>

      <dimensions> «1»
        <extent id="«nonnegint»"> «+»
          <limit min="unbounded" max="unbounded"/> «1»
          <wrap/> «?»
        </extent>
      </dimensions>

      <transitions> «1»
        <transition cellstate-n="any" cellstate-n1="1"> «+»
          <neighborhoodstate count="3"/> «?…»
        </transition>
        <transition cellstate-n="1" cellstate-n1="1">
          <neighborhoodstate count="2"/>
        </transition>
        <transition cellstate-n="any" cellstate-n1="0"/>
      </transitions>
    </system>
  </systems>
</cellular-automaton>
```
