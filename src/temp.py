import csv
import io

# Mapping of dance titles to genres
dance_genre = {
    "FEEL THE BEAT": "Feel the beat",
    "ACRO": "Acro",
    "JAZZ FUNK 1": "Jazz Funk",
    "ADV JAZZ": "Jazz",
    "INT OPEN": "Open",
    "ADV HEELS": "Heels",
    "INT JAZZ": "Jazz",
    "K-POP": "K-pop",
    "INT LYRICAL": "Lyrical",
    "INT HIP HOP": "Hip hop",
    "BALLET": "Ballet",
    "ADV CONTEMP": "Contemporary",
    "JAZZ FUNK 2": "Jazz Funk",
    "ADV LYRICAL": "Lyrical",
    "BEG HIPHOP": "Hip Hop",
    "ADV HIP HOP 1": "Hip Hop",
    "AFRO FUSION": "Afro Fusion",
    "BEG HEELS": "Heels",
    "TAP": "Tap",
    "BEG CONTEMP": "Contemporary",
    "ADV HIP HOP 2": "Hip hop",
    "ADV OPEN": "Open",
    "DANCEHALL": "Dancehall",
    "INT HEELS": "Heels",
    "INT CONTEMP": "Contemporary"
}

# Input text: each section starts with a dance title (in all caps) followed by the list of names.
# (Include your full data here; the sample below is abbreviated.)
input_text = """
FEEL THE BEAT
Jonathan Kupina
Alex Morrison
Tom Pilarski
Connor Elliott
Michael Alexanian
Jessica Hadden
Jessica Costello
Britany Kennedy 
Becky Fleming
Emily Pike
Ren Franklin
Erin Callon
Sara Kim
Lydia Kara
Ava Albertie
Tim Lorentz
Camden Braaten
Ava Clayford
Aleeza Cooper
Emily Donnelly 
Liliana Duma
Gianna Garate
Hannah Hopkins
Hannah Jaramillo 
Ava McDonald
Virginia Murphy
Alexis Nusink 
Kiera Parliament 
Kealey Parliament 
Natalie Reaume 
Tori Reay 
Karly Willis
Lesley Zosky 


ACRO
Kealey Parliament
Elliote Seagrave
Maggie Best
Sami Poulsen
Aryana Jebely
Hannah Hopkins
Kaylee Devries
Hannah Dietrich
madi parsons
Jaidyn Smith
Nina Wulff
Yvonne Chen
Kiera Parliament
Rachel Roberts
Mikayla Simon
Blaise Racki
Maya Altshuller
Teagan Gage
Caitlin MacInally
Maria Boutros
Andrea Hill

JAZZ FUNK 1
Geena Melbourne
emily corturillo
Abigail Altosaar
Lexis Vincent
Ishani Sinnarajah
Kyra Wolstenholme
tori reay
avani tharmalingam
Eliana Scanga
Keziah Kobia
Sara Kreutzkamp
Bella Yanovsky
Jill Carroll
Kay Lavery
Lara Jagota
claudia muniz
Kemi Akinyode
Daria Kay
Jadyn Sherman
Madeline Turgeon
Amrit Matharu
Talia Hirst
Shria Siramshetty
Parnian Raoofnia
Jávielle Walters
Emmerson Zafiris

ADV JAZZ
Jamie Smith
Ella Annis
Sarah Levinsohn
Sydney Giancola
Sydney Cordes
Jill Carroll 
Morgan Weinfeld
Andrea Hill
emily corturillo
Kaylee Devries
madi parsons
Alessia Carneiro
Abby Rosenthal
Natalie Reaume
Aryana Jebely
Divreen Sohi
gianna garate
Kealey Parliament
Lorelai Piekosz
Jadyn Shuster
Emma Richler
Jaidyn Smith
avani tharmalingam
Aleeza Cooper
Geena melbourne
Sophia Gryshchenko
sydney jacobson
Paulina Szyszka
Lauren Conrod
Nina Wulff
Lena Henrikson
Chloe Dickson
Kalia Rivera
Alyssa Flinkert
Jadyn Sherman
Rachel Roberts
Abigail Altosaar
Tiffany Locsin
Elizabeth Estabrooks
Lea Braun
Tanis Alexander

INT OPEN
Megan Doherty
Heather Booth
Emma Lustic
Sami Poulsen
Alexys-Marie Smith
Hannah Dietrich
Daria Kay
Cassie Howse
Rhiannon Murphy-Fricker
Maya Altshuller
Maria Boutros
Megan Kreutzkamp
Teagan Lawson
Shelley Xie
Lexis Vincent

ADV HEELS
Tiffany Locsin
Alessia Carneiro
Aryana Jebely
Aspen Maciel
Atinuke Laja
Bethany Aggelakos
Cassie Howse
Chloe Poulter
Daniella Okonkwo
Elizabeth Estabrooks
Emily Cardona
Esha Dyal
Genevieve Ajudah
Isabelle Hatzimalis
Jaidyn Smith
Jamie Smith
Kay Lavery
Kaylee Devries
Kealey Parliament
Lauren Conrod
Lea Braun
Lexis Vincent
madi parsons
Mariah Gribowski
marissa laird
Mikayla Weagle
Natasha Shantz
Niane Simms
Priya Sharma
Quiana Fernandes
sarah elmugamar
Sydney Giancola
tori reay
Lisa Nguyen

INT JAZZ
Rachel Roberts
Julia Roy
Maggie Best
Mackenzie Cohall
Emma Lustic
Kayden duncan
Hannah Hopkins
Jesse Stone
chloe jacobs
Yvonne Chen
Agassi Iu 
Tanis Alexander
Casey Christie
Rhiannon Murphy-Fricker
Rachel Tanentzap
Alicia Spagat
Heather Booth
Maya Altshuller
Abbey Jean
Cassandra Brown
Brianna Comeau
Mattigan Wenzel

K-POP
Matteo Amoranto
Kareem Chaudhry
Annie Yu
Emmanuella Sanni
Aarthi Karamchedu
Natalie Palombi
Kira Robinson
Edward Wanyan
Yuxi Wang
Jess Monastero
Mia Aranovich
Rhea Jeetun
Violette Mai
Gehena Brojmohun
Ashton Mansourian
Kiran Rohra
Shria Siramshetty
Damian Slater
Seanna Lorentz
Mahima Purohit
Ugonna Okorie
Crystarbell Okunsoyien
Maria Camila Reyes Castano

INT LYRICAL
Sarah Levinsohn
Agassi Iu
Grace O'Brien
Heather Booth
Maya Altshuller
Jesse Stone
Sarah Christoff
Nuha Yousuf
Vanessa Ventrella
Rhiannon Murphy-Fricker
Gemma Samuels
abigail aziz
Claire Christoff
Inès Chandon

INT HIP HOP
Emily Kogan
Ella Annis
Emma Richler
Derek Song
Quiana Fernandes
Madeline Turgeon
Kay Lavery
Leo Wilkinson
Mikayla Weagle
Kareem Chaudhry
Mackenzie Cohall
Louise Owen
Elliote Seagrave
Emma Mayer
Aleeza Cooper
Grace Churchill
Megan Doherty
Riley Bloch
Shylee Babitsky
Emma de Blois
Lisa Cohen
marissa laird
Bianca Aghar
Emma Labuz
Marion Satgé
Gabriella Boungou
Abby Rosenthal
Camille Laurent
Dariana Rodriguez
Rhiannon Murphy-Fricker
Anastasia Sullivan
Madison Manafo
Mahima Purohit
Chloe Kreger
Kae-Lynn Koe
Lesley Zosky
isabella mena
Marie Cooper

BALLET
Natalie Reaume
Parnian Raoofnia
Casey Christie
Amrit Matharu
Alyssa Flinkert
skye ingram
Lena Henrikson
Genevieve Ajudah
Marina Faillace Andrade
Rosaleigh Davey
Maya Altshuller
Brooke Fraser
Rachel Tanentzap
Regan Berlin Bromstein
Katherine Long
Alexandra Rossanos
Lexi Basile
Gemma Samuels
owen Philipps-Gange
Natasha Shantz
Anna Witzke
Shannon Wilson
Max Reeve
Daini Xiong
Cassie Howse
Emma Bullock 

ADV CONTEMP
Elliote Seagrave
Megan Doherty
Anastasia Sullivan
Abby Rosenthal
madi parsons
Sarah Levinsohn
Lena Henrikson
Divreen Sohi
Ella Annis
Selena Mekhaeil
Jaclyn Appelby
Kealey Parliament
Elizabeth Estabrooks
Kiera Parliament
Andrea Hill
Leah Walters
Joshua Durham
Alexys-Marie Smith
Ava McDonald
Emily Kogan
Rosaleigh Davey
Carlie Stubbert
Lauren Conrod
Teagan Gage
Thea Stamatakos
Agassi Iu
Juia Pizzi
Olivia Sampaio
Priya Sharma
Hannah Jaramillo
Megan Lavery
Alyssa Flinkert
Aleeza Cooper
Emily Cain
Emma de Blois
marissa laird
tori reay
Gabriella Boungou
Haylea Heimpel
Hailey Durham
madison manafo

JAZZ FUNK 2
Javielle Walters
Meron Mehari
Natalie Reaume
julia silverstone
Stacey Batalla
Sarah Ewan
Liliana Duma
Geena melbourne
Lara Jagota
Maya Lane
abby aiello
Mackenzie Cohall
Emily Cardona
Chayanne Romat
Annie Yu
Emmanuella Sanni
Noa Mortensen
serena ladhani
Aarthi Karamchedu
Emily Donnelly
Marina Faillace Andrade
Emily Shaw
Maya Altshuller
Katrina Brady
Noelle Gray
Jennifer Sonam


INT CONTEMP
Emily Corturillo
Leshelle Tate
Abigail Altosaar
Agassi Iu
madi parsons
Heather Booth
Jamie Smith
Ava McConnell
Sami Poulsen
Kate Craig
Aryana Jebely
Kalia Rivera
Madison McGuire
Sara Thoeny
Nikol Pintea
Aspen Maciel
Olivia Alvey
bella verdugo
Cassy Brown
Hannah Dietrich
Jerome EBRARD
Olivia Furman
Carlie Stubbert
Emma Shapland
Abbey Jean
Léonie FELDMANN

ADV LYRICAL
Abigail Altosaar
Ava McConnell
Jadyn Sherman
Rachel Roberts
Jill Carroll
Kiera Parliament
emily corturillo
Abby Rosenthal
Sydney Cordes
Aryana Jebely
Alyssa Flinkert
Kate Wright
Avery Deir
Ellie Ovsenny
madi parsons
Leigh Rotstein
Kristina Bauer
Emma de Blois
Rosaleigh Davey
Sarah Mercier
Jamie Smith
Alessia Carneiro
Aleeza Cooper
Kealey Parliament
Sophia Gryshchenko
Sara Kreutzkamp
Jadyn Shuster
chiara michelazzi
Sami Poulsen
Emma Labuz
Megan Kreutzkamp
Emma Shapland
Kalia Rivera
Nikol Pintea
ava clayford
Camden Braaten
Megan Leung
Emily Kogan
Katie Adderson
abigail aziz


BEG HIPHOP
Natalie Reaume
Prina Shah
Stephanie Teelucksingh
zaara khan
Ella Donovan
Jasmine Gill
kenzie Aguiar
Natasha Kovacs
Prabita Gill
Iqra Morkas
Akash Sharma
Maya Altshuller
Aishwarya Bahirathan
Tom Pilarski
Lexis Vincent 


ADV HIP HOP 1
Sydney Giancola
Gabriel Panlaqui
Emily Kogan
Jamie Smith
Sarah Levinsohn
Kareem Chaudhry
sydney jacobson
Jasmin Townsend
Sydney Cordes
gianna garate
Amanda Hilliard
Liliana Duma
Noa Mortensen
Emily Kolbe
Megan Lavery
Ishani Sinnarajah
Lesley Zosky
Eliana Scanga
Kealey Parliament
Jadyn Shuster
Julia Stratton
Emma Richler
Vanessa Ventrella
Matias Alvarez
Menar Osman
Sydney Yoanidis

AFRO FUSION
Meron Mehari
Mariah Gribowski
Kareem Chaudhry
Daniella Okonkwo
Kassandra Mukamba
Atinuke Laja
Edith Nyamekye
Meghan Osborne
Rose Parackal
Kayla Burton
Nadia Wasak
Nneke Lockhart
Matias Alvarez
Aspen Maciel
Jaya Vos
Audrey Iteka
Anahita Sumoreeah
Samara Stewart
maryam shina
Aaliyah Norris
Bukola Adeniyi
Kriya Budhu
sarah elmugamar
Seanna Lorentz


BEG HEELS
Claire Christoff
Sarah Christoff
Jaya Vos
Jamie Beatty
Cristela Lopez
Lauren Frieday
Katrina Brady
Casey Christie


TAP
Anastasia Sullivan
 Emma de Blois
 Joshua Durham
 Hailey Durham
 Lexis Vincent
 Thea Stamatakos
 Lauren Ferrara
 Talia Kierstead
 Megan Lavery
 Claudia Muniz
 Ava McDonald
 Katie Adderson
 Laura Hampel
 Emily Kolbe
 Allison Trinca
 Lexi Basile
 Aspen Maciel
 Elizabeth Kireev


BEG CONTEMP
Ella Annis
Anna Tiemens
Natalie Groves
Camille Laurent
Olivia Saunders


ADV HIP HOP 2
Gabriel Panlaqui
Tiffany Locsin
Jávielle Walters
Matteo Amoranto
Lauren O'Sullivan
Ashton Mansourian
Jasmin Townsend
Mackenzie Cohall
Natalie Reaume
Divreen Sohi
Kyra Wolstenholme
Derek Song
Ishani Sinnarajah
Kayla Burton
Thanuja Thayalan
Matias Alvarez
tori reay
Kalia Rivera
Amanda Hilliard
Megan Lavery
Emmanuella Sanni
Aryana Jebely
Fangzhou Jiang
Kay Lavery
Lara Jagota
Meron Mehari


ADV OPEN
Ava Mcconnell
Abigail Altosaar
Amanda Hilliard
Anastasia Sullivan
ava clayford
avani tharmalingam
Avery Deir
Bethany Aggelakos
Carlie Stubbert
Elizabeth Estabrooks
emily corturillo
Emma de Blois
Emma Kusiar
Emma Lustic
Emma Richler
Emmerson Zafiris
Geena melbourne
Hailey Durham
Hannah Dietrich
Jaclyn Appelby
Jamie Smith
Jávielle Walters
Jill Carroll
Kate Wright
Kealey Parliament
Kristina Bauer
Kyra Wolstenholme
Leah Walters
Lexis Vincent
madi parsons
Meg Doherty
Natalie Reaume
Priya Sharma
Rachel Roberts
Sami Poulsen
Sophia Gryshchenko
sydney jacobson
Tanis Alexander
Thea Stamatakos
tori reay


DANCEHALL
Leshelle Tate
Tiffany Locsin
Maggie Best
Nina Wulff
Jaeda Dennis
kelice morgan ranger
Emily Cardona
Shaampavi Kamalarajan
Julie-Ann Da Silva
Emily Cain
Nadia Wasak
Niane Simms
Jennifer Sonam
Bianca Aghar
Genevieve Ajudah
Alexys-Marie Smith
Kristen Ram
Thanuja Thayalan
Lara Jagota
Talia Hirst
Giselle Smith
Camille Laurent
Sydney Yoanidis
Fangzhou Jiang
Stacey Batalla
Mia Smith


INT HEELS
Cassie Howse
Caitlin MacInally
Vanessa Manrique
Phoebe Bernardo
Rachana Bharwani
Megha Krishna
Isabelle Hatzimalis
Olivia Saunders
Eesha Irfan
Shelley Xie
Brisseika Beltran
Brianna Comeau
"""

# Parse the input text into sections.
# We assume that each dance section is separated by a blank line.
sections = input_text.strip().split("\n\n")

# Build a dictionary mapping each dance to the set of dancer names.
# Names are normalized (trimmed and lowercased) for consistency.
dance_to_dancers = {}
for section in sections:
    lines = section.strip().splitlines()
    if not lines:
        continue
    # First line is the dance title; we convert it to uppercase to match our mapping keys.
    dance = lines[0].strip().upper()
    # Subsequent lines are dancer names (normalized to lowercase)
    dancers = {line.strip().lower() for line in lines[1:] if line.strip()}
    dance_to_dancers[dance] = dancers

# Create a sorted list of all dancer names across all dances.
all_dancers = set()
for dancers in dance_to_dancers.values():
    all_dancers.update(dancers)
sorted_dancers = sorted(all_dancers)

# Prepare CSV output.
# The header includes "Dance", "Genre", then one column per dancer.
output = io.StringIO()
writer = csv.writer(output)
header = ["Dance", "Genre"] + sorted_dancers
writer.writerow(header)

# Write one row per dance.
# We use the ordering defined by the dance_genre mapping.
for dance in dance_genre:
    genre = dance_genre[dance]
    dancers = dance_to_dancers.get(dance, set())
    # For each dancer column, mark 1 if the dancer is in the dance; otherwise 0.
    row = [dance, genre] + [1 if dancer in dancers else 0 for dancer in sorted_dancers]
    writer.writerow(row)

# Get the CSV result and print it (or write it to a file)
csv_result = output.getvalue()
# Write to a file
with open("output.csv", "w", newline="") as f:
    f.write(csv_result)