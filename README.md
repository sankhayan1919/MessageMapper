# MessageMapper 📱

MessageMapper is a powerful WhatsApp chat analysis tool that provides detailed insights into your chat history. It visualizes various aspects of your conversations, including message patterns, user activity, and media usage.

## Features ✨

- **Message Statistics**: Total messages, words, media, links, emojis, and stickers
- **User Analysis**: Most active users, response times, and chat patterns
- **Time-based Analysis**: Daily, weekly, and monthly activity patterns
- **Media Analysis**: Voice messages, calls, and other media statistics
- **Text Analysis**: Word clouds, message lengths, and deleted messages
- **Group Dynamics**: Mentions, replies, and interaction patterns
- **Individual User Analysis**: Detailed statistics for specific users
- **Interactive Visualizations**: Bar charts, heatmaps, and pie charts

## 🚀 Deployment

You can check out the live version of the app here:  
(https://huggingface.co/spaces/Sankhayan1919/MessageMapperhttps://myapp.vercel.app)

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/sankhayan1919/Machine-Learning/tree/main/Projects/MessageMapper
cd MessageMapper
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies 📦

The project uses the following Python libraries:
- `streamlit`: Web application framework
- `pandas`: Data manipulation and analysis
- `matplotlib`: Data visualization
- `seaborn`: Statistical data visualization
- `wordcloud`: Word cloud generation
- `emoji`: Emoji handling
- `urlextract`: URL extraction from text

## Usage Guide 📖

1. Export your WhatsApp chat:
   - Open WhatsApp
   - Go to the chat you want to analyze
   - Click on three dots (menu)
   - Select "More" > "Export chat"
   - Choose "Without Media"
   - Save the .txt file

2. Run the application:
```bash
streamlit run app.py
```

3. Upload your exported chat file through the sidebar

4. Select a user from the dropdown to view individual statistics or choose "Overall" for group analysis

## Features in Detail 🔍

### Overall Statistics
- Total messages, words, and media shared
- Most active users and their contribution percentages
- Chat age and first message information
- Voice and video call statistics

### Time-based Analysis
- Monthly message timeline
- Daily activity patterns
- Busiest days and months
- Activity heatmap (day vs. time)

### User-specific Analysis
- Individual message statistics
- Response time analysis
- First message of the day patterns
- Late-night activity (12 AM - 3 AM)
- Text length analysis
- Deleted message statistics

### Media Analysis
- Voice message statistics
- Media file analysis
- Call patterns
- Emoji usage

### Group Dynamics
- User mentions and replies
- Interaction patterns
- Message streaks
- Group activity metrics

## Project Structure 📁

```
MessageMapper/
├── app.py              # Main Streamlit application
├── helper.py           # Helper functions for data analysis
├── preprocessor.py     # Data preprocessing functions
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- Thanks to all contributors who have helped improve this project
- Special thanks to the open-source community for the amazing libraries used in this project

## Contact 📧

For any queries or suggestions, please open an issue in the repository.

---

Made with ❤️ by Sankhayan Sadhukhan
