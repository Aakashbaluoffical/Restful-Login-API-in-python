#Build the Docker image 

docker build -t restfulapiloginsystem .
or

docker build --no-cache -t restfulapiloginsystem .



#Run the Docker Container
docker run -d --name restfull_api_container -p 5200:5200 restfulapiloginsystem

or 

docker run restfulapiloginsystem

Access Your Application
Your FastAPI app should now be accessible at http://localhost:5200.


#find all running containers
docker ps

#stop container
docker stop restfulapiloginsystem 
