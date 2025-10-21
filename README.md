🧠 Anti-Cyberbullying Chat Monitor (Python + Tkinter)

🔍 Overview
The Anti-Cyberbullying Chat Monitor is a desktop-based chat simulation system built using Python and Tkinter.
It monitors real-time chat messages and automatically detects cyberbullying or abusive language using a keyword-based detection system.
All chat history and bullying incidents are logged automatically for review by administrators.

💡 Key Features:
✅ Real-time chat monitoring
✅ Keyword-based bullying detection (customizable keyword list)
✅ Automatic logging of chat messages and bullying incidents
✅ Separate Admin Console to monitor alerts live
✅ Chat history restoration on startup
✅ Interactive and user-friendly GUI built with Tkinter
✅ Alert notifications for detected bullying messages

⚙️ Technologies Used:
Python 3
Tkinter (GUI library)
Regex (for keyword detection)
Datetime & OS modules (for logging & file management)

📁 Auto-generated Files:
chat_history.log — Records all user messages
bullying_incidents.log — Records detected bullying messages

🚀 How It Works:
The user enters a username and message.
The system checks the message for bullying-related keywords.
If bullying is detected:
The message is highlighted in red in the chat
An admin alert popup appears
The incident is logged automatically
Chat history is stored and restored on startup for continuity.
