# 🚀 SecureNetX - Network Environment Setup

هذا المستودع (Repository) يحتوي على سكريبت التشغيل الآلي (Ansible Playbook) لتجهيز بيئة عمل الشبكات (SDN) لمشروع SecureNetX. السكريبت يقوم بتسطيب وإعداد الأدوات التالية بضغطة زر:
- Mininet
- Ryu Controller
- Open vSwitch (OVS)
- Wireshark & Tshark
- Python3 & Git & SSH

## 🛠️ خطوات التشغيل (لرويعي)

يرجى تجهيز نسخة Ubuntu وهمية (VM) نظيفة، ثم فتح الـ Terminal وتنفيذ الخطوات التالية بالترتيب:

### 1. تسطيب أداة Ansible
```bash
sudo apt update && sudo apt install ansible -y
```

### 2. تحميل ملف السكريبت
```bash
wget [https://raw.githubusercontent.com/AmrNagy74/SecureNetX-Infrastructure/main/setup-network-env.yml](https://raw.githubusercontent.com/AmrNagy74/SecureNetX-Infrastructure/main/setup-network-env.yml)
```

### 3. تشغيل السكريبت لتجهيز البيئة
```bash
ansible-playbook -i localhost, -c local setup-network-env.yml -K
```
