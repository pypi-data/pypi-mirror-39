**tkDataCanvas** is a tabular data display widget for Python + Tkinter. It is intended as a more efficient replacement for [tkMagicGrid](https://github.com/bmjcode/tkMagicGrid) and [tkScrolledFrame](https://github.com/bmjcode/tkScrolledFrame) for displaying large amounts of static data.

tkDataCanvas is designed to be simple above all else. It has no dependencies outside the Python standard library. Its API is designed to let you accomplish tasks with as few method calls as possible.

Both Python 2 and 3 are supported, on Windows and Unix platforms.

## Usage

tkDataCanvas consists of a single module, `tkdatacanvas` (note the module name is lowercase), which exports a single class, `DataCanvas`.

A brief example program:

```python
# This assumes Python 3
from tkinter import *
from tkdatacanvas import DataCanvas
import io
import csv

# Create a root window
root = Tk()

# Create a DataCanvas widget
dc = DataCanvas(root)
dc.pack(side="top", expand=1, fill="both")

# Display the contents of some CSV file
with io.open("test.csv", "r", newline="") as csv_file:
    reader = csv.reader(csv_file)
    parsed_rows = 0
    for row in reader:
        if parsed_rows == 0:
    	    # Display the first row as a header
    	    dc.add_header(*row)
        else:
    	    dc.add_row(*row)
        parsed_rows += 1
dc.display()

# Start Tk's event loop
root.mainloop()
```

For detailed documentation, try `python -m pydoc tkdatacanvas`.
