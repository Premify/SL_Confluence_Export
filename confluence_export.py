import streamlit as st
import zipfile
import os
import io
import shutil

# Function to edit the HTML file
def edit_html_file(file_path, placeholders, replacements):
    with open(file_path, 'r') as file:
        data = file.read()

    # Replace the placeholders
    for placeholder, replacement in zip(placeholders, replacements):
        data = data.replace(placeholder, replacement)

    with open(file_path, 'w') as file:
        file.write(data)


# Streamlit App
def main():
    st.title('Optimize Confluence ZIP Files')

    uploaded_file = st.file_uploader("Choose a zip file", type="zip")
    if uploaded_file is not None:
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall('extracted_files')

        # Walk through the extracted files
        for foldername, subfolders, filenames in os.walk('extracted_files'):
            for filename in filenames:
                if filename.endswith('.html'):
                    if filename == 'index.html':
                        placeholders = ['<ul>']
                        replacements = ['<ul class="toc">']
                    else:
                        placeholders = [
                            '<div class="panel" style="background-color: #EAE6FF;border-color: #998DD9;border-width: 1px;"><div class="panelContent" style="background-color: #EAE6FF;">',
                            '<div class="confluence-information-macro confluence-information-macro-note"><span class="aui-icon aui-icon-small aui-iconfont-warning confluence-information-macro-icon"></span>'
                        ]
                        replacements = [
                            '<div class="confluence-information-macro confluence-information-macro-information"><span class="aui-icon aui-icon-small aui-iconfont-info confluence-information-macro-icon"></span> <div class="confluence-information-macro-body">',
                            '<div class="confluence-information-macro confluence-information-macro-warning"><span class="aui-icon aui-icon-small aui-iconfont-error confluence-information-macro-icon"></span>'
                        ]
                    file_path = os.path.join(foldername, filename)
                    edit_html_file(file_path, placeholders, replacements)

        # Creating zip file again
        shutil.make_archive("updated_files", 'zip', 'extracted_files')
        st.download_button(
            label="Download updated ZIP file",
            data=open("updated_files.zip", "rb"),
            file_name="updated_files.zip",
            mime="application/zip",
        )

        # Deleting the folders after use
        shutil.rmtree('extracted_files')
        os.remove("updated_files.zip")

if __name__ == "__main__":
    main()
