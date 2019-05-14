# runos-forecast
Runos load forecasting

Usage:

```sh
PYTHONPATH=path/to/project/dir python3 scripts/method.py \
    [-h] [--dc] --interval INTERVAL --hist_len HIST_LEN [--k K] \
    [--corr_interval CORR_INTERVAL] [-s S] [-c] file    

positional arguments:
  file                  CSV input

optional arguments:
  -h, --help            show this help message and exit
  --dc, -d              Specify if input is not Runos
  --interval INTERVAL, -F INTERVAL
                        F
  --hist_len HIST_LEN, -W HIST_LEN
                        W
  --k K                 k
  --corr_interval CORR_INTERVAL, -M CORR_INTERVAL
                        M
  -s S                  JSON with predefined models
  -c                    Count model changes and steps
```
