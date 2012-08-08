function() {
	var configMap =  {};
	{% for key, fieldInstance in fields.items %}try{
		configMap['{{ key }}'] = {{ fieldInstance.toJavascript }};
	} catch(ex) {
		// Skip
	}{% endfor %}
	return configMap;
}
