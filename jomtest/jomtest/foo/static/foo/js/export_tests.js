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
<<<<<<< HEAD
	ok(instance ['getName'] != undefined, "no getter");
        ok(instance ['setName'] != undefined, "no setter");
=======
	ok(instance ['getName'] != undefined, "it has no getter");
        ok(instance ['setName'] != undefined, "it has no setter");
>>>>>>> e0623014ea48fbf7b119af805228591da9a269c9
});

test("Readonly fields have no setter", function() {
	var instance = createInstance(config);
	throws(
	    function() {
	      instance.setId(12);
	    },
	    "Readonly field ID should not have a setter method"
	);

});

test("Getters and Setters works", function() {
        var instance = createInstance(config);
        ok(instance.getName() == config['name'], "Wrong name, getter does not work");
        ok(instance.getId() == config['id'], "Wrong name, getter does not work");
        instance.setName('top');
        ok(instance.getName() == "top", "Wrong name,  setter does not work");
});

test("Export to Map", function() {
	var instance = createInstance(config);
        ok(instance.toMap, "not exported to map");
});



