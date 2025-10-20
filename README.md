# 🤖 AI Resume Builder

A modern, AI-powered resume builder that creates professional resumes through conversational chat. Built with Streamlit, it features real-time preview, multiple templates, and intelligent AI assistance.

## ✨ Features

- **💬 Conversational Interface**: Chat with an AI assistant to build your resume naturally
- **👁️ Live Preview**: See your resume update in real-time as you provide information
- **🎨 Multiple Templates**: Choose from Modern Clean, Classic Serif, and Compact Two-Column designs
- **📄 Professional Export**: Download as PDF or DOCX with consistent formatting
- **🤖 AI-Powered**: Intelligent extraction and formatting of your experience, skills, and education
- **📱 Responsive Design**: Clean, modern interface with iMessage-style chat bubbles

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (optional, for enhanced AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/resume_builder.git
   cd resume_builder
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install streamlit python-docx python-dotenv openai beautifulsoup4 reportlab
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎯 How to Use

1. **Start a Conversation**: The AI will greet you and ask about your background
2. **Provide Information**: Share your work experience, education, skills, and contact details
3. **Watch Live Updates**: Your resume updates in real-time on the right side
4. **Choose Template**: Select from available templates using the dropdown
5. **Download**: Click PDF or DOCX buttons to download your finished resume

### Example Conversation
```
AI: Hi! I'm your AI resume assistant. Tell me about your background, work experience, and skills.

You: I'm a product designer with 5 years of experience at tech startups. I've led UX design for mobile apps and have experience with Figma, React, and user research.

AI: Great! I've added your experience as a Product Designer. What's the name of your current company and when did you start this role?
```

## 🏗️ Project Structure

```
resume_builder/
├── app.py                 # Main Streamlit application
├── chat_handler.py        # AI conversation logic
├── templates.py           # Resume templates and styling
├── exporters.py           # PDF/DOCX export functionality
├── resume_builder.py      # Resume generation utilities
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🎨 Templates

### Modern Clean
- Clean, professional design with Inter font
- Two-column layout for experience and education
- Subtle colors and modern typography

### Classic Serif
- Traditional serif design with Georgia font
- Centered layout with classic styling
- Professional and timeless appearance

### Compact Two-Column
- Space-efficient design
- Grid-based layout
- Perfect for detailed resumes

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Customization
- **Templates**: Modify `templates.py` to add new designs
- **AI Behavior**: Adjust prompts in `chat_handler.py`
- **Styling**: Update CSS in `app.py` for UI changes

## 📦 Dependencies

- **streamlit**: Web application framework
- **python-docx**: Word document generation
- **openai**: AI conversation handling
- **beautifulsoup4**: HTML parsing
- **reportlab**: PDF generation
- **python-dotenv**: Environment variable management

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py --server.port 8501
```

### Production Deployment
1. **Streamlit Cloud**: Connect your GitHub repo to Streamlit Cloud
2. **Heroku**: Use the included `Procfile` and `requirements.txt`
3. **Docker**: Build and deploy using the included `Dockerfile`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [OpenAI](https://openai.com/)
- Icons and styling inspired by modern design systems

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/your-username/resume_builder/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

---

**Happy Resume Building! 🎉**
