-- Vytvoření databáze
CREATE DATABASE Knihovna;
USE Knihovna;

-- Tabulka Knihy
CREATE TABLE Knihy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazev VARCHAR(255) NOT NULL,
    datum_vydani DATE NOT NULL,
    zanr ENUM('beletrie', 'naučná', 'sci-fi', 'fantasy') NOT NULL,
    cena FLOAT NOT NULL
);

-- Tabulka Autori
CREATE TABLE Autori (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jmeno VARCHAR(255) NOT NULL,
    zije BOOLEAN NOT NULL
);

-- Vazební tabulka Knihy_Autori
CREATE TABLE Knihy_Autori (
    kniha_id INT,
    autor_id INT,
    PRIMARY KEY (kniha_id, autor_id),
    FOREIGN KEY (kniha_id) REFERENCES Knihy(id) ON DELETE CASCADE,
    FOREIGN KEY (autor_id) REFERENCES Autori(id) ON DELETE CASCADE
);

-- Tabulka Uzivatele
CREATE TABLE Uzivatele (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jmeno VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    datum_registrace DATETIME NOT NULL
);

-- Tabulka Vypujcky
CREATE TABLE Vypujcky (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kniha_id INT NOT NULL,
    uzivatel_id INT NOT NULL,
    datum_vypujceni DATE NOT NULL,
    datum_vraceni DATE,
    FOREIGN KEY (kniha_id) REFERENCES Knihy(id) ON DELETE CASCADE,
    FOREIGN KEY (uzivatel_id) REFERENCES Uzivatele(id) ON DELETE CASCADE
);

-- Vytvoření pohledů
-- Pohled 1: Nejčastěji půjčované knihy
CREATE VIEW NejvicePujcovaneKnihy AS
SELECT 
    K.nazev AS Kniha,
    COUNT(V.id) AS PocetVypujcek
FROM 
    Vypujcky V
JOIN 
    Knihy K ON V.kniha_id = K.id
GROUP BY 
    K.nazev
ORDER BY 
    PocetVypujcek DESC;

-- Pohled 2: Aktuálně půjčené knihy s údaji o uživateli
CREATE VIEW AktualniVypujcky AS
SELECT 
    V.id AS VypujckaID,
    K.nazev AS Kniha,
    U.jmeno AS Uzivatel,
    V.datum_vypujceni AS DatumVypujceni
FROM 
    Vypujcky V
JOIN 
    Knihy K ON V.kniha_id = K.id
JOIN 
    Uzivatele U ON V.uzivatel_id = U.id
WHERE 
    V.datum_vraceni IS NULL;