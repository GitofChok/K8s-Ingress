# K8s Ingress - www.id-594.com

งานวิชา K8s ของ โชคชัย ฟักกลัด รหัส 68130594 (เลข 3 ตัวท้าย = 594)

ทำ service บน Kubernetes (minikube) แล้วเข้าผ่าน Ingress ด้วยชื่อ www.id-594.com กับ admin.id-594.com

| URL | ทำงานด้วย | แสดงอะไร |
|---|---|---|
| http://www.id-594.com/about | app-about | รูป ชื่อ รหัสนักศึกษา |
| http://www.id-594.com/research | app-research | สรุปงานวิจัยที่นำเสนอในวิชาสัมมนา |
| http://www.id-594.com/api/ข้อความ | app-api | เอาข้อความมาแสดงตัวใหญ่กลางจอ |
| http://admin.id-594.com | app-research (/edit) | หน้าแก้ไขสรุปงานวิจัย กดบันทึกแล้วหน้า /research เปลี่ยนตาม |

## โครงสร้างไฟล์

```
K8s-Ingress/
├── deploy.sh              สคริปต์ deploy ทั้งหมด
├── hosts.txt              บรรทัดที่ต้องเพิ่มในไฟล์ hosts
├── k8s/
│   ├── 00-namespace.yaml  namespace id-594
│   ├── app-about.yaml     Deployment + Service ของ app-about (nginx)
│   ├── app-research.yaml  PVC + Deployment + Service ของ app-research (python)
│   ├── app-api.yaml       Deployment + Service ของ app-api (python)
│   └── ingress.yaml       Ingress ของ www.id-594.com และ admin.id-594.com
├── app-about/             หน้าเว็บ about (index.html, about.html, photo.png, default.conf ของ nginx)
├── app-research/          app.py กับ research.txt (สรุปงานวิจัยตั้งต้น)
└── app-api/               app.py
```

ไฟล์ในโฟลเดอร์ app-xxx จะถูกเอาไปทำเป็น ConfigMap ตอน deploy (ไม่ต้อง build docker image เอง)
ใช้ image nginx:1.27-alpine กับ python:3.12-alpine

## วิธี deploy

ต้องมี minikube กับ kubectl ก่อน (บน Windows ใช้ Git Bash รัน)

```bash
bash deploy.sh
```

สคริปต์จะทำตามนี้

1. `minikube start` และ `minikube addons enable ingress`
2. `kubectl apply -f k8s/00-namespace.yaml`
3. สร้าง ConfigMap จากโฟลเดอร์ app-about, app-research, app-api
4. `kubectl apply` ไฟล์ใน k8s/ ทั้งหมด แล้วรอให้ pod ขึ้นครบ
5. แสดงผล `kubectl get all -n id-594` กับ `kubectl get ingress -n id-594`

## ตั้งค่าไฟล์ hosts

ดูใน hosts.txt

- Linux แก้ /etc/hosts ใช้ IP จาก `minikube ip` เช่น `192.168.49.2 www.id-594.com admin.id-594.com`
- Windows / Mac ที่ใช้ docker driver ให้ใช้ `127.0.0.1 www.id-594.com admin.id-594.com` แล้วเปิด `minikube tunnel` ค้างไว้อีกหน้าต่าง
  (Windows ไฟล์อยู่ที่ C:\Windows\System32\drivers\etc\hosts ต้องเปิด Notepad แบบ Run as administrator)

## ทดสอบ

```bash
curl http://www.id-594.com/about
curl http://www.id-594.com/research
curl http://www.id-594.com/api/hello
curl -I http://admin.id-594.com      # จะ redirect ไป /edit
```

เช็คสถานะ

```bash
kubectl get all -n id-594
kubectl get ingress -n id-594
kubectl describe ingress www-ingress -n id-594
```

## หมายเหตุ

- ข้อมูลที่แก้จากหน้า admin เก็บใน PVC research-data ลบ pod แล้วข้อมูลยังอยู่
- app-research ใช้ replicas 1 เพราะ PVC เป็น ReadWriteOnce
- ถ้าจะเปลี่ยนรูป ให้แทนไฟล์ app-about/photo.png แล้วรัน `bash deploy.sh` ใหม่
- ลบทั้งหมด `kubectl delete namespace id-594`
