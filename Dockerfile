FROM nikolaik/python-nodejs:python3.10-nodejs18
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app/node
COPY node/pnpm-lock.yaml pnpm-lock.yaml
RUN npm i -g pnpm && pnpm fetch
COPY node/package.json package.json
RUN pnpm i

WORKDIR /app
COPY . .

CMD node --experimental-specifier-resolution=node node/index.js
ENV TZ=Asia/Kuala_Lumpur
