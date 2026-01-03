import streamlit as st
import os
from pathlib import Path
import pypdf as PyPDF2

# Page configuration
st.set_page_config(
    page_title="NCERT Learning Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'selected_chapter' not in st.session_state:
    st.session_state.selected_chapter = None
if 'selected_chapter_name' not in st.session_state:
    st.session_state.selected_chapter_name = None
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None
if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False
if 'show_mcq' not in st.session_state:
    st.session_state.show_mcq = False

# Base path for PDFs
BASE_PDF_PATH = "/home/alok-mohan/Downloads/NCERT/Books"

# Title
st.title("📚 NCERT Learning Assistant")
st.markdown("#### Smart Learning Platform for Students")
st.markdown("---")

# ================== SIDEBAR FILTERS ==================
with st.sidebar:
    st.header("🎯 Select Your Options")
    
    # Step 1: Class Selection
    class_options = {
        "Class 9": "CLASS 9TH",
        "Class 10": "CLASS 10TH",
        "Class 11": "CLASS 11TH",
        "Class 12": "CLASS 12TH"
    }
    
    class_display = st.selectbox(
        "📌 Step 1: Choose Your Class",
        list(class_options.keys()),
        index=0
    )
    
    class_selected = class_options[class_display]
    
    st.markdown("---")
    
    # Step 2: Subject Selection (based on class)
    st.markdown("📌 **Step 2: Choose Subject**")
    
    # Available subjects per class (you can expand this)
    if class_selected == "CLASS 9TH":
        subjects = ["Hindi", "English", "Mathematics", "Science", "Social Science"]
    elif class_selected == "CLASS 10TH":
        subjects = ["Hindi", "English", "Mathematics", "Science", "Social Science"]
    else:
        subjects = ["Hindi"]  # Add more later
    
    subject_selected = st.selectbox(
        "Select Subject:",
        subjects,
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Step 3: Book Selection (for Hindi only)
    if subject_selected == "Hindi":
        st.markdown("📌 **Step 3: Choose Book**")
        
        if class_selected == "CLASS 9TH":
            books = ["Kshitij", "Kritika", "Sanchayan"]
        elif class_selected == "CLASS 10TH":
            books = ["Kshitij Part 2", "Kritika Part 2", "Sanchayan Part 2"]
        else:
            books = ["All"]
        
        book_selected = st.selectbox(
            "Select Book:",
            books,
            index=0,
            label_visibility="collapsed"
        )
    else:
        book_selected = None
    
    st.markdown("---")
    st.success("✅ Filters Applied!")
    st.info("👇 Scroll down to see chapters")

# ================== CHAPTER DATABASE ==================
def get_chapter_database():
    """Complete chapter database for all classes"""
    
    db = {
        "CLASS 9TH": {
            "Hindi": {
                "Kshitij": [
                    {"num": "101", "name": "दो बैलों की कथा", "author": "प्रेमचंद"},
                    {"num": "102", "name": "ल्हासा की ओर", "author": "राहुल सांकृत्यायन"},
                    {"num": "103", "name": "उपभोक्तावाद की संस्कृति", "author": "श्यामाचरण दुबे"},
                    {"num": "104", "name": "साँवले सपनों की याद", "author": "जाबिर हुसैन"},
                    {"num": "105", "name": "नाना साहब की पुत्री देवी मैना को भस्म कर दिया गया", "author": "चपला देवी"},
                    {"num": "106", "name": "प्रेमचंद के फटे जूते", "author": "हरिशंकर परसाई"},
                    {"num": "107", "name": "मेरे बचपन के दिन", "author": "महादेवी वर्मा"},
                    {"num": "108", "name": "एक कुत्ता और एक मैना", "author": "हजारी प्रसाद द्विवेदी"},
                ],
                "Kritika": [
                    {"num": "201", "name": "इस जल प्रलय में", "author": "फणीश्वरनाथ रेणु"},
                    {"num": "202", "name": "मेरे संग की औरतें", "author": "मृदुला गर्ग"},
                    {"num": "203", "name": "रीढ़ की हड्डी", "author": "जगदीश चंद्र"},
                    {"num": "204", "name": "माटी वाली", "author": "विद्यासागर नौटियाल"},
                    {"num": "205", "name": "किस तरह आखिरकार मैं हिंदी में आया", "author": "शमशेर बहादुर सिंह"},
                ],
                "Sanchayan": [
                    {"num": "301", "name": "गिल्लू", "author": "महादेवी वर्मा"},
                    {"num": "302", "name": "स्मृति", "author": "श्रीराम शर्मा"},
                    {"num": "303", "name": "कल्लू कुम्हार की उनाकोटी", "author": "के. सच्चिदानंदन"},
                    {"num": "304", "name": "मेरा छोटा-सा निजी पुस्तकालय", "author": "धर्मवीर भारती"},
                    {"num": "305", "name": "हामिद खान", "author": "एस. आर. हरनोट"},
                ]
            }
        },
        "CLASS 10TH": {
            "Hindi": {
                "Kshitij Part 2": [
                    {"num": "101", "name": "नेताजी का चश्मा", "author": "स्वयं प्रकाश"},
                    {"num": "102", "name": "बालगोबिन भगत", "author": "रामवृक्ष बेनीपुरी"},
                    {"num": "103", "name": "लखनवी अंदाज़", "author": "यशपाल"},
                ]
            }
        }
    }
    
    return db

# Function to check if PDF exists
def check_pdf_exists(class_name, subject, chapter_num):
    """Check if PDF file exists"""
    # Try different possible paths
    possible_paths = [
        Path(BASE_PDF_PATH) / class_name / subject / f"{chapter_num}.pdf",
        Path(BASE_PDF_PATH) / class_name / subject / chapter_num,  # Without extension
        Path(BASE_PDF_PATH) / class_name / subject / f"Chapter_{chapter_num}.pdf",
    ]
    
    for pdf_path in possible_paths:
        if pdf_path.exists():
            return True, str(pdf_path)
    
    return False, str(possible_paths[0])

# ================== MAIN CONTENT AREA ==================

# Show current selection info
st.markdown(f"### 📚 {class_display} → {subject_selected}" + (f" → {book_selected}" if book_selected else ""))
st.markdown("---")

# Get chapters based on selection
chapter_db = get_chapter_database()

try:
    if subject_selected == "Hindi" and book_selected:
        chapters = chapter_db[class_selected][subject_selected][book_selected]
    else:
        chapters = []
        st.warning("⚠️ Chapter data not available yet for this selection.")
except:
    chapters = []
    st.error("❌ Chapter database not found for this combination.")

# ================== CHAPTER DISPLAY (FRONT PAGE) ==================
if chapters and not st.session_state.show_explanation and not st.session_state.show_mcq:
    
    st.markdown("### 📖 Available Chapters")
    st.markdown(f"*Total Chapters: {len(chapters)}*")
    st.markdown("")
    
    # Display chapters in expandable format
    for idx, chapter in enumerate(chapters, 1):
        
        # Check if PDF exists
        pdf_exists, pdf_path = check_pdf_exists(class_selected, subject_selected, chapter["num"])
        
        # Create expander for each chapter
        with st.expander(
            f"**{idx}. {chapter['name']}**  |  लेखक: {chapter.get('author', 'N/A')}",
            expanded=False
        ):
            
            # Status indicator
            col_status, col_actions = st.columns([1, 3])
            
            with col_status:
                if pdf_exists:
                    st.success("✅ Available")
                else:
                    st.error("❌ Not Found")
                    st.caption(f"Expected: `{chapter['num']}.pdf`")
            
            with col_actions:
                # Three buttons in a row
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                
                # Button 1: Download PDF
                with btn_col1:
                    if pdf_exists:
                        with open(pdf_path, "rb") as file:
                            st.download_button(
                                label="📥 Download PDF",
                                data=file,
                                file_name=f"{chapter['name']}.pdf",
                                mime="application/pdf",
                                key=f"dl_{chapter['num']}",
                                use_container_width=True
                            )
                    else:
                        st.button(
                            "📥 Download PDF",
                            disabled=True,
                            key=f"dl_{chapter['num']}",
                            use_container_width=True
                        )
                
                # Button 2: Explain Chapter
                with btn_col2:
                    if st.button(
                        "🎓 Explain Chapter",
                        key=f"exp_{chapter['num']}",
                        disabled=not pdf_exists,
                        use_container_width=True
                    ):
                        st.session_state.selected_chapter = chapter['num']
                        st.session_state.selected_chapter_name = chapter['name']
                        st.session_state.pdf_path = pdf_path
                        st.session_state.show_explanation = True
                        st.session_state.show_mcq = False
                        st.rerun()
                
                # Button 3: Practice MCQs
                with btn_col3:
                    if st.button(
                        "📝 Practice MCQs",
                        key=f"mcq_{chapter['num']}",
                        disabled=not pdf_exists,
                        use_container_width=True
                    ):
                        st.session_state.selected_chapter = chapter['num']
                        st.session_state.selected_chapter_name = chapter['name']
                        st.session_state.pdf_path = pdf_path
                        st.session_state.show_mcq = True
                        st.session_state.show_explanation = False
                        st.rerun()

# ================== EXPLANATION VIEW ==================
elif st.session_state.show_explanation:
    
    # Back button
    if st.button("⬅️ Back to Chapters"):
        st.session_state.show_explanation = False
        st.session_state.selected_chapter = None
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"## 🎓 Chapter Explanation")
    st.markdown(f"### {st.session_state.selected_chapter_name}")
    st.markdown("---")
    
    # Read PDF and extract text
    def read_pdf(pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages[:3]:  # First 3 pages only for preview
                    text += page.extract_text()
                return text
        except Exception as e:
            return f"Error: {str(e)}"
    
    with st.spinner("📖 Reading PDF..."):
        pdf_text = read_pdf(st.session_state.pdf_path)
    
    # Display extracted text
    with st.expander("📄 View PDF Text (First 3 pages)", expanded=False):
        st.text_area("Extracted Content", pdf_text[:2000], height=300)
    
    st.markdown("---")
    
    # Explanation generation
    st.markdown("### 🤖 AI Explanation")
    
    if st.button("🚀 Generate Explanation with AI"):
        with st.spinner("🔄 AI is generating explanation..."):
            # Placeholder - You'll add Groq API here
            st.markdown("""
            #### 📌 Chapter Summary (Sample)
            
            **प्रस्तावना:**
            यह कहानी/पाठ... [AI explanation will come here]
            
            **मुख्य बिंदु:**
            - Point 1
            - Point 2
            - Point 3
            
            **निष्कर्ष:**
            इस पाठ से हमें यह सीख मिलती है...
            
            ---
            *🔜 Real AI explanation coming soon (Groq API integration needed)*
            """)

# ================== MCQ VIEW ==================
elif st.session_state.show_mcq:
    
    # Back button
    if st.button("⬅️ Back to Chapters"):
        st.session_state.show_mcq = False
        st.session_state.selected_chapter = None
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"## 📝 Practice MCQs")
    st.markdown(f"### {st.session_state.selected_chapter_name}")
    st.markdown("---")
    
    # MCQ Settings
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.slider("Number of Questions", 5, 20, 10)
    with col2:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Mixed"])
    
    if st.button("▶️ Start Quiz"):
        st.markdown("### Quiz Questions:")
        
        # Sample MCQs (You'll generate with AI)
        sample_mcqs = [
            {
                "q": "1. इस पाठ के लेखक कौन हैं?",
                "options": ["प्रेमचंद", "जयशंकर प्रसाद", "महादेवी वर्मा", "सूर्यकांत त्रिपाठी"],
                "correct": 0
            },
            {
                "q": "2. कहानी का मुख्य पात्र कौन है?",
                "options": ["राम", "श्याम", "मोहन", "सोहन"],
                "correct": 1
            }
        ]
        
        score = 0
        for mcq in sample_mcqs:
            st.markdown(f"**{mcq['q']}**")
            answer = st.radio(
                "Select answer:",
                mcq['options'],
                key=f"q_{mcq['q']}"
            )
            
            if st.button(f"Check Answer ✓", key=f"check_{mcq['q']}"):
                if mcq['options'].index(answer) == mcq['correct']:
                    st.success("✅ सही जवाब!")
                    score += 1
                else:
                    st.error(f"❌ गलत! सही जवाब: **{mcq['options'][mcq['correct']]}**")
            
            st.markdown("---")
        
        if st.button("🏆 Show Final Score"):
            st.balloons()
            percentage = (score/len(sample_mcqs))*100
            st.success(f"### 🎉 Your Score: {score}/{len(sample_mcqs)} ({percentage:.0f}%)")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>📚 NCERT Learning Assistant | Made with ❤️ for Students</p>
        <p><small>Chapter-wise PDFs • AI Explanations • MCQ Practice</small></p>
    </div>
    """,
    unsafe_allow_html=True
)
