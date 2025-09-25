# Use the JDK (Java Development Kit) image which includes the compiler 'javac'
FROM openjdk:11-jdk-slim

WORKDIR /usr/src/app
COPY Main.java .
RUN javac Main.java
ENTRYPOINT ["java", "Main"]