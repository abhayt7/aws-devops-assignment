pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID = '523835808303'
        ECR_REPOSITORY = 'demo-app'
        EKS_CLUSTER = 'demo-ekscluster'
        ECR_REGISTRY = '523835808303.dkr.ecr.ap-south-1.amazonaws.com'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies and Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r app/requirements.txt
                    cd app
                    ../.venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                    -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG \
                    ./app
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password \
                    --region $AWS_REGION |
                    docker login \
                    --username AWS \
                    --password-stdin $ECR_REGISTRY
                '''
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    docker push \
                    $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                    aws eks update-kubeconfig \
                    --region $AWS_REGION \
                    --name $EKS_CLUSTER

                    sed "s|IMAGE_PLACEHOLDER|$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG|g" \
                    k8s/deployment.yaml | kubectl apply -f -

                    kubectl apply -f k8s/service.yaml

                    kubectl rollout status deployment/demo-app --timeout=300s

                    kubectl get deployments
                    kubectl get pods
                    kubectl get services
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline failed. Check Console Output.'
        }
    }
}
