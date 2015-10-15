#!/usr/bin/env python
# -*- coding: utf-8 -*-

corredores = [
    {
        'corredor': 'Independencia',
        'segmento': 'Paseo Colón - 9 de julio',
        'sentido' : 'centro',
        'id': 10,
        'ids': 'cInde',
        'from': '-34.617132, -58.369498',
        'to': '-34.617584, -58.380221',
        'waypoints': [
            "-34.617178, -58.372625",
            "-34.617354, -58.376659"
        ],
    },
    {
        'corredor': 'Illia',
        'segmento': 'Sarmiento - General Paz',
        'sentido' : 'provincia',
        'id': 11,
        'ids':'cIlli',
        'from': '-34.567044, -58.407682',
        'to': '-34.534481, -58.465146',
        'waypoints': [
            "-34.557510, -58.422456",
            "-34.549204, -58.436253",
            "-34.541551, -58.449782"
        ],

    },
    {
        'corredor': 'Illia',
        'segmento': 'General Paz - Sarmiento',
        'sentido' : 'centro',
        'id': 12,
        'ids':'cIlli',
        'from': '-34.534799, -58.465800',
        'to': '-34.567291, -58.407972',
        'waypoints': [
            "-34.539254, -58.456938",
            "-34.543186, -58.448269",
            "-34.547905, -58.439622",
            "-34.555354, -58.426275"
        ]
    },
    {
        'corredor': '9 de julio',
        'segmento': 'Arroyo - Corrientes',
        "sentido": "provincia",
        'id': 13,
        'ids': 'c9int',
        'from': '-34.591657, -58.382086',
        'to': '-34.603760, -58.382123',
        'waypoints': [
            "-34.595490, -58.382493",
            "-34.599120, -58.382122"
        ]
    },
    {
        'corredor': 'Cerrito',
        'segmento': 'Arroyo - Corrientes',
        'sentido': 'provincia',
        'id': 14,
        'ids':'cCerr',
        'from': '-34.591573, -58.382939',
        'to': '-34.603742, -58.382290',
        'waypoints': [
            "-34.595521, -58.382762",
            "-34.599155, -58.382595"
        ]
    },
    {
        'corredor': '9 de julio',
        'segmento': 'Corrientes - Arroyo',
        'sentido':'centro',
        'id': 15,
        'ids': 'c9int',
        'from': '-34.603575, -58.381227',
        'to': '-34.591665, -58.381887',
        'waypoints': [
            "-34.599094, -58.381650",
            "-34.595475, -58.381989"
        ]
    },
    {
        'corredor': 'Pellegrini',
        'segmento': 'Corrientes - Arroyo',
        'sentido': 'centro',
        'id': 16,
        'ids': 'cPell',
        'from': '-34.603606, -58.380969',
        'to': '-34.591657, -58.381587',
        'waypoints': [
            "-34.599080, -58.381291",
            "-34.595435, -58.381469"
        ]
    },
    {
        'corredor': '9 de julio',
        'segmento': 'San Juan - Corrientes',
        'sentido' : 'centro',
        'id': 17,
        'ids': 'c9int',
        'from': '-34.622146, -58.380568',
        'to': '-34.603577, -58.381222',
        'waypoints': [
            "-34.618500, -58.380659",
            "-34.614257, -58.380852",
            "-34.609675, -58.381088",
            "-34.606138, -58.381335"
        ]
    },
    {
        'corredor': 'Pellegrini',
        'segmento': 'San Juan - Corrientes',
        'sentido': 'centro',
        'id': 18,
        'ids': 'cPell',
        'from': '-34.622133, -58.379994',
        'to': '-34.603608, -58.380970',
        'waypoints': [
            "-34.619758, -58.380187",
            "-34.615260, -58.380396",
            "-34.610770, -58.380616",
            "-34.607312, -58.380782"
        ]
    },
    {
        'corredor': '9 de julio',
        'segmento': 'Corrientes - San Juan',
        'sentido': 'provincia',
        'id': 19,
        'ids': 'c9int',
        'from': '-34.60372, -58.38210',
        'to': '-34.62213, -58.38102',
        'waypoints': [
            "-34.60736, -58.38160",
            "-34.61108, -58.38140",
            "-34.61528, -58.38119",
            "-34.61974, -58.38104"
        ]
    },
    {
        'corredor': 'Cerrito',
        'segmento': 'Corrientes - San Juan',
        'sentido' : 'provincia',
        'id': 20,
        'ids':'cCerr',
        'from': '-34.60374, -58.38222',
        'to': '-34.62215, -58.38143',
        'waypoints': [
            "-34.60374, -58.38222",
            "-34.61126, -58.38185",
            "-34.61581, -58.38164",
            "-34.61975, -58.38145",

        ]
    },
    {
        'corredor': 'Alem',
        'segmento': 'Rojas - Casa Rosada',
        'sentido': 'provincia',
        'id': 21,
        'ids':'cAlem',
        'from': '-34.59501, -58.37287',
        'to': '-34.60727, -58.37029',
        'waypoints': [
            "-34.59903, -58.37095",
            "-34.60215, -58.37039",
            "-34.60577, -58.37008"
        ]
    },
    {
        'corredor': 'Alem',
        'segmento': 'Casa Rosada - Rojas',
        'sentido' : 'centro',
        'id': 22,
        'ids':'cAlem',
        'from': '-34.60660, -58.36964',
        'to': '-34.59497, -58.37265',
        'waypoints': [
            "-34.60372, -58.37003",
            "-34.60056, -58.37034",
            "-34.59770, -58.37132"
        ]
    },
    {
        'corredor': 'Corrientes',
        'segmento': 'Medrano - Obelisco ',
        'sentido' : 'centro',
        'id': 23,
        'ids':'cCorr',
        'from': '-34.60317, -58.42099',
        'to': '-34.60371, -58.38207',
        'waypoints': [
            "-34.60412, -58.41214",
            "-34.60455, -58.40542",
            "-34.60450, -58.39570",
            "-34.60412, -58.38748"
        ]
    },
    {
        'corredor': 'Rivadavia',
        'segmento': 'Pueyrredón - Montevideo',
        'sentido': 'centro',
        'id': 24,
        'ids':'cRiva',
        'from': '-34.60914, -58.38913',
        'to': '-34.61012, -58.40598',
        'waypoints': [
            "-34.60944, -58.39436",
            "-34.60978, -58.39947",
            "-34.61000, -58.40351"
        ]
    },
    {
        'corredor': 'Av. de Mayo',
        'segmento': 'Montevideo - Plaza de Mayo',
        'sentido': 'centro',
        'id': 25,
        'ids':'cAvdm',
        'from': '-34.60859, -58.37350',
        'to': '-34.60915, -58.38916',
        'waypoints': [
            "-34.60888, -58.37783",
            "-34.60911, -58.38206",
            "-34.60938, -58.38625"
        ]
    },
    {
        'corredor': 'San Martín',
        'segmento': 'General Paz - Beiró',
        'sentido' : 'centro',
        'id': 26,
        'ids':'cSanm',
        'from': '-34.58947, -58.51822',
        'to': '-34.59677, -58.49717',
        'waypoints': [
            "-34.59121, -58.51258",
            "-34.59246, -58.50878",
            "-34.59540, -58.50094"
        ]
    },
    {
        'corredor': 'San Martín',
        'segmento': 'Beiró - General Paz',
        'sentido' : 'provincia',
        'id': 27,
        'ids':'cSanm',
        'from': '-34.59677, -58.49717',
        'to': '-34.58947, -58.51822',
        'waypoints': [
            "-34.59540, -58.50094",
            "-34.59246, -58.50878",
            "-34.59121, -58.51258"
        ]
    },
    {
        'corredor': 'San Martín',
        'segmento': 'Beiró - Juan B. Justo',
        'sentido' : 'centro',
        'id': 28,
        'ids':'cSanm',
        'from': '-34.59677, -58.49717',
        'to': '-34.60451, -58.45864',
        'waypoints': [
            "-34.59719, -58.49041",
            "-34.59760, -58.48520",
            "-34.59922, -58.47988",
            "-34.60124, -58.47160",
            "-34.60318, -58.46357"
        ]
    },
    {
        'corredor': 'San Martín',
        'segmento': 'Juan B. Justo - Beiró',
        'sentido' : 'provincia',
        'id': 29,
        'ids':'cSanm',
        'from': '-34.60451, -58.45864',
        'to': '-34.59677, -58.49717',
        'waypoints': [
            "-34.60318, -58.46357",
            "-34.60124, -58.47160",
            "-34.59922, -58.47988",
            "-34.59760, -58.48520",
            "-34.59719, -58.49041"
        ]
    },
    {
        'corredor': 'Juan B. Justo',
        'segmento': 'Santa Fé - Corrientes',
        'sentido': 'provincia',
        'id': 30,
        'ids': 'cJuan',
        'from': '-34.57824, -58.42660',
        'to': '-34.59472, -58.44439',
        'waypoints': [
            "-34.58110, -58.42930",
            "-34.58493, -58.43437",
            "-34.59145, -58.43969"
        ]
    },
    {
        'corredor': 'Juan B. Justo',
        'segmento': 'Corrientes - Santa Fé',
        'sentido' : 'centro',
        'id': 31,
        'ids': 'cJuan',
        'from': '-34.59472, -58.44439',
        'to': '-34.57824, -58.42660',
        'waypoints': [
            "-34.59145, -58.43969",
            "-34.58493, -58.43437",
            "-34.58110, -58.42930"
        ]
    },
    {
        'corredor': 'Juan B. Justo',
        'segmento': 'Nazca - Corrientes',
        'sentido' : 'centro',
        'id': 32,
        'ids': 'cJuan',
        'from': '-34.61803, -58.47614',
        'to': '-34.59472, -58.44439',
        'waypoints': [
            "-34.61268, -58.47069",
            "-34.60892, -58.46479",
            "-34.60295, -58.45636",
            "-34.59852, -58.44986"
        ]
    },
    {
        'corredor': 'Juan B. Justo',
        'segmento': 'Corrientes - Nazca',
        'sentido' : 'provincia',
        'id': 33,
        'ids': 'cJuan',
        'from': '-34.59472, -58.44439',
        'to': '-34.61803, -58.47614',
        'waypoints': [
            "-34.59852, -58.44986",
            "-34.60295, -58.45636",
            "-34.60892, -58.46479",
            "-34.61268, -58.47069"
        ]
    },
    {
        'corredor': 'Juan B. Justo',
        'segmento': 'Nazca - General Paz',
        'sentido' : 'provincia',
        'id': 34,
        'ids': 'cJuan',
        'from': '-34.61803, -58.47614',
        'to': '-34.63474, -58.52899',
        'waypoints': [
            "-34.62118, -58.48001",
            "-34.62492, -58.48569",
            "-34.62992, -58.49550",
            "-34.63407, -58.50571",
            "-34.63391, -58.52215"
        ]
    },
    {
        'corredor': 'Juan B. Justo',
        'segmento': 'General Paz - Nazca',
        'sentido' : 'centro',
        'id': 35,
        'ids': 'cJuan',
        'from': '-34.63474, -58.52899',
        'to': '-34.61803, -58.47614',
        'waypoints': [
            "-34.63391, -58.52215",
            "-34.63407, -58.50571",
            "-34.62992, -58.49550",
            "-34.62492, -58.48569",
            "-34.62118, -58.48001"
        ]
    },
    {
        'corredor': 'Córdoba',
        'segmento': '9 de julio - Estado de Israel',
        'sentido' : 'centro',
        'id': 36,
        'ids': 'cCord',
        'from': '-34.59908, -58.38193',
        'to': '-34.59768, -58.42352',
        'waypoints': [
            "-34.59948, -58.38994",
            "-34.59976, -58.39743",
            "-34.59847, -58.40386",
            "-34.59807, -58.41116",
            "-34.59786, -58.41760"
        ]
    },
    {
        'corredor': 'Córdoba',
        'segmento': 'Estado de Israel - Dorrego',
        'sentido' : 'centro',
        'id': 37,
        'ids': 'cCord',
        'from': '-34.59768, -58.42352',
        'to': '-34.58452, -58.44478',
        'waypoints': [
            "-34.59514, -58.42873",
            "-34.59245, -58.43292",
            "-34.58970, -58.43697",
            "-34.58703, -58.44103"
        ]
    },
    {
        'corredor': 'Paseo Colón',
        'segmento': 'San Juan - Casa Rosada',
        'sentido' : 'centro',
        'id': 38,
        'ids':'cPase',
        'from': '-34.62172, -58.36835',
        'to': '-34.60944, -58.36932',
        'waypoints': [
            "-34.61935, -58.36865",
            "-34.61718, -58.36874",
            "-34.61297, -58.36925"
        ]
    },
    {
        'corredor': 'Paseo Colón',
        'segmento': 'Casa Rosada - San Juan',
        'sentido': 'provincia',
        'id': 39,
        'ids':'cPase',
        'from': '-34.60951, -58.36957',
        'to': '-34.62168, -58.36835',
        'waypoints': [
            "-34.61241, -58.36953",
            "-34.61637, -58.36942",
            "-34.61935, -58.36895"
        ]
    },
    {
        'corredor': 'Cabildo',
        'segmento': 'General Paz - Congreso',
        'sentido' : 'centro',
        'id': 40,
        'ids':'cCabi',
        'from': '-34.53942, -58.47538',
        'to': '-34.55533, -58.46268',
        'waypoints': [
            "-34.54321, -58.47268",
            "-34.54763, -58.46959",
            "-34.55197, -58.46590"
        ]
    },
    {
        'corredor': 'Cabildo',
        'segmento': 'Congreso - General Paz',
        'sentido' : 'provincia',
        'id': 41,
        'ids':'cCabi',
        'from': '-34.55524, -58.46264',
        'to': '-34.53934, -58.47532',
        'waypoints': [
            "-34.55273, -58.46500",
            "-34.54960, -58.46746",
            "-34.54552, -58.47066",
            "-34.54170, -58.47354"
        ]
    },
    {
        'corredor': 'Cabildo',
        'segmento': 'Lacroze - Congreso',
        'sentido' : 'provincia',
        'id': 42,
        'ids':'cCabi',
        'from': '-34.56994, -58.44491',
        'to': '-34.55547, -58.46253',
        'waypoints': [
            "-34.56793, -58.44897",
            "-34.56500, -58.45416",
            "-34.56167, -58.45706",
            "-34.55842, -58.45980"
        ]
    },
    {
        'corredor': 'Cabildo',
        'segmento': 'Congreso - Lacroze',
        'sentido': 'centro',
        'id': 43,
        'ids':'cCabi',
        'from': '-34.55547, -58.46253',
        'to': '-34.56994, -58.44491',
        'waypoints': [
            "-34.55842, -58.45980",
            "-34.56167, -58.45706",
            "-34.56500, -58.45416",
            "-34.56793, -58.44897"
        ]
    },
    {
        'corredor': 'Cabildo',
        'segmento': 'Lacroze - Juan B. Justo',
        'sentido' : 'centro',
        'id': 44,
        'ids':'cCabi',
        'from': '-34.56994, -58.44491',
        'to': '-34.57818, -58.42663',
        'waypoints': [
            "-34.57288, -58.43936",
            "-34.57666, -58.43135"
        ]
    },
    {
        'corredor': 'Cabildo',
        'segmento': 'Juan B. Justo - Lacroze',
        'sentido' : 'provincia',
        'id': 45,
        'ids':'cCabi',
        'from': '-34.57818, -58.42663',
        'to': '-34.56994, -58.44491',
        'waypoints': [
            "-34.57666, -58.43135",
            "-34.57288, -58.43936"
        ]
    },
    {
        'corredor': 'Pueyrredón',
        'segmento': 'Mitre - Córdoba',
        'sentido' : 'provincia',
        'id': 46,
        'ids':'cPuey',
        'from': '-34.60888, -58.40605',
        'to': '-34.59849, -58.40376',
        'waypoints': [
            "-34.60628, -58.40595",
            "-34.60181, -58.40485"
        ]
    },
    {
        'corredor': 'Pueyrredón',
        'segmento': 'Córdoba - Mitre',
        'sentido' : 'centro',
        'id': 47,
        'ids':'cPuey',
        'from': '-34.59849, -58.40376',
        'to': '-34.60888, -58.40605',
        'waypoints': [
            "-34.60181, -58.40485",
            "-34.60628, -58.40595"
        ]
    },
    {
        'corredor': 'Libertador',
        'segmento': 'Cerrito - Sarmiento',
        'sentido' : 'provincia',
        'id': 48,
        'ids':'cLibe',
        'from': '-34.58878, -58.38193',
        'to': '-34.57547, -58.41399',
        'waypoints': [
            "-34.58560, -58.38809",
            "-34.58332, -58.39629",
            "-34.58159, -58.40307",
            "-34.57827, -58.40773"
        ]
    },
    {
        'corredor': 'Libertador',
        'segmento': 'Sarmiento - Cerrito',
        'sentido' : 'centro',
        'id': 49,
        'ids':'cLibe',
        'from': '-34.57547, -58.41399',
        'to': '-34.58878, -58.38193',
        'waypoints': [
            "-34.57827, -58.40773",
            "-34.58159, -58.40307",
            "-34.58332, -58.39629",
            "-34.58560, -58.38809"
        ]
    },
    {
        'corredor': 'Libertador',
        'segmento': 'Sarmiento - La Pampa',
        'sentido': 'provincia',
        'id': 50,
        'ids':'cLibe',
        'from': '-34.57489, -58.41509',
        'to': '-34.55943, -58.44534',
        'waypoints': [
            "-34.57312, -58.41880",
            "-34.57115, -58.42339",
            "-34.56798, -58.42918",
            "-34.56464, -58.43494",
            "-34.56279, -58.43918"
        ]
    },
    {
        'corredor': 'Libertador',
        'segmento': 'La Pampa - Sarmiento',
        'sentido': 'centro',
        'id': 51,
        'ids':'cLibe',
        'from': '-34.55943, -58.44534',
        'to': '-34.57489, -58.41509',
        'waypoints': [
            "-34.56279, -58.43918",
            "-34.56464, -58.43494",
            "-34.56798, -58.42918",
            "-34.57115, -58.42339",
            "-34.57312, -58.41880"
        ]
    },
    {
        'corredor': 'Libertador',
        'segmento': 'La Pampa - General Paz',
        'sentido' : 'provincia',
        'id': 52,
        'ids':'cLibe',
        'from': '-34.55954, -58.44530',
        'to': '-34.53584, -58.46684',
        'waypoints': [
            "-34.55614, -58.44820",
            "-34.55270, -58.45120",
            "-34.54922, -58.45448",
            "-34.54573, -58.45860",
            "-34.54147, -58.46335",
            "-34.53815, -58.46547"
        ]
    },
    {
        'corredor': 'Libertador',
        'segmento': 'General Paz - La Pampa',
        'sentido' : 'centro',
        'id': 53,
        'ids': 'cLibe',
        'from': '-34.53584, -58.46684',
        'to': '-34.55954, -58.44530',
        'waypoints': [
            "-34.53815, -58.46547",
            "-34.54147, -58.46335",
            "-34.54573, -58.45860",
            "-34.54922, -58.45448",
            "-34.55270, -58.45120",
            "-34.55614, -58.44820"
        ]
    },
    {
        'corredor': 'Alcorta',
        'segmento': 'Cerrito - Sarmiento',
        'sentido' : 'provincia',
        'id': 54,
        'ids':'cAlco',
        'from': '-34.58512, -58.38854',
        'to': '-34.57161, -58.41189',
        'waypoints': [
            "-34.58217, -58.39502",
            "-34.57917, -58.40112",
            "-34.57505, -58.40683"
        ]
    },
    {
        'corredor': 'Alcorta',
        'segmento': 'Sarmiento - Udaondo',
        'sentido' : 'provincia',
        'id': 55,
        'ids':'cAlco',
        'from': '-34.57161, -58.41189',
        'to': '-34.54629, -58.45211',
        'waypoints': [
            "-34.56864, -58.41590",
            "-34.56577, -58.41927",
            "-34.56175, -58.42421",
            "-34.55671, -58.43064",
            "-34.55291, -58.43564",
            "-34.54837, -58.44019",
            "-34.54717, -58.44661"
        ]
    },
    {
        'corredor': 'Illia',
        'segmento': '9 de julio - Sarmiento',
        'sentido': 'provincia',
        'id': 56,
        'ids':'cIlli',
        'from': '-34.59127, -58.38180',
        'to': '-34.56703, -58.40772',
        'waypoints': [
            "-34.58645, -58.38036",
            "-34.58173, -58.38285",
            "-34.57652, -58.39115",
            "-34.57305, -58.39770",
            "-34.56874, -58.40508"
        ]
    },
    {
        'corredor': 'Illia',
        'segmento': 'Sarmiento - 9 de julio',
        'sentido' : 'centro',
        'id': 57,
        'ids':'cIlli',
        'from': '-34.56736, -58.40795',
        'to': '-34.59116, -58.38207',
        'waypoints': [
            "-34.57077, -58.40235",
            "-34.57374, -58.39688",
            "-34.57735, -58.39083",
            "-34.58120, -58.38448",
            "-34.58569, -58.38029"
        ]
    }
]