### Project description

Dailylog is a utility for recording daily logs on your own word.  

You can easily master its usage through this document.

### Why should I use dailylog?

The goal of dailylog is to provide a simple way to create daily-log files. In the build-in modules **logging**, 
which has to config the date and log format, besides, if you want to devide the logs by day, you will need to create a 
TimedRotatingFileHandler.

But in the dailylog, we provide a simply way to handle the log files, you can flexibly record what you want, avoiding to 
take some unimportant information, such as trackback, warning from the django, and so on. Also, the module can 
automatically make daily-log files. 

### Installation

`$pip install dailylog`

nowadays we only provide linux wheel, if you are using Windows platform, you can download the source file and run the following command:
  
`$python setup.py install`

### Using dailylog

1. import the module and create a filehandler:

```
import dailylog
file_handler = dailylog.LogHandler()
```

we provide three parameters for LogHandler:

- date_format: as named, default is "%Y-%m-%d--%H:%M:%S"
- log_dir: target folder to save the log files, default is "./logs/". if the folder does not exist, the system will create it automatically.
- print_symbol: whether to print the message on the terminal. Default is **True**

2. make different logs:

```angular2html
file_handler.debug(some message)
file_handler.info(some message)
file_handler.warning(some message)
file_handler.error(some message)
```

3. show different logs:

```angular2html
file_handler.show_debug(date)
file_handler.show_info(date)
file_handler.show_warning(date)
file_handler.show_error(date)
```

While will show the corresponding message of the date. The default date is *time.strftime('%Y-%m-%d', time.localtime(time.time()))*，
 which means today. 

### Github

https://github.com/darkwhale/day_log
