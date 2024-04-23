import yaml
import pdfkit

class HTMLResumeGenerator:
    """
    Quick and dirty HTML resume generator that takes a YAML file as input and generates an HTML resume, 
    which can then be converted to a PDF file.
    """
    def __init__(self, resume_data):
        self.resume = resume_data
        self.config = resume_data['config']
        self.html_content = []

    def create_html_resume(self):
        self.html_content.append(f"<h1>{self.resume['name']}</h1>")
        self.html_content.append("<table><tr><td><strong>Personal Information</strong></td><td><strong>Contact Details</strong></td></tr>")
        self.html_content.append(f"<tr><td><strong>Languages:</strong> Dutch, English, German<br><strong>Birth Date:</strong> 15-08-1981<br><strong>Marital Status:</strong> Married<br><strong>Driving License:</strong> B</td><td><strong>Email:</strong> {self.resume['email']}<br><strong>Address:</strong> {self.resume['address']}<br><strong>Phone:</strong> {self.resume['phone']}<br><strong>LinkedIn:</strong> {self.resume['linkedin']}<br><strong>GitHub:</strong> {self.resume['github']}</td></tr></table>")
        self.html_content.append("<h2>Summary</h2>")
        self.html_content.append(f"<p>{self.resume['summary']}</p>")
        self.add_experience()
        self.add_education()
        self.add_skills()
        self.add_awards()
        self.add_leisure()
        with open('resume.html', 'w') as file:
            file.write('\n'.join(self.html_content))

    def add_experience(self):
        self.html_content.append("<h2>Experience</h2>")
        self.html_content.append("<table style='width: 100%;'>")
        for exp in self.resume['experience']:
            self.html_content.append("<tr>")
            self.html_content.append(f"<td style='width: 30%; vertical-align: top;'><h3 style='margin-top: 20px;'>{exp['title']}</h3><p><strong>Company:</strong> {exp['company']}<br>{exp['location']}<br>{exp['date']}<br>{exp['duration']}</p></td>")
            self.html_content.append("<td style='width: 70%; vertical-align: top;'><ul style='margin-top: 20px;'>")
            for highlight in exp.get('highlights', []):
                self.html_content.append(f"<li>{highlight}</li>")
            self.html_content.append("</ul></td>")
            self.html_content.append("</tr>")
        self.html_content.append("</table>")

    def add_education(self):
        self.html_content.append("<h2>Education</h2>")
        self.html_content.append("<table>")
        for edu in self.resume['education']:
            self.html_content.append("<tr>")
            self.html_content.append(f"<td><h3>{edu['degree']} in {edu['major']}</h3></td>")
            self.html_content.append(f"<td><p><strong>School:</strong> {edu['school']} {edu['date']}</p></td>")
            self.html_content.append("</tr>")
        self.html_content.append("</table>")

    def add_skills(self):
        self.html_content.append("<h2>Skills</h2>")
        self.html_content.append("<table><tr>")
        skills = self.resume['skills']
        mid_point = len(skills) // 2
        left_column = skills[:mid_point]
        right_column = skills[mid_point:]
        self.html_content.append("<td><ul>")
        for skill in left_column:
            self.html_content.append(f"<li>{skill}</li>")
        self.html_content.append("</ul></td>")
        self.html_content.append("<td><ul>")
        for skill in right_column:
            self.html_content.append(f"<li>{skill}</li>")
        self.html_content.append("</ul></td>")
        self.html_content.append("</tr></table>")

    def add_awards(self):
        self.html_content.append("<table><tr><td style='width: 50%; vertical-align: top;'><h2>Awards</h2>")
        for award in self.resume['awards']:
            self.html_content.append(f"<h3>{award['title']}</h3>")
            self.html_content.append(f"<p><strong>Company:</strong> {award['company']} {award['date']}</p>")
            self.html_content.append("<ul>")
            for highlight in award.get('highlights', []):
                self.html_content.append(f"<li>{highlight}</li>")
            self.html_content.append("</ul>")
        self.html_content.append("</td>")

    def add_leisure(self):
        self.html_content.append("<td style='width: 50%; vertical-align: top;'><h2>Leisure</h2>")
        self.html_content.append("<ul>")
        for hobby in self.resume['leisure']:
            self.html_content.append(f"<li>{hobby['title']}</li>")
        self.html_content.append("</ul>")
        self.html_content.append("</td></tr></table>")

class HTMLToPDFConverter:
    def __init__(self, html_content, resume_data, font_name_heading, font_name_body, wkhtmltopdf_path=None):
        self.html_content = html_content
        self.resume = resume_data
        self.font_name_heading = font_name_heading
        self.font_name_body = font_name_body
        self.wkhtmltopdf_path = wkhtmltopdf_path or 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'

    def convert_html_to_pdf(self, output_filename):
        config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)
        style_content = (
            "<style>"
            "body { font-family: '" + self.font_name_body + "'; letter-spacing: 0.05em; }"
            "h1, h2, h3 { font-family: '" + self.font_name_heading + "'; letter-spacing: 0.05em; }"
            "table { width: 100%; }"
            "td { width: 50%; vertical-align: top; }"  # Set each table cell to take up 50% of the table width for both columns
            "p { margin: 0; padding: 0; }"
            "</style>"
        )
        html_content = style_content + '\n'.join(self.html_content)
        try:
            pdfkit.from_string(html_content, output_filename, configuration=config)
        except Exception as e:
            print(f"Failed to generate PDF: {e}")

# Load resume data from YAML
resume_data = yaml.safe_load(open('resume.yaml'))
generator = HTMLResumeGenerator(resume_data)
generator.create_html_resume()
print("HTML resume created successfully!")

# Create PDFs with different font combinations
converter1 = HTMLToPDFConverter(generator.html_content, resume_data, 'Garamond', 'Helvetica')
converter2 = HTMLToPDFConverter(generator.html_content, resume_data, 'Playfair Display', 'Futura')

converter1.convert_html_to_pdf('202404_Daniel_Hamelberg_Resume.pdf')
# converter2.convert_html_to_pdf('resume_font_combination_2.pdf')

