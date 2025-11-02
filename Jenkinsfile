pipeline {
    agent any

    environment {
        IMAGE_REPO_NAME = 'mental-health-bot'
        CONTAINER_NAME = 'mental-health-bot-container'
        PORT = '8000'
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "📥 Checking out code from GitHub..."
                git branch: 'main', credentialsId: 'github-creds', url: 'https://github.com/prathaaaaaaam/mental-health-bot.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🔨 Building Docker image..."
                sh '''
                docker build -t $IMAGE_REPO_NAME .
                '''
            }
        }

        stage('Run Chatbot Container') {
            steps {
                echo "🚀 Running chatbot locally inside Docker..."
                sh '''
                # Stop and remove any existing container with the same name
                if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
                    echo "🧹 Stopping existing container..."
                    docker stop $CONTAINER_NAME
                    docker rm $CONTAINER_NAME
                fi

                # Run new container
                docker run -d --name $CONTAINER_NAME -p $PORT:8000 $IMAGE_REPO_NAME
                '''
            }
        }

        stage('Verify Container') {
            steps {
                echo "🔍 Checking if chatbot container is running..."
                sh '''
                docker ps | grep $CONTAINER_NAME || (echo "❌ Chatbot container not running!" && exit 1)
                '''
            }
        }

        /*
        =============================
        💤 Deployment Steps (Paused)
        =============================

        stage('Login to AWS ECR') {
            steps {
                withAWS(credentials: 'aws-creds', region: 'ap-south-1') {
                    sh '''
                    echo "🔑 Logging into AWS ECR..."
                    aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 745540665884.dkr.ecr.ap-south-1.amazonaws.com
                    '''
                }
            }
        }

        stage('Tag and Push Docker Image') {
            steps {
                sh '''
                echo "🏷️ Tagging and pushing Docker image to ECR..."
                docker tag $IMAGE_REPO_NAME:latest 745540665884.dkr.ecr.ap-south-1.amazonaws.com/mental-health-bot:latest
                docker push 745540665884.dkr.ecr.ap-south-1.amazonaws.com/mental-health-bot:latest
                '''
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                withAWS(credentials: 'aws-creds', region: 'ap-south-1') {
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
                echo "🚀 Deploying to Kubernetes..."
                kubectl apply -f k8s/
                '''
            }
        }

        stage('Prometheus & Grafana Setup') {
            steps {
                dir('infra/prometheus') {
                    sh 'kubectl apply -f .'
                }
            }
        }
        */
    }

    post {
        success {
            echo "✅ Chatbot running successfully at http://<your-ec2-public-ip>:8000"
        }
        failure {
            echo "❌ Build failed! Check logs for details."
        }
    }
}
