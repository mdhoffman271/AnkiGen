FROM python

WORKDIR /app

# Add dependencies for korean.
ENV JAVA_HOME /usr/lib/jvm/java-1.7-openjdk/jre
RUN apt-get update -y
RUN apt-get install -y g++ default-jdk

# Install python dependencies globally.
COPY ./requirements.txt .
RUN pip install -r requirements.txt
