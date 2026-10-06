FROM nginx:1.25-alpine

RUN apk update && apk upgrade && apk add --no-cache curl

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]