---
title: Intelligent Sourcing
emoji: 🐨
colorFrom: yellow
colorTo: blue
sdk: gradio
sdk_version: 5.20.1
app_file: app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# 📌 Intelligent Sourcing App

Welcome to the **Intelligent Sourcing App**! 🚀
This application optimizes sourcing decisions by analyzing fulfilment location stock, order priorities, costs, and distances. It uses **Linear Optimization** to efficiently allocate stock while minimizing cost and maximizing efficiency.

[![GitHub Repo](https://img.shields.io/badge/GitHub-Intelligent_Sourcing-blue?logo=github)](https://github.com/kk20krishna/Intelligent-Sourcing)
[![HF Space](https://img.shields.io/badge/HuggingFace-Intelligent_Sourcing_App-orange?logo=huggingface)](https://huggingface.co/spaces/kk20krishna/Intelligent-Sourcing)

---
## 🏆 Created By
| Role | Contributors |
|-----------------------------|------------------------------------------------------|
| **Business Knowledge, Concept, and Domain Expertise** | Achyuthanand.S, Christopher.B, Shafeeque.M, Soumyajeet.M |
| **App Design, Development, and Implementation** | Krishna Kumar.S  |
---
## 🚀 Problem Statement
Efficient sourcing is critical for businesses with multiple fulfilment locations. This app addresses the challenge of identifying **optimal fulfilment locations** while considering parameters like:
- **fulfilment location stock levels**
- **fulfilment location priorities**
- **Order Quantity**
- **Costs associated with sourcing**
- **Distance between fulfilment locations and delivery points**
- **Expected delivery in days**

By balancing these factors, the app provides an optimal fulfillment solution.

---
## 🔍 Approach
The application uses **Linear Optimization** (via **PuLP**) to maximize the sourcing efficiency while considering constraints such as stock availability and order demands.

### 🛠️ Summary of Linear Optimization Model
- **Objective Function**: Maximize the weighted sum of **priority fulfillment while minimizing cost, distance, and delivery time**.
- **Decision Variables**: Determines the amount of stock to be allocated from each fulfilment location to fulfill each order.
- **Constraints**:
  - fulfilment location stock limits.
  - Fulfillment of order quantities.
  - Trade-offs between cost, distance, priority, and delivery time.
---
## 📊 Cost Function & Constraints
### **Objective Function**
The **goal is to maximize sourcing efficiency** while balancing cost, priority, distance, and delivery time:

$$
\text{Objective} = -\sum \left( \text{Priority} \times \text{Priority Weightage} + \text{Cost} \times \text{Cost Weightage} + \text{Distance} \times \text{Distance Weightage} + \text{Days} \times \text{Days Weightage} \right)
$$

where:
- **Priority Weightage**: Ensuring high-priority orders are fulfilled first.
- **Cost Weightage**: Reducing overall procurement and transportation costs.
- **Distance Weightage**: Minimizing the distance between fulfilment locations and order locations to optimize logistics.
- **Days Weightage**: Reducing delivery time while balancing cost efficiency.

### **Constraints**
1. **Stock Limitation**: Each fulfilment location cannot supply more than its available stock.
2. **Order Fulfillment**: Each order must be completely fulfilled without partial deliveries.
3. **Trade-offs**: Adjusting weightages impacts sourcing decisions (e.g., prioritizing lower costs vs. faster delivery).
4. **Non-Negativity Constraint**: The allocated supply quantity must always be non-negative.
5. **Multi-Objective Optimization**: The algorithm balances multiple constraints simultaneously to provide the best solution.
---
## ⚖️ Dynamic Weightage Adjustment
To provide flexibility in decision-making, the app allows users to **adjust weightages** for cost, priority, distance, and delivery time dynamically. This enables businesses to analyze different scenarios by modifying:
- **Cost Sensitivity**: Prioritizing cost reduction over other factors.
- **Priority-Based Fulfillment**: Ensuring urgent orders are processed first.
- **Logistics Optimization**: Minimizing the impact of long-distance sourcing.
- **Timely Delivery**: Balancing speed of fulfillment against costs.

Users can tweak these values through an **interactive UI** and observe changes in the optimization results, helping them make data-driven decisions.

---
## 📊 Code Structure & Control Flow
This app consists of multiple Python modules, each handling a specific function:
- **generate_data.py**: Generates synthetic fulfilment location, order, and cost data.
- **read_data.py**: Loads Excel data into Pandas DataFrames for processing.
- **create_optimization_problem.py**: Constructs the **Linear Programming** model using PuLP.
- **solve_optimization_problem.py**: Solves the LP problem and generates fulfillment solutions.
- **network_diagram.py**: Creates sourcing network visualizations based on optimization results.
- **app.py**: Defines the **Gradio UI**, handling user interactions and workflow.

### **Optimization Control Flow**
```markdown
Start → Load Data (`read_data.py`) → Adjust Weightages (User Input) → Create Optimization Model (`create_optimization_problem.py`) → Solve Optimization (`solve_optimization_problem.py`) → Generate Results (fulfilment location Fulfillment, Costs, Delivery Time) → Visualize Results (`network_diagram.py`) → UI Interaction (`app.py`) → End
```
1. **Data Loading**: Reads Excel input files using read_data.py.
2. **Weightage Adjustment**: Users modify cost, priority, distance, and time weightages.
3. **Problem Formulation**: create_optimization_problem.py generates a **mathematical model**.
4. **Optimization Execution**: solve_optimization_problem.py runs the solver to determine optimal stock allocations.
5. **Result Visualization**: network_diagram.py generates sourcing network graphs.
6. **UI Interaction**: Users review results in app.py, download optimized data, and adjust settings for further analysis.

---
## 🚀 Deployment Details
This application is **deployed on Hugging Face Spaces** using **Gradio** for UI.

### **🔄 Continuous Deployment**
The app is set up for **continuous deployment** using **GitHub Actions**:
- **Workflow triggers**: Updates are automatically pushed to Hugging Face when changes are made to the GitHub repository.
- **Deployment pipeline**:
  - GitHub → Hugging Face Spaces (Auto-sync via GitHub Actions).
  - Uses `ci-pipeline.yml` to automate deployment.

---
## 🛠️ Installation & Setup
### **Requirements**
Install dependencies:
```bash
pip install -r requirements.txt
```
### **Run Locally**
To run the app locally, execute:
```bash
python app.py
```

---
## ❓ Need Help?
If you encounter any issues, double-check input values and file formats. Happy optimizing! 🎯
