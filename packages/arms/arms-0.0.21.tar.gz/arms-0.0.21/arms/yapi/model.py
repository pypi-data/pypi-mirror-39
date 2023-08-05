import json
import yaml
from arms.yapi.util import prefix, extract_include, \
    big_mdtitle_group, small_mdtitle_group, mdyaml_group, pathparam_names, merge_dicts, parse_comment


def sql_type_of(pytype):
    typename_map = {
        'int': 'INT(11)',
        'long': 'BIGINT(20)',
        'bool': 'TINYINT(1)',
        'float': 'DOUBLE',
        'str': 'VARCHAR(200)',
        'text': 'TEXT',
        'datetime': 'DATETIME',
        'date': 'DATE',
        'time': 'TIME',
        'json': 'JSON',
    }
    if pytype.startswith('~'):
        return sql_type_of(pytype[1:])
    if pytype.startswith('str('):
        return 'VARCHAR(' + pytype[4:]
    return typename_map.get(pytype, None)


class Project:
    """
    includes:
      - str
    list:  //projectItems
      - name: str e.g.学校管理
        list:  //projectSubItems
          - name: str e.g.查询学校详情
            method: str
            path: str
            tag: str
            input:
              - Dict
            output: Dict

    """
    @staticmethod
    def subitem_of(yaml_dict):
        """
        后续会做yaml_dict内的类型扩展
        """
        return yaml_dict

    @staticmethod
    def loads(text):
        """
        >>> text = open("example/api.md", encoding='utf8').read()
        >>> assert Project.loads(text)
        >>> assert json.dumps(Project.loads(text), indent=2)
        """
        project = {'includes': [], 'list': []}
        lines = text.splitlines()
        project['includes'] = list(prefix(lines, extract_include))
        for big_lines in big_mdtitle_group(lines):
            title = big_lines[0].replace('#', ' ').strip()
            project_subitems = []
            for small_lines in small_mdtitle_group(big_lines[1:]):
                subtitle = small_lines[0].replace('#', ' ').strip()
                yaml_groups = list(mdyaml_group(small_lines[1:]))
                assert yaml_groups, "Missing yaml part: " + subtitle
                yaml_dict = yaml.load('\n'.join(yaml_groups[0][1:-1]))
                yaml_dict['name'] = subtitle
                yaml_dict.setdefault('tag', '')
                assert 'method' in yaml_dict, subtitle
                assert 'path' in yaml_dict, subtitle
                assert 'input' in yaml_dict and isinstance(yaml_dict['input'], list), subtitle
                assert 'output' in yaml_dict and isinstance(yaml_dict['output'], dict), subtitle
                project_subitems.append(Project.subitem_of(yaml_dict))
            project['list'].append({'name': title, 'list': project_subitems})
        return project


class YapiProject:
    """
    //yapiProjectItems
    - name: str e.g.学校管理
      desc: null
      index: 0
      list: //yapiProjectSubItems
        - method: str e.g."POST"
          title: str e.g."增加或修改学校"
          markdown: str e.g.接口详细描述
          path: str e.g."/school/save"
          req_headers: [{ "value": "", "name": "token", "required": "1"}]
          req_params:
            - name: str e.g."schoolId"
              desc: str e.g."学校ID"
              example: str e.g."北京大学"
          req_query:
            - name: str e.g."schoolName"
              desc: str e.g."学校名称 (搜索参数)"
              required: str e.g."0"
              example: str e.g."北京大学"
          req_body_is_json_schema: false
          req_body_type: form
          req_body_form:
            - name: str e.g."schoolName"
              desc: str e.g."学校名称"
              required: str e.g."0"
              example: str e.g."北京大学"
              type: text
          res_body_type: json
          res_body_is_json_schema: false
          res_body: str e.g."{...}"
          type: static //req_params为空时
          type: var    //req_params非空时
          __v: 0
          api_opened: false
          query_path: {"path": "/school/{schoolId}", "params": []},
          status: undone
    """
    @staticmethod
    def yapijson_of(project):
        yapi_project_items = []
        for project_item in project['list']:
            name, project_subitems = project_item['name'], project_item['list']
            yapi_project_subitems = [YapiProject.subitem_of(item) for item in project_subitems]
            yapi_project_item = {'name': name, 'desc': None, 'index': 0, 'list': yapi_project_subitems}
            yapi_project_items.append(yapi_project_item)
        return json.dumps(yapi_project_items, indent=2)

    @staticmethod
    def subitem_of(project_subitem):
        method = project_subitem['method'].upper()
        title = project_subitem['name']
        markdown = ''
        path = project_subitem['path']
        pathparams = pathparam_names(path)
        itemtype = 'var' if pathparams else 'static'
        inputreqs = merge_dicts(project_subitem['input'])
        req_params = []
        req_query = []
        req_body_form = []
        # 根据method, inputreqs和pathparams设置req_*
        use_body = (method == 'POST' or method == 'PUT')
        for key, value in inputreqs.items():
            if key == '//':
                continue
            elif key in pathparams:
                reqitem = YapiProject.reqitem_of(key, value, is_param=True)
                req_params.append(reqitem)
            elif use_body:
                reqitem = YapiProject.reqitem_of(key, value, is_form=True)
                req_body_form.append(reqitem)
            else:
                reqitem = YapiProject.reqitem_of(key, value)
                req_query.append(reqitem)
        # 根据output生成res_body
        res_body = YapiProject.resbody_of(project_subitem['output'])
        return {
            'method': method,
            'title': title,
            'markdown': markdown,
            'path': path,
            'req_headers': [{ "value": "", "name": "token", "required": "1"}],
            'req_params': req_params,
            'req_query': req_query,
            'req_body_is_json_schema': False,
            'req_body_type': 'form',
            'req_body_form': req_body_form,
            'res_body_type': 'json',
            'res_body_is_json_schema': False,
            'res_body': res_body,
            'type': itemtype,
            '__v': 0,
            'api_opened': False,
            'query_path': {"path": path, "params": []},
            'status': 'undone',
        }

    @staticmethod
    def reqitem_of(key, value, is_param=False, is_form=False):
        """
        {key='id?', value='int hehe||22'} => {name='id', desc='hehe', example='22', required='0', type='text'}
        """
        assert isinstance(key, str) and key, "invalid key: " + str(key)
        name, required = (key[:-1], "0") if key[-1] == '?' else (key, "1")
        pytype, comment, realvalue = parse_comment(value)
        assert sql_type_of(pytype) is not None, "invalid type: " + value
        if realvalue.startswith('"'):
            realvalue = json.loads(realvalue)
        reqitem = {'name': name, 'desc': comment, 'example': realvalue}
        if not is_param: reqitem['required'] = required
        if is_form: reqitem['type'] = 'text'
        return reqitem

    @staticmethod
    def resbody_of(output_dict):
        """
        >>> output_dict = {'//': 'comment', 'aa': True, 'bb': 'str n||"true"', 'cc': 'long hehe||22'}
        >>> print(YapiProject.resbody_of(output_dict))
        {
          // comment
          "aa": true,
          "bb": "true",  //n
          "cc": 22  //hehe
        }
        """
        lines = json.dumps(output_dict, indent=2).splitlines()
        new_lines = []
        for line in lines:
            if '||' in line:
                tail = ''
                key, value = line.split(': ', 1)
                if value[-1] == ',':
                    value, tail = value[:-1], ','
                value = json.loads(value)
                pytype, comment, realvalue = parse_comment(value)
                assert sql_type_of(pytype) is not None, "invalid type: " + value
                new_line = '%s: %s%s  //%s' % (key, realvalue, tail, comment)
                new_lines.append(new_line)
            elif line.strip().startswith('"//"'):
                key, value = line.split(': ', 1)
                if value[-1] == ',': value = value[:-1]
                new_lines.append('%s// %s' % (key[:-4], json.loads(value)))
            else:
                new_lines.append(line)

        return '\n'.join(new_lines)


class ClassDef:
    """
    className: str
    args:
      - name: str
        typehint: str
        desc: str
        example: str
    """
    pass


class EnumDef:
    """
    className: str
    args:
      - name: str
        value: str
        desc: str
    """
    pass


class ModelDefs:
    """
    enums: List[EnumDef]
    classes: List[ClassDef]
    """
    pass