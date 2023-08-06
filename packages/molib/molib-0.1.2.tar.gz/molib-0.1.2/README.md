# molib
This package contains functions that I keep re-using in different packages, so I decided to publish it in case it helps other too.

# Installation
To install molib, use pip (or similar):
```{.sourceCode .bash}
pip install molib
```

# Documentation
```python
label_subplots(fig, size=14)
  ```
Adds letter labels to all subplots in a figure.
Adjusts figure padding and left margin to make labels fit.

```python
add_subfig_label(ax, label, size=14)
```
Adds a subplot label to an axis.

```python
gen_sub_label(lower=False, paren=False)
```
Generates the next letter in the alphabet as a subfig label.
Label can be uppercase or lowercase, with optional parentheses.

```python
save_plot(output_filename, proj_dir=Path.cwd(), subdir=None, fig=None)
```
Function for saving plots and printing message; makes plots directory.
