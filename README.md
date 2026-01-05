# 🏢 Expert System for Smart Building Energy Management

## 📖 Introduction
This project implements an **expert system** for smart building energy management.  
The system uses **rule-based reasoning** to optimize lighting, heating, cooling, and ventilation, while ensuring **security, safety, and comfort**.  
It is designed as part of the *Expert Systems* course project, combining academic rigor with practical implementation.

---

## 🎯 Objectives
- Reduce unnecessary energy consumption in smart buildings.  
- Provide transparent and explainable decision-making through **if–then rules**.  
- Integrate user preferences (e.g., sleep mode, party mode).  
- Enhance safety and security (fire detection, intrusion alerts).  
- Offer an interactive simulation environment via **Streamlit UI**.  

---

## 🏗️ System Architecture
The system is composed of the following modules:

1. **Knowledge Base** – Stores expert rules and decision tables.  
2. **Inference Engine** – Evaluates rules and derives actions.  
3. **Working Memory** – Holds current building states (temperature, occupancy, light, humidity).  
4. **User Interface** – Built with Streamlit for simulation and visualization.  
5. **Actions/Actuators** – Executes decisions (lighting, HVAC, alarms).  

---

## 📜 Sample Rules (Knowledge Base)
- If no occupancy is detected and lights are ON → turn OFF lights.  
- If temperature < 18°C → activate heating.  
- If temperature > 28°C → activate cooling.  
- If smoke is detected → stop ventilation and trigger alarm.  
- If user mode = "Sleep" → dim lights and reduce noise.  
- If user mode = "Party" → adjust lighting and ventilation accordingly.  

---

## ⚙️ Installation & Usage
### Requirements
- Python 3.9+  
- Libraries: `experta`, `streamlit`, `pandas`, `numpy`, `matplotlib`

### Steps


# Install dependencies
pip install -r requirements.txt

# Run the system
streamlit run appp.py

