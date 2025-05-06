# curl -X GET "https://api-fxpractice.oanda.com/v3/accounts/101-004-21322380-001" \
# -H "Authorization: Bearer bb1d421d5ff8b46afc88b98ea098fb16-6366a971f49832b64f2992233bb88b6b"
docker rm jenkins
docker build -t jenkins-docker-agent .
echo "starting a jenkins container as docker image on port 8080"
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins-docker-agent
echo "jenkins adminPassword :"
docker exec -it jenkins-container cat /var/jenkins_home/secrets/initialAdminPassword
