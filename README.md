# Refyre: Filesystem dominance is all you need
[![PyPI Version](https://img.shields.io/pypi/v/refyre.svg)](https://pypi.python.org/pypi/refyre)
___ 

Refyre is an AI-fused Python package that provides two high level features:
- Easy large scale filesystem manipulations
- Efficient, code-less directory structuring and restructuring

Enhance your favorite Python packages such as Pandas, NumPy, Spark, and other data manipulation tools to quickly structure scattered data.

## Features
- Filesystem agnostic data handshakes 
- Kickstart loading entire repositories & setting up virtual environments in a single command, your way
- Perform mass operations on files such as copying, moving, zipping, POST-ing, in 1 line of code
- Homebrew structured data such as Pandas DataFrames, and image datasets in a snap of your fingers (< 30 lines)
- Refactor, organize, and analyze periodic research experiments with zero lines of code

## Quickstart
Simply provide refyre with an "input specification", telling it what directories to focus on

`sample_input_spec.txt`
```python
'''
Suppose you have a directory structure

a/
    a1.txt
    a2.txt
    ...
b/
    c/
        c1.txt
        c2.txt
        d.txt
        d2.txt
        ...

You seek to analyze the a files and the c files
'''
[dir="a"|name="a_var"]
[dir="b"]
    [dir="c"|pattern="g!c?.txt"|name="c_var"] #Glob patterns start with 'g!', regex with 'r!', no need for just normal pattern matching
```

Have refyre analyze the directory with the following:
```python
#Main analysis line
ref = Refyre(input_specs = ['sample_input_spec.txt'])

#Now, have a bit of fun!
a_var = ref["a_var"]
c_var = ref["c_var"]

print(len(a_var)) #Number of files

#Move all the files to another directory, copy works the same way
a_var = a_var.move('dir2') #.copy() ...

#Get all the files in a List[Pathlib.Path] objects
all_a_var = a_var.vals()

#Automatically zip a copy of all the files 
zipped_c_var = c_var.zip()

print(len(zipped_c_var)) #1, the zipped c_var files

#Get all the parents dirs
c_var_parent_dirs = c_var.dirs()

print(type(c_var)) #refyre.cluster.FileCluster (this is what each variable type is)

#Do mass file management operations such as delete(), filter()
all_a_var_and_c_vars = FileCluster(values = []) #Values are strings of filepaths you want to do operations on
all_a_var_and_c_vars = a_var + c_var

filtered_c = all_a_var_and_c_vars.filter(lambda p : p.name.startswith('c'))

#Delete all files
filtered_c.delete()

#Automatically account for any modifications by variables
print(len(all_a_var_and_c_vars))

```

And finally, after any analysis, you can use the variables to generate
specs

Let's say you want to generate directories & data in the format specified by `output_spec.txt`:

```python
'''
Sample output spec, creates
directories d & e, and ports the data
from a_var and c_var into it.
'''
[dir="d"|name="a_var"]
[dir="e"|name="c_var"]
```

One line.
```python
ref.create_spec('output_spec.txt')
```

Alternatively, this entire process (minus the in-between analysis) can be done through our CLI.
```python
refyre -i input.txt -o output.txt
```

## Microdocs

Let's provide a quick overview of the various capabilities refyre packs.

### Spec Attributes:

Specs, as shown above are a Pythonic way for you to feed information to refyre. Each [] represents a *cluster*, which usually has a dir attribute specified. Attributes are seperated using the '|' seperator. 

As shown above, Pythonic comments can be used in a similar fashion to Python. Back to the various attributes:

- **dir**: Specifies the directory the cluster is targeting. *Usually, the clusters are relative paths*.
    - You can specify the three pattern types to target multiple directories
- **pattern**: Allows you to target specific files by specifying a template pattern. Currently, glob, regex, and "generator expressions" are supported.
  - For glob patterns, add a 'g!' before the pattern; ex: `g!*.txt`
  - For regex patterns, add an 'r!' before the pattern ex: `r!.txt`
  - Generator expressions a simplified pattern matching, that's more humanly controllable
    - Just one template matching --> `$` matches to a number
    - refyre supports generator expressions the most out of the three

- **name**: The workhorse of specs. Arguably the **meat** of the spec. Assigns all the values to a variable specified by **name**. *Only single variable / cluster are supported*
    - You can achieve 'appending' by specifying a `+` before the name
- **flags**: A grab bag of various tricks you can use. You can specify as many as you want, and they work together to bring out cool cluster behaviours
  - `*m` makes a directory if it doesn't exist in a read spec
  - `*d` (only during generation) deletes everything in the *current* directory except for the clusters specified
  - `*da` deletes everything in the *current & all subclusters* except for clusters listed
  - `*f` gets all the files listed in the current directory
  - `*d` gets all the directories listed in the current directory
  - `*r` allows `*f` and `*d` to behave recursively (i.e, get all files from subdirectories, etc.)
  - `*s` enables *step generation*, Each time `refyre.step()` is called, the next directory in the pattern is generated. (ex:, if `dir="test$"` and `*s`, `test1` would be generated on first `.step()`, `test2`, ...)
  - `*c` enables code analysis. If you seek to import a directory / repository you recently cloned, you can specify the `*c` flag and then import it in your code
  - `type & link` are used for specific behaviours, most commonly *git cloning*. Automatically clone in repos by specifying `type="git"` and the link to your git.
- **mode**: Can either be set to `cut` or `copy`. During generation, the variable files will either be cut or copied to their respective place.
- **limit**: Limits the number of results targeted, or directories generated
- **serialize** specify a generator expression to rename all the files into a consistent format

These are all the basic quantifiers you can use, they cover ~80% of refyre's inner power. The other 20% are pretty obscure and aren't that useful normally.

### FileClusters (Variables)

Variables are the backbone of refyre. The clusters provide an *avenue* for the variables to easily target the data without worrying about writing any code. However, they aren't the only way to access variable's powers. The docs below, again, specify the most useful abilities for these variables.

`FileCluster(values = [], dirs = [], patterns = [], as_pathlib = False,)`
    - `values`: string filepaths, or `Path` objects depending on whether `as_pathlib` is true or false.
    - `patterns`: corresponds to the dirs, lists what patterns you want to target

FileClusters are strongly rooted in *object oriented operations*, meaning each operation returns another FileCluster, so you can continue channeling FileCluster capabilities. To get out of FileClusters, you can use the following options:
    - `.vals()`: Returns a list of Path objects
    - `.item()`: Returns the first Path object

Using this basic constructor, you can make some easy operations:
  - `.move(target_dir)`
  - `.copy(target_dir)`
  - `.filter(filter_func)`
  - `.map(map_func)`
  - `.zip()`
  - `.delete()`
  - `.post(url, additional_data, payload_name)` 
  - `.filesize()`
  - `.clone()`

You can also do other operations between FileClusters
  - `+` (Returns the sum of the contents of two FileClusters)  
  - `-` (Returns the contents in the current FileCluster while removing all other contents that are also in the other FileCluster)
  - `&` (Intersection operator)
  - `|` (Union operator)

### The Refyre Object

These docs are running too long already, I will try to keep this as short as possible.

- `Refyre(input_specs = [], output_specs = [])`
  - Instantiates a refyre spec

- `add_spec(spec_path, track = False)`
  - Adds a spec for refyre *reading*. If track is set to true, it can
  later be reused for step generation.

- `create_spec(spec_path, track = False)`
  - Creates a spec. If track is set to true, it can later be reused for step 
  generation.

- `step()`
  - Any specs with a `*s` attribute have the next directory in the patterns they specify generated

Accessing variables can be done using the `[]` notation. Use it to get and attach variables to a `Refyre` object.

**Congratulations, you know everything to be a refyre expert!**

### Misc Docs

#### DataStack
Let's say you want to brew a dataset & structure data of you're own. refyre allows you to combine the power of variables with the DataStack, processing them to create constructs such as Pandas Dataframes.

The process is twofold - (1) *secure your variables*, and then (2) *run them through the DataStack*. The DataStack itself is a *processor*, taking in a bunch of variables, and producing the variables.

Your job with the DataStack will be to figure out how can you convert the variables to the dataset format you want.

Consider the PandasStack (a DataStack). Here, your job is to figure out how you can convert each row of variables into a *DataFrame column*

```python

from refyre import Refyre
from refyre.datastack import PandasStack
from PIL import Image
import pandas as pd

ref = Refyre(input_specs = ['specs/in.txt'])

#We will do some pandas visualizations on the input data
stack = PandasStack(AssociationCluster(input_vars = [ref["images"]]))

def processor(fp):
    print('processing', fp)
    im = Image.open(fp).convert('RGB')
    width, height = im.size 

    ar, ag, ab = 0.0, 0.0, 0.0
    for i in range(width):
        for j in range(height):
            r, g, b = im.getpixel((i, j))
            ar, ag, ab = ar + r, ag + g, ab + b 
        
    ar, ag, ab = ar / (width * height), ag / (width * height), ab / (width * height)
    return (fp.name, width, height, ar, ag, ab)

df = stack.create_dataframe(['image_name', 'image_width', 'image_height', 'average_red', 'average_green', 'average_blue'], processor)
```

As you can see, the majority of the work here comes from building a *processor* method to convert each row of variables into a DataFrame row.
