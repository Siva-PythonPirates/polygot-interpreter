FROM gcc:latest
WORKDIR /usr/src/app
COPY main.c .
RUN gcc -o myapp main.c
# Use ENTRYPOINT to set the executable
ENTRYPOINT ["./myapp"]