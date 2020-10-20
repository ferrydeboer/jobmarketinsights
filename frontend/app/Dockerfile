FROM node:current-buster-slim

LABEL Maintainer = Ferry de Boer
LABEL Name = Job Market Insights front-end

# Node modules cache layer
ADD package.json package-lock.json ./tmp/
RUN cd /tmp && npm i npm@latest -g && npm install && npm i -g nodemon
RUN mkdir -p /usr/local/src/app && cp -a /tmp/node_modules /usr/local/src/app

# Deploy code. I expect a virtual volume suits this better in development
COPY . /usr/local/src/app

# Expose
WORKDIR /usr/local/src/app
EXPOSE 4200

# #############################################################################
# Start dev server with polling for Windows
#
ENTRYPOINT ["/bin/bash", "-c", "if [ \"$ENABLE_POLLING\" = \"enabled\" ]; \
then npm run start:docker:poll; else npm run start:docker; fi"]
