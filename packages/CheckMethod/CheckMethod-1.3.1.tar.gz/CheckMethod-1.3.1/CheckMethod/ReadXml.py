# coding:utf-8
import xml.dom.minidom


def get_files_path():
    dom = xml.dom.minidom.parse('config.xml')
    root = dom.documentElement
    for node in root.childNodes:
        if type(node) is type(dom.documentElement):
            #print(node)
            ip = node.getElementsByTagName("ip")[0].firstChild.data.split()[0]
            username = node.getElementsByTagName("username")[0].firstChild.data.split()[0]
            password = node.getElementsByTagName("password")[0].firstChild.data.split()[0]
            port = node.getElementsByTagName("port")[0].firstChild.data.split()[0]
            path = node.getElementsByTagName("path")[0].firstChild.data.split()[0]
            local_path = node.getElementsByTagName("localpath")[0].firstChild.data.split()[0]
            return ip, username, password, port, path, local_path


def get_process_flow_path():
    process_list = []
    # 打开xml文档
    dom = xml.dom.minidom.parse('rules.xml')
    rules = {}
    # 得到文档元素对象
    root = dom.documentElement
    # print(root.nodeName)
    for node in root.childNodes:
        if type(node) is type(dom.documentElement):
            file_name = node.getAttribute("name")
            # print(file_name)
            check_rules = []
            for i in node.getElementsByTagName("column"):
                check = {}
                column_name = i.getAttribute("column_name")
                function_type = i.getAttribute("type")
                column_value = i.firstChild.data.split()[0]
                # print(column_name, function_type, column_value)
                check["column_name"] = column_name
                check["type"] = function_type
                check["value"] = column_value
                check_rules.append(check)
            rules[file_name] = check_rules
    return rules


if __name__ == "__main__":
    get_files_path()
# rules = get_process_flow_path()
# print(rules)
