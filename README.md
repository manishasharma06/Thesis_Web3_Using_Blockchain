# Blockchain-Based Supply Chain Management System

This project is a Java-based **Blockchain implementation for Supply Chain Management**, designed to improve transparency, traceability, and security in the product lifecycle — from manufacturing to delivery.

It simulates the working of a basic blockchain where each block records a transaction/event in the supply chain, and all records are cryptographically secured.

---

## Project Highlights

- Blockchain implementation from scratch in Java.
- Simulates key supply chain stages like Manufacturing, Warehouse, Distributor, and Retail.
- SHA-256 hashing to ensure data immutability.
- Timestamped blocks and linked records.
- Real-time addition of blocks to simulate ongoing supply chain events.

---

## Project Structure

BlockChain_SupplyManagement/ │ ├── src/ │ ├── Block.java │ ├── SupplyChainBlock.java │ ├── Blockchain.java │ └── Main.java │ └── README.md

markdown
Copy
Edit

- `Block.java`: Defines the structure of each block including hash, previous hash, data, and timestamp.
- `SupplyChainBlock.java`: Represents the data model for supply chain-related transactions.
- `Blockchain.java`: Handles the chain, validation, and block addition logic.
- `Main.java`: Provides a simple console interface to simulate supply chain operations.

---

## How to Run

### Requirements

- Java 8 or above
- Any Java IDE (IntelliJ IDEA, Eclipse, VS Code)

### Steps

1. Clone the repository:

```bash
git clone https://github.com/yourusername/blockchain-supply-management.git
cd blockchain-supply-management
Open the project in your IDE and run Main.java.

Simulate creating blocks by adding supply chain events (like manufacturing, shipping, etc.).

Sample Output

Creating genesis block...
Block 1 added to the chain
Block 2 added to the chain

Blockchain valid: true
Tech Stack
Java (Core)

SHA-256 (Hashing)

Console-based UI

Learning Outcomes:

Understanding Blockchain principles (hashing, block structure, linking)

Hands-on experience building a ledger-like system

Applying OOP principles to simulate real-world systems

