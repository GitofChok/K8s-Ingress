#!/bin/bash
# deploy งาน K8s Ingress www.id-594.com
# ใช้ได้ทั้ง Linux และ Git Bash บน Windows (ต้องมี minikube กับ kubectl)

set -e
cd "$(dirname "$0")"
NS=id-594

echo "== 1. start minikube + เปิด ingress addon"
minikube start
minikube addons enable ingress
kubectl wait -n ingress-nginx --for=condition=Ready pod -l app.kubernetes.io/component=controller --timeout=300s

echo "== 2. สร้าง namespace"
kubectl apply -f k8s/00-namespace.yaml

echo "== 3. สร้าง configmap จากไฟล์ในแต่ละ app"
kubectl create configmap about-files -n $NS --from-file=app-about/ --dry-run=client -o yaml | kubectl apply -f -
kubectl create configmap research-files -n $NS --from-file=app-research/ --dry-run=client -o yaml | kubectl apply -f -
kubectl create configmap api-files -n $NS --from-file=app-api/ --dry-run=client -o yaml | kubectl apply -f -

echo "== 4. deploy app ทั้ง 3 ตัว + ingress"
kubectl apply -f k8s/app-about.yaml
kubectl apply -f k8s/app-research.yaml
kubectl apply -f k8s/app-api.yaml
kubectl apply -f k8s/ingress.yaml

# ถ้า configmap เปลี่ยน ให้ pod โหลดใหม่
kubectl rollout restart deployment -n $NS
kubectl rollout status deployment/app-about -n $NS
kubectl rollout status deployment/app-research -n $NS
kubectl rollout status deployment/app-api -n $NS

echo "== 5. เช็คผล"
kubectl get all -n $NS
kubectl get ingress -n $NS

echo ""
echo "เสร็จแล้ว ต่อไปให้"
echo " - เพิ่มบรรทัดใน hosts.txt ลงไฟล์ hosts (/etc/hosts หรือ C:\\Windows\\System32\\drivers\\etc\\hosts)"
echo " - Windows/Mac (docker driver) ให้เปิด minikube tunnel ค้างไว้อีกหน้าต่าง"
echo " - เปิด http://www.id-594.com"
