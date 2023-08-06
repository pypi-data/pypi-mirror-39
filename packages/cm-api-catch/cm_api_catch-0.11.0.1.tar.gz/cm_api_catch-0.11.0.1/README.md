
=======
Cloudera Manager RESTful API Clients
====================================

> [Cloudera Manager](http://www.cloudera.com/products-services/tools/) is the market-leading management platform 
> for [CDH](http://www.cloudera.com/hadoop/). As the industry’s first end-to-end 
> management application for Apache Hadoop, Cloudera Manager sets the standard for enterprise deployment by 
> delivering granular visibility into and control over every part of CDH – empowering operators to improve 
> cluster performance, enhance quality of service, increase compliance and reduce administrative costs.

This project contains all the source, examples and documentation 
you need to easily build a [Cloudera Manager](http://www.cloudera.com/products-services/tools/) client in 
[Java](java) or [Python](python).

All source in this repository is [Apache-Licensed](LICENSE.txt).

This client code allows you to interact with Cloudera Manager to:
* Manage multiple clusters
* Start and stop all or individual services or roles
* Upgrade services running on your cluster
* Access time-series data on resource utilitization for any activity in the system
* Read logs for all processes in the system as well as stdout and stderr
* Programmatically configure all aspects of your deployment
* Collect diagnostic data to aid in debugging issues
* Run distributed commands to manage auto-failover, host decommissioning and more
* View all events and alerts that have occurred in the system
* Add and remove users from the system


Welcome to Cloudera Manager API Client!

Python Client
=============
The python source is in the `python` directory. The Python client comes with a 
`cm_api` Python client module, and examples on performing certain Hadoop cluster 
administrative tasks using the Python client.

Getting Started
---------------
Here is a short snippet on using the `cm_api` Python client:

    Python 2.7.2+ (default, Oct  4 2011, 20:06:09) 
    [GCC 4.6.1] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from cm_api.api_client import ApiResource
    >>> api = ApiResource('rhel62-1.ent.cloudera.com', 7180, 'admin', 'admin')
    >>> for h in api.get_all_hosts():
    ...   print h.hostname
    ... 
    rhel62-2.ent.cloudera.com
    rhel62-4.ent.cloudera.com
    rhel62-3.ent.cloudera.com
    rhel62-1.ent.cloudera.com
    >>> 

Another example: getting all the services in a cluster:

    >>> for c in api.get_all_clusters():
    ...   print c.name
    ... 
    Cluster 1 - CDH4
    >>> for s in api.get_cluster('Cluster 1 - CDH4').get_all_services():
    ...  print s.name
    ... 
    hdfs1
    mapreduce1
    zookeeper1
    hbase1
    oozie1
    yarn1
    hue1
    >>> 

Shell
-----
After installing the `cm_api` Python package, you can use the API shell `cmps`
(CM Python Shell):

    $ cmps -H <host> --user admin --password admin
    Welcome to the Cloudera Manager Console
    Select a cluster using 'show clusters' and 'use'
    cloudera> show clusters
    +------------------+
    |   CLUSTER NAME   |
    +------------------+
    | Cluster 1 - CDH4 |
    | Cluster 2 - CDH3 |
    +------------------+
    cloudera> 

Please see the `SHELL_README.md` file for more.

Example Scripts
---------------
You can find example scripts in the `python/examples` directory.

* `bulk_config_update.py` ---
  Useful for heterogenous hardware environment. It sets the configuration on
  the roles running on a given set of hosts.
