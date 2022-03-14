
FROM python:3.6

# install build utilities
RUN apt-get update && \
	apt-get install -y gcc make apt-transport-https ca-certificates build-essential

# check our python environment
RUN python3 --version
RUN pip3 --version

RUN mkdir ./scripts
ADD /src ./scripts
RUN chmod +x ./scripts/schedule.sh

COPY requirements.txt ./scripts
RUN pip install --no-cache-dir -r ./scripts/requirements.txt
# CMD [ "python", "./scripts/main.py" ]
ENTRYPOINT ["./scripts/schedule.sh"]