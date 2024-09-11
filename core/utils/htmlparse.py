from ExObject.ExParsel import ExSelector


def _article_node_parser(nodes: ExSelector, process_deep=False, result=None, stop_on=None, filter=None, _state=None):
    if not result:
        result = [["div", ""]]
    if _state == None:
        _state = {"stop_mark": False}
    for tag in nodes:
        try:
            tag_name = tag.xpath("name()").FIrstCleanString()
        except:
            tag_name = ""
        if tag_name and stop_on and stop_on(tag_name, tag):
            _state["stop_mark"] = True
            break

        if tag_name and filter and filter(tag_name, tag):
            continue

        if not tag_name:
            _content = tag.ToString().strip()
            if _content.startswith("<!--"):
                continue
            elif _content in ["::before", "::after"]:
                continue
            if len(result[-1][1]) > 0 and result[-1][1][-1] != " ":
                result[-1][1] += " "
            result[-1][1] += _content
        elif tag_name.lower() == "br":
            result.append(["div", ""])
        elif tag_name.lower() == "img":
            img_url = tag.xpath("./@src").FIrstCleanString()
            result.append(["img", img_url])
            result.append(["div", ""])
        elif tag_name.lower() in ["a", "span", "em", "strong", "i", "b"]:
            _article_node_parser(tag.xpath("./node()"), process_deep, result, stop_on=stop_on, filter=filter, _state=_state)
        elif tag_name.lower() in ["h1", "h2", "h3", "h4", "h5", "h6", "li"]:
            result.append([tag_name.lower(), ""])
            _article_node_parser(tag.xpath("./node()"), process_deep, result, stop_on=stop_on, filter=filter, _state=_state)
            result.append(["div", ""])
        elif tag_name.lower() in ["p", "ul"]:
            result.append(["div", ""])
            _article_node_parser(tag.xpath("./node()"), process_deep, result, stop_on=stop_on, filter=filter, _state=_state)
        elif tag_name.lower() in ["style", "script", "iframe"]:
            continue
        elif tag_name.lower() == "table":
            continue
        elif process_deep:
            result.append(["div", ""])
            _article_node_parser(tag.xpath("./node()"), process_deep, result, stop_on=stop_on, filter=filter, _state=_state)
        if _state["stop_mark"]:
            break
    return result


def article_node_parser(nodes: ExSelector, process_deep=False, result=None, stop_on=None, filter=None, _state=None):
    result = []
    for item in _article_node_parser(nodes, process_deep, result, stop_on, filter, _state):
        if len(item[1].strip()) > 0:
            result.append(item)
    return result
