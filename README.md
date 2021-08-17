allfed-integrated-model
==============================

An integrated economic model for resilient foods

# Installation
Dependencies are managed using Poetry - install it if you don't have it: https://python-poetry.org/
To install:
```bash
poetry install
```
# Run the model

### Using Colab (most users use this):
The interactive model runs off colab. It doesn't require any downloading or code, you just need to hit the right buttons as they show up. Here's a demo:

first click on the "notebooks" folder, highlighted below
![step1](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step1.png)

[!step2](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step2.png)

open example_optimize.ipynb

![step3](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step3.png)

click 'Open in Colab'

![step4](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step4.png)

'Authorize with github'
![step5](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step5.png)

'OK'

![step6](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step6.png)

for repository, select 'allfed/allfed-integrated-model' branch 'main', then click on the item labelled under Path, 'notebooks/example_optimize.ipynb'

![step7](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step7.png)


Now we're in the actual code! If you scroll down, you can see where all the constants are set. But first we need to run the Colab environment. Following along with the instructions,
![step8](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step8.png)


"Run Anyway"

![step9](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step9.png)


Hit the black arrow on the left, and press 'enter' inside each entry box as the instructions say.
You will get a nice ascii picture.
Moving on, run the lines up to and including the 'cat' command.
![step10](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step10.png)

select all that text the cat command generateds, and copy it.

![step11](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step11.png)

navigate to the URL mentioned, hit 'New SSH Key'. Name it something and paste the key in.

![step12](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step12.png)


hit 'Add SSH key'. Might have to put your github password in again.

Finally, return to the code to check that it worked.

![step13](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step13.png)
Should look like message above.
Run the remaining blocks one at a time, be sure they've completed before running the next one.
![step14](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step14.png)

and continue to run the blocks, if everything has gone well, you can run each block of the code.
![step15](https://raw.githubusercontent.com/allfed/allfed-integrated-model/main/step15.png)

Please let me know if any of these steps go awry!

### From the command line (requires cloned repo):
```bash
poetry shell
python src/cheri.py
```

### Using Jupyter (requires cloned repo):
```bash
poetry run jupyter lab
```
Then navigate to the `notebooks` folder, open `1.0-example-run-cheri.ipynb`, and
execute each cell in order, ignoring the first cell

# Project Tree

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── pyproject.toml   <- The dependencies file for reproducing the modelling environment using poetry
    ├── poetry.lock   <- Fixed versions for each dependency
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
        └── __init__.py    <- Makes src a Python module

--------
