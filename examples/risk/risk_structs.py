#! /usr/bin/env python3

adjacentCountriesD={"Alaska":["Kamchatka","Northwest Territory","Alberta"],
    "Northwest Territory":["Alaska","Alberta","Ontario","Greenland",],
    "Greenland":["Northwest Territory","Ontario","Eastern Canada","Iceland"],
    "Alberta":["Alaska","Northwest Territory","Ontario","Western United States"],
    "Ontario":["Greenland","Alberta","Western United States","Eastern United States","Eastern Canada","Northwest Territory"],
    "Eastern Canada":["Eastern United States","Ontario","Greenland"],
    "Western United States":["Alberta","Ontario","Eastern United States","Central America"],
    "Eastern United States":["Ontario","Eastern Canada","Western United States","Central America"],
    "Central America":["Western United States","Eastern United States","Venezuela"],

    "Venezuela":["Central America","Peru","Brazil"],
    "Peru":["Argentina","Brazil","Venezuela"],
    "Brazil":["Argentina","Peru","Venezuela","North Africa"],
    "Argentina":["Peru","Brazil"],

    "North Africa":["Brazil","Western Europe","Southern Europe","Egypt","East Africa","Central Africa"],
    "Egypt":["Southern Europe","Middle East","East Africa","North Africa"],
    "East Africa":["Middle East","Central Africa","Madagascar","Egypt","South Africa","North Africa"],
    "Central Africa":["North Africa","East Africa","South Africa"],
    "South Africa":["Central Africa","East Africa","Madagascar"],
    "Madagascar":["South Africa","East Africa"],

    "Western Europe":["Great Britain","Northern Europe","Southern Europe","North Africa"],
    "Southern Europe":["Western Europe","Northern Europe","Russia","Middle East","Egypt","North Africa"],
    "Northern Europe":["Great Britain","Scandinavia","Russia","Southern Europe","Western Europe"],
    "Russia":["Southern Europe","Northern Europe","Scandinavia","Ural","Afghanistan","Middle East"],
    "Great Britain":["Iceland","Scandinavia","Northern Europe","Western Europe"],
    "Iceland":["Greenland","Scandinavia","Great Britain"],
    "Scandinavia":["Iceland","Russia","Northern Europe","Great Britain"],

    "Ural":["Russia","Siberia","China","Afghanistan"],
    "Siberia":["Ural","Yakutsk","Irkutsk","Mongolia","China"],
    "Yakutsk":["Siberia","Irkutsk","Kamchatka"],
    "Kamchatka":["Alaska","Japan","Yakutsk","Irkutsk","Mongolia"],
    "Irkutsk":["Siberia","Yakutsk","Kamchatka","Mongolia"],
    "Japan":["Kamchatka","Mongolia"],
    "Mongolia":["Japan","Kamchatka","China","Siberia","Irkutsk"],
    "China":["Mongolia","Southeast Asia","India","Afghanistan","Ural","Siberia"],
    "Afghanistan":["Russia","Ural","China","India","Middle East"],
    "Middle East":["Southern Europe","Russia","Afghanistan","India","East Africa","Egypt"],
    "India":["Middle East","Afghanistan","China","Southeast Asia"],
    "Southeast Asia":["Indonesia","India","China"],

    "Indonesia":["Southeast Asia","Western Australia","New Guinea"],
    "New Guinea":["Eastern Australia","Western Australia","Indonesia"],
    "Western Australia":["Indonesia","Eastern Australia","New Guinea"],
    "Eastern Australia":["New Guinea","Western Australia"]
}

continentD={"Asia":["Ural","Siberia","Yakutsk","Kamchatka","Irkutsk","Japan","Mongolia","China","Afghanistan","Middle East","India","Southeast Asia"],
            "North America":["Alaska","Northwest Territory","Greenland","Alberta","Ontario","Eastern Canada","Western United States","Eastern United States","Central America"],
            "Europe":["Western Europe","Southern Europe","Northern Europe","Russia","Great Britain","Iceland","Scandinavia"],
            "Africa":["North Africa","Egypt","East Africa","Central Africa","South Africa","Madagascar"],
            "Australia":["Indonesia","New Guinea","Western Australia","Eastern Australia"],
            "South America":["Venezuela","Peru","Brazil","Argentina"]}

armiesPerContinentD={"Asia":7,
                     "North America":5,
                     "Europe":5,
                     "Africa":3,
                     "Australia":2,
                     "South America":2}
