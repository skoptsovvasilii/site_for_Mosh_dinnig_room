<h1 align="center">МОШ Предпроффесиональная олимпиада кейс №2 про столовую</h1>

<p align="center">Профиль «Информационные технологии»
Командный кейс № 2 «Управление столовой»</p>

---

## Инструкция по установке
Скачайте все файлы папки, разместите их в таком же расположении(файлы в этих директивах должны лежать)
установите на питон библиотеку flask  
можно воспользоваться команой pip install flask
и запустите питон файл  chek_email_password



This project was created by me for school and city science conferences.  
**Health-AI** is an autonomous system that monitors a patient’s condition during surgery using:

- ECG signals  
- camera video  
- additional sensor data  

The program detects possible complications and gives their probabilities in real time.

---

<h2>📌 System Components</h2>

1. 🫀 **ECG model** — a ResNet1D network for classifying lead-II ECG signals  
2. 📷 **Vision model** — a ResNet50 for detecting complications using the patient’s face  
3. 📈 **Sensor algorithm** — checks complications using external sensor readings  
4. 🔁 **Re-check algorithm** — compares AI outputs with rule-based logic  
5. 🎛️ **Final probability module** — combines all predictions  
6. 🖥️ **Interface program** — the main window with alerts and visualization  

---
