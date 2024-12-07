services:
  - type: web
    name: flask-wkhtmltopdf-service
    env: python
    buildCommand: ./render-build.sh
    startCommand: flask run --host=0.0.0.0 --port=10000
    plan: free
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_APP
        value: app.py
