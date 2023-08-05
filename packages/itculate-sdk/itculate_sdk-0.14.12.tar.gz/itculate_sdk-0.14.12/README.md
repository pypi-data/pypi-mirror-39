# Overview #
This repository is the Software Developer Kit (SDK) for ITculate. 
For more information on ITculate please visit our web site: [ITculate.io](https://goo.gl/FkWxS4).

# Python SDK #

Python client SDK providing convenient wrapper for the ITculate REST API to upload graph, time-series and dictionary data to the ITculate engine.

### Initializing ###

Before using the SDK, you need to initialize it. 

The SDK can work directly with the ITculate API (upload to https://api.itculate.io). 
In this case, you must provide the tenant_id, API key & secret for the tenant (you can get all 3 values from the Setup page in the Web UI).

    import itculate_sdk as itsdk
    
    itsdk.init(tenant_id="<<< tenant ID >>>", api_key="<<< your API key>>>, api_secret="<<< your API secret>>>")


Alternatively, if an agent is installed, the SDK can forward payloads to the agent for uploading. In this case, no additional credentials are 
 required (these are all part of the agent's configuration)

    import itculate_sdk as itsdk 
    
    itsdk.init(provider="AgentForwarder")


### Reporting Graph (Topology) Data ###

To report topology data, you need to decide on a collector ID. This is the identifier that will be used by the ITculate graph engine to automatically 
 detect changes between reports. Each time a collector reports graph, it needs to report 'everything it sees'. A full topology can (and is encouraged to) be 
 split into multiple different collectors, each reporting about a part of the environment.
 
Note that a vertex is a document and can have any number of attributes.
A vertex can have more than one key (as long as their unique). You do this by providing a dict of keys instead of a string.
   
    collector_id = "my_collector"
    
    with itsdk.Flusher():
        group = itsdk.add_vertex(collector_id=collector_id,
                                 name="my group",
                                 vertex_type="MyVertexGroupType",
                                 keys="my-group-key",
                                 some_additional_attribute="some value",
                                 some_typed_attribute=itsdk.CapacityDataType.value(10.0)

        server1 = itsdk.add_vertex(collector_id=collector_id,
                                   name="my server 1",
                                   vertex_type="MyVertexType",
                                   keys="my-server-key1")

        server1 = itsdk.add_vertex(collector_id=collector_id,
                                   name="my server 2",
                                   vertex_type="MyVertexType",
                                   keys="my-server-key2")
                                   
        server1 = itsdk.add_vertex(collector_id=collector_id,
                                   name="my server 3",
                                   vertex_type="MyVertexType",
                                   keys="my-server-key3")

To connect an edge between vertices, you can use either use a key (string) or simply provide the vertex object. When providing more than one vertex, the SDK 
will automatically connect all the individual list items.

The 'topology' is a name you give to the edge type. Later on, you can decide to view / filter topologies by their type.

    itsdk.connect(collector_id=collector_id,
                  source=group,
                  target=[server1, server2, server3],
                  topology="dependency")

This is it! Since we used the itsdk.Flusher, the itsdk.flush_all() will be automatically called.


### Reporting timeseries data ###

A vertex can have any number of counters reported for it. Each counter has a data type (one of itsdk.DataTypeWithUnit subclasses)
that indicates metadata information about this counter like priority, resampling method, default units, etc...

To report a sample:

    itsdk.add_sample(vertex=server1,
                     counter="requests",
                     value=itsdk.RequestCountDataType.value(100.0))


### About Data Types ###

Data types are an importance concept. Choosing the correct data type affects how the metric will be displayed in the product. Metrics of similar data types are displayed together to allow to easily identify correlated values. 

#### 'Importance' - The Sorting order ####

In addition to basic meta data properties like units, labels, description, etc... data types also define how they should be sorted. Before displaying selected metrics, the UI will sort all counters by their 'importance' and make sure to display the more important ones first.

When choosing a resource to display, the system will automatically pick the 3 most 'important' metrics to display with. 

#### 'Importance' - ranges ####

To make it easier to define the importance values, we split the data type importance into a few buckets:

    0-999     (itsdk.Importance.KPI_USER)         - Reserved for custom metrics. Indicate a metric that should be addressed as a KPI
    1000-1999 (itsdk.Importance.KPI_SYSTEM)       - Used by the system to report KPIs for auto discovered objects (e.g. AWS instances)
    2000-2999 (itsdk.Importance.IMPORTANT_USER)   - Reserved for custom metrics. Indicate a metric that is important but is not a KPI
    3000-3999 (itsdk.Importance.IMPORTANT_SYSTEM) - Used by the system to report metrics that are important by not KPIs
    4000-4999 (itsdk.Importance.OTHER_USER)       - Reserved for custom metrics. Should be used for any other metric
    5000-5999 (itsdk.Importance.OTHER_SYSTEM)     - Used by the system to report other metrics

You can play within these ranges for a better control on how counters of the same range are sorted

### Reporting event data ###

The SDK can be used to report events about vertices.

You can report health related events

    itsdk.vertex_unhealthy(collector_id=collector_id, 
                           vertex=server1, 
                           message="Server 1 is DOWN!")
    
    itsdk.vertex_healthy(collector_id=collector_id, 
                         vertex=server1, 
                         message="Server 1 is back up!")

Or you can report a generic event

    vertex_event(collector_id=collector_id,
                 vertex=server1,
                 message="Some generic message",
                 event_type="INFORMATIONAL",
                 severity="INFO")


# REST API #

The SDK is using the ITculate REST API to upload data. This API can be used directly, given an API key for the 'upload' role.

### Endpoint ###
POST https://api.itculate.io/api/v1/upload

    Content-Type: application/json
    Accept: application/json
    Authorization: Basic <<< ENCODED KEYS >>>

Simple authentication with api key pair for the '**upload**' role. This is the same user (and role) used to upload data with the ITculate collector module. An API key can be retrieved from the web UI.

### Collector ID ###

* Format: a-z, A-Z, 0-9 or '_' only
* Unique (within the tenant) 

Represents the 'reporter' of the topology and is used by the ITculate engine to detect changes between subsequents reports made by the same collector.

After the first report, the collector status can be viewed using the https://api.itculate.io/api/v1/collectors/ endpoint.

Removing a collector (and deleting everything it reported) can be done via a DELETE http call to https://api.itculate.io/api/v1/collectors/your_collector_id endpoint.

### Collector Version ###

Any string representing the version of the code that collected the data. This information can be tracked in the collectors view (or https://api.itculate.io/api/v1/collectors/).

### Host ###

A string representing the machine that hosts the collector. This information can be tracked in the collectors view (or https://api.itculate.io/api/v1/collectors/).

### Vertices ###

Each vertex document describes a single vertex in the graph.
A vertex is a document that contain any data, and has a few mandatory attributes.

##### Keys ("_keys") #####
A vertex can have more than one key. Keys are provided with names (mostly used for reference) and need to be globally unique.
These keys are used by the ITculate engine to identify existing vertices, as well as connecting between edges to form graphs.

##### Type ("_type") #####
Vertex type is a string that categorizes the vertex and allows visual grouping. Each vertex type will be assigned a unique color (or icon) to represent it visually on the graph. 

##### Name ("_name") #####
A human readable display name for the vertex.

##### Custom attributes #####
Since a vertex is a document, it can hold any number of additional custom attributes (their name should NOT start with "_"). These attributes can be used to add information about the vertex, contact information, URLs to documentation, etc...


### Edges ###
Edges represent connections between vertices in the graph. Each edge identified the 'source' and 'target' vertices it connects and is associated with a type.

A graph that traverses a specific edge type is called a 'Topology'. Topologies are used to represent different layers and perspectives of the architecture and infrastructure.

##### Edge Type ("_type") #####
The edge type. 

* Edge type should NOT start with "_".
* There is no limit for the number of edge types.
* There is no limit to the number of edges (of different types) that can connect two vertices.

##### Source ("_source_keys") and Target ("_target_keys") keys #####
Identify the source / target vertex the edge connects.

* Can be a subset of the vertex keys (at least one needs to match)
* An edge will be created only if BOTH source AND target keys are resolved to existing vertices in the DB

### JSON example ###

    {
        "collector_id": "unique_collector_id",
        "collector_version": "0.1.1",
        "host": "1.1.1.1",
        "vertices": [
            {
                "_type": "MyVertexType",
                "_name": "The vertex display name",
                "_keys": {
                    "any_key_name1": "globally_unique_key_value1",
                    "any_key_name2": "globally_unique_key_value2",
                    ...
                },
                "custom_attribute1": "Anything",
                ...
            },
            ...
        ],
        "edges": [
            {
                "_type": "my_edge_type",
                "_source_keys": {
                    # One of more of a vertex keys
                    "any_key_name1": "globally_unique_key_value1",
                },
                "_target_keys": {
                    # One or more of a vertex keys
                    "any_key_name2": "globally_unique_key_value2",
                }
            },
            ...
        ],
    }

### Who do I talk to? ###

* email to opensource@itculate.io