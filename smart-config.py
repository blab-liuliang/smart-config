import os
import xml.etree.cElementTree as ET

root_path = os.getcwd() + '/'
configure_dir = root_path + 'example/config/'
excel_dir = root_path + 'example/excel/'
output_dir = root_path + 'example/output/'

def write_binary_meta_by_config_data_and_xml_data( xml_file, variable_list):
    print(xml_file, variable_list)

def convert_xml_to_binary_meta(config_file, xml_file_dir, output_binary_dir):
    # parse config_xml iterate all beans
    config_xml_tree = ET.parse( config_file)
    root = config_xml_tree.getroot()
    if root.tag != "namespace":
        print("error: root node tag should be 'namespace'")
        return

    # record namespace
    namespace = root.attrib["name"]

    # iterate beans
    for bean in root.iter("bean"):
        bean_name = bean.attrib["name"]
        bean_genxml = bean.attrib["genxml"]
        variable_list = []
        if bean_genxml == "client":
            xml_file = "smart.config." + namespace + "." + bean_name + ".xml"

            for variable in bean.iter("variable"):
                variable_name = variable.attrib["name"]
                variable_type = variable.attrib["type"]
                variable_value = ""
                if variable_type == "vector" :
                    variable_value = variable.attrib["value"]

                variable_info = [variable_name, variable_type, variable_value]
                variable_list.append(variable_info)


            write_binary_meta_by_config_data_and_xml_data( xml_file, variable_list)

    return

convert_xml_to_binary_meta(configure_dir + 'example.xml', output_dir + 'xml/', output_dir + 'binary/')
