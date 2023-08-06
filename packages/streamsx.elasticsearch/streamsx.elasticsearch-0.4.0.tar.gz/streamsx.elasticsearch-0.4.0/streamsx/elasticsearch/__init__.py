# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2018

"""
Overview
++++++++

Provides functions to store tuple data as JSON documents in Elasticsearch indices.

Use this package with the following services on IBM Cloud:

  * `Streaming Analytics <https://www.ibm.com/cloud/streaming-analytics>`_
  * `Compose for Elasticsearch <https://www.ibm.com/cloud/compose/elasticsearch>`_


Credentials
+++++++++++

Elasticsearch credentials are defined using a Streams application configuration.

By default an application configuration named `es` is used,
a different configuration can be specified using the ``credentials``
parameter to :py:func:`bulk_insert` or :py:func:`bulk_insert_dynamic`.


Sample
++++++

A simple hello world example of a Streams application writing string messages to
an index::

    from streamsx.topology.topology import *
    from streamsx.topology.schema import CommonSchema, StreamSchema
    from streamsx.topology.context import submit
    import streamsx.elasticsearch as es

    topo = Topology('ElasticsearchHelloWorld')

    s = topo.source(['Hello', 'World!']).as_string()
    es.bulk_insert(s, 'test-index-cloud')

    submit('STREAMING_ANALYTICS_SERVICE', topo)


A simple example of a Streams application writing JSON messages to an index, with dynamic index name (part of the stream)::

    from streamsx.topology.topology import *
    from streamsx.topology.schema import CommonSchema, StreamSchema
    from streamsx.topology.context import submit
    import streamsx.elasticsearch as es

    schema = StreamSchema('tuple<rstring indexName, rstring document>')
    topo = Topology()
    s = topo.source([('idx1','{"msg":"This is message number 1"}'), ('idx2','{"msg":"This is message number 2"}')])
    s = s.map(lambda x : x, schema=schema)
    es.bulk_insert_dynamic(s, index_name_attribute='indexName', message_attribute='document')

    submit('STREAMING_ANALYTICS_SERVICE', topo)

"""

__all__ = ['bulk_insert', 'bulk_insert_dynamic']
from streamsx.elasticsearch._elasticsearch import bulk_insert, bulk_insert_dynamic
