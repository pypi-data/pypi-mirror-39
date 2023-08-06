## <project-root>

#### this directory keeps the main code specifically written for this project
This directory **is tracked by git**.

This directory **is tarballed into the `data_runs` directory** at every run.

***

This directory includes:

./main.py:
- pyton script responsible for managing data and collecting output, saving data,
tarballing source-code, etc.  
- it calls all subsequent experiments located in ./src/experiments

./experiments/
- directory containing sub-experiments

./include/
- directory containing additional files required to run
   
   (for example;)
   ./include/spice/ 
   - subdirectory containing spice netlists.

./METADATA.md:
- text file (markdown) describing the experiment and data completely

./post
- directory housing codes used for post-processing of data (if any)

