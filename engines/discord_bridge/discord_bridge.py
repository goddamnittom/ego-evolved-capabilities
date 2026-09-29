import os
import sys
import json
import argparse
import requests
from datetime import datetime

CONFIG_PATH = os.path.expanduser("~/.discord_bridge.json")
INBOX_PATH = os.path.expanduser("~/.discord_inbox.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

def load_inbox():
    if os.path.exists(INBOX_PATH):
        try:
            with open(INBOX_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_inbox(messages):
    with open(INBOX_PATH, 'w') as f:
        json.dump(messages, f, indent=4)

def send_message(content, config):
    # Try Webhook first if configured
    webhook_url = config.get("webhook_url")
    if webhook_url:
        payload = {"content": content}
        r = requests.post(webhook_url, json=payload)
        if r.status_code in [200, 204]:
            return True, "Message sent via Webhook successfully."
        else:
            return False, f"Failed to send via Webhook: {r.status_code} - {r.text}"

    # Try Bot Token and Channel ID
    bot_token = config.get("bot_token")
    channel_id = config.get("channel_id")
    if bot_token and channel_id:
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bot {bot_token}",
            "Content-Type": "application/json"
        }
        payload = {"content": content}
        r = requests.post(url, headers=headers, json=payload)
        if r.status_code in [200, 201]:
            return True, "Message sent via Bot Token successfully."
        else:
            return False, f"Failed to send via Bot Token: {r.status_code} - {r.text}"

    return False, "No webhook_url or bot_token/channel_id configured. Use 'init' command."

def fetch_messages(config, limit=10, after_id=None):
    bot_token = config.get("bot_token")
    channel_id = config.get("channel_id")
    if not bot_token or not channel_id:
        return False, "Bot Token and Channel ID are required to fetch messages."

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit={limit}"
    if after_id:
        url += f"&after={after_id}"

    headers = {
        "Authorization": f"Bot {bot_token}"
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return True, r.json()
    else:
        return False, f"Failed to fetch: {r.status_code} - {r.text}"

def poll_channel(config):
    bot_token = config.get("bot_token")
    channel_id = config.get("channel_id")
    if not bot_token or not channel_id:
        return "Not configured for polling."

    inbox = load_inbox()
    last_id = config.get("last_seen_message_id")

    success, messages = fetch_messages(config, limit=20, after_id=last_id)
    if not success:
        return f"Poll failed: {messages}"

    if not messages:
        return "No new messages."

    # Filter messages to avoid duplicates and self-messages (optional, let's keep all)
    new_messages = []
    for msg in reversed(messages):  # Chronological order
        # Skip messages sent by the bot itself to prevent echoes
        author_bot = msg.get("author", {}).get("bot", False)
        # We can store key fields
        formatted_msg = {
            "id": msg["id"],
            "author": msg.get("author", {}).get("username", "Unknown"),
            "author_id": msg.get("author", {}).get("id"),
            "content": msg.get("content", ""),
            "timestamp": msg.get("timestamp"),
            "is_bot": author_bot
        }
        new_messages.append(formatted_msg)

    if new_messages:
        # Update last seen message ID
        config["last_seen_message_id"] = messages[0]["id"] # messages[0] is the newest in the response
        save_config(config)
        
        # Append to inbox queue
        combined_inbox = inbox + new_messages
        # Keep last 100 messages in local queue
        save_inbox(combined_inbox[-100:])
        return f"Successfully polled {len(new_messages)} new messages."
    
    return "No new messages."

def main():
    parser = argparse.ArgumentParser(description="Discord to Kai Bridge CLI Utility")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # init
    parser_init = subparsers.add_parser("init", help="Initialize configuration")
    parser_init.add_argument("--webhook", help="Discord Webhook URL")
    parser_init.add_argument("--token", help="Discord Bot Token")
    parser_init.add_argument("--channel", help="Discord Channel ID")

    # send
    parser_send = subparsers.add_parser("send", help="Send a message to Discord")
    parser_send.add_argument("message", help="Message text")

    # receive
    parser_receive = subparsers.add_parser("receive", help="Fetch latest messages")
    parser_receive.add_argument("--limit", type=int, default=10, help="Number of messages to retrieve")

    # poll
    subparsers.add_parser("poll", help="Poll for new messages and queue them in inbox")

    # clear
    subparsers.add_parser("clear", help="Clear the local inbox queue")

    args = parser.parse_args()
    config = load_config()

    if args.command == "init":
        if args.webhook:
            config["webhook_url"] = args.webhook
        if args.token:
            config["bot_token"] = args.token
        if args.channel:
            config["channel_id"] = args.channel
        save_config(config)
        print("Configuration updated successfully.")
        print(json.dumps(config, indent=2))

    elif args.command == "send":
        success, msg = send_message(args.message, config)
        print(msg)
        sys.exit(0 if success else 1)

    elif args.command == "receive":
        success, res = fetch_messages(config, limit=args.limit)
        if success:
            print(json.dumps(res, indent=2))
        else:
            print(res)
            sys.exit(1)

    elif args.command == "poll":
        result = poll_channel(config)
        print(result)

    elif args.command == "clear":
        save_inbox([])
        print("Local inbox queue cleared.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
