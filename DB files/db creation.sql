-- Tabela de links
CREATE TABLE links (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL,
    descricao TEXT NOT NULL
);

-- Tabela de tags
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL
);

-- Tabela de associação links_tags
CREATE TABLE "links_tags" (
	"link_id"	INTEGER,
	"tag_id"	INTEGER,
	"id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("tag_id") REFERENCES "tags"("id"),
	FOREIGN KEY("link_id") REFERENCES "links"("id")
);

CREATE UNIQUE INDEX "links_url" ON "links" (
	"url"
);