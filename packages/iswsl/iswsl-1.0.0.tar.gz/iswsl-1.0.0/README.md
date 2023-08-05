Python utility to check whether the current script runs inside Windows' WSL.

Here's how to use it:

```python
from iswsl import is_wsl

if is_wsl():
    print('Running inside WSL')
else:
    print('Running outside WSL')

```