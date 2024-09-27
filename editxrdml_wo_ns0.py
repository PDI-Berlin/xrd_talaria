import xml.etree.ElementTree as ET

def modify_xrdml(file_path, user_name, sample_id):
    # Register the namespace
    ET.register_namespace('', "http://www.xrdml.com/XRDMeasurement/2.1")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Modify the author name
    for author in root.findall(".//{http://www.xrdml.com/XRDMeasurement/2.1}author"):
        name = author.find("{http://www.xrdml.com/XRDMeasurement/2.1}name")
        if name is not None:
            name.text = user_name

    # Modify the sample information
    for sample in root.findall(".//{http://www.xrdml.com/XRDMeasurement/2.1}sample"):
        id_elem = sample.find("{http://www.xrdml.com/XRDMeasurement/2.1}id")
        if id_elem is not None:
            id_elem.text = sample_id

    # Save the modified XML to a new file
    new_file_path = file_path.replace('.xrdml', '_modified.xrdml')
    tree.write(new_file_path, encoding='utf-8', xml_declaration=True)
    print(f"Modified file saved as: {new_file_path}")

# Example usage
file_path = '2theta-omega.xrdml'
USER_NAME = 'Altug Yildirim'
SAMPLE_ID = 'Sample123'

modify_xrdml(file_path, USER_NAME, SAMPLE_ID)