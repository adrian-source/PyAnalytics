

curl http://localhost:5000/register -d "appname=app1&email=adrian@gmail.com" -X PUT
curl http://localhost:5000/register -d "email=adrian@gmail.com" -X GET
curl http://localhost:5000/register -d "appname=app2&email=katie@gmail.com" -X PUT
curl http://localhost:5000/register -d "email=katie@gmail.com" -X GET

curl http://localhost:5000/register -d "appname=app3&email=adrian@gmail.com" -X PUT
curl http://localhost:5000/register -d "email=adrian@gmail.com" -X GET
curl http://localhost:5000/register -d "appname=app4&email=katie@gmail.com" -X PUT
curl http://localhost:5000/register -d "email=katie@gmail.com" -X GET


