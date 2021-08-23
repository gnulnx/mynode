FROM node:lts-alpine

WORKDIR /app

RUN apk add --update tzdata
# RUN apt-get update -y
#     && apt-get install -y \
#     tzdata \
#     && rm -rf /var/lib/apt/lists/*

ENV TZ=American/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY package*.json ./
RUN npm install
COPY . .

COPY entrypoint.sh /app/
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

