# fserver
a simple http.server implement with flask and gevent


### install 
```shell
$ pip install fserver
```


### usage
```
Usage:
  fserver [-h] [-d] [-u] [-o] [-i ADDRESS] [-w PATH] [-b PATH] [port]

Positional arguments:
  port                                Specify alternate port, default value 2000

Optional arguments:

  -h, --help                          Show this help message and exit
  -d, --debug                         Use debug mode of fserver
  -u, --upload                        Open upload file function. This function is closed by default
  -o, --override                      Set upload file with override mode, only valid when [-u] is used
  -i ADDRESS, --ip ADDRESS            Specify alternate bind address [default: all interfaces]
  -w PATH, --white PATH               Use white_list mode. Only PATH, sub directory or file, will be share. 
                                      You can use [-wi PATH], i is num from 1 to 23, to share 24 PATHs at most    
  -b PATH, --black PATH               Use black_list mode. It's similar to option '-w'    
  -r PATH, --root PATH                Set PATH as root path for server
```
### license
[MIT](LICENSE)