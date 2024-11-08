FROM golang:1.23.2

LABEL org.opencontainers.image.source=https://github.com/mjsully/ontologies-api:go

COPY . /go/api/
WORKDIR /go/api/
RUN go build api.go