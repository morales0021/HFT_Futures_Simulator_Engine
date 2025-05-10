# ⚡ High-Frequency Trading Simulation Environment

This project provides a **simulation environment** for high-frequency trading in the **futures market**, leveraging **historical tick data**.

---

## 🎯 Features

- Simulates real market conditions using **tick-level historical data**
- Supports input from:
  - 📄 **CSV files**
  - 🧠 **Redis database** (recommended for multi-instance training)
- Optimized for **reinforcement learning (RL)** agent training
- Scalable across **multiple environments without added overhead**

---

## 🗃️ Data Handling

- **CSV Mode**: Load tick data directly from CSV files
- **Redis Mode**: Store and read data using Redis for faster access and better parallelism

> ✅ **Redis is recommended** when training RL agents across multiple instances, ensuring shared memory with minimal latency.

---

## 📂 Usage Examples

Explore the `tests/` folder for sample usage scenarios.

For more detailed documentation, check the `README.md` inside the `futsimulator/` folder.

---

## 📚 Documentation

- [futsimulator/README.md](./futsimulator/README.md) – Deep dive into the simulator
- `tests/` – Example scripts and test runs
