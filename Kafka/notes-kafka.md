created by linkedin maintained by confluent
distributed, resilient
horizontal scaleable
high performance < 10ms, real time
used by 35% of fortune 500

use cases:
messaging system
activity tracking form diff locations
log
streaming - kafka stream
decouple source and tgt 
integration with spark, flint, storm, hadoop etc.

ex:
netflix use kafka to recommend realtime shows
uber use real time data to compute price
linkedin use kafka to prevent spam

!!kafka is a transportation tool


# Kafka Theory:
Topics: particular stream of data
    similar to database
    identified as a name
Partitions
    many Partitions make up a Topics
    partition make up of offsets id
offsets:
    make up a partition

topic[name][partition_id][offset_id]

ex:
20 trucks sents data to kafka
topic[truck_gps][]
    
!order guranteed in partition not cross partition
!offset is deleted after one week
!offset id is incremental
!data in partition is immutable
!data is assigned randomly to a partition unless key is specified

Brokers:
kafka cluster is composed of broker (servers)

broker_id contains some Partitions
connected to one broker will connect to entire cluster
num_broker = 3 is recommended , can go up to 100'scale


#Topic replacation: define replication factor 2,3, etc
n copy of data on different Brokers
only one broker can be leader for Partitions
only leader can recieve data
leader and isr( insync replcia) determined by zoo keeper

Produers: write data to Topics
auto matically knows how to load balance and knows which partiton to write to

ack=0: won't wait for acknowledge ( possible all)
default ack=1: producer wait for leader to acknowledge ( limited)
acks=all: leader and replcias acknowledgement ( no data loss)

producer can choose to send to a partition key or round robin 
key = truck_id_123 -> partition 0
      truck_id_345 -> partition 1
guarantee same data source exist in same partition


#Consumers: read data from topic
knows which topic and brker to read from
data id read in order
can read from multiple partition , but order not guarantee

consumer groups:
many consumers read data in groups
each consumer reads from specific partition
ex: consumer( application ) n reads partition m and displays dashboard


consumer offsets:
kafka stores the offset at which a consumer groups has been reading
__consumer_offets
why? to keep track of last read offset


consumer choose when to commit offsets in 3 ways:
at most once:
commit as soon as message is recieved
bad

at least once
commit after message is processed
might duplicate
idempotent : no dup

exactly once
using kafka streams api



# Kafka Broker Discovery
every kakfa broker is called a bootstrap server.
conect to 1, connect to all
each broker has metadata about everything

kafka client can a producer or consumer


# ZooKeeper
manage Brokers
help perform leader election
sent notification to kafka with change
kakfa requires ZooKeeper

zookeeper is designed to be odd number of servers
zookeeper leader handle writes, followers handle read
zookeeper now don't store kafka offset since v.10


# kafka Guarantees
messages are append in order in partition
consumer read message in order
replication 3 is good factor
same key goes to same partition


# starting Kafka
tar xvf

bin/kafka-topic.sh
<!-- if fails -->
requires java8
java -version
brew tap caskroom/versions
brew cask install java8

<!-- let's add to path -->

cat .bash_profile
export PATH="$PATH:/thekafkabin"

