import os
import pypdf
import docx

class SubjectManager:
    def __init__(self, base_path="data/subjects"):
        self.base_path = base_path
        # Map user-friendly names to folder names
        self.subject_map = {
            "📚 الرياضيات": "math",
            "🧪 الفيزياء": "physics",
            "🧬 الأحياء": "biology",
            "🇸🇦 اللغة العربية": "arabic",
            "🇬🇧 اللغة الإنجليزية": "english",
            "💻 علوم الحاسوب": "cs",
            "🆘 الدعم الفني": "support",
            "📝 أسئلة دورات": "general",
            "📅 التقويم الدراسي": "general"
        }

    def get_subject_folder(self, subject_name):
        return self.subject_map.get(subject_name)

    def get_subject_context(self, subject_name):
        folder_name = self.get_subject_folder(subject_name)
        if not folder_name:
            return ""

        folder_path = os.path.join(self.base_path, folder_name)
        if not os.path.exists(folder_path):
            return ""

        context_text = ""
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                if filename.endswith(".txt") or filename.endswith(".md"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        context_text += f"\n--- Content from {filename} ---\n"
                        context_text += f.read()
                        context_text += "\n--------------------------------\n"
                        
                elif filename.endswith(".pdf"):
                    try:
                        reader = pypdf.PdfReader(file_path)
                        text = ""
                        for page in reader.pages:
                            text += page.extract_text() + "\n"
                        
                        context_text += f"\n--- Content from {filename} (PDF) ---\n"
                        context_text += text
                        context_text += "\n--------------------------------\n"
                    except Exception as e:
                        print(f"Error reading PDF {filename}: {e}")

                elif filename.endswith(".docx"):
                    try:
                        doc = docx.Document(file_path)
                        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                        
                        context_text += f"\n--- Content from {filename} (DOCX) ---\n"
                        context_text += text
                        context_text += "\n--------------------------------\n"
                    except Exception as e:
                        print(f"Error reading DOCX {filename}: {e}")

        except Exception as e:
            print(f"Error reading subject context: {e}")
            
        return context_text
