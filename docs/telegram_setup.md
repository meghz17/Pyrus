# Telegram Bot Setup (5 Minutes) - FREE Forever

## Why Telegram?
- ✅ **100% FREE** (no costs ever)
- ✅ **No approvals needed** (instant setup)
- ✅ **No 24-hour window** (send anytime)
- ✅ **No templates required** (send any message)
- ✅ **Simple API** (no OAuth complexity)

---

## Step 1: Create Bot (2 minutes)

1. Open Telegram app
2. Search for `@BotFather`
3. Send: `/newbot`
4. **Bot name:** `Pyrus Health Agent`
5. **Username:** `pyrus_health_bot` (or any available name)
6. Copy the **bot token** (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

---

## Step 2: Get Your Chat ID (1 minute)

1. Send any message to your new bot (e.g., "Hello")
2. Open this URL in your browser (replace `YOUR_BOT_TOKEN`):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
3. Look for `"chat":{"id":123456789}`
4. Copy that number (your Chat ID)

**Example:**
If your token is `987654321:ABCxyz`, visit:
```
https://api.telegram.org/bot987654321:ABCxyz/getUpdates
```

---

## Step 3: Update n8n Node (2 minutes)

### Replace "Notify WhatsApp" Node

**Delete the current "Notify WhatsApp" node**

**Add new HTTP Request node:**

**Method:** `POST`

**URL:**
```
https://api.telegram.org/botYOUR_BOT_TOKEN/sendMessage
```

Replace `YOUR_BOT_TOKEN` with your actual token.

**Authentication:** None (no auth needed!)

**Send Body:** Toggle ON

**Body Content Type:** `JSON`

**JSON Body:**
```json
{
  "chat_id": "YOUR_CHAT_ID",
  "text": "=Status: {{ $json.joint_status }}\nAction: {{ $json.recommended_action }}\nPartner A: {{ $json.partner_a.normalized }}%\nPartner B: {{ $json.partner_b.normalized }}%"
}
```

Replace `YOUR_CHAT_ID` with your actual chat ID.

---

## Step 4: Test

1. Click **"Execute Workflow"** in n8n
2. Check Telegram - you should get a message instantly! 🎉

---

## Example Configuration

**If your bot token is:** `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
**And your chat ID is:** `987654321`

**URL:**
```
https://api.telegram.org/bot123456789:ABCdefGHIjklMNOpqrsTUVwxyz/sendMessage
```

**JSON Body:**
```json
{
  "chat_id": "987654321",
  "text": "=Status: {{ $json.joint_status }}\nAction: {{ $json.recommended_action }}\nPartner A: {{ $json.partner_a.normalized }}%\nPartner B: {{ $json.partner_b.normalized }}%"
}
```

---

## Comparison

| Feature | WhatsApp (Twilio) | Telegram |
|---------|-------------------|----------|
| **Cost** | $15-25/month | **FREE** |
| **Setup Time** | 30+ min (approvals) | **5 minutes** |
| **Restrictions** | 24-hour window | **None** |
| **Templates** | Required | **Not needed** |
| **Authentication** | OAuth/Basic Auth | **None** |

**Telegram is the clear winner for this use case!** ✅

---

## Bonus: Rich Formatting

Telegram supports Markdown and HTML:

**Markdown example:**
```json
{
  "chat_id": "YOUR_CHAT_ID",
  "text": "=*Status:* {{ $json.joint_status }}\n*Action:* {{ $json.recommended_action }}\nPartner A: {{ $json.partner_a.normalized }}%\nPartner B: {{ $json.partner_b.normalized }}%",
  "parse_mode": "Markdown"
}
```

**HTML example:**
```json
{
  "chat_id": "YOUR_CHAT_ID",
  "text": "=<b>Status:</b> {{ $json.joint_status }}\n<b>Action:</b> {{ $json.recommended_action }}\nPartner A: {{ $json.partner_a.normalized }}%\nPartner B: {{ $json.partner_b.normalized }}%",
  "parse_mode": "HTML"
}
```

---

## Total Time: 5 Minutes
## Total Cost: $0 Forever

Ready to switch? Just follow the 4 steps above!
