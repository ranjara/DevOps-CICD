pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = 'ranjara'
        IMAGE_NAME = 'cicd-demo'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code downloaded from GitHub'
            }
        }

        stage('Install Dependencies') {
            steps {
                dir('application') {
                    sh '''
                        if [ ! -d ".venv" ]; then
                            python3 -m venv .venv
                        fi

                        .venv/bin/python -m pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                dir('application') {
                    sh '.venv/bin/python -m pytest -v'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    env.IMAGE_TAG = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                }

                dir('application') {
                    sh '''
                        docker build -t $DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG .
                    '''
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'dockerhub-token',
                        variable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        set +x

                        echo "$DOCKER_PASS" | docker login \
                            -u "$DOCKERHUB_USERNAME" \
                            --password-stdin

                        docker push \
                            "$DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG"

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'kubeconfig-minikube',
                        variable: 'KUBECONFIG'
                    )
                ]) {
                    sh '''
                        set -e

                        echo "Deploying application to Minikube"

                        sed "s|IMAGE_PLACEHOLDER|$DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG|g" \
                            gitops/deployment.yaml | kubectl apply -f -

                        kubectl apply -f gitops/service.yaml

                        kubectl rollout status deployment/cicd-demo \
                            -n cicd --timeout=180s

                        echo "Kubernetes deployment completed"
                    '''
                }
            }
        }

        stage('Verify Kubernetes Deployment') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'kubeconfig-minikube',
                        variable: 'KUBECONFIG'
                    )
                ]) {
                    sh '''
                        set -e

                        echo "Checking Kubernetes deployment"

                        kubectl get deployments -n cicd
                        kubectl get pods -n cicd
                        kubectl get services -n cicd

                        echo "Application deployment verified"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD pipeline failed. Check the stage logs.'
        }
    }
}
