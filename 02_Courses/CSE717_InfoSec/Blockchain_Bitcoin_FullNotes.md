# Blockchain & Bitcoin — Full Lecture Notes (Lc#11A + Lc#11B)
> [[wiki/blockchain|Exam-pattern wiki page]] · [[Blockchain_Solutions.pdf|Past-paper solutions]] · [[_Topics]] · [[00_Dashboard]]

> Comprehensive coverage of **every topic** in Lc#11A (Blockchain) and Lc#11B (Bitcoin Mining), with diagrams, for memorization. The [[wiki/blockchain|wiki page]] is the condensed exam-pattern version — use THIS note for full recall / "explain everything" prep.

---

## PART A — Blockchain (Lc#11A)

### A1. What is Blockchain?
- A **blockchain is a chain of blocks** that contains data/information.
- It's a **distributed ledger** — duplicated and spread across an entire network of computer systems.
- Each block links to the next, forming a chronological chain.

```
[Block 1] ⇄ [Block 2] ⇄ [Block 3] ⇄ ... ⇄ [Block N]
```

---

### A2. Blockchain Architecture — Block Structure
- Blocks are data structures whose purpose is to **bundle sets of transactions** and distribute them to all nodes in the network.
- Blocks contain a **block header**, which holds **metadata**, plus the **transactions** themselves.

**6 fields in the block header (memorize all 6):**
1. **Version** — version number of the block validation rules.
2. **Previous Block Header Hash** — reference to (hash of) this block's parent block. ⚠️ **This is what makes it a "chain."**
3. **Merkle Root Hash** — a cryptographic hash summarizing ALL the transactions included in this block.
4. **Time** — the (approximate) time this block was created.
5. **nBits** — the current **difficulty target** for the Proof-of-Work.
6. **Nonce ("number used once")** — a random/counter value the block creator is allowed to manipulate to satisfy the PoW.

```
┌────────────────────────────┐
│            Block            │
│ ┌──────────────────────────┐│
│ │ previous block hash       ││  ← metadata
│ │ merkle root                ││     (header,
│ │ timestamp                  ││      6 fields)
│ │ nonce                      ││
│ └──────────────────────────┘│
│ ┌──────────────────────────┐│
│ │ coinbase transaction       ││
│ │ transaction                ││
│ │ transaction                ││  ← transactions
│ │ ...                        ││
│ └──────────────────────────┘│
└────────────────────────────┘
```
- The **miner gets a reward** from the block they have mined. After completing checks, each node adds the block to the chain.

---

### A3. Hashing — the Fingerprint of a Block
- A block's **hash** is like a **fingerprint** — unique to that block and all its contents.
- Once a block is created, **any change inside it changes its hash**.
- This is why hashing is useful for **detecting changes/intersections** — if the fingerprint of a block changes, it's no longer the same block.

**Hash-chain example (3 blocks):**
```
Block 1            Block 2            Block 3
Hash: 2ZB1   <───  Hash: 7B2Z   <───  Hash: 3DfV
Prev Hash: 0000    Prev Hash: 2ZB1    Prev Hash: 7B2Z
```
- Block 1 = no predecessor → Previous Hash = `0000` (this is the **genesis block** — see A8).
- Block 2 stores the hash of Block 1.
- Block 3 stores the hash of Block 2.

**Tamper detection:**
```
Block 1            Block 2 (TAMPERED!)     Block 3
Hash: 2ZB1   <───  Hash: 7B2Z → AA23  ✗──  Hash: 3DfV
Prev Hash: 0000    Prev Hash: 2ZB1          Prev Hash: 7B2Z  (no longer matches AA23!)
```
- If block 2's content changes, its hash changes (7B2Z → AA23).
- But Block 3's "Previous Hash" still says `7B2Z` → **mismatch detected**.
- ⚠️ **All blocks containing hashes of previous blocks is the technique that makes a blockchain so secure.**

---

### A4. Proof of Work (PoW)
- Hashes are an **excellent mechanism** to prevent tampering — because computers are now so fast, they could recalculate hundreds of thousands of hashes per second.
- An attacker could tamper with one block and then **recalculate all the other block hashes** to make the blockchain valid again.
- **To avoid this**, blockchains use the concept of **Proof-of-Work**, which slows down the creation of new blocks.

**Definition:**
- A proof-of-work is a **computational problem that takes certain amount of effort and time to solve**.
- The time required to verify the results of the computational problem is very low compared to the effort it takes to solve the computational problem itself.

**In Bitcoin:**
- It takes almost **10 minutes** to calculate the required proof-of-work and add a new block to the chain.
- Considering one example, if a hacker would want to **modify the data in Block 2**, they would need to perform proof of work (which would take 10 minutes) and only then make changes in Block 3 and all succeeding blocks.

```
[Block 1] ⇄ [Block 2] ⇄ [Block 3]
              10 min      10 min     ← each "⇄" link costs ~10 min of PoW to redo
```
- ⚠️ **This kind of mechanism makes it quite tough to tamper with any of the blocks**, since even if you tamper with a single block, you will need to recalculate the PoW for ALL the succeeding blocks. Thus, **hashing and proof-of-work mechanism make a blockchain secure.**

---

### A5. Distributed P2P Network
- A blockchain is used in a decentralized way — **no single computer or organization can own the chain**.
- It is a **distributed ledger** via the nodes connected to the network.
- A node can be **any kind of electronic device** that maintains copies of the blockchain and keeps the network functioning.
- Every node has its own copy of the blockchain, and the network must **algorithmically approve any newly mined block** for the chain to be updated/trusted/verified.
- Because blockchains are transparent, **every action is easily checked and viewed**. Each participant is given a unique alphanumeric ID number that shows their transactions.

**To successfully tamper with a blockchain, an attacker would need to:**
1. Tamper with **all blocks** on the chain.
2. **Redo** the proof-of-work for **each block**.
3. **Take control of more than 50%** of the peer-to-peer network.
- After doing all these, the tampered block would become accepted by everyone else. Hence, **blockchains are virtually impossible**. (i.e., practically impossible to tamper)

---

### A6. How Blockchain Ensures Security — SUMMARY (3 pillars)
> Combines A3 + A4 + A5:

- **Hashing** → every block has a unique fingerprint; any change to a block changes its hash, and breaks the "previous hash" link in the next block → **tamper-evident**.
- **Proof of Work** → adding/altering a block requires a costly computational puzzle (~10 min in Bitcoin); tampering with one block means redoing PoW for it AND every block after it → **tamper-resistant**.
- **Distributed P2P Network** → thousands of nodes hold copies of the chain and must reach consensus; an attacker needs >50% of the network's power to force a fraudulent chain to be accepted → **tamper-impossible at scale**.

---

### A7. How a Blockchain Transaction Works (4 steps)
```
Transaction Requested → Broadcast Transaction → Validate Transaction → Add to Blockchain
```
- **Step 1:** Someone requests a transaction. The transaction could involve cryptocurrency, contracts, records, or other information.
- **Step 2:** The requested transaction is broadcast to a **P2P network of nodes**.
- **Step 3:** The network of nodes validates the transaction and the user's status using **known algorithms**.
- **Step 4:** Once the transaction is verified, it is then combined with other transactions to create a new block of data for the ledger. The new block is then added to the existing blockchain, in a way that is permanent and unalterable.

**Diagram (the canonical "how a blockchain transaction works" figure):**
```
 A wants to send money     Cryptographic keys are        The transaction is
 to B ("transaction")  →   assigned to the transaction,  broadcast and verified
                            proving that both A and B     by a distributed network
                            hold them
                                  ↓
 Once validated, a new block   ←  This block is then     ←  The transaction between
 is added to the chain,            added to the chain        A and B is complete
 creating a permanent &
 transparent record
```

---

### A8. What is the Genesis Block?
- The **first block** ever discovered on a given blockchain is called the **genesis block**.
- The Bitcoin genesis block was mined in **January 2009**.
- The rest of a block contains transaction data; the **previous hash** field is the field that links blocks together.
- The genesis block has **no predecessor** → its "previous hash" field is `0000...` (all zeros).

---

### A9. Features of Blockchain
> Mnemonic-friendly bullet list — 9 features:

- **Resilience:** Blockchain is often replicated across thousands of nodes — there is no single point of failure (no central server to attack/crash).
- **Time Reduction:** In the financial industry, blockchain can play a vital role by allowing the **quicker settlement of trades** — no lengthy verification/settlement/clearance process (since a single version of agreed-upon data is available between all stakeholders).
- **Reliability:** Blockchain certifies and verifies the identities of every interested party — removes double records, reducing rates and accelerating transactions.
- **Unchangeable Transactions:** By registering transactions in chronological order, blockchain certifies the **immutability** of all operations — meaning that whenever a new block is added to the chain of ledgers, it cannot be edited or removed.
- **Fraud Prevention:** Concepts of shared information + consensus eliminate fraud risks; data on the blockchain is incorruptible.
- **Security:** Attacking a traditional database means an attacker only has to corrupt a single database. With distributed-ledger technology, each party owns the full chain — making it extremely hard for attackers to attack.
- **Transparency:** Changes to public blockchains are publicly viewable by everyone — provides full transparency, and all transactions are immutable.
- **Collaboration:** Allows parties to transact directly with each other without the need for a mediating third party.
- **Decentralized:** There are standards rules on how every node exchanges blockchain information. This method ensures that all transactions are validated, and all valid transactions are added one by one.

---

### A10. Different Types of Blockchain (3 variants)
> There are 3 primary types: **traditional databases or distributed ledger databases (DLT)** that are often confused with traditional blockchains.

1. **Public Blockchains** — e.g. Bitcoin and Ethereum
2. **Private Blockchains**
3. **Hybrid Blockchains** — e.g. Dragonchain

```
   Public            Hybrid             Private
  (open mesh,      (mix of public/    (small, controlled
   many nodes,      private nodes)      circle of nodes,
   fully connected)                     star-like topology)
```

**Public Blockchains:**
- **Open source** — anyone can participate, view, audit ongoing activities.
- Transactions are **fully transparent**, meaning anyone can examine the transaction details.
- No individual or entity controls who can participate, conduct, or record transactions — fully **decentralized**.
- Anyone is free to join the network and become an authorized node.
- Lastly, public blockchains all have a token associated with them, which is typically designed to incentivize and reward participants on the network.
- Public blockchains are limited in the fact that these networks are slow and require a lot of devices to encrypt data on a large scale.
- **Examples:** Bitcoin, Ethereum, Litecoin, etc.

**Private Blockchains:**
- Also known as **permissioned blockchains** — they possess a number of notable differences from public blockchains.
- **Participants need consent to join the network.**
- Transactions are private, and are only available to ecosystem participants who have been given permission to access them.
- Private blockchains are more centralized than public blockchains.
- Private blockchains are valuable for enterprises who want to collaborate and share data — but don't want their sensitive data visible on a public blockchain.
- Private blockchains are much faster and cheaper as they can be controlled by a specified amount of users and the consensus can be regulated.
- **Example:** Hyperledger, R3 Corda, etc.

**Hybrid Blockchains:**
- Combines the benefits of a permissioned and private blockchain with the **security and transparency** benefits of a public blockchain.
- Gives businesses significant flexibility to choose what data they want to make public, and transparent and what data they want to keep private.
- The hybrid blockchain platform allows us to easily connect with other blockchain protocols. Allowing for a multi-chain network of blockchains.
- Also, being able to post to multiple public blockchains at once confirmed if enough computational power was devoted to the block that contains them. More blocks mean more computation, which means more trust.
- **Example:** Dragonchain, Bankchain, etc.

---

### A11. Blockchain vs. Shared Database

| Parameter | Blockchain | Shared Database |
|---|---|---|
| **Operations** | Insert | Create / Read / Update / Delete |
| **Replication** | Full replication on every peer | Master-slave or Multi-master |
| **Consensus** | Most peers agree on the outcome of transactions | Distributed transactions held in two phases: commit and Paxos |
| **Validation** | Global rules enforced on the whole blockchain system | Offers only local integrity constraints |
| **Disintermediation** | Allowed | Not allowed |
| **Confidentiality** | Fully confidential | Not totally confidential |
| **Robustness** | Fully robust technology | Not entirely robust |

**Schematic diagrams:**
```
BLOCKCHAIN (Crowdsourced):              SHARED DATABASE (Superuser):

  [Org 1] <==> [Org 2]                   [Org 1] <==> [Org 2]
     \   blockchain    /                       \  centralized  /
      \   network     /                         \  trusted     /
       \   (mesh of  /                           \ authority  /
        \  many nodes)                            \ (single   /
                                                     server)
```
- **Blockchain:** every org connects to a decentralized mesh network of peers.
- **Shared DB:** every org connects through one centralized trusted authority (single point of control = "Superuser").

---

### A12. Blockchain Use Cases (by sector)

| Sector | Usage |
|---|---|
| **Markets** | Billing/monitoring/data transfer; quota management in supply chain network |
| **Government Sector** | Transnational personalized governance services; voting/propositions P2P bond; digitization of documents/contracts and proof of ownership for transfers; registry & identify; tele-attorney service; IP registration/exchange; tax receipts/notary service/document registry |
| **IoT** | Agricultural & drone sensor networks; smart home networks/sensors; integrated smartcity; self-driving cars; personalized robots/robotic components; personalized drones; digital assistants |
| **Health** | Data management; universal EMR health databanks; QS data commons; big health data stream analytics; digital health wallet/smart property; health token; personal development contracts |
| **Finance & Accounting** | Digital currency payment; payments & remittance; decentralized capital markets using a network of computers on the blockchain; inter-divisional accounting; clearing & trading & derivatives; bookkeeping |

---

### A13. Important Real-Life Use Cases of Blockchain
- **Dubai:** The Smart City by year 2016, Dubai Office introduced Blockchain strategy. Using this technology, entrepreneurs and developers will be able to come up with smart energy solutions and leading companies.
- **Incent Customer Retention:** Incent is CRaaS (Consumer retention as a service) offered to the Blockchain technology. It is a loyalty program which is based on generating tokens for business affiliated with its related network. **This proof of work is used in blockchain instantaneously, and it can be stored in digital register of user's phone or saved on the browser.**
- **Blockchain for Humanitarian Aid:** In January 2017 the United Nations world food program started a project related to humanitarian aid. The project was developed in rural areas of Sindh region of Pakistan. By using blockchain technology, beneficiaries received money, food and all type of transactions are registered on a blockchain to ensure security and transparency of this process.

---

### A14. Limitations of Blockchain Technology
- **Higher Costs:** Nodes seek higher rewards for completing transactions in a business which work on the principle of Supply and Demand.
- **Slower Transactions:** Nodes prioritize transactions with higher rewards, backlogs of transactions build up.
- **Smaller Ledger:** It's not possible to fit a full copy of the blockchain, potentially which can affect immutability, confidence, trust.
- **Transaction Costs, Network Speed:** The transactions cost of Bitcoin can be very high if the network is being tested for a long time.
- **Risk of Error:** There is always a risk of error, as long as the human factor is involved. In case a blockchain serves as a database, all of the incoming data has to be of high quality. However, human involvement can quickly resolve the error.
- **Wasteful:** Every node that runs the blockchain has to maintain consensus across the blockchain. This offers very low downtime and makes data stored on the blockchain forever unchangeable. However, all this is wasteful, because each node repeats a task to reach consensus.

---

## PART B — Bitcoin Mining (Lc#11B)

### B1. What is Bitcoin?
- Bitcoin is a **consensus network** that enables a new payment system and a completely digital money.
- It is the **first decentralized peer-to-peer payment network** that is powered by its users with no central authority or middleman.
- From a user perspective, Bitcoin is pretty much like **cash for the Internet**.

---

### B2. Are Bitcoin and Blockchain Similar?
```
   Bitcoin   ≠   Blockchain
```
- **Blockchain is not Bitcoin** — but it IS the technology behind Bitcoin.
- Bitcoin is the **digital token**, and Blockchain is the ledger that keeps track of who holds the digital tokens.
- ⚠️ **One can't have Bitcoin without blockchain — but one CAN have blockchain without Bitcoin.**

---

### B3. What is Bitcoin Mining and How it Works?
- Mining is the process of spending computing power to process transactions, secure the network, and **keep everyone in the system synchronized together**.
- It can be perceived like the **Bitcoin data center** — except that it has been designed to be fully decentralized, with miners operating in all countries and no individual or company controlling the network.
- "Mining" is an analogy to gold mining because it is also a **temporary mechanism** used to issue new bitcoins.
- Unlike gold mining, however, **Bitcoin mining provides a reward in exchange for useful services** required to operate a secure payment network.

**The bitcoin mining process serves two purposes (memorize both!):**
1. **Mining creates new bitcoins** in each block, almost like a central bank printing new money. The amount of bitcoin created per block is fixed and diminishes with time.
2. **Mining creates trust** by ensuring transactions are only confirmed if enough computational power was devoted to the block that contains them. More blocks mean more computation, which means more trust.

**Mining flowchart (Lc#11B p2 — "Bitcoin Mining"):**
```
        ┌──────────────────────────┐
        │ Header of most recent     │
        │ block + Transactions       │
        └────────────┬──────────────┘
                      ↓
              ┌───────────────┐
              │  Hash function │ ←─── Nonce (random value)
              └───────┬────────┘
                      ↓
            ┌───────────────────┐
            │ Hash < Target?      │── No ──► increment Nonce, try again
            │ (compare to Target  │
            │  Value / difficulty)│
            └─────────┬──────────┘
                      │ Yes
                      ↓
        ┌──────────────────────────┐
        │ Block solved! Broadcast    │
        │ & add to blockchain        │
        │ → Reward (BTC + fees)      │
        └──────────────────────────┘

  [Target Value] ──compares with──> [Hash Function output]
  [Determines mining difficulty]
```
- New miners join the network → a new transaction is broadcast → the network races to find a hash below the **Target Value** by varying the **Nonce** → first to solve broadcasts the block → block is added to the chain and the miner gets the **reward**.

---

### B4. How Bitcoin Miners Ensure Security in Bitcoin Network?
- Bitcoin miners help keep the Bitcoin network secure by approving transactions.
- Mining is an important and integral part of Bitcoin that ensures fairness while keeping the Bitcoin network stable, safe, and secure.
- Bitcoin miners are doing the **same equivalent work as gold miners**, except that instead of digging in the ground, bitcoin miners "dig" through **digital documents** to find blocks.
- They achieve this by making **trillions of calculations per second**.
- Miners who use this excessive amount of energy to validate transactions and ensure they're authentic compete for **block rewards** and **transaction fees**.

---

### B5. What Do You Mean by Bitcoin Mining Difficulty?

**The Computationally-Difficult Problem:**
- Bitcoin mining a block is difficult because the **SHA-256 hash of a block's header must be lower than or equal to the target** in order for the block to be accepted by the network.
- This problem can be simplified for explanation purposes: The hash of a block must start with a certain number of zeros. The probability of calculating a hash that starts with many zeros is very low, therefore many attempts must be made.
- In order to generate a new hash each round, a **nonce is incremented**. See [Proof of Work] for more information.

**The Bitcoin Network Difficulty Metric:**
- The Bitcoin mining network difficulty is the measure of how difficult it is to find a hash below a given target.
- The Bitcoin network has a **global block difficulty**; valid blocks must have a hash below this target.
- Mining pools also have a **pool-specific share difficulty**, setting a lower limit for shares.
- As more miners join, the rate of block creation goes up — the network automatically adjusts difficulty so the time to find a valid block returns to ~10 minutes. Hence, every **2016 blocks** is a "*Target Recalculation*" time.
- Any blocks released by malicious miners that do not meet the required difficulty target will simply be **rejected** by everyone else on the network and thus will be **worthless**.

---

### B6. How is Bitcoin Maintaining Average Mining Time?
- As more miners join, the rate of block creation goes up.
- As the rate of block generation goes up, the **difficulty** rises to compensate, which pushes the rate of block creation back down.
- Any blocks released by malicious miners that don't meet the required difficulty target will simply be **rejected** by everyone else on the network, and thus will be worthless.

```
More miners        Block creation        Average mining
join network  →    rate increases   →    time decreases
      ↑                                          │
      │                                          ↓
Determines              ←   Mining        ←   Average mining
mining difficulty           difficulty        time goes back
                             increases          to normal (~10 min)
```
- This is a **very competitive business** where no individual miner can control what is included in the blockchain or reverse spent transactions.

---

### B7. Properties Required for Cryptographic Hash Functions
> Hashing is a one-way function during the message transmission process. In simple terms, hashing means taking an input string of any length and giving out an output of a fixed length. In the context of cryptocurrencies like Bitcoin, the transactions are taken as input and run through a hashing algorithm (Bitcoin uses SHA-256) which gives an output of a fixed length.

**5 properties (memorize all — exam-favorite list):**

1. **Property 1: Deterministic** — A hash function is **deterministic**, meaning that it must always produce the same output for the same input.
2. **Property 2: Quick Computation** — The hash function should be capable of returning the hash of an input quickly. If the process isn't fast enough, the system simply won't be efficient.
3. **Property 3: Pre-Image Resistance** — Given $H(A)$, it is infeasible to determine $A$, where $A$ is the input and $H(A)$ is the output hash. "Infeasible" instead of "impossible" because, given infinite computing resources and time, a hash function CAN be reversed. Let's take a look at how this property protects the network from attacks:
   - Suppose you are rolling a dice and the output that the number comes out (the hash) gives a small clue about your roll. How will you be able to determine what the original number was? It's simply that you have to do is find out the numbers of all the hashes of the combination 1-6 and compare them — deterministic, the same set of numbers in the hash table will always produce the same output.
   - As you can see, it is much easier to crack collision resistance than it is to break pre-image resistance. No hash function is collision-free, but it is seek for trying to find a collision.
   - So, if you are using a function like SHA-256, it's safe to assume that $H(A)=H(B)$ where $A=B$.
4. **Property 4: Small Changes In The Input Changes the Hash (Avalanche Effect)** — Even if you change one character in your data of any size, the entire hash changes completely.
   - **Best Case Scenario:** You get your answer on the first try. You will seriously have to be the luckiest person in the world for this to happen.
   - **Worst Case Scenario:** You get your answer on the $2^{128}-1$ try. Basically, it means that you would need to go through the entire data set.
   - **Average Scenario:** You will find it in the middle. So, you will find it somewhere on the $2^{127} \approx 1.7 \times 10^{38}$ try.
5. **Property 5: Puzzle Friendly** — for every "puzzle" $H(A)=X$ to be solved, no solving strategy is more efficient than brute-force trial-and-error (try a value, hash it, compare to target). This is exactly what Bitcoin mining is.
   - **SHA-256:** produces a 256-bit hash, currently used by **Bitcoin**.
   - **Keccak-256:** produces a 256-bit hash, currently used by **Ethereum**.
   - **Mining procedure:** whenever a new block arrives, all its contents are first hashed. If the hash is **less than the difficulty target**, the block is added to the blockchain and everyone acknowledges it. If not, the **nonce** (an arbitrary string concatenated with the block's hash) is changed and the whole thing is re-hashed — repeating potentially millions of times until the requirement is met.
   - **Why puzzle-friendliness matters:** if solving were easier than brute force, blocks would be found much faster than the ~10 min target, making the network less competitive/secure. No shortcut exists — only trial-and-error across nonces.

> *Note: the slide text for Properties 3–5 is dense and somewhat garbled in the source — the core memorizable points above (deterministic, fast, pre-image resistant, avalanche effect, collision resistant, puzzle-friendly) are the standard properties of a good hash function and overlap directly with [[wiki/hash_functions|Hash Functions (#4)]].*

> ⚠️ **The slides themselves explicitly say: "Rest of the parts are optional (Probably for Leisure Reading)" — i.e. everything from B8 (Bitcoin Wallet) onward is the LOWEST priority in this whole topic.** Skim B8–B10 once for familiarity; do not spend real study time there with one day left.

---

### B8. How to Obtain a Bitcoin Wallet
- Understanding how Bitcoin works may be interesting to some, but you're probably wanting to know how you can use **Bitcoin** to spend some bitcoins of your own. There are actually a few ways you can legally get bitcoins — but obtaining Bitcoin via the network. As long as you have an Internet connection and the necessary hardware to mine bitcoins, you will be paid in Bitcoin.
- First, it should be noted that it's really difficult to purchase bitcoins with credit cards — there's a **fee charged**. Bitcoin may seem cumbersome at first, but trust us when we say it's not.
- ⚠️ **Security** — The most important aspect you want to think about is security. If a Bitcoin exchange is new to the Internet and is missing crucial information, for example, give other people the chance to evaluate it; an exchange that doesn't yet have a security track record probably isn't going to be in your or your money's best interest.
- **Geography** — While Bitcoin is a decentralized network that spreads around the globe, you still need to think about which exchange is geographically nearest/most convenient for you (regulations differ by country).

**Step One: Get a Bitcoin Wallet**
- The very first thing you're going to need is a **Bitcoin Wallet** — aka a Bitcoin client.
- What type of computer you're running, there's a likely an installer for you to download — at minimum, **5 to 10 minutes to get a Bitcoin wallet installed and ready** to go.
- Be sure you take your time to find a client you're comfortable using. Most are designed with simplicity in mind, but some have more advanced options to offer than others which might make it easier or harder to get started.
- The most popular option for Windows, Mac, and Linux is currently **Multibit**. Bitcoin Wallet for Android/iOS is also available.

**Choosing a wallet:**
- Another option is to use a tool/website to find a Bitcoin Wallet, although this might make it easier for you to get started.
- While you may be able to find a service that allows you to use a single address for transactions, your level/way you'll have to install the software on whatever device you have available — these are typically free or low-cost.

---

### B9. Bitcoin Exchanges
- Bitcoin exchanges are a popular and convenient way to obtain bitcoins — there are exchanges around the world that are ready to swap your local currency for bitcoins.
- ❖ **Bitstamp** — This exchange is similar to CoinBase in a lot of ways, but they're a bit more international/global in their reach.
- ❖ **Coinbase** — One of the most popular Bitcoin Exchanges. By that, we mean that you can exchange your local currency for Bitcoin and use the Bitcoin to buy, sell, or trade. They're best known for fast/easy transfers between users and Bitcoin-only wallets — Coinbase walks you through the process of setting up a wallet too.
- ❖ **bTer** — With slow transaction speeds and limits on the size of transfers, bTer is not generally recommended, but they should be discussed because it's on the list that you may run into.
- ❖ **BTC China** — One of the largest growing Bitcoin exchanges. While BTC China is implemented primarily in China and used mostly by Chinese traders, it is very rapidly catching up to other major exchanges in trading volume.

---

### B10. Face to Face / Over the Counter Trades
- Even though it's one of the most popular ways to trade Bitcoin, exchanges aren't the only way to obtain your initial investment in person and at a place that's convenient to both of you.
- The local **BitcoinACH / LocalBitcoins** is one of the best places to find people in your area that are interested in performing trades face-to-face, and also serves as a directory of physical locations around the world where you can find a person willing to buy or sell with cash.
- When the world, you may not be happy about and may be hard to get linked with funds to local bitcoins to your account.
- In addition to one-on-one meetings, many people across Bulgaria, so you might be capable of finding a "Satoshi Square" or Bitcoin markets set-up in public locations.
- It should be noted that in most cases, exchanges might be the simplest way to go about getting bitcoins for you — but for those who prefer to do face-to-face or person-to-person transactions, the methods above can be the best avenue for the job.

---

## Quick Cross-Reference: Topics → Past-Paper Questions
| Slide topic | Past-paper appearance |
|---|---|
| A3 Hashing + A4 PoW + A6 Security summary | 2024 Q3(b) — "explain how blockchain ensures security in terms of hashing and PoW" |
| A2 Blockchain architecture / B2 Bitcoin≠Blockchain | 2021 B-Q3(a) — "how is blockchain related to cryptography" / "what is bitcoin" |
| B3 Mining (not directly examined yet) | — (bonus/insurance) |
| Bitcoin transaction signature validation (covered in [[Blockchain_Solutions.pdf]], not directly in these slides) | 2021 B-Q3(b) — input/output script validation |
| A10 Public/Private/Hybrid, A11 Blockchain vs shared DB, A8 Genesis block, A2 Merkle root | Not yet seen — bonus/insurance for 2026 |

> See [[wiki/blockchain]] for the condensed exam-focused cheat sheet and [[Blockchain_Solutions.pdf]] for full worked past-paper answers.
