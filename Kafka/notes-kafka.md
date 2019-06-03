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
brew install kafka

port :2181 will be used and terminal needs to be open
./zookeeper-server-start.sh config/zookeeper.properties

mkdir data/zookeeper
cat config/zookeeper.properties
change tempDir = data/zookeeper

server.properties
log.dirs=data/kafka

start zookeeper and kafka

# CLI
//replication factor <= broker
./bin/kafka-topics.sh --zookeeper 127.0.0.1:2181  --topic firstTopic --create --partitions 3 --replication-factor 1
create topic

--topic firstTopic --describe
displays the number of partitions

Topic:firstTopic        PartitionCount:3        ReplicationFactor:1     Configs:
        Topic: firstTopic       Partition: 0    Leader: 0       Replicas: 0     Isr: 0
        Topic: firstTopic       Partition: 1    Leader: 0       Replicas: 0     Isr: 0
        Topic: firstTopic       Partition: 2    Leader: 0       Replicas: 0     Isr: 0

--topic topic_name --delete
delete topic


producer:
./bin/kafka-console-producer.sh --broker-list 127.0.0.1:9092 --topic firstTopic
>adds messages

./bin/kafka-console-producer.sh --broker-list 127.0.0.1:9092 --topic firstTopic --producer-property acks=all


./bin/kafka-console-producer.sh --broker-list 127.0.0.1:9092 --topic newTopic
this will create the topic but not have a leader, so always create the topic first

# Kafka consumer
./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic firstTopic
now we can recieve live .

./bin/kafka-console-consumer.sh --boots-server 127.0.0.1:9092 --topic firstTopic --from-beginning
to read from begining

# kafka consumer --groups
./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic firstTopic --group myFirstApp
we can spin up multiple consumers for same topic with same command

./bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic firstTopic --group myFirstApp --from-beginning
from begining can only be run once, because committed,


# kafka-consumer-groups
manage consumer groups

./bin/kafka-consumer-groups.sh --bootstrap-server 127.0.0.1:9092 --list
listyall groups

./bin/kafka-consumer-groups.sh --bootstrap-server 127.0.0.1:9092 --describe --group myFirstApp
displays
LAG 0 means read all
also can show what/where is consuming

127.0.0.1 is lcoalhost
# resetting offset
./bin/kafka-consumer-groups.sh --bootstrap-server 127.0.0.1:9092 --reset-offsets --to-earliest --ecexute --topic firstTopic
resets offset for a given topic

--to-earliest, --shift-by (-,+)n

# Producer with keys

kafka-console-producer --broker-list 127.0.0.1:9092 --topic first_topic --property parse.key=true --property key.separator=,
> key,value
> another key,another value

# Consumer with keys

kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic first_topic --from-beginning --property print.key=true --property key.separator=,

# UI
kafka tools, kafkacat yahoo/kafka


# kafka Java programming, reproduce CLI 
requires java 1.8

pom.xml contains all the dependencies for maven



# debugging
sudo lsof -i :2181
 , list port and pid
lsof -n -i :9092 | grep LISTEN
kill p_id , kills process
ps -ax | grep name , list process with name



