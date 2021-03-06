# engine/__init__.py
# Copyright (C) 2005, 2006, 2007 Michael Bayer mike_mp@zzzcomputing.com
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""defines the basic components used to interface DBAPI modules with
higher-level statement-construction, connection-management, 
execution and result contexts.  The primary "entry point" class into
this package is the Engine.

The package is represented among several individual modules, including:

    base.py
        Defines interface classes and some implementation classes
        which comprise the basic components used to interface between
        a DBAPI, constructed and plain-text statements, 
        connections, transactions, and results.
        
    default.py
        Contains default implementations of some of the components 
        defined in base.py.  All current database dialects use the 
        classes in default.py as base classes for their own database-specific
        implementations.
    
    strategies.py
        the mechanics of constructing ``Engine`` objects are represented here.
        Defines the ``EngineStrategy`` class which represents how to go from 
        arguments specified to the ``create_engine()`` function, to a fully
        constructed ``Engine``, including initialization of connection pooling,
        dialects, and specific subclasses of ``Engine``.
        
    threadlocal.py
        the ``TLEngine`` class is defined here, which is a subclass of the generic
        ``Engine`` and tracks ``Connection`` and ``Transaction`` objects against
        the identity of the current thread.  This allows certain programming patterns
        based around the concept of a "thread-local connection" to be possible.  The
        ``TLEngine`` is created by using the "threadlocal" engine strategy in 
        conjunction with the ``create_engine()`` function.
        
    url.py
        Defines the ``URL`` class which represents the individual components of a 
        string URL passed to ``create_engine()``.  Also defines a basic module-loading
        strategy for the dialect specifier within a URL.
        
"""

from sqlalchemy import databases
from sqlalchemy.engine.base import *
from sqlalchemy.engine import strategies
import re

def engine_descriptors():
    """Provide a listing of all the database implementations supported.

    This data is provided as a list of dictionaries, where each
    dictionary contains the following key/value pairs:

    name
      the name of the engine, suitable for use in the create_engine function

    description
      a plain description of the engine.

    arguments
      a dictionary describing the name and description of each
      parameter used to connect to this engine's underlying DBAPI.

    This function is meant for usage in automated configuration tools
    that wish to query the user for database and connection
    information.
    """

    result = []
    for module in sqlalchemy.databases.__all__:
        module = getattr(__import__('sqlalchemy.databases.%s' % module).databases, module)
        result.append(module.descriptor())
    return result

default_strategy = 'plain'
def create_engine(*args, **kwargs):
    """Create a new Engine instance.

    The standard method of specifying the engine is via URL as the
    first positional argument, to indicate the appropriate database
    dialect and connection arguments, with additional keyword
    arguments sent as options to the dialect and resulting Engine.

    The URL is a string in the form 
    ``dialect://user:password@host/dbname[?key=value..]``, where 
    ``dialect`` is a name such as ``mysql``, ``oracle``, ``postgres``,
    etc.  Alternatively, the URL can be an instance of ``sqlalchemy.engine.url.URL``.

    `**kwargs` represents options to be sent to the Engine itself as
    well as the components of the Engine, including the Dialect, the
    ConnectionProvider, and the Pool.  A list of common options is as
    follows:

    poolclass
      a subclass of ``sqlalchemy.pool.Pool`` which will be used to 
      instantiate a connection pool.
      
    pool
      an instance of ``sqlalchemy.pool.DBProxy`` or
      ``sqlalchemy.pool.Pool`` to be used as the underlying source for
      connections (DBProxy/Pool is described in the previous
      section).  This argument supercedes "poolclass".

    echo
      Defaults to False: if True, the Engine will log all statements
      as well as a repr() of their parameter lists to the engines
      logger, which defaults to ``sys.stdout``.  A Engine instances'
      `echo` data member can be modified at any time to turn logging
      on and off.  If set to the string 'debug', result rows will be
      printed to the standard output as well.

    logger
      Defaults to None: a file-like object where logging output can be
      sent, if `echo` is set to True.  This defaults to
      ``sys.stdout``.

    encoding
      Defaults to 'utf-8': the encoding to be used when
      encoding/decoding Unicode strings.

    convert_unicode
      Defaults to False: true if unicode conversion should be applied
      to all str types.

    module
      Defaults to None: this is a
      reference to a DBAPI2 module to be used instead of the engine's
      default module.  For Postgres, the default is psycopg2, or
      psycopg1 if 2 cannot be found.  For Oracle, its cx_Oracle.  For
      mysql, MySQLdb.

    strategy
      allows alternate Engine implementations to take effect.
      Current implementations include ``plain`` and ``threadlocal``.  
      The default used by this function is ``plain``.

      ``plain`` provides support for a Connection object which can be used
      to execute SQL queries with a specific underlying DBAPI connection.

      ``threadlocal`` is similar to ``plain`` except that it adds support
      for a thread-local connection and transaction context, which
      allows a group of engine operations to participate using the same
      underlying connection and transaction without the need for explicitly
      passing a single Connection.
    """

    strategy = kwargs.pop('strategy', default_strategy)
    strategy = strategies.strategies[strategy]
    return strategy.create(*args, **kwargs)
