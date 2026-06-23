pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  environment {
    GIT_REPO_URL = "https://github.com/itsChandramahesh/microservices-project2.git"
    GIT_BRANCH = "main"
    SOURCE_DIR = "source"
    MINIKUBE_PROFILE = "minikube"
    REGISTRY = "docker.io"
    IMAGE_TAG = "local"
  }

  stages {
    stage("Checkout") {
      steps {
        sh """
          rm -rf ${SOURCE_DIR}
          git clone --branch ${GIT_BRANCH} --single-branch ${GIT_REPO_URL} ${SOURCE_DIR}
        """
      }
    }

    stage("Detect Layout") {
      steps {
        script {
          def layout = sh(
            script: """
              set -eu
              if [ -d "${SOURCE_DIR}/ecommerce/api-gateway" ]; then
                printf 'ecommerce\\nsource/ecommerce'
                exit 0
              fi
              if [ -d "${SOURCE_DIR}/api-gateway" ]; then
                printf '.\\nsource'
                exit 0
              fi
              printf 'unknown\\nunknown'
            """,
            returnStdout: true
          ).trim().split("\\n")
          env.PROJECT_SUBDIR = layout[0]
          env.APP_DIR = layout[1]
          env.K8S_DIR = "${SOURCE_DIR}/${env.PROJECT_SUBDIR}/k8s"
        }
      }
    }

    stage("Unit Tests") {
      parallel {
        stage("api-gateway") {
          steps {
            dir("${APP_DIR}/api-gateway") {
              sh """
                python3 --version
                python3 -m venv .venv
                . .venv/bin/activate
                export PYTHONPATH=$PWD
                python -c 'import sys; print(sys.path)'
                pip install --upgrade pip
                pip install -r requirements.txt
                pytest --import-mode=importlib --cov=app --cov-report=xml
              """
            }
          }
        }
        stage("user-service") {
          steps {
            dir("${APP_DIR}/user-service") {
              sh """
                python3 --version
                python3 -m venv .venv
                . .venv/bin/activate
                export PYTHONPATH=$PWD
                python -c 'import sys; print(sys.path)'
                pip install --upgrade pip
                pip install -r requirements.txt
                pytest --import-mode=importlib --cov=app --cov-report=xml
              """
            }
          }
        }
        stage("product-service") {
          steps {
            dir("${APP_DIR}/product-service") {
              sh """
                python3 --version
                python3 -m venv .venv
                . .venv/bin/activate
                export PYTHONPATH=$PWD
                python -c 'import sys; print(sys.path)'
                pip install --upgrade pip
                pip install -r requirements.txt
                pytest --import-mode=importlib --cov=app --cov-report=xml
              """
            }
          }
        }
        stage("cart-service") {
          steps {
            dir("${APP_DIR}/cart-service") {
              sh """
                python3 --version
                python3 -m venv .venv
                . .venv/bin/activate
                export PYTHONPATH=$PWD
                python -c 'import sys; print(sys.path)'
                pip install --upgrade pip
                pip install -r requirements.txt
                pytest --import-mode=importlib --cov=app --cov-report=xml
              """
            }
          }
        }
      }
    }

    stage("Build Images") {
      parallel {
        stage("api-gateway") {
          steps { sh "docker build -t ecommerce/api-gateway:${IMAGE_TAG} ${APP_DIR}/api-gateway" }
        }
        stage("user-service") {
          steps { sh "docker build -t ecommerce/user-service:${IMAGE_TAG} ${APP_DIR}/user-service" }
        }
        stage("product-service") {
          steps { sh "docker build -t ecommerce/product-service:${IMAGE_TAG} ${APP_DIR}/product-service" }
        }
        stage("cart-service") {
          steps { sh "docker build -t ecommerce/cart-service:${IMAGE_TAG} ${APP_DIR}/cart-service" }
        }
        stage("inventory-service") {
          steps { sh "docker build -t ecommerce/inventory-service:${IMAGE_TAG} ${APP_DIR}/inventory-service" }
        }
        stage("order-service") {
          steps { sh "docker build -t ecommerce/order-service:${IMAGE_TAG} ${APP_DIR}/order-service" }
        }
        stage("payment-service") {
          steps { sh "docker build -t ecommerce/payment-service:${IMAGE_TAG} ${APP_DIR}/payment-service" }
        }
        stage("admin-service") {
          steps { sh "docker build -t ecommerce/admin-service:${IMAGE_TAG} ${APP_DIR}/admin-service" }
        }
      }
    }

    stage("Minikube Load Images") {
      steps {
        sh """
          minikube start -p ${MINIKUBE_PROFILE}
          kubectl config use-context ${MINIKUBE_PROFILE}
          kubectl get nodes
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/api-gateway:${IMAGE_TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/user-service:${IMAGE_TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/product-service:${IMAGE_TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/cart-service:${IMAGE_TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/inventory-service:${IMAGE_TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/order-service:${IMAGE_TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/payment-service:${IMAGE_TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/admin-service:${IMAGE_TAG}
        """
      }
    }

    stage("Deploy to Minikube") {
      steps {
        sh """
          kubectl config use-context ${MINIKUBE_PROFILE}
          kubectl apply -k ${K8S_DIR}
          kubectl get pods -A
        """
      }
    }

    stage("Smoke Test") {
      steps {
        sh """
          kubectl -n ecommerce rollout status deploy/api-gateway --timeout=180s
          kubectl -n ecommerce rollout status deploy/user-service --timeout=180s
          kubectl -n ecommerce rollout status deploy/product-service --timeout=180s
          kubectl -n ecommerce rollout status deploy/cart-service --timeout=180s
          kubectl -n ecommerce rollout status deploy/inventory-service --timeout=180s
          kubectl -n ecommerce rollout status deploy/order-service --timeout=180s
          kubectl -n ecommerce rollout status deploy/payment-service --timeout=180s
          kubectl -n ecommerce rollout status deploy/admin-service --timeout=180s
        """
      }
    }
  }

  post {
    always {
      sh 'kubectl config use-context minikube || true; kubectl get pods -A || true'
    }
  }
}
