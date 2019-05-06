case study

# Migration from data center to AWS #

## Assumptions ##
1. The 3 tier application is running on on-premise datacenter is not containerized.
2. When moving to AWS - also need to containerize the application and deploy on an orchestrator like Kubernetes or Docker-Swarm
3. During peak load only specific portion of app is used. It is ok if other parts are not accessible during this time.
4. Reduce costs and try to keep it in check

## Tools ##
1. Kubernetes (kops)
2. Ansible 
3. Terraform
4. Monitring tools - metrics-server, prometheus, grafana, weavescope
5. ELK stack (logging) 
6. CI/CD pipeline - git, Jenkins, SonarQube, Docker registry
7. Testing tools - Jmeter, Selenium, Junit 
8. DB migration tool - AWS Database Migration Service

## Steps ##

1. First create a new forked repo for front-end and backend code with 3 main branches - master, develop and test. Developers do not have permission over test and master. But can create new branches from develop as feature branches. And create a repo for Kubernetes configuration files.
2. Create resources on AWS using terraform - dev and prod. (reuse dev as test to reduce costs). Both environemnts must have similar resources. Order only dev initially till all testing is complete.
3. I would use Kuberentes as orchestrator for docker containers. Instead of going with EKS, I would install Kubernetes on the servers using kops. (control over master node, control plane and reduced costs). This step must be automated using ansible script.
4. The Ansible script also install monitoring service - metrics-server, prometheus and grafana for visual representation. I would also add weavescope to see interations between various pods and realtime architecture diagram of the application.
5. These steps must have the enironment up and running without any intervention. All the services can be exposed using ingress or publicIP and mapped to develop.myapp.example.com to interact with external world.
6. Now that the dev environemnt is setup and automated, start with application code.
7. We will follow frying workflow for images. So we have to move every confiuration or password to configmap, environemnt variables, or as secrets in Kubernetes. These might vary from environmnet to environment. Create yamls for different environemnts. Make sure the pods write logs to a location which can then be fed to Elasticsearch(ELK).
8. From the CI/CD pipeline - (git, Jenkins, SOnarqube, docker registry) build all the different docker images required for the deployment.
9. Create all unit tests, integration tests, DB scripts, health checks for each deployment.
9. Take a dump of the old DB on filesystem and move it to required mount location on Kubernetes. (This step has lot of options - move manually assuming it is not very huge, or use 3rd party services like Amazon Database migration Service etc..)
10. start the entire application and expose the required service using ingress service.
11. Run the basic integration tests or DB test scripts and create a report. For UI some selenium scripts can also be integrated
12. Validate secrets, configmaps, and volumes mounts are properly setup. Also check for the logs. (If possible create dummy user and run all tests for the user and then finally delete the user). Check if logs are coming up in ELK as expected.
13. If there are any issues, create a new git branch and fix them and raise a PR. Once approved, build new image and deploy it using the CI/CD pipeline.
14. Once everything seems to work fine, raise a PR to test branch and get it approved from tech lead.
15. Now we will re-use the same dev environment as test/load-testing. Since we follow frying workflow, we will just change the environment variables, secrets and configmaps without rebuilding the images.
16. All these configurations are deployed to kubernetes from a seperate Jenkins Job that applies yaml files to Kubernetes.
17. Run all scripts and tests again. If things are positive --> the frying workflow is working as expected and the images are built as per the requirement.
18. Now start load testing scripts using Jmeter or . If max load is 50x of normal load, the load test environment must be running upto 75x (50% more than prod max) for about 12 hours.
19. If the system is unable to handle this load, increase the resources. This is where our automation helps to get back upto this step wihtout much hassle. 
20. While running load tests - also monitor grafana, weavescope and other monitoring tools. This will give better idea of how much resources to increase or decrease. You can also monitor the logs in ELK to get idea of how app is performing.
21. If the environment is working as expected, keep this as environment for further tests.
22. Now procure the prod environemt on AWS using terraform. Using the above automation, deploy every app related containers on prod and setup monitoring and logging similar to the dev environemnt and run all the automated tests that were run on test. (except load test or stress test).
23. Coming to DB, now use AWS Database migration service for moving realtime data from datacenter to AWS. Now that we have same data between our datacenter DB and the one on Kubernetes, we will use Blue-green deployment.
24. We will redirect traffic to Kubernetes version. If any thing goes wrong, fall back to the app running on Datacenter. 
25. If everything runs smooth, we will retire the Datacenter version of our application. 

