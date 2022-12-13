from nlp import NLP
from pprint import pprint
from docx import *
from flask import *
from werkzeug.utils import secure_filename
from utils import get_content, allowed_file
import os


app = Flask(__name__)

nlp = NLP()

uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

@app.route('/summarize/<doc_name>')
def get_summary(doc_name):
    try:
        sections,_ = get_content(doc_name)
        summary_output = {}
        for title,content in sections.items():
            summary = nlp.summary(content)
            summary_output[title] = summary

        pprint(summary_output)

        return jsonify(summary_output)
    except:
        return {"error": "File not found"}
    

@app.route('/summarize_sections/<doc_name>',methods=['POST'])
def summarize_sections(doc_name):
    try:
        if request.method == "POST":
            sub_sections = request.get_json()
            sub_sections = sub_sections.get('sections')

            sections,_ = get_content(doc_name)
            summary_output = {}

            for title,content in sections.items():
                if title in sub_sections:
                    summary = nlp.summary(content)
                    summary_output[title] = summary
                else:
                    continue

            return jsonify(summary_output)
        
    except:
        return {"error": "File not found"}
    
    
@app.route('/get_subsections/<doc_name>',methods=['GET'])
def get_all_subsections(doc_name):
    if doc_name:
        try:   
            _,topics = get_content(doc_name)
            return {"topics": topics}
        except Exception as err:
            return {"error": "File not found"}
    return {"error": "Please provide document name"}


@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")



@app.route('/get_all')
def get_all_documents():
    files = os.listdir(uploads_dir)

    return {"files":files}




@app.route('/save',methods=['GET','POST'])
def save_doc():
    if request.method == 'POST':
        if request.files:
            file = request.files['file']
            
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('upload'))
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(uploads_dir, filename))
                return {"message":"File successfully uploaded"}
            
            return {"error": "Please upload docx file"}
        
        return redirect(url_for('upload'))
    
    

@app.route('/view/<doc_name>')
def view_document(doc_name):
    if doc_name:
        sections,bolds = get_content(doc_name)
        document = {'sections':sections,'topics':bolds}
        return jsonify(document)
    return {"error": "Please provide the document name"}




        

if __name__ == '__main__':  
    app.secret_key = os.urandom(24)
    app.run(debug = True) 