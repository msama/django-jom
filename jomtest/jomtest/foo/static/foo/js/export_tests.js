module( "Export" );

var config = {
	id: 1,
	name: "bar"	
}

createInstance = function(config) {
	var instance = new SimpleModelJomDescriptor(config);
        return instance;
}

emptyMap = function isEmpty(map) {
	for(var key in map) {
		if (map.hasOwnProperty(key)) {
		return false;
		}
   	return true;
	}
}


test("Constructor works", function() {
	var instance = createInstance(config);
	ok(instance.getId() == config['id'], "Wrong id");
	ok(instance.getName() == config['name'], "Wrong name");
});

test("Public fields have Getters and Setters", function() {
	var instance = createInstance(config);
	ok(instance ['getName'] != undefined,
			"A getter for field name should have been defined.");
    ok(instance ['setName'] != undefined,
    		"A setter for field name should have been defined");
});

test("Readonly fields have no setter", function() {
	var instance = createInstance(config);
	ok(instance ['setId'] == undefined,
	    "Readonly field ID should not have a setter method");

});

test("Getters and Setters works", function() {
        var instance = createInstance(config);
        ok(instance.getName() == config['name'],
        		"Wrong name, getter does not work");
        ok(instance.getId() == config['id'],
        		"Wrong name, getter does not work");
        instance.setName('top');
        ok(instance.getName() == "top",
        		"Wrong name, setter does not work");
});

test("Export to Map", function() {
	var instance = createInstance(config);
	var exportedMap = instance.toMap;
	for (key in config) {
		ok(exportedMap[key] == config[key],
				"not exported to map");
	}
	ok(exportedMap['model'] == "SimpleModel",
			"Unexpected or missing model entry.")
});



