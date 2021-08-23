FROM node:lts-alpine

WORKDIR /app

RUN apk add --update tzdata
ENV TZ=American/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY package*.json ./
RUN npm install
COPY . .

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

