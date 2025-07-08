# clase05-2bim

* Considerar lo siguiente para el proyecto de **ejemplo2**

## Dar de alta una aplicación en GitHub OAuth application

1. Ingresar a https://github.com/settings/applications/new

2. Ingresar la siguiente información

2.1 Application name: Nombre que se desee. Ejem: demo-django-personal

2.2 Homepage URL: http://127.0.0.1:8000

2.3 Application description: "es una app académica"

2.4 Authorization: http://127.0.0.1:8000/accounts/github/login/callback/

2.5 Pulsar Register

## Agregar información para el funcionamiento de django-allauth

1. Instalar pip install django-allauth

2. Agregar información en

2.1 settings.py

2.2 templates
