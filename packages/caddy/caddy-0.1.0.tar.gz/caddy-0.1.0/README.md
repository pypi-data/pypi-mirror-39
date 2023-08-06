Caddy
--------------------
> Semester project for OOP course


The goal of this project is to create a simple version of a CAD application inspired by the early versions of Autocad.

## Installation

To install Caddy, simply use pip:

```
$ pip install caddy
```

and run with following command:
```
$ caddy
```

### Requirements

The following software and libraries are required to run Caddy:

- Tkinter

## Project assignment

The application allows one to draw the following shapes:

- polylines (a line containing multiple segments)
- rectangles
- circles
- _optional_ any other objects you might want to add

Next to drawing shapes, the application provide additional actions:

- save shapes into a file
- load shapes from a file
- remove a shape
- move a shape 
- remove all shapes upon getting a confirmation from a user
- list drawn shapes 
- quit the application asking to save any changes
- _optional_ undo the last action
- _optional_ redo the last action
- _optional_ export as SVG file
- _optional_ zoom in / out the canvas
- _optional_ pan the canvas

The drawing can be done by either typing commands into the command panel or by using mouse.

### Command-line interface

At the bottom of the application, there is a command panel.
It contains a command input area where a user can type commands corresponding to the above actions.
Above the input, it shows a history of executed commands with any additional command output or error messages in case there was a problem. 

### Mouse interface

All the actions are also to be invoked using mouse by selecting an appropriate menu item or a toolbar icon.
Some actions need additional parameters:

- points are selected by clicking in the canvas (_optional_ changing the mouse cursor to `crosshair`).
- shapes are selected by clicking in the canvas (_optional_ changing the mouse cursor to `select`).
- filenames are represented by appropriate file selection dialogs

### Actions

The following is the grammar of the command language in BNF format with regex definition for `STRING`, `NAT` and `INT`:

```
STRING ::= "\w+"
NAT ::= \d+
INT ::= [+-]\d+ 
POINT ::= <ABSOLUTE_POINT> | <RELATIVE_POINT>
POINTS ::= <POINT> | <POINTS> 
ABSOLUTE_POINT ::= <NAT>,<NAT>
RELATIVE_POINT ::= <INT>,<INT>

ACTION ::= <LINE> 
  | <RECT> 
  | <CIRCLE> 
  | <SAVE> 
  | <LOAD> 
  | <REMOVE> 
  | <MOVE> 
  | <CLEAR> 
  | <LS> 
  | <QUIT>

LINE ::= line <POINT> <POINTS>

RECT ::= rect <POINT> <POINT>
  | rect <POINT> <NAT> <NAT>

CIRCLE ::= circle <POINT> <NAT>
  | circle <POINT> <POINT> 

SAVE ::= save <STRING>

LOAD ::= load <STRING>

REMOVE ::= remove <POINT>

MOVE ::= move <POINT> <POINT>

CLEAR ::= clear

LS ::= ls
  | ls <POINT>

QUIT ::= quit
```

#### Datatypes

The language contains 5 data types: a stringm a natural number, an integer, a point and a relative point.
The difference between a point (eg. `10,20`) and a relative point (e.g. `+10,-20`) is that relative point is always calculated from the coordinates of its predecessor or from `0,0` if it does not have any preceding point.

#### Line

Draw a line connecting all given points.

#### Rectangle

Draw a rectangle.
It accepts two forms:

- `rect <POINT> <POINT>` where the first point is top-left corner and the second is bottom-right corner.
- `rect <POINT> <NAT> <NAT>` where point is the top-left corner and the two natural numbers indicate width and height.

#### Circle

Draw a circle.
It accepts two forms:

- `circle <POINT> <NAT>` where point is the center and the natural number indicates radius.
- `circle <POINT> <POINT>` where the first point is left-most point of the circle and the second is the right-most point.

#### Save, Load

Save or load shapes to or from a given filename.
The representation is simply a sequence of commands the shapes.

#### Remove

Remove all the shapes that intersects with the given point.

#### Move

Move all the shapes that intersects with the given point to a new point.

#### Clear

Ask for a conformation and if accepted, removes all the shapes.

#### List

List all the shapes or the shapes intersecting the given point in the form of an action that could be used to draw them.  

#### Quit

Ask for a confirmation and if accepted, quits the application.

### Implementation Details

- Most GUI frameworks define `0,0` origin in the top left corner and the `width,height` in the bottom right corner.
- In technical drawing, however, it it usually the bottom left corner that defines origin `0,0` going to top right corner for `width,height`.
- This application will honor the technical drawing. The conversion is done using affine transformation.
- For simplicity make the window non-resizeable and only use the available canvas size. For the ones who want to challenge themselves, feel free to implement panning (scrolling the canvas) and different zoom levels.
- You need Java 11. If you see any problems with running maven, make use maven uses the right Java.

### Implementation Rules

- The requirements marked as _optional_ will earn you extra points. They are also fun to implement.
- Feel free to use the provided skeleton and change whatever needs to be changed.
- You will be judged by the quality of the final application and proper use of object-oriented design.
- Do not copy from other teams, plagiarism is illegal and all concerning teams will be punished.
- Do not use any additional library except for testing. The point is that you, yourself try to implement some of the basic concepts.  
- We provide a few basic icons, feel free to replace them with a better alternatives.
- **If something is not clear, just raise an [issue](https://gitlab.fit.cvut.cz/BI-OOP/cad-java-skeleton/issues/new) in the repo so everyone can see it.**
- If you get stack, contact one of the [teaching assistant](https://moodle.fit.cvut.cz/enrol/index.php?id=38).
- Good luck!
