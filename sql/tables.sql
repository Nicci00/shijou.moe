PRAGMA encoding="UTF-8";

CREATE TABLE song (
	id integer primary key,
	filename varchar2 not null unique,
	artist varchar2 not null,
	album varchar2 not null,
	title not null
);
CREATE TABLE sideimage (
	id integer primary key,
	filename varchar2 not null unique,
	source varchar2
);