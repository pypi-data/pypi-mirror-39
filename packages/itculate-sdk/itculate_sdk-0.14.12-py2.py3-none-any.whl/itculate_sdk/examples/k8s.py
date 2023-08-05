import datetime

from unix_dates import UnixDate

import itculate_sdk as itsdk

itsdk.init(role="cloudoscope")

#############################
# create topology
#############################

collector_id = "kubernetes"

kubernetes = itsdk.add_vertex(name="lab-cluster",
                              vertex_type="Kubernetes",
                              keys="kubernetes-cluster",
                              collector_id=collector_id,
                              data={
                                  "attr1": "attr_value_1",
                                  "attr2": "attr_value_2",
                              })

node1 = itsdk.add_vertex(name="node1 (i-1438811)",
                         vertex_type="EC2",
                         keys="i-1438811",
                         collector_id=collector_id,
                         data={
                             "platform": "kubernetes",
                             "instance-type": "",
                             "estimated-cost": "m5.xlarge",
                             "availability-zone": "us-east-1b",
                             "compute-type": {"local_storage_gb": 0},
                             "state": "running",
                         })

node2 = itsdk.add_vertex(name="node1 (i-9434223)",
                         vertex_type="EC2",
                         keys="i-9434223",
                         collector_id=collector_id,
                         data={
                             "platform": "kubernetes",
                             "instance-type": "",
                             "estimated-cost": "m5.xlarge",
                             "availability-zone": "us-east-1c",
                             "compute-type": {"local_storage_gb": 0},
                             "state": "running",
                         })

pod1 = itsdk.add_vertex(name="pod-config-1",
                        vertex_type="Cluster",
                        keys="pods-config-1",
                        collector_id=collector_id,
                        data={
                            "attr1": "attr_value_1",
                            "attr2": "attr_value_2",
                        })

pod2 = itsdk.add_vertex(name="pod-config-2",
                        vertex_type="Cluster",
                        keys="pods-config-2",
                        collector_id=collector_id,
                        data={
                            "attr1": "attr_value_1",
                            "attr2": "attr_value_2",
                        })

pod1_containers = [itsdk.add_vertex(name="container-1-{}".format(i),
                                    vertex_type="container",
                                    keys="container-1-{}".format(i),
                                    collector_id=collector_id,
                                    ) for i in range(6)]

pod2_containers = [itsdk.add_vertex(name="container-2-{}".format(i),
                                    vertex_type="container",
                                    keys="container-2-{}".format(i),
                                    collector_id=collector_id,
                                    ) for i in range(4)]

itsdk.connect(source=kubernetes,
              target=[node1, node2],
              topology="cluster-to-node",
              collector_id=collector_id)

itsdk.connect(source=kubernetes,
              target=[pod1, pod2],
              topology="node-to-pods",
              collector_id=collector_id)

itsdk.connect(source=pod1,
              target=pod1_containers,
              topology="pod-to-containers",
              collector_id=collector_id)

itsdk.connect(source=pod2,
              target=pod2_containers,
              topology="pod-to-containers",
              collector_id=collector_id)

itsdk.flush_all()
