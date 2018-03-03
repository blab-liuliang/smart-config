import os
import struct
import xml.etree.cElementTree as ET

root_path = os.getcwd() + '/'
configure_dir = root_path + 'example/config/'
excel_dir = root_path + 'example/excel/'
output_dir = root_path + 'example/output/'

def write_binary_meta_by_config_data_and_xml_data( xml_file, binary_meta_file, variable_list):
    version = 1
    record_num = 0
    record_id  = 0
    record_data_len = 0
    record_meta_list = []

    data_xml_tree = ET.parse(xml_file)
    root = data_xml_tree.getroot()
    for record in root.iter("record"):
        record_num += 1
        record_meta_list.append( [record_id, record_data_len])
        record_id = int(record.attrib["id"])
        for variable in variable_list:
            variable_name = variable[0]
            variable_type = variable[1]
            variable_value = variable[2]

            if variable[1] == "int":
                record_data_len += 4
            elif variable[1] == "string":
                record_data_len += 4
                record_data_len += len(record.attrib[variable_name])
            elif variable[1] == "vector":
                record_data_len += 4
                for variable_node in record.iter():
                    if variable_node.tag == variable_name:
                        for value_node in variable_node.iter():
                            if variable_value == "int":
                                record_data_len += 4
                            elif variable_value == "string":
                                record_data_len += 4
                                record_data_len += len(value_node.text)


    # write meta file
    print("write binary meta file : " + binary_meta_file)
    f = open(binary_meta_file, "wb")
    f.write(struct.pack( '!ii',version, record_num))

    for record_meta in record_meta_list:
        print(record_meta[0], record_meta[1])
        f.write(struct.pack( '!ii', record_meta[0], record_meta[1]))
    f.close()

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
            binary_meta_file = "smart.config." + namespace + "." + bean_name + ".binary.meta"

            for variable in bean.iter("variable"):
                variable_name = variable.attrib["name"]
                variable_type = variable.attrib["type"]
                variable_value = ""
                if variable_type == "vector" :
                    variable_value = variable.attrib["value"]

                variable_info = [variable_name, variable_type, variable_value]
                variable_list.append(variable_info)


            write_binary_meta_by_config_data_and_xml_data( xml_file_dir + xml_file, output_binary_dir + binary_meta_file, variable_list)

    return

convert_xml_to_binary_meta(configure_dir + 'example.xml', output_dir + 'xml/', output_dir + 'binary/')
