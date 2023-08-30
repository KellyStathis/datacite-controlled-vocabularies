import csv
import xml.etree.ElementTree as ET
import os, os.path
def convert_csv_to_xsd():

    # If running locally, move to root directory
    cwd = os.getcwd()
    if cwd.split("/")[-1] == "src":
        from dotenv import load_dotenv
        load_dotenv()
        os.chdir("..")

    directory = os.environ["SAVE_DIR"]
    file_name = os.environ["FILE_NAME"]

    for vocabulary_name in ["contributorType", "dateType", "descriptionType", "funderIdentifierType", "nameType", "numberType", "relatedIdentifierType", "resourceTypeGeneral", "relationType", "titleType"]:

        vocabulary_version_history = "placeholder" # fixme - need a way to pull this in from a separate file

        # build xml tree
        schema = ET.Element("xs:schema")
        schema.set("xmlns:xs", "http://www.w3.org/2001/XMLSchema")
        schema.set("xmlns", "http://datacite.org/schema/kernel-4")
        schema.set("targetNamespace", "http://datacite.org/schema/kernel-4")
        schema.set("elementFormDefault", "qualified")

        simpleType = ET.SubElement(schema, "xs:simpleType")
        simpleType.set("name", vocabulary_name)
        simpleType.set("id", vocabulary_name)

        annotation = ET.SubElement(simpleType, "xs:annotation")
        documentation = ET.SubElement(annotation, "xs:documentation")

        restriction = ET.SubElement(simpleType, "xs:restriction")
        restriction.set("base", "xs:string")

        with open(directory + file_name + ".csv") as file:
            csv_file = csv.DictReader(file)
            namespace = "datacite:"
            include_definitions = False

            # get all the options (children) for the controlled list
            term_dict = {}
            for term in csv_file:
                if namespace in term["skos:broader(separator=\",\")"] and term["skos:broader(separator=\",\")"].split(namespace)[1].lower() == vocabulary_name.lower():
                    term_dict[term["skos:prefLabel@en"]] = term["skos:definition@en"]
                if vocabulary_name == term["skos:prefLabel@en"]:
                    documentation.text = term["skos:definition@en"]

            # write options to the xsd in alphabetical order
            for term_value in sorted(term_dict):
                enumeration = ET.SubElement(restriction, "xs:enumeration")
                enumeration.set("value", term_value)
                if include_definitions:
                    annotation = ET.SubElement(enumeration, "xs:annotation")
                    documentation = ET.SubElement(annotation, "xs:documentation")
                    documentation.text = term_dict[term_value]

        # add comment with version history
        comment = ET.Comment(vocabulary_version_history.replace(";", "\n"))
        schema.insert(0, comment)

        # format with indentation
        ET.indent(schema)

        # write tree to xsd
        tree = ET.ElementTree(schema)
        tree.write(directory + "xsd/datacite-{}-v4.xsd".format(vocabulary_name), encoding='UTF-8', xml_declaration=True, default_namespace=None, method='xml', short_empty_elements=True)


if __name__ == '__main__':
    convert_csv_to_xsd()