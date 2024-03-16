USE woodytoys;

CREATE TABLE products(
	id mediumint(8) unsigned NOT NULL auto_increment,
	name varchar(255) default NULL,
	price varchar(255) default NULL,
	PRIMARY KEY (id)) AUTO_INCREMENT=1;

INSERT INTO products(name, price) VALUES
	("Set de 100 cubes multicolores","50"),
	("Yoyo","10"),
	("Circuit de billes","75"),
	("Arc à flèches","20"),
	("Maison de poupées","150");
