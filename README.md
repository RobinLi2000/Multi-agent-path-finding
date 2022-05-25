# Universal Plans for Multi-Agent Path Finding

### Dependence:

```
pip install -r requirements.txt
```

### Usage:

```
usage: run.py [-h] [--agents AGENTS [AGENTS ...]] [--map MAP] [--goals GOALS [GOALS ...]] [--vis]
              [--save SAVE]

Multi-Agent Path Finding Term Project.

optional arguments:
  -h, --help            show this help message and exit
  --agents AGENTS [AGENTS ...]
                        Specify a list of agent names
  --map MAP             Specify a map
  --goals GOALS [GOALS ...]
                        Specify the goals for each agent,e.g. 2_0 0_2
  --vis                 Visulize the process
  --save SAVE           Specify the path to save the animation vedio
```

Example:

```
python run.py --agents p1 p2 --map empty --goals 5_5 1_5 --vis --save empty.mp4
```

You may need to install `ffmpeg` to support `.mp4` extension,

```
conda install -c conda-forge ffmpeg
```
