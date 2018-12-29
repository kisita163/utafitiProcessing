docker build -t gcr.io/${PROJECT_ID}/utafiti-app:v1 .
docker push  gcr.io/${PROJECT_ID}/utafiti-app:v1 

#Create container cluster before using kubectl
gcloud container clusters create utafiti-cluster --num-nodes=1 --zone=europe-west1


#create utafiti pod containing two containers. nginx and utafiti processing
kubectl create -f utafiti-deployment.yaml

#Expose my application to internet
kubectl expose deployment utafiti-deployment --type=LoadBalancer --port 80 --target-port 80


