# Created by Balazs Bohar (bbazsi41@gmail.com) 11-03-2021
import os


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
input_file_folder = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "SalmoNet", "public", "protein"))

for subdir, dirs, files in os.walk(input_file_folder):

    # Iterate the protein pages files
    for file in files:
        file_path = subdir + os.sep + file
        output_file = f'{"/".join(file_path.split("/")[0:-1])}/index.html'
        file_path_helper = f'{file_path.split(".")[0]}_helper2.html'
        os.rename(file_path, file_path_helper)

        # Change the html and java variables on the protein pages
        with open(file_path_helper, 'r') as i, open(output_file, 'w') as out:

            html_number = 0
            java_number = 0

            # Change the html variables (indexing)
            for line in i:
                line = line.strip()

                if 'id="actual_ortholog_strain"' in line:
                    
                    # Skipp the first html variable line (this will be the zero)
                    if html_number == 0:
                        html_number += 1
                        out.write(line + '\n')
                        continue

                    # Change the indexing of the html variable
                    elif html_number > 0:
                        new_line_html = line.replace('id="actual_ortholog_strain"', f'id="actual_ortholog_strain_{html_number}"')
                        html_number += 1
                        out.write(new_line_html + '\n')
                        continue
                
                # Change the java variables (indexing)
                if 'document.getElementById("actual_ortholog_strain")' in line:

                    # Skipp the first java variable line (this will be the zero)
                    if java_number == 0:
                        java_number += 1
                        out.write(line + '\n')
                        continue

                    # Change the indexing of the java variable
                    elif java_number > 0:
                        new_line_java = line.replace('document.getElementById("actual_ortholog_strain")', f'document.getElementById("actual_ortholog_strain_{java_number}")')
                        java_number += 1
                        out.write(new_line_java + '\n')
                        continue
                
                # Write the line back to the protein page html file
                out.write(line + '\n')

        # Remove the helper file
        os.remove(file_path_helper)
