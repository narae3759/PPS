from eml2pdf import Eml2Pdf

def main():
    wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    eml_filepath = 'eml_folder/[피피에스] 사업 공고 전달의 건.eml'
    eml_dir = 'inputs'

    tool = Eml2Pdf(eml_dir, wkhtmltopdf)
    tool.run()

if __name__ == "__main__":
    main()