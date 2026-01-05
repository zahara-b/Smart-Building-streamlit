# Expert System for Smart Building Energy Management

## 📖 Introduction
With the increasing energy consumption in buildings and the rapid expansion of smart building technologies, the need for systems capable of intelligently managing and optimizing energy usage has become more significant.  
This project presents an **expert system** designed to manage and optimize energy consumption in smart buildings using human expert knowledge and rule-based reasoning.

---

## ⚙️ Features
- Knowledge base with multiple **if–then rules** for energy management.  
- Forward-chaining **inference engine** for decision-making.  
- Interactive **user interface** built with Streamlit for simulation and visualization.  
- Decision tables for structured representation of rules.  
- Actions include control of **lighting, heating, cooling, and ventilation** systems.  

---

## 🏗️ System Architecture
The system consists of:
1. **Knowledge Base** – Expert rules for building management.  
2. **Inference Engine** – Rule evaluation and decision-making.  
3. **Working Memory** – Current state of the building (temperature, occupancy, light, air quality).  
4. **User Interface** – Interactive simulation with Python/Streamlit.  
5. **Actions** – Optimized control of building subsystems.  

---

## 🚀 Installation & Usage
### Requirements
- Python 3.9+  
- Libraries: `experta`, `streamlit`, `pandas`, `numpy`

### Steps
```bash
# Clone the repository
git clone https://github.com/your-username/smart-building-expert-system.git

# Navigate to project folder
cd smart-building-expert-system

# Install dependencies
pip install -r requirements.txt

# Run the system
streamlit run ui.py
