import base64
import json
import gradio as gr
import requests
from groq import Groq

# ==========================================================
# STEP 1: PASTE YOUR 3 KEYS INSIDE THE QUOTES ""
# ==========================================================
GROQ_API_KEY = "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"
PAYPAL_CLIENT_ID = "BAA5XI9i8kV05U0TTrC0GVSEIxoLZJkd_IjdBdHN69FG1A8lVBL0clDMthYz5ceYDuOQbTaqdpUobcpAWA"
PAYPAL_SECRET = "ECF1R7UJGH77RJOdUpqxCqUtpBtLlNZ0hFPWMn_F1BJefRCSsOjsykTC_bAV70XL7nFbHiH2V6Fxe50y"

# Protected PayPal Sandbox URLs (Encoded so copy-paste can NEVER alter them)
PAYPAL_AUTH_URL = base64.b64decode(
    "aHR0cHM6Ly9hcGktbS5zYW5kYm94LnBheXBhbC5jb20vdjEvb2F1dGgyL3Rva2Vu"
).decode()
PAYPAL_ORDER_URL = base64.b64decode(
    "aHR0cHM6Ly9hcGktbS5zYW5kYm94LnBheXBhbC5jb20vdjIvY2hlY2tvdXQvb3JkZXJz"
).decode()
PAYPAL_RETURN_URL = base64.b64decode(
    "aHR0cHM6Ly93d3cuc2FuZGJveC5wYXlwYWwuY29tL2NoZWNrb3V0bm93L3N1Y2Nlc3M="
).decode()
PAYPAL_CANCEL_URL = base64.b64decode(
    "aHR0cHM6Ly93d3cuc2FuZGJveC5wYXlwYWwuY29tL2NoZWNrb3V0bm93L2NhbmNlbA=="
).decode()

client = Groq(api_key=GROQ_API_KEY.strip())


# Automatically discover valid chat models on your Groq account
def get_groq_models():
    skip = ["whisper", "guard", "tts", "audio", "embedding", "vision"]
    models = []
    try:
        for m in client.models.list().data:
            if not any(s in m.id.lower() for s in skip):
                models.append(m.id)
    except Exception:
        pass
    models.sort(
        key=lambda x: (
            "70b" not in x.lower()
            and "120b" not in x.lower()
            and "versatile" not in x.lower()
        )
    )
    return models if models else ["llama-3.1-8b-instant", "openai/gpt-oss-120b"]


ACTIVE_MODELS = get_groq_models()
print("✅ Active Groq Models found:", ACTIVE_MODELS)


# ==========================================================
# STEP 2: PAYPAL SANDBOX AUTOPAY FUNCTION
# ==========================================================
def create_paypal_autopay(amount: float, currency: str, plan_name: str) -> str:
    """Creates a live PayPal Sandbox payment approval URL for the user's Smart-SIP plan."""
    try:
        auth_res = requests.post(
            PAYPAL_AUTH_URL,
            auth=(PAYPAL_CLIENT_ID.strip(), PAYPAL_SECRET.strip()),
            data={"grant_type": "client_credentials"},
            timeout=15,
        )
        if auth_res.status_code != 200:
            return (
                f"ERROR: PayPal Auth failed (HTTP {auth_res.status_code}):"
                f" {auth_res.text}"
            )

        access_token = auth_res.json().get("access_token")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        order_payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "description": f"PulseSIP Adaptive Autopay: {plan_name}",
                "amount": {
                    "currency_code": currency.upper(),
                    "value": f"{float(amount):.2f}",
                },
            }],
            "application_context": {
                "brand_name": "PulseSIP AI Wealth Agent",
                "user_action": "PAY_NOW",
                "return_url": PAYPAL_RETURN_URL,
                "cancel_url": PAYPAL_CANCEL_URL,
            },
        }
        order_res = requests.post(
            PAYPAL_ORDER_URL,
            headers=headers,
            json=order_payload,
            timeout=15,
        )
        if order_res.status_code not in (200, 201):
            return (
                f"ERROR: PayPal Order failed (HTTP {order_res.status_code}):"
                f" {order_res.text}"
            )

        for link in order_res.json().get("links", []):
            if link.get("rel") == "approve":
                return link.get("href")

        return f"ERROR: Approval link missing in response: {order_res.text}"
    except Exception as e:
        return f"ERROR connecting to PayPal Sandbox: {str(e)}"


# ==========================================================
# STEP 3: AI AGENT WITH TOOL CALLING
# ==========================================================
SYSTEM_PROMPT = """
You are PulseSIP, an intelligent AI Wealth & Smart-SIP Agent built for the PayPal AI Hackathon.
Your goal is to help users invest in US (USD) or UK (GBP) stock markets using an Adaptive SIP strategy that overcomes traditional SIP disadvantages (no rigid fixed amounts, scales up on market dips, scales down during low-cash months to prevent overdrafts, and requires zero complex brokerage apps).

Follow these exact steps:
1. Greet the user warmly and ask 3 quick questions if they haven't answered them yet:
   - Country (US or UK)
   - Monthly investment budget (in USD or GBP)
   - Risk preference (Conservative, Balanced, or Aggressive Growth)
2. Once they answer, present a clear, structured "Adaptive Smart-SIP Plan" showing:
   - Recommended diversified Index ETF allocation (e.g., S&P 500 / FTSE 100)
   - Base monthly contribution vs. Dip-Boost rule & Overdraft-Protection pause rule
   - Ask: "Would you like me to generate your one-click PayPal Autopay link now?"
3. As soon as the user says "Yes", "Approve", or "Setup Autopay", IMMEDIATELY call the `create_paypal_autopay` tool using their monthly budget amount, currency (USD for US, GBP for UK), and a short plan name.
4. Present the clickable PayPal Sandbox approval link clearly so they can authorize payment. Include a brief one-line disclaimer that this is an AI financial simulation powered by PayPal Sandbox.
"""

TOOLS = [{
    "type": "function",
    "function": {
        "name": "create_paypal_autopay",
        "description": (
            "Generate a PayPal Sandbox payment approval link for the user's"
            " Smart-SIP plan."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {"type": "number", "description": "Monthly amount"},
                "currency": {
                    "type": "string",
                    "description": "USD for US, GBP for UK",
                },
                "plan_name": {
                    "type": "string",
                    "description": "Short name of the SIP plan",
                },
            },
            "required": ["amount", "currency", "plan_name"],
        },
    },
}]


def chat_with_agent(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history:
        if isinstance(turn, dict):
            role = turn.get("role", "user")
            content = turn.get("content", "")
            if isinstance(content, list):
                content = " ".join(
                    [c.get("text", "") for c in content if isinstance(c, dict)]
                )
            if content:
                messages.append({"role": role, "content": str(content)})
        elif isinstance(turn, (list, tuple)) and len(turn) == 2:
            if turn[0]:
                messages.append({"role": "user", "content": str(turn[0])})
            if turn[1]:
                messages.append({"role": "assistant", "content": str(turn[1])})

    messages.append({"role": "user", "content": message})

    last_err = ""
    for model_id in ACTIVE_MODELS:
        try:
            res = client.chat.completions.create(
                model=model_id,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.4,
            )
            choice = res.choices[0].message

            # Check if the AI called the PayPal Autopay tool
            if choice.tool_calls:
                tool_call = choice.tool_calls[0]
                args = json.loads(tool_call.function.arguments)
                paypal_url = create_paypal_autopay(
                    amount=args["amount"],
                    currency=args["currency"],
                    plan_name=args["plan_name"],
                )
                messages.append({
                    "role": "assistant",
                    "tool_calls": [{
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }],
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": paypal_url,
                })
                second_res = client.chat.completions.create(
                    model=model_id,
                    messages=messages,
                )
                return second_res.choices[0].message.content

            return choice.content or "No response."
        except Exception as e:
            last_err = str(e)
            continue

    return f"⚠️ Error across models: {last_err}"


# ==========================================================
# STEP 4: LAUNCH WEB CHAT INTERFACE
# ==========================================================
demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="💸 PulseSIP: Autonomous AI Smart-SIP & PayPal Autopay Agent",
    description="Overcome traditional SIP limits with adaptive AI planning + one-click PayPal Sandbox Autopay.",
    examples=[
        "Hi! I want to start a smart SIP.",
        "I am in the US, budget is $200/month, and I want Balanced growth.",
        "Yes, generate my PayPal Autopay link now!",
    ],
)

demo.launch(share=True, debug=True)  
