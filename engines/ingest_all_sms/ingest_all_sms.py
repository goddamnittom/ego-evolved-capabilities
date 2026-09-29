import sys
from personal_lifecycle_orchestrator import PersonalLifecycleOrchestrator

sms_list = [
    {
        "id": 730,
        "sender": "64908",
        "body": "It's Amy, your request has been processed & accepted, Tap now to continue https://go.lendlli.com/osn9c40y msg STOP to opt-out (Lendli)",
        "timestamp": "2026-06-09T14:10:00"
    },
    {
        "id": 731,
        "sender": "64908",
        "body": "Welcome to Lendli, your app. was received, we will update once progress is made. Txt HELP for help. STOP to opt-out. Msg freq may vary Msg&Data Rates May Apply",
        "timestamp": "2026-06-09T14:11:00"
    },
    {
        "id": 733,
        "sender": "59392",
        "body": "CheckGo: Thanks for joining! Reply HELP for help, STOP to cancel. Msg&Data rates may apply. Msg freq varies.",
        "timestamp": "2026-06-09T14:15:00"
    },
    {
        "id": 734,
        "sender": "59392",
        "body": "Thomas, CheckGo update - new details are available around 3100. View more here: sub.checkgo.org/DaAitcgb Reply STOP to opt out",
        "timestamp": "2026-06-09T14:16:00"
    },
    {
        "id": 735,
        "sender": "59392",
        "body": "Thomas, Your account is in good standing, your options are now available to view: login.checkgo.io/lJTCYgdp\n(CheckGo)\n\nmsg STOP to quit",
        "timestamp": "2026-06-09T14:17:00"
    },
    {
        "id": 736,
        "sender": "59392",
        "body": "Form ending in 1858 is ready for you to view - Link expires in 12 hours myaccount.checkgo.io/wXc9yFYf Text STOP to Quit (CG)",
        "timestamp": "2026-06-09T14:18:00"
    },
    {
        "id": 746,
        "sender": "97832",
        "body": "9553 is your Grant verification code. Do not share. Grant agents never ask for it.",
        "timestamp": "2026-06-09T15:00:00"
    },
    {
        "id": 747,
        "sender": "+12107910801",
        "body": "Your FloatMe Access Code is 367898.",
        "timestamp": "2026-06-09T15:10:00"
    },
    {
        "id": 748,
        "sender": "75243",
        "body": "Your Plaid verification code is: 905668. Do NOT share it with anyone. Plaid will never call you to ask for this code.\nhuDrUar/xgn",
        "timestamp": "2026-06-09T15:15:00"
    },
    {
        "id": 749,
        "sender": "+18886188273",
        "body": "Your Lenme verification code: 3840973",
        "timestamp": "2026-06-09T15:18:00"
    },
    {
        "id": 750,
        "sender": "+12109344979",
        "body": "173465 is your verification code for FloatMe. Please enter this code to verify your enrollment.",
        "timestamp": "2026-06-09T15:20:00"
    },
    {
        "id": 751,
        "sender": "+12062075207",
        "body": "Your Possible verification code is: 7331. Don't share this code with anyone: our employees will never ask for the code.",
        "timestamp": "2026-06-09T15:25:00"
    },
    {
        "id": 752,
        "sender": "75243",
        "body": "Your Plaid verification code is: 870727. Do NOT share it with anyone. Plaid will never call you to ask for this code.\ndoLuTseHI1n",
        "timestamp": "2026-06-09T15:30:00"
    },
    {
        "id": 753,
        "sender": "+18559476006",
        "body": "Hi! Your Gerald Wallet verification code is: 285506. It will expire in 1 minute.",
        "timestamp": "2026-06-09T15:35:00"
    },
    {
        "id": 754,
        "sender": "+18559476006",
        "body": "Hi! Your Gerald Wallet verification code is: 490138. Your code will expire in 2 minutes.",
        "timestamp": "2026-06-09T15:36:00"
    },
    {
        "id": 755,
        "sender": "75243",
        "body": "Your Plaid verification code is: 344285. Do NOT share it with anyone. Plaid will never call you to ask for this code.",
        "timestamp": "2026-06-09T15:40:00"
    },
    {
        "id": 756,
        "sender": "75243",
        "body": "Your Plaid verification code is: 505996. Do NOT share it with anyone. Plaid will never call you to ask for this code.",
        "timestamp": "2026-06-09T15:42:00"
    },
    {
        "id": 757,
        "sender": "+18559476006",
        "body": "Hi! Your Gerald Wallet verification code is: 400699. Your code will expire in 2 minutes.",
        "timestamp": "2026-06-09T15:45:00"
    },
    {
        "id": 758,
        "sender": "22395",
        "body": "Your EarnIn verification code is: 5630. Don't share this code with anyone.\n@idp.earnin.com #5630",
        "timestamp": "2026-06-09T15:50:00"
    },
    {
        "id": 759,
        "sender": "22395",
        "body": "Your EarnIn verification code is: 5630. Don't share this code with anyone.\n@idp.earnin.com #5630",
        "timestamp": "2026-06-09T15:51:00"
    },
    {
        "id": 760,
        "sender": "32766",
        "body": "Welcome to EarnIn! Your money's ready when you are. Cash out now: https://earnin.link/RC_T1b Reply STOP to opt out",
        "timestamp": "2026-06-09T15:55:00"
    },
    {
        "id": 761,
        "sender": "44398",
        "body": "831308 is your verification code for Klover - Instant Cash Advance.",
        "timestamp": "2026-06-09T16:00:00"
    },
    {
        "id": 762,
        "sender": "+18552424331",
        "body": "831308 is your verification code for Klover - Instant Cash Advance.",
        "timestamp": "2026-06-09T16:01:00"
    },
    {
        "id": 763,
        "sender": "+18339691998",
        "body": "Your Klover advance is on the way! Please leave a review and let us know if you enjoy using Klover:\nhttps://rateklover.onelink.me/edvg/97f5de38",
        "timestamp": "2026-06-09T16:05:00"
    },
    {
        "id": 764,
        "sender": "+18592955380",
        "body": "Your Credit Genie verification code is 564110",
        "timestamp": "2026-06-09T16:10:00"
    },
    {
        "id": 765,
        "sender": "70739",
        "body": "Borrowly: Thanks for joining! Reply HELP for help, STOP to cancel. Msg&Data rates may apply. Msg freq varies. support@borrowly.io.",
        "timestamp": "2026-06-09T16:15:00"
    },
    {
        "id": 766,
        "sender": "70739",
        "body": "Thomas, your request has been accepted! Sign documents now to finalize go.borrowlly.com/CZS7GPLQ Text STOP to Quit - Borrowly",
        "timestamp": "2026-06-09T16:16:00"
    },
    {
        "id": 767,
        "sender": "+19132460230",
        "body": "Identity Prover: Thomas, we received your details. Reply YES to continue to next steps. Reply STOP if you no longer wish to receive messages.",
        "timestamp": "2026-06-09T16:20:00"
    },
    {
        "id": 768,
        "sender": "64908",
        "body": "Lendli - Form reviewed and pre-accepted, Tap Now login.lendlli.com/XvzEGUK5 Text STOP to Quit",
        "timestamp": "2026-06-09T16:25:00"
    },
    {
        "id": 769,
        "sender": "64908",
        "body": "Thomas your account is ready to go! FINAL results: 700. Confirm Now: \n\nhttps://login.lendlli.com/E5GEfBP7\n\nSTOP to end",
        "timestamp": "2026-06-09T16:30:00"
    },
    {
        "id": 770,
        "sender": "64908",
        "body": "Thomas You are in great standing. Log in & view form login.lendlli.com/2oKOzYoP. Text STOP to Quit (Lendli)",
        "timestamp": "2026-06-09T16:35:00"
    }
]

plo = PersonalLifecycleOrchestrator()
for sms in sms_list:
    plo.process_sms(sms["id"], sms["sender"], sms["body"], sms["timestamp"])

plo.generate_dashboard()
print("Ingestion complete. Updated life_state.json and regenerated life_dashboard.html.")
