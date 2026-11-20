# Образ микросервиса веб-сервера nginx со своей конфигурацией
FROM nginx:1.27-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/dance-studio.conf

EXPOSE 80
