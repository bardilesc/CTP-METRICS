FROM python:3.9

# Define el argumento de compilación para las variables de entorno
ARG BASE_URL_CTP
ARG MONGODB_HOST
ARG MONGODB_PORT
ARG MONGODB_USER
ARG MONGODB_PASS

# Establece las variables de entorno
ENV TZ=America/Santiago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# ** CTP SETTING **
ENV BASE_URL_CTP=$BASE_URL_CTP
# ** MONGO DB **
ENV MONGODB_HOST=$MONGODB_HOST
ENV MONGODB_PORT=$MONGODB_PORT
ENV MONGODB_USER=$MONGODB_USER
ENV MONGODB_PASS=$MONGODB_PASS

# Define el UID deseado
ARG USER_ID=1000

# Crea un usuario no privilegiado y establece el directorio de trabajo
WORKDIR /app
RUN groupadd -r parasoft && useradd -r -g parasoft -u $USER_ID parasoft
RUN chown -R parasoft:parasoft /app && chmod -R 777 /app


COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER parasoft
COPY app .
EXPOSE 5000
CMD ["python", "main.py"]