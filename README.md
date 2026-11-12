# PulseSIP — Smart AI Investing with PayPal Autopay

**Built for the PayPal AI Hackathon**  
**Created by:** Rajarajeswari Saravanan (Third-Year University Student)  
**Demo Video:** [Watch the 3-Minute Walkthrough Video](INSERT_YOUR_YOUTUBE_LINK_HERE)

---

## Overview

**PulseSIP** is an autonomous AI financial assistant designed for everyday retail investors in the **US and UK**. Traditional Systematic Investment Plans (SIPs) run on a rigid, blind schedule—investing the exact same amount whether stock prices are peaking or dipping, and continuing to pull money even when a user's checking account is running low.

PulseSIP upgrades passive monthly investing into intelligent, **human-in-the-loop Agentic Commerce** by combining **Google Gemini** market intelligence with **PayPal's** trusted payment approval workflow.

---

## The Problem (STAR: Situation & Task)

* **Situation:** Millions of everyday investors rely on monthly automated SIPs to build long-term wealth consistently.
* **Task (Two Major Blind Spots):**
  1. **Market-Blind Buying:** Fixed monthly contributions buy fewer units when prices are high and miss opportunities to buy more when market prices drop.
  2. **Cash-Blind Deductions:** Rigid auto-debits keep pulling funds even when checking balances drop too low, risking overdraft stress or shortfalls on everyday bills.

---

## How PulseSIP Works (STAR: Action)

PulseSIP guides the user through a simple, four-step conversational workflow inside a clean Gradio interface:

1. **Conversational Onboarding:** No complicated brokerage forms. The user simply chats with PulseSIP to share their target market (**US** or **UK**), monthly budget, and risk comfort.
2. **Adaptive Allocation & Dip-Boost Rules:** Powered by **Google Gemini**, PulseSIP generates a balanced investment mix and sets configurable **Dip-Boost rules**—automatically increasing the planned contribution (e.g., during a **5%** or **10%** market dip) subject to user-approved limits.
3. **Safety Pause (Cash Protection):** Before any payment is triggered, PulseSIP checks against a user-defined cash threshold (for example, **\$2,000**). If the checking balance falls below that threshold, **Safety Pause** skips that month's contribution so everyday cash stays protected.
4. **Human-in-the-Loop PayPal Sandbox Approval:** PulseSIP never moves money without explicit permission. Once the user reviews the plan and replies **"Yes"**, the agent generates a one-click **PayPal Sandbox** payment approval link.

```text
[User Chat (Gradio)] 
        │
        ▼
[Google Gemini AI Agent] ──► Generates ETF Mix + Dip-Boost & Safety Pause Rules
        │
        ▼
[Human Approval ("Yes")] ──► Explicit User Confirmation
        │
        ▼
[PayPal Sandbox API]     ──► Generates One-Click Payment Approval Link
```

---

## Key Impact (STAR: Result)

* **Smarter Timing Without Chart-Watching:** Retail investors respond to market dips automatically using pre-approved rules.
* **Built-In Cash Safeguards:** Safety Pause protects everyday checking balances from unexpected shortfalls.
* **Trusted Payment Execution:** Bridges AI financial planning directly with PayPal's familiar checkout and recurring payment ecosystem, driving mutual value for both investors and financial platforms.

---

## Tech Stack

* **AI Engine:** Google Gemini (`google-genai` / Google AI Studio)
* **Frontend Interface:** Gradio (Dark-Mode Conversational UI)
* **Payments Integration:** PayPal Developer Sandbox API
* **Environment:** Python / Google Colab

---

## How to Run Locally or in Google Colab

1. **Clone the repository** (or open the `.ipynb` notebook directly in Google Colab):
   ```bash
   git clone https://github.com
   cd PulseSIP
   ```

2. **Install dependencies:**
   ```bash
   pip install google-genai gradio requests python-dotenv
   ```

3. **Set your API keys** as environment variables (or inside Colab Secrets):
   ```bash
   export GEMINI_API_KEY="your_google_gemini_api_key"
   export PAYPAL_CLIENT_ID="your_paypal_sandbox_client_id"
   export PAYPAL_CLIENT_SECRET="your_paypal_sandbox_client_secret"
   ```

4. **Launch the app:**
   Run all cells in the Google Colab notebook or execute your Python script to open the Gradio chat interface.

---

## Disclaimer

*PulseSIP is a hackathon prototype built for demonstration purposes using the **PayPal Sandbox** environment. Market dip triggers, portfolio allocations, and balance thresholds are configurable demo examples and do not constitute personalized financial or investment advice.*
