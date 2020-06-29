import pyrebase

config = {
	'apiKey': "AIzaSyB5Kr4pKwoCuvVoJWdgyTuPwTWnS4j2d08",
    'authDomain': "krolchansk-fdea7.firebaseapp.com",
    'databaseURL': "https://krolchansk-fdea7.firebaseio.com",
    'projectId': "krolchansk-fdea7",
    'storageBucket': "krolchansk-fdea7.appspot.com",
    'messagingSenderId': "808335114604",
    'appId': "1:808335114604:web:b37444b60e5194da1df349"
}

firebase     = pyrebase.initialize_app(config)
fireauth     = firebase.auth()
database     = firebase.database()

id_list      = []
name_list    = []
price_list   = []
measure      = []

id_list.append('1')
name_list.append('Крольчатина парная')
price_list.append('600р/кг')
measure.append('кг')

id_list.append('2')
name_list.append('ФИЛЕ кролика')
price_list.append('1700р/кг')
measure.append('кг')

id_list.append('3')
name_list.append('ВЫРЕЗКА мяса кролика (со спинной части и с бедер задних лап)')
price_list.append('3400р/кг')
measure.append('кг')

id_list.append('4')
name_list.append('ФАРШ кролика (без лука и др.добавок)')
price_list.append('2000р/кг')
measure.append('кг')

id_list.append('5')
name_list.append('ПЕЧЕНЬ КРОЛИКА (заморозка)')
price_list.append('1700р/кг')
measure.append('кг')

id_list.append('6')
name_list.append('ПЕЛЬМЕНИ С МЯСОМ КРОЛИКА')
price_list.append('1500р/кг')
measure.append('кг')

id_list.append('7')
name_list.append('ПОЧКИ КРОЛИКА, СЕРДЦЕ (заморозка, уточняйте наличие)')
price_list.append('1700р/кг')
measure.append('кг')

id_list.append('8')
name_list.append('ЯЙЦО куринoе')
price_list.append('160р/дес')
measure.append('шт')

id_list.append('9')
name_list.append('ЯЙЦО утки')
price_list.append('50р/шт')
measure.append('шт')

id_list.append('10')
name_list.append('ЯЙЦО перепелинoe')
price_list.append('160р/2дес')
measure.append('шт')

id_list.append('11')
name_list.append('ЯЙЦО индейки')
price_list.append('100р/шт')
measure.append('шт')

id_list.append('12')
name_list.append('ПЕРЕПЕЛ тушка ~0,2кг')
price_list.append('999р/кг')
measure.append('шт')

id_list.append('13')
name_list.append('ЦЕСАРКА тушка ~1,2кг')
price_list.append('999р/кг')
measure.append('шт')

id_list.append('14')
name_list.append('кypы суповые ~0.8-1.4кг')
price_list.append('800р/кг')
measure.append('шт')

id_list.append('15')
name_list.append('кypы бройлеры ~1,4-2,5кг')
price_list.append('600р/кг')
measure.append('шт')

id_list.append('16')
name_list.append('ГУCЬ сepые ~2,2-2,7кг')
price_list.append('750р/кг')
measure.append('шт')

id_list.append('17')
name_list.append('УTKА пeкинcкая ~2кг')
price_list.append('650р/кг')
measure.append('шт')

id_list.append('18')
name_list.append('ИНДЕЙКА домашняя')
price_list.append('600р/кг')
measure.append('шт')

id_list.append('19')
name_list.append('ФИЛЕ индейки')
price_list.append('999р/кг')
measure.append('шт')

id_list.append('20')
name_list.append('БAPAHИHA ~10кг (пол туши барашка, нарублено, в коробке, ПРЕДЗАКАЗ!)')
price_list.append('650р/кг')
measure.append('шт')

id_list.append('21')
name_list.append('ТУШЕНКА кролика (стекл. банка 0,5л)')
price_list.append('450р/шт')
measure.append('шт')

id_list.append('22')
name_list.append('куры (банка)')
price_list.append('450р/шт')
measure.append('шт')

id_list.append('23')
name_list.append('тушенка перепела (добавлены специи: соль, перец, лавр.лист)')
price_list.append('700р/шт')
measure.append('шт')

id_list.append('24')
name_list.append('МАСЛО сливoчнoе фермерское 0,2кг')
price_list.append('300р/шт')
measure.append('шт')
 
id_list.append('25')
name_list.append('СЫР сливочный, головка 0.8 кг')
price_list.append('960р/шт')
measure.append('шт')

id_list.append('26')
name_list.append('творог домашний жирный 0,5кг')
price_list.append('699р/шт')
measure.append('шт')

id_list.append('27')
name_list.append('сметана жирная 0,5л')
price_list.append('499р/шт')
measure.append('шт')

id_list.append('28')
name_list.append('козье молоко')
price_list.append('250р/л')
measure.append('л')

id_list.append('29')
name_list.append('козий творог 0,5кг')
price_list.append('500р/шт')
measure.append('шт')

id_list.append('30')
name_list.append('козий сыр 0,4кг')
price_list.append('600р/шт')
measure.append('шт')

id_list.append('31')
name_list.append('шкурка кролика 1 шкура ~ 1.4кв.м')
price_list.append('800р/шт')
measure.append('шт')

for item_id, name, price, meas in zip(id_list, name_list, price_list, measure):
    database.child('prices').child(item_id).child('name').set(name)
    database.child('prices').child(item_id).child('price').set(price)
    database.child('prices').child(item_id).child('measure').set(meas)