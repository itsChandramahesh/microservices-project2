pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  environment {
    APP_DIR = "ecommerce"
    K8S_DIR = "ecommerce/k8s"
    MINIKUBE_PROFILE = "minikube"
    REGISTRY = "docker.io"
    TAG = "${env.BUILD_NUMBER ?: 'local'}"
  }

  stages {
    stage("Checkout") {
      steps {
        checkout scm
      }
    }

    stage("Unit Tests") {
      parallel {
        stage("api-gateway") {
          steps {
            dir("${APP_DIR}/api-gateway") {
              sh "python -m pip install --upgrade pip && pip install -r requirements.txt && pytest --cov=app --cov-report=xml"
            }
          }
        }
        stage("user-service") {
          steps {
            dir("${APP_DIR}/user-service") {
              sh "python -m pip install --upgrade pip && pip install -r requirements.txt && pytest --cov=app --cov-report=xml"
            }
          }
        }
        stage("product-service") {
          steps {
            dir("${APP_DIR}/product-service") {
              sh "python -m pip install --upgrade pip && pip install -r requirements.txt && pytest --cov=app --cov-report=xml"
            }
          }
        }
        stage("cart-service") {
          steps {
            dir("${APP_DIR}/cart-service") {
              sh "python -m pip install --upgrade pip && pip install -r requirements.txt && pytest --cov=app --cov-report=xml"
            }
          }
        }
      }
    }

    stage("Build Images") {
      parallel {
        stage("api-gateway") {
          steps { sh "docker build -t ecommerce/api-gateway:${TAG} ${APP_DIR}/api-gateway" }
        }
        stage("user-service") {
          steps { sh "docker build -t ecommerce/user-service:${TAG} ${APP_DIR}/user-service" }
        }
        stage("product-service") {
          steps { sh "docker build -t ecommerce/product-service:${TAG} ${APP_DIR}/product-service" }
        }
        stage("cart-service") {
          steps { sh "docker build -t ecommerce/cart-service:${TAG} ${APP_DIR}/cart-service" }
        }
        stage("inventory-service") {
          steps { sh "docker build -t ecommerce/inventory-service:${TAG} ${APP_DIR}/inventory-service" }
        }
        stage("order-service") {
          steps { sh "docker build -t ecommerce/order-service:${TAG} ${APP_DIR}/order-service" }
        }
        stage("payment-service") {
          steps { sh "docker build -t ecommerce/payment-service:${TAG} ${APP_DIR}/payment-service" }
        }
        stage("admin-service") {
          steps { sh "docker build -t ecommerce/admin-service:${TAG} ${APP_DIR}/admin-service" }
        }
      }
    }

    stage("Minikube Load Images") {
      steps {
        sh """
          minikube profile ${MINIKUBE_PROFILE} || minikube start -p ${MINIKUBE_PROFILE}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/api-gateway:${TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/user-service:${TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/product-service:${TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/cart-service:${TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/inventory-service:${TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/order-service:${TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/payment-service:${TAG}
          minikube -p ${MINIKUBE_PROFILE} image load ecommerce/admin-service:${TAG}
        """
      }
    }

    stage("Deploy to Minikube") {
      steps {
        sh "kubectl apply -k ${K8S_DIR}"
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
      sh 'kubectl get pods -A || true'
    }
  }
}
