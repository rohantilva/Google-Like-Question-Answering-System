#!/bin/bash


set -e  # if there is an error, exit immediately

OUTPUT_DIR=output
DEFAULT_WAIT_TIMEOUT=10
DEFAULT_WAIT_INTERVAL=1

wait_timeout=$DEFAULT_WAIT_TIMEOUT
wait_interval=$DEFAULT_WAIT_INTERVAL

force_remove_container() {
    docker rm -f "$1" >/dev/null 2>&1 || true
}

force_remove_volume() {
    docker volume rm -f "$1" >/dev/null 2>&1 || true
}

wait_concrete_service() {
    local container="$1"
    local service="$2"
    local host="$3"
    local port="$4"
    docker run --rm --network=container:$container concrete-python-image \
        wait-concrete-service.py $service --host $host --port $port --timeout $wait_timeout --sleep-interval $wait_interval
}

clean_up() {
    force_remove_container data-copy
    force_remove_container fetch
    force_remove_container boolean-search
    force_remove_container weighted-search
    force_remove_volume data
    force_remove_volume index
}


#
# Read command-line arguments.
#

usage() {
    cat << EOF
Usage: $0 [options] <input-path>

Build search client, indexing, and search service images; run a fetch
service container on the Concrete data at <input-path> (a zip or tar
file of Communications); run an indexing container against the fetch
service, and run boolean and weighted search services against the
index.  Note this command will remove several images, containers, and
volumes on startup, if they exist.

Options:
    -w/--wait <wait-timeout>:  wait <wait-timeout> seconds for services
                               to become alive
                               (default: $DEFAULT_WAIT_TIMEOUT)
    -h/--help:                 print this help and exit
EOF
}

input_path=
wait_timeout=$DEFAULT_WAIT_TIMEOUT

while [ $# -gt 0 ]
do
    case "$1" in
        -w|--wait)
            shift
            wait_timeout="$1"
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            if [ -z "$input_path" ]
            then
                input_path="$1"
            else
                usage >&2
                exit 1
            fi
            ;;
    esac
    shift
done

if [ -z "$input_path" ]
then
    usage >&2
    exit 1
fi

#
# Remove existing container and volume names we use.
#

echo && echo "Removing existing containers and volumes."
clean_up

#
# Initialize output directory.
#

echo && echo "Clearing and re-creating output directory."
rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR

#
# Pull/build Docker images, create volumes.
#

# (You don't need to implement these!)
echo && echo "Building concrete-python base image."
docker build -t concrete-python-image -f Dockerfile.concrete_python .
echo && echo "Building search client image."
docker build -t search-client-image -f Dockerfile.search_client .

# (You wrote these!)
echo && echo "Building the indexing image."
docker build -t indexing-image -f Dockerfile.index .
echo && echo "Building the boolean search image."
docker build -t boolean-search-image -f Dockerfile.boolean_search .
echo && echo "Building the weighted search image."
docker build -t weighted-search-image -f Dockerfile.weighted_search .

echo && echo "Creating data and index volumes."
docker volume create --name=data
docker volume create --name=index

#
# Copy specified data set to data volume and run indexer.
#

echo && echo "Copying $input_path to data volume."
docker run --name=data-copy -d -v data:/mnt/data concrete-python-image \
    sleep infinity
docker cp $input_path data-copy:/mnt/data/comms.zip
docker rm -f data-copy

echo && echo "Starting the fetch container."
docker run --name=fetch -d -v data:/mnt/data concrete-python-image \
    fetch-server.py /mnt/data/comms.zip --host localhost --port 9090
echo && echo "Waiting for fetch service to become alive."
wait_concrete_service fetch FetchCommunication localhost 9090

echo && echo "Starting the indexing container."
# The --network=container:fetch flag instructs Docker to reuse the
# network stack of the fetch container for this container: it is as if
# the fetch service and indexer are running in the same container (as
# far as networking is concerned).  In particular, the fetch service
# has been instructed to listen on localhost:9090 and the indexer can
# connect to it on localhost:9090.
docker run --rm -v index:/mnt/index --network=container:fetch indexing-image
docker run --rm -v index:/mnt/index concrete-python-image \
    cat /mnt/index/top-terms.txt > $OUTPUT_DIR/top_50_terms.txt
paste -s $OUTPUT_DIR/top_50_terms.txt

#
# Start boolean search service and execute queries.
#

echo && echo "Starting the boolean search container."
docker run --name=boolean-search -d -v index:/mnt/index boolean-search-image
echo && echo "Waiting for boolean search service to become alive."
wait_concrete_service boolean-search Search localhost 9090
run_boolean_search="docker run -i --rm --network=container:boolean-search search-client-image"
echo && echo 'Running sample queries.'
$run_boolean_search -b < sample_queries.txt > $OUTPUT_DIR/boolean_search.txt
paste sample_queries.txt $OUTPUT_DIR/boolean_search.txt

#
# Start weighted search service and execute queries.
#

echo && echo "Starting the weighted search container."
docker run --name=weighted-search -d -v index:/mnt/index weighted-search-image
echo && echo "Waiting for weighted search service to become alive."
wait_concrete_service weighted-search Search localhost 9090
run_weighted_search="docker run -i --rm --network=container:weighted-search search-client-image"
echo && echo 'Running sample queries.'
$run_weighted_search -b < sample_queries.txt > $OUTPUT_DIR/weighted_search.txt
paste sample_queries.txt $OUTPUT_DIR/weighted_search.txt
