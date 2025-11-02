pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        ECR_URL = '745540665884.dkr.ecr.ap-south-1.amazonaws.com'
        IMAGE_REPO_NAME = 'mental-health-bot'
        AWS_CREDS = 'aws-creds'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'github-creds', url: 'https://github.com/prathaaaaaaam/mental-health-bot.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "🔨 Building Docker image..."
                docker build -t $IMAGE_REPO_NAME .
                '''
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withAWS(credentials: "${AWS_CREDS}", region: "${AWS_DEFAULT_REGION}") {
                    sh '''
                    echo "🔑 Logging into AWS ECR..."
                    aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_URL
                    '''
                }
            }
        }

        stage('Tag and Push Docker Image') {
            steps {
                sh '''
                echo "🏷️ Tagging and pushing Docker image to ECR..."
                docker tag $IMAGE_REPO_NAME:latest $ECR_URL/$IMAGE_REPO_NAME:latest
                docker push $ECR_URL/$IMAGE_REPO_NAME:latest
                '''
            }
        }

        stage('Terraform Init & Apply') {
    steps {
        withAWS(credentials: "${AWS_CREDS}", region: "${AWS_DEFAULT_REGION}") {
            dir('terraform') {
                sh '''
                echo "⚙️ Running Terraform..."
                terraform init -input=false
                terraform apply -auto-approve
                '''
            }
        }
    }
}


        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                echo "🚀 Deploying application to Kubernetes..."
                kubectl apply -f k8s/01-namespace.yaml
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                kubectl apply -f k8s/hpa.yaml
                kubectl apply -f k8s/ingress.yaml
                '''
            }
        }

        stage('Prometheus & Grafana Setup') {
            steps {
                dir('infra/prometheus') {
                    sh '''
                    echo "📊 Setting up Prometheus and Grafana monitoring..."
                    kubectl apply -f .
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment Successful!"
        }
        failure {
            echo "❌ Build failed!"
        }
    }
}
