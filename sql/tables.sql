PRAGMA encoding="UTF-8";

CREATE TABLE song (
	id integer primary key,
	filename varchar2 not null unique,
	artist varchar2 not null,
	album varchar2 not null,
	title varchar2 not null
);
CREATE TABLE sideimage (
	id integer primary key,
	filename varchar2 not null unique,
	source varchar2
);

CREATE TABLE newspost (
	id integer primary key,
	author varchar2 not null,
	newstext varchar2 not null,
	creationdate date not null
);

/*
CREATE TABLE vote (
	id integer primary key,
	song_id integer,
	ip_address varchar2,
	vote_timestamp date
);
*/