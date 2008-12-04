#!/bin/sh -e

DIRECTORY=`pwd` # FIXME: replace it with real path

case "$1" in
  start)
    $DIRECTORY/start.py serve --daemon --pid-file=$DIRECTORY/webgriffith.pid --log-file=$DIRECTORY/logs/deamon.log $DIRECTORY/production.ini start
    ;;
  stop)
    $DIRECTORY/start.py serve --daemon --pid-file=$DIRECTORY/webgriffith.pid --log-file=$DIRECTORY/logs/deamon.log $DIRECTORY/production.ini stop
    ;;
  restart)
    $DIRECTORY/start.py serve --daemon --pid-file=$DIRECTORY/webgriffith.pid --log-file=$DIRECTORY/logs/deamon.log $DIRECTORY/production.ini restart
    ;;
  *)
    echo $"Usage: $0 {start|stop|restart}"
    exit 1
esac

exit 0
