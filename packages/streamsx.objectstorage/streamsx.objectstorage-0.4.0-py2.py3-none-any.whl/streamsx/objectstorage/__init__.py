# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2018

"""
Overview
++++++++

`IBM® Cloud Object Storage <https://www.ibm.com/cloud/object-storage>`_ (COS) makes it possible to store practically limitless amounts of data, simply and cost effectively. It is commonly used for data archiving and backup, web and mobile applications, and as scalable, persistent storage for analytics.

This module allows a Streams application to create objects in parquet format :py:func:`write_parquet <write_parquet>` or
to write string messages with :py:func:`write <write>` from a stream
of tuples.
Objects can be listed with :py:func:`scan <scan>` and read with :py:func:`read <read>`.

Credentials
+++++++++++

Cloud Object Storage credentials are defined using a Streams application configuration or setting the Cloud Object Storage service credentials JSON directly to the ``credentials`` parameter of the functions.

By default an application configuration named `cos` is used,
a different configuration can be specified using the ``credentials``
parameter to :py:func:`write`, :py:func:`write_parquet`, :py:func:`scan` or :py:func:`read`.

The application configuration must contain the property ``cos.creds`` with a value of the raw Cloud Object Storage credentials JSON.

Sample
++++++

A simple hello world example of a Streams application writing string messages to
an object. Scan for created object on COS and read the content::

    from streamsx.topology.topology import *
    from streamsx.topology.schema import CommonSchema
    from streamsx.topology.context import submit
    import streamsx.objectstorage as cos

    topo = Topology('ObjectStorageHelloWorld')

    to_cos = topo.source(['Hello', 'World!'])
    to_cos = to_cos.as_string()

    bucket = 'streamsx-py-sample'
    # Write a stream to COS
    cos.write(to_cos, bucket, '/sample/hw%OBJECTNUM.txt')

    scanned = cos.scan(topo, bucket=bucket, directory='/sample')
    
    # read text file line by line
    r = cos.read(scanned, bucket=bucket)
    
    # print each line (tuple)
    r.print()

    submit('STREAMING_ANALYTICS_SERVICE', topo)

"""

__version__='0.4.0'

__all__ = ['write_parquet', 'scan', 'read', 'write']
from streamsx.objectstorage._objectstorage import write_parquet, scan, read, write
