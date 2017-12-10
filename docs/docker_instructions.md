To build kscore: `docker build -t kscore -f Dockerfile.kscore .`
To build search passthrough: `docker build -t kdft -f Dockerfile.search .`
To startup docker: `docker-compose up`
If index is not built (try docker-compose up first): ./build-index.sh
