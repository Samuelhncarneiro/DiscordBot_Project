CREATE TABLE IF NOT EXISTS guild (
    GuildID integer PRIMARY KEY,
	Prefix text DEFAULT "!"
);

CREATE TABLE IF NOT EXISTS exp(
    UserID integer PRIMARY KEY,
    XP integer DEFAULT 0,
    LEVEL integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
); 

CREATE TABLE IF NOT EXISTS mutes(
    UserID integer PRIMARY KEY,
    RolesIDs integer,
    EndTime text
);

CREATE TABLE IF NOT EXISTS register(
    UserID integer PRIMARY KEY,
    RolesIDs integer 
); 