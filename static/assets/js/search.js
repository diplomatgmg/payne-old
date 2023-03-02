function addQueryStringAsHidden(form) {
    if (form.attr("action") === undefined) {
        throw "form does not have action attribute"
    }

    let url = form.attr("action");
    if (url.includes("?") === false) return false;

    let index = url.indexOf("?");
    let action = url.slice(0, index)
    let params = url.slice(index);
    url = new URLSearchParams(params);
    for (param of url.keys()) {
        let paramValue = url.get(param);
        let attrObject = {"type": "hidden", "name": param, "value": paramValue};
        let hidden = $("<input>").attr(attrObject);
        form.append(hidden);
    }
    form.attr("action", action)
}