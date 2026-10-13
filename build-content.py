from pathlib import Path
from PIL import Image
import json
root=Path(__file__).parent
(root/'assets').mkdir(exist_ok=True)
items=[]
seen=set()
def add(ko,en,page,group='hangul',kind='word',box=None,image=None):
    key=(ko,group)
    if key in seen:return
    seen.add(key)
    ident=f'item-{len(items)+1:03}'
    if box:
        im=Image.open(root/f'tmp/page-{page:03}.jpg'); w,h=im.size
        im=im.crop(tuple(int(v*(w if i%2==0 else h)) for i,v in enumerate(box)))
        im.thumbnail((550,420)); image=f'assets/{ident}.jpg'; im.save(root/image,quality=88)
    items.append(dict(id=ident,ko=ko,en=en,page=page,group=group,kind=kind,image=image))
def grid(page,rows,left,right,ys):
    for row,(words,y) in enumerate(zip(rows,ys)):
        for col,term in enumerate(words.split('|')):
            ko,en=term.split('~'); width=(right-left)/len(words.split('|'))
            add(ko,en,page,box=(left+col*width+.005,y,left+(col+1)*width-.005,y+.070))
grid(37,['나라~country|나비~butterfly|누구~who|누나~older sister (male speaker)|다리미~iron','머리~hair / head|모자~hat|바나나~banana|바지~pants|버스~bus','비누~soap|사자~lion|소리~sound|아버지~father|어디~where','어머니~mother|지도~map|하마~hippopotamus|허리~waist|호수~lake'],.153,.837,[.163,.330,.497,.665])
grid(44,['요가~yoga|요리~cooking|우유~milk|유리~glass|이야기~story','벼~rice plant|혀~tongue|겨자~mustard|교수~professor|휴가~vacation|휴지~toilet paper'],.175,.86,[.162,.325])
grid(50,['조카~niece / nephew|치마~skirt|치즈~cheese|카드~card|커피~coffee','코트~coat|쿠키~cookie|타조~ostrich|토마토~tomato|투수~pitcher','파도~wave|파리~Paris|파마~perm|포도~grapes|피자~pizza'],.176,.859,[.162,.321,.482])
grid(56,['따다~to pick|뜨다~to float|머리띠~headband|비싸다~to be expensive|뿌리~root','싸다~to be inexpensive|싸우다~to fight|쓰다~to write|아빠~dad|아저씨~middle-aged man','오빠~older brother (female speaker)|짜다~to be salty|찌다~to steam|코끼리~elephant|토끼~rabbit'],.175,.859,[.162,.321,.482])
grid(62,['개~dog|게~crab|귀~ear|뭐~what|왜~why','가게~store|과자~snack|노래~song|돼지~pig|매워요~is spicy','메뉴~menu|세계~world|세수~face washing|시계~clock|얘기~story (short form)','어깨~shoulder|예쁘다~to be pretty|웨이터~waiter|의사~doctor|의자~chair','제주도~Jeju Island|지우개~eraser|키위~kiwi|화가~painter|회사~company'],.175,.86,[.155,.292,.428,.565,.702])
# Words in the earlier letter lessons and final-consonant lessons.
for page,terms in [(31,'오~five|이~tooth|아이~child|오이~cucumber'),(36,'가구~furniture|가수~singer|거기~there|고기~meat|구두~dress shoes'),(43,'야구~baseball|야자수~palm tree|여우~fox|여자~woman|여기~here'),(49,'코~nose|기차~train|파~green onion|표~ticket|차~tea / car|고추~chili pepper|기상~weather|버터~butter|슈퍼~supermarket|우표~postage stamp'),(55,'뼈~bone|뺨~cheek|까치~magpie|꼬리~tail|도끼~axe'),(68,'수박~watermelon|약~medicine|부엌~kitchen|밖~outside|산~mountain|레몬~lemon|신문~newspaper|부산~Busan'),(69,'빗~comb|낮~daytime|꽃~flower|밑~bottom|물~water|팔~arm|딸기~strawberry|할머니~grandmother|김치~kimchi|이름~name|엄마~mom|컴퓨터~computer|집~house|밥~rice / meal|숲~forest|무릎~knee|공~ball|가방~bag|시장~market|영화~movie'),(72,'한강~Han River|남산~Namsan|자전거~bicycle|아이스크림~ice cream|강아지~puppy|사람~person'),(74,'가족~family|전화~telephone|날씨~weather|운동~exercise|생일~birthday|음식~food|버섯~mushroom|공원~park|등산~hiking|연필~pencil|선생님~teacher'),(75,'딸랑딸랑~ding ding|짹짹~chirp chirp|뻐꾸기~cuckoo|칙칙폭폭~chug chug|부릉부릉~vroom vroom|야옹~meow|꽥꽥~quack quack|멍멍~woof woof|음매~moo|개굴개굴~ribbit|꿀꿀~oink'),(76,'비빔밥~bibimbap|순대~Korean blood sausage|떡~rice cake|닭갈비~spicy stir-fried chicken|갈치구이~grilled cutlassfish')]:
    for term in terms.split('|'):
        ko,en=term.split('~'); add(ko,en,page)
# Crop illustrated rows with known geometry; replace generic images for these words.
def setgrid(page,terms,left,right,ys,height=.07):
    for row,(line,y) in enumerate(zip(terms,ys)):
        words=line.split('|')
        for col,ko in enumerate(words):
            found=next((x for x in items if x['ko']==ko),None)
            if not found:continue
            width=(right-left)/len(words); im=Image.open(root/f'tmp/page-{page:03}.jpg'); w,h=im.size
            im=im.crop((int((left+col*width+.004)*w),int(y*h),int((left+(col+1)*width-.004)*w),int((y+height)*h)))
            im.thumbnail((500,350)); image=f"assets/{found['id']}.jpg"; im.save(root/image,quality=88);found['image']=image
setgrid(31,['오|이|아이|오이'],.176,.684,[.477])
setgrid(36,['가구|가수|거기|고기|구두'],.176,.86,[.477])
setgrid(43,['야구|야자수|여우|여기|여자'],.176,.86,[.477])
setgrid(49,['코|기차|파|표|차','고추|기상|버터|슈퍼|우표'],.176,.86,[.474,.587])
setgrid(55,['뼈|뺨|까치|꼬리|도끼'],.176,.86,[.474])
setgrid(68,['수박|약|부엌|밖','산|레몬|신문|부산'],.176,.86,[.652,.804])
setgrid(69,['빗|낮|꽃|밑','물|팔|딸기|할머니','김치|이름|엄마|컴퓨터','집|밥|숲|무릎','공|가방|시장|영화'],.176,.86,[.127,.283,.440,.596,.752])
# Vocabulary sections, including all glossary additions in the four chapters.
chapters={
'1':[(84,'한국~Korea|일본~Japan|브라질~Brazil|베트남~Vietnam|미국~United States|프랑스~France|말레이시아~Malaysia|러시아~Russia|중국~China|몽골~Mongolia|나라~country'),(85,'한국 사람~Korean person|미국 사람~American person|중국 사람~Chinese person|일본 사람~Japanese person|프랑스 사람~French person|러시아 사람~Russian person|브라질 사람~Brazilian person|말레이시아 사람~Malaysian person|몽골 사람~Mongolian person|베트남 사람~Vietnamese person|사람~person'),(86,'저~I (polite)|씨~Mr. / Ms.'),(87,'어느~which'),(88,'인도~India'),(90,'선생님~teacher|학생~student|기자~reporter|의사~doctor|배우~actor / actress|대학생~university student'),(91,'회사원~office worker|가수~singer|프로그래머~programmer|요리사~chef|운동선수~athlete'),(93,'아니요~no|대학원생~graduate student|제~my (polite)|룸메이트~roommate|이름~name|뭐~what|직업~occupation')],
'2':[(100,'교실~classroom|창문~window|컴퓨터~computer|책상~desk|시계~clock|의자~chair'),(101,'가방~bag|공책~notebook|휴대폰~cell phone|책~book|지우개~eraser|볼펜~ballpoint pen|필통~pencil case|연필~pencil'),(102,'한국어~Korean language|누구~who|이거~this thing|그거~that thing (near you)|저거~that thing (over there)'),(106,'집~house|화장실~bathroom|부엌~kitchen|방~room'),(107,'침대~bed|노트북~laptop|세탁기~washing machine|냉장고~refrigerator|텔레비전~television|에어컨~air conditioner'),(108,'여기~here|서울대학교~Seoul National University|기숙사~dormitory|학교~school|옷걸이~hanger'),(113,'와이파이~Wi-Fi|아이디~ID|비밀번호~password|무료~free of charge|지하철~subway|카페~café')],
'3':[(116,'음식~food|빵~bread|샌드위치~sandwich|과일~fruit|사과~apple|딸기~strawberry|수박~watermelon|음료수~beverage|물~water|우유~milk|커피~coffee|차~tea|주스~juice'),(117,'하나~one|둘~two|셋~three|넷~four|다섯~five|여섯~six|일곱~seven|여덟~eight|아홉~nine|열~ten'),(118,'케이크~cake|초콜릿~chocolate|빙수~shaved ice dessert|녹차~green tea|아이스크림~ice cream|초콜릿빵~chocolate bread|딸기 케이크~strawberry cake|초콜릿 케이크~chocolate cake|녹차 아이스크림~green tea ice cream'),(119,'오렌지~orange|키위~kiwi|햄~ham|오렌지 주스~orange juice|딸기 주스~strawberry juice|망고 주스~mango juice|키위 주스~kiwi juice'),(122,'여기~here|저기~over there|거기~there'),(123,'앞~front|뒤~back|옆~next to|위~on / above|아래~below|밑~underneath|안~inside|밖~outside'),(124,'편의점~convenience store|카페~café|강남~Gangnam|바나나~banana|안경~eyeglasses|과일 가게~fruit store'),(130,'교통 카드~transportation card|삼각김밥~triangular gimbap|라면~instant noodles|도시락~lunch box')],
'4':[(132,'보다~to see / watch|좋아하다~to like|사다~to buy|아르바이트하다~to work part-time|전화하다~to call|먹다~to eat|만나다~to meet'),(133,'자다~to sleep|읽다~to read|일하다~to work|공부하다~to study|배우다~to learn|마시다~to drink|운동하다~to exercise'),(134,'지금~now'),(135,'하고~and / with|빵집~bakery'),(137,'숙제하다~to do homework|같이~together|요리~cooking|오늘~today'),(138,'학교~school|병원~hospital|약국~pharmacy|도서관~library|식당~restaurant|우체국~post office|영화관~movie theater'),(139,'서점~bookstore|공원~park|백화점~department store|회사~company|은행~bank|스포츠 센터~sports center|시장~market'),(140,'가다~to go|매일~every day|그리고~and / then|들~plural suffix|학생 식당~student cafeteria'),(141,'오다~to come|명동~Myeongdong|많이~a lot|영화~movie|내일~tomorrow'),(142,'혼자~alone|옷~clothes|쇼핑~shopping|그래서~so / therefore'),(145,'옛날~long ago|화가~painter|그림~painting|일상생활~everyday life')]
}
for group,pages in chapters.items():
    for page,terms in pages:
        for term in terms.split('|'):
            ko,en=term.split('~'); existing=next((x for x in items if x['ko']==ko and x['image']),None)
            add(ko,en,page,group,image=existing['image'] if existing else None)
# Course expressions: full sentences and short replies, not just dictionary headwords.
expressions={
'hangul':[(30,'나나는 자요.~Nana sleeps.|나나는 커피를 마셔요.~Nana drinks coffee.|저는 토요일에 식당에서 친구를 만나요.~I meet a friend at a restaurant on Saturday.'),(65,'누구예요?~Who is it?|거예요. 어디예요?~Where is it?|제주도예요.~It is Jeju Island.|뭐 해요?~What are you doing?|매워요.~It is spicy.|어때요?~How is it?|추워요.~It is cold.|더워요.~It is hot.|네. 그래요.~Yes, that is right.'),(77,'보세요.~Look.|읽으세요.~Read.|들으세요.~Listen.|쓰세요.~Write.|앉으세요.~Sit down.|이야기하세요.~Talk.|따라 하세요.~Repeat after me.|쉬세요.~Rest.|좋아요.~Good.|질문 있어요?~Do you have a question?|네. 있어요.~Yes, I do.|아니요. 없어요.~No, I do not.')],
'1':[(83,'안녕하세요?~Hello.|저는 이유진이에요.~I am Yujin Lee.'),(85,'저는 김민우예요.~I am Minwoo Kim.|한국 사람이에요.~I am Korean.|저는 다니엘이에요.~I am Daniel.|미국 사람이에요.~I am American.|어느 나라 사람이에요?~What country are you from?'),(86,'저는 마리예요.~I am Mari.|만나서 반가워요.~Nice to meet you.|반가워요.~Nice to meet you too.'),(87,'저는 제니예요.~I am Jenny.|저는 에릭이에요.~I am Eric.|만나서 반가워요, 에릭 씨.~Nice to meet you, Eric.|제니 씨는 어느 나라 사람이에요?~Jenny, what country are you from?|저는 미국 사람이에요.~I am American.|저는 프랑스 사람이에요.~I am French.'),(88,'저는 미국에서 왔어요.~I come from the United States.|저는 인도에서 왔어요.~I come from India.'),(90,'유진 씨는 학생이에요?~Yujin, are you a student?'),(91,'학생이에요.~I am a student.|운동선수예요.~I am an athlete.|직업이 뭐예요?~What is your occupation?'),(92,'하이 씨는 어느 나라 사람이에요?~Hai, what country are you from?|저는 대학원생이에요.~I am a graduate student.|테오 씨는 제 룸메이트예요.~Theo is my roommate.|테오 씨는 미국 사람이 아니에요.~Theo is not American.|브라질 사람이에요.~He is Brazilian.|대학생이에요.~He is a university student.'),(93,'저는 나나예요.~I am Nana.|이름이 뭐예요?~What is your name?|나나 씨는요?~And you, Nana?|저는 중국에서 왔어요.~I come from China.'),(94,'저는 중국 사람이에요.~I am Chinese.|저는 학생이에요.~I am a student.'),(96,'아니요. 저는 중국 사람이에요.~No, I am Chinese.|아니요. 저는 회사원이에요.~No, I am an office worker.|아니요. 저는 선생님이에요.~No, I am a teacher.|저는 한국 사람이 아니에요.~I am not Korean.'),(97,'여러분 나라에서는 어떻게 인사해요?~How do people greet each other in your country?|안나 씨는 어느 나라 사람이에요?~Anna, what country are you from?|저는 독일 사람이에요.~I am German.|나나 씨는 회사원이에요?~Nana, are you an office worker?|아니요. 선생님이에요.~No, I am a teacher.')],
'2':[(100,'이거는 시계예요.~This is a clock.'),(101,'이거는 뭐예요?~What is this?'),(102,'한국어 책이에요.~It is a Korean book.|이거는 제니 씨의 가방이에요?~Is this Jenny’s bag?|네. 제 가방이에요.~Yes, it is my bag.|저거는 누구의 책이에요?~Whose book is that over there?|줄리앙 씨의 책이에요.~It is Julien’s book.'),(103,'이거는 누구의 공책이에요?~Whose notebook is this?|제 공책이에요.~It is my notebook.|이거는 나나 씨의 볼펜이에요?~Is this Nana’s pen?|아니요. 제 볼펜이 아니에요.~No, it is not my pen.|선생님, 그거는 제 볼펜이에요.~Teacher, that is my pen.'),(104,'이거는 누구의 책이에요?~Whose book is this?|이거는 한국어 책이에요?~Is this a Korean book?'),(105,'여기는 교실이에요.~This is a classroom.|책상하고 의자가 있어요.~There are desks and chairs.|시계하고 컴퓨터가 있어요.~There are a clock and a computer.'),(106,'이 가방은 나나 씨 가방이에요.~This bag is Nana’s bag.'),(107,'방에 뭐가 있어요?~What is in the room?'),(108,'여기는 서울대학교 기숙사예요.~This is a Seoul National University dormitory.|제 방이에요.~It is my room.|책상하고 의자가 있어요.~There are a desk and a chair.|침대도 있어요.~There is a bed too.|옷걸이가 있어요.~There is a hanger.|냉장고가 있어요.~There is a refrigerator.|텔레비전은 없어요.~There is no television.'),(109,'이거는 제 가방이에요.~This is my bag.|한국어 책, 공책, 필통이 있어요.~There are a Korean book, a notebook and a pencil case.|이 지우개는 제 지우개가 아니에요.~This eraser is not mine.|볼펜이 있어요?~Do you have a pen?|네. 있어요.~Yes, I do.|아니요. 볼펜이 없어요.~No, I do not have a pen.|연필이 있어요.~I have a pencil.|누구의 볼펜이에요?~Whose pen is it?|친구의 볼펜이에요.~It is a friend’s pen.'),(110,'제 방에 침대하고 책상이 있어요.~There are a bed and a desk in my room.|책하고 공책도 있어요.~There are books and notebooks too.'),(112,'지우개가 있어요?~Do you have an eraser?|아니요. 없어요.~No, I do not.|제 지우개가 아니에요.~It is not my eraser.'),(113,'와이파이 비밀번호가 뭐예요?~What is the Wi-Fi password?|와이파이 아이디가 뭐예요?~What is the Wi-Fi ID?|이 필통은 에릭 씨의 필통이에요?~Is this pencil case Eric’s?|네. 제 필통이에요.~Yes, it is my pencil case.|나나 씨의 책이에요.~It is Nana’s book.|그 책은 누구 책이에요?~Whose book is that?')],
'3':[(116,'이 빵 하나 주세요.~Please give me one of these breads.'),(117,'과일 가게에 뭐가 있어요?~What is in the fruit store?'),(118,'어서 오세요.~Welcome.|케이크가 있어요?~Do you have cake?|딸기 케이크하고 초콜릿 케이크가 있어요.~There are strawberry and chocolate cakes.|초콜릿빵이에요.~It is chocolate bread.|네. 여기 있어요.~Yes, here you are.'),(119,'주스가 있어요?~Do you have juice?|오렌지 주스하고 딸기 주스가 있어요.~There are orange and strawberry juices.|그럼 오렌지 주스 주세요.~Then please give me orange juice.|여기 있어요.~Here you are.'),(120,'뭐가 있어요?~What is there?|뭐를 좋아해요?~What do you like?'),(121,'이거는 주스예요?~Is this juice?|아니요. 우유예요.~No, it is milk.|사과하고 바나나가 있어요.~There are apples and bananas.'),(122,'집 앞에 편의점이 있어요.~There is a convenience store in front of the house.'),(123,'교실 안에 뭐가 있어요?~What is inside the classroom?|휴대폰이 어디에 있어요?~Where is the cell phone?'),(124,'집이 어디에 있어요?~Where is the house?|여기는 카페예요.~This is a café.|이 카페는 강남에 있어요.~This café is in Gangnam.|여기에 딸기 케이크하고 커피가 있어요.~There are strawberry cake and coffee here.|이 카페 옆에 과일 가게가 있어요.~There is a fruit store next to this café.|과일 가게에는 사과하고 바나나하고 오렌지가 있어요.~There are apples, bananas and oranges in the fruit store.|과일 가게가 어디에 있어요?~Where is the fruit store?'),(125,'지금 교실에 있어요?~Are you in the classroom now?|교실에 제 안경이 있어요?~Are my glasses in the classroom?|책상 위에 있어요.~They are on the desk.|침대하고 책상하고 의자가 있어요.~There are a bed, a desk and a chair.|책상이 어디에 있어요?~Where is the desk?|침대 옆에 있어요.~It is next to the bed.|책상 위에 뭐가 있어요?~What is on the desk?|공책이 있어요.~There is a notebook.'),(126,'빵집 옆에 카페가 있어요.~There is a café next to the bakery.|빵집 앞에 과일 가게가 있어요.~There is a fruit store in front of the bakery.'),(127,'지우개가 어디에 있어요?~Where is the eraser?|물 옆에 있어요.~It is next to the water.'),(128,'여기는 어디예요?~Where is this?|우리 집이에요.~It is our house.|안경이 어디에 있어요?~Where are the glasses?|방에 없어요.~They are not in the room.|가방에 없어요.~They are not in the bag.'),(130,'편의점에 뭐가 있어요?~What is in the convenience store?|이 초콜릿은 어디에 있어요?~Where is this chocolate?|안경이 집에 있어요?~Are the glasses at home?|아니요. 안경은 가방 안에 있어요.~No, the glasses are inside the bag.')],
'4':[(132,'저는 한국어를 공부해요.~I study Korean.'),(134,'제니 씨는 지금 뭐 해요?~Jenny, what are you doing now?|공부해요.~I am studying.|테오 씨는 뭐 해요?~What is Theo doing?|테오 씨는 커피를 마셔요.~Theo is drinking coffee.|다니엘 씨, 지금 어디에 있어요?~Daniel, where are you now?|집에 있어요.~I am at home.|뭐 해요?~What are you doing?|잘 자요.~I sleep well.'),(135,'에릭 씨, 지금 집에 있어요?~Eric, are you at home now?|아니요. 저는 카페에 있어요.~No, I am in a café.|친구를 만나요?~Are you meeting a friend?|네. 친구하고 커피를 마셔요.~Yes, I am drinking coffee with a friend.|안나 씨는 뭐 해요?~Anna, what are you doing?|저는 집에 있어요.~I am at home.|책을 읽어요.~I am reading a book.'),(136,'오늘 뭐 해요?~What are you doing today?|여기에서 뭐를 사요?~What do you buy here?'),(137,'학교에서 뭐 해요?~What do you do at school?|매일 뭐 해요?~What do you do every day?|숙제해요.~I do homework.'),(138,'오늘 회사에 가요.~I am going to work today.'),(139,'도서관에서 뭐 해요?~What do you do in the library?|오늘 어디에 가요?~Where are you going today?'),(140,'학교에 가요.~I go to school.|시장에 가요.~I go to the market.|병원에 가요.~I go to the hospital.|배가 아파요.~My stomach hurts.|사과를 사요.~I buy apples.|한국어를 배워요.~I learn Korean.|저는 서울대학교에서 한국어를 배워요.~I learn Korean at Seoul National University.|매일 학교에 가요.~I go to school every day.|그리고 우리 반 친구들하고 같이 학생 식당에 가요.~Then I go to the student cafeteria with my classmates.|거기에서 밥을 먹어요.~I eat there.|학생 식당 옆에는 도서관이 있어요.~There is a library next to the student cafeteria.|우리는 도서관에서 숙제해요.~We do homework in the library.'),(141,'오늘 친구가 우리 집에 와요.~A friend comes to our house today.|저는 친구하고 같이 명동에 가요.~I go to Myeongdong with a friend.|명동에는 식당이 많이 있어요.~There are many restaurants in Myeongdong.|우리는 식당에서 한국 음식을 먹어요.~We eat Korean food in a restaurant.|그리고 영화관에 가요.~Then we go to the movie theater.|영화관은 식당 옆에 있어요.~The movie theater is next to the restaurant.|우리는 영화관에서 영화를 봐요.~We watch a movie at the theater.|내일 어디에 가요?~Where are you going tomorrow?|거기에서 뭐 해요?~What do you do there?'),(142,'저는 오늘 혼자 강남에 가요.~Today I go to Gangnam alone.|강남에 가게가 많이 있어요.~There are many stores in Gangnam.|저는 쇼핑을 좋아해요.~I like shopping.|그래서 강남에서 옷하고 가방을 사요.~So I buy clothes and bags in Gangnam.|가게 옆에는 식당이 있어요.~There is a restaurant next to the store.|거기에서 한국 음식을 먹어요.~I eat Korean food there.|그리고 집에 와요.~Then I come home.|누구하고 가요?~Who do you go with?'),(143,'여기에서 한국어를 배워요.~I learn Korean here.|선생님하고 학생이 있어요.~There are a teacher and students.|여기는 도서관이에요.~This is a library.|도서관에서 공부해요.~I study in the library.|도서관에서 책을 읽어요.~I read books in the library.'),(144,'학교에서 공부해요.~I study at school.'),(145,'한국의 화가 김홍도의 그림이에요.~This is a painting by the Korean painter Kim Hongdo.|여기는 옛날 학교예요.~This is a school from long ago.|여기는 옛날 식당이에요.~This is a restaurant from long ago.|누가 있어요?~Who is there?|여기에서 뭐 해요?~What do you do here?|오늘 도서관에서 공부해요?~Are you studying in the library today?|아니요. 집에서 공부해요.~No, I study at home.|서점에서 책을 사요.~I buy books in the bookstore.')]
}
for group,pages in expressions.items():
    for page,terms in pages:
        for term in terms.split('|'):
            ko,en=term.split('~');add(ko,en,page,group,'phrase')
# Full alphabet, letter names and syllable examples; all 40 modern letters.
consonants='ㄱ ㄲ ㄴ ㄷ ㄸ ㄹ ㅁ ㅂ ㅃ ㅅ ㅆ ㅇ ㅈ ㅉ ㅊ ㅋ ㅌ ㅍ ㅎ'.split()
names='기역 쌍기역 니은 디귿 쌍디귿 리을 미음 비읍 쌍비읍 시옷 쌍시옷 이응 지읒 쌍지읒 치읓 키읔 티읕 피읖 히읗'.split()
for ko,name in zip(consonants,names):add(ko,name+' · consonant',28,'hangul','letter')
vowels='ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅘ ㅙ ㅚ ㅛ ㅜ ㅝ ㅞ ㅟ ㅠ ㅡ ㅢ ㅣ'.split()
sounds='a ae ya yae eo e yeo ye o wa wae oe yo u wo we wi yu eu ui i'.split()
for ko,sound in zip(vowels,sounds):add(ko,sound+' · vowel',28,'hangul','letter')
for ko,name in zip(names,names):add(ko,'Letter name: '+name,28,'hangul','letter-name')
# Additional illustrative nouns and final consonant examples shown in reading practice.
for term in '국~soup|눈~snow / eye|곧~soon|밭~field|옷~clothes|있다~to exist|서울~Seoul|봄~spring|입~mouth|앞~front|강~river|시청~city hall|구름~cloud|연~kite|남자~man|동산~hill|세배~New Year bow|야채~vegetables|카메라~camera|스웨터~sweater|재미~fun'.split('|'):
    ko,en=term.split('~');add(ko,en,68)
# Illustration-only crops for scenes; prompts supply a precise meaning for ambiguous images.
scenes={
'hangul':(72,(.2,.18,.85,.83)), '1':(90,(.17,.16,.82,.75)), '2':(107,(.19,.19,.84,.77)), '3':(116,(.15,.25,.85,.71)), '4':(132,(.17,.19,.85,.70))}
for group,(page,box) in scenes.items():
    im=Image.open(root/f'tmp/page-{page:03}.jpg');w,h=im.size;im=im.crop(tuple(int(v*(w if i%2==0 else h)) for i,v in enumerate(box)));im.thumbnail((600,500));im.save(root/f'assets/scene-{group}.jpg',quality=88)
# Reuse exact book photography wherever a headword appears in several chapters.
for item in items:
    if not item['image']:
        counterpart=next((x for x in items if x['ko']==item['ko'] and x['image']),None)
        item['image']=counterpart['image'] if counterpart else f"assets/scene-{item['group']}.jpg"
        item['contextImage']=counterpart is None
    else:item['contextImage']=False
# Correct a stray OCR fragment manually rather than publishing it.
items=[x for x in items if x['ko']!='거예요. 어디예요?']
add('어디예요?','Where is it?',65,'hangul','phrase',image='assets/scene-hangul.jpg')
items[-1]['contextImage']=True
(root/'content.js').write_text('window.COURSE = '+json.dumps({'title':'서울대 한국어+ 1A','scope':'PDF pages 1–145 · Hangul + units 1–4','items':items,'consonants':consonants,'vowels':vowels,'names':names},ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print('items',len(items),'photos',len(list((root/'assets').glob('*.jpg'))))
# Additional glossary entries and complete writing / task examples.
for group,page,terms in [
('1',89,'친구~friend / classmate|호주~Australia|태국~Thailand|호주 사람~Australian person|태국 사람~Thai person|우리~our / we|반~class|국적~nationality'),('1',94,'메일~email|주소~address|여러분~everyone|메일 주소~email address|독일~Germany|독일 사람~German person'),
('2',105,'그럼~then'),('2',110,'우리~our|저기~over there|그리고~and'),('3',120,'가게~store|망고~mango'),('3',121,'어디~where|문구점~stationery store'),('3',128,'콜라~cola'),('3',129,'우산~umbrella|쓰레기봉투~garbage bag'),('4',140,'우리~we / our|반~class|친구~friend')]:
 for t in terms.split('|'):
  ko,en=t.split('~');add(ko,en,page,group)
for group,page,terms in [
('1',89,'안나 씨예요.~It is Anna.|러시아 사람이에요.~She is Russian.|크리스 씨예요.~It is Chris.|크리스 씨는 호주 사람이에요.~Chris is Australian.|우리 반 친구는 어느 나라 사람이에요?~Where are our classmates from?'),
('1',92,'저는 베트남 사람이에요.~I am Vietnamese.|하이 씨는 학생이에요?~Hai, are you a student?|아니요. 회사원이에요.~No, I am an office worker.'),
('1',94,'한국 사람이에요?~Are you Korean?|학생이에요?~Are you a student?|메일 주소가 뭐예요?~What is your email address?|여러분, 안녕하세요?~Hello, everyone.|저는 크리스예요.~I am Chris.|호주 사람이에요.~I am Australian.|요리사예요.~I am a chef.|제 메일 주소는 lovegimbap@snulei.com이에요.~My email address is lovegimbap@snulei.com.'),
('1',96,'저는 테오예요.~I am Theo.|저는 호주 사람이에요.~I am Australian.|저는 브라질 사람이에요.~I am Brazilian.|크리스 씨는 학생이에요?~Chris, are you a student?|아니요. 학생이 아니에요.~No, I am not a student.|테오 씨는 학생이에요?~Theo, are you a student?|네. 저는 학생이에요.~Yes, I am a student.'),
('2',105,'이거는 누구의 물건이에요?~Whose item is this?|이거는 책상이에요.~This is a desk.'),
('2',108,'여기는 제 방이에요.~This is my room.|책상, 의자, 옷걸이가 있어요.~There are a desk, a chair and a hanger.|여기는 부엌이에요.~This is a kitchen.|여기는 화장실이에요.~This is a bathroom.'),
('2',110,'제 방이에요.~It is my room.|침대가 있어요.~There is a bed.|여기는 우리 집이에요.~This is our house.|이 방은 제 방이에요.~This room is my room.|침대, 책상, 의자, 컴퓨터가 있어요.~There are a bed, a desk, a chair and a computer.|그리고 저기는 부엌이에요.~And that over there is the kitchen.|냉장고가 있어요.~There is a refrigerator.'),
('3',120,'저기요.~Excuse me (over there).|여기요.~Excuse me (over here).|딸기 주스가 있어요?~Do you have strawberry juice?|딸기 주스 하나 주세요.~Please give me one strawberry juice.'),
('3',121,'문구점에 뭐가 있어요?~What is in the stationery store?'),
('3',126,'과일 가게에 자주 가요.~I often go to the fruit store.|사과하고 바나나가 있어요.~There are apples and bananas.|토마토하고 딸기가 있어요.~There are tomatoes and strawberries.|우리 집 옆에 과일 가게가 있어요.~There is a fruit store next to our house.|이 가게에 사과하고 수박하고 딸기가 있어요.~There are apples, watermelons and strawberries in this store.'),
('3',128,'어디에 있어요?~Where is it?|볼펜 옆에 있어요.~It is next to the pen.|연필이 있어요?~Do you have a pencil?|그럼 콜라가 있어요?~Then do you have cola?|네. 저기 냉장고 안에 있어요.~Yes, it is inside the refrigerator over there.|지우개하고 콜라 주세요.~Please give me an eraser and cola.'),
('3',130,'사과가 어디에 있어요?~Where are the apples?|저기에 있어요.~They are over there.|집 옆에 가게가 있어요?~Is there a store next to the house?|방에 컴퓨터가 있어요?~Is there a computer in the room?|가방 안에 뭐가 있어요?~What is inside the bag?'),
('4',134,'자요.~I sleep.'),('4',136,'여자는 지금 사과를 사요.~The woman is buying apples now.|남자는 지금 집에 없어요.~The man is not at home now.'),('4',137,'남자는 학교에 있어요.~The man is at school.|여자는 지금 숙제해요.~The woman is doing homework now.|여자는 친구의 집에 있어요.~The woman is at a friend’s house.')]:
 for t in terms.split('|'):
  ko,en=t.split('~');add(ko,en,page,group,'phrase')
# Give chapter vocabulary its own clean illustration, without printed answers.
def crop_for(ko,page,box):
 im=Image.open(root/f'tmp/page-{page:03}.jpg');w,h=im.size
 im=im.crop(tuple(int(v*(w if i%2==0 else h)) for i,v in enumerate(box)));im.thumbnail((500,400))
 path=f'assets/photo-{page}-{ko.encode().hex()}.jpg';im.save(root/path,quality=90)
 for x in items:
  if x['ko']==ko:x['image']=path;x['contextImage']=False
for ko,box in [('선생님',(.156,.147,.307,.428)),('학생',(.308,.215,.419,.416)),('기자',(.479,.187,.596,.470)),('의사',(.718,.151,.837,.426)),('배우',(.216,.525,.471,.797)),('대학생',(.596,.511,.828,.792))]:crop_for(ko,90,box)
for ko,box in [('보다',(.116,.315,.329,.482)),('좋아하다',(.337,.320,.480,.483)),('사다',(.662,.320,.811,.448)),('아르바이트하다',(.275,.525,.448,.602)),('전화하다',(.365,.556,.474,.704)),('먹다',(.576,.583,.698,.705)),('만나다',(.708,.495,.880,.648))]:crop_for(ko,132,box)
for ko,box in [('읽다',(.300,.233,.433,.460)),('일하다',(.497,.205,.617,.451)),('마시다',(.628,.208,.746,.427)),('공부하다',(.816,.215,.905,.459)),('배우다',(.127,.554,.311,.641)),('운동하다',(.693,.551,.889,.710))]:crop_for(ko,133,box)
# Clean common scene backgrounds; sentence cues disambiguate who / what / where.
for group,page,box in [('hangul',72,(.195,.25,.845,.82)),('1',90,(.16,.15,.30,.42)),('2',107,(.24,.30,.50,.48)),('3',116,(.53,.35,.74,.61)),('4',133,(.30,.235,.43,.455))]:
 im=Image.open(root/f'tmp/page-{page:03}.jpg');w,h=im.size;im=im.crop(tuple(int(v*(w if i%2==0 else h)) for i,v in enumerate(box)));im.thumbnail((600,500));im.save(root/f'assets/scene-{group}.jpg',quality=90)
# Country flags are shown as country cues; Hangul must still be recalled.
flags={'한국':'🇰🇷','일본':'🇯🇵','미국':'🇺🇸','중국':'🇨🇳','프랑스':'🇫🇷','러시아':'🇷🇺','몽골':'🇲🇳','베트남':'🇻🇳','브라질':'🇧🇷','말레이시아':'🇲🇾','호주':'🇦🇺','태국':'🇹🇭','인도':'🇮🇳','독일':'🇩🇪'}
roman_names='giyeok ssanggiyeok nieun digeut ssangdigeut rieul mieum bieup ssangbieup siot ssangsiot ieung jieut ssangjieut chieut kieuk tieut pieup hieut'.split()
for x in items:
 if x['kind']=='letter':
  if x['ko'] in consonants:x['en']=roman_names[consonants.index(x['ko'])]+' · consonant';x['speak']=names[consonants.index(x['ko'])]
  else:x['speak']=chr(0xac00+vowels.index(x['ko'])*28)
 if x['kind']=='letter-name':x['en']='Letter name: '+roman_names[names.index(x['ko'])]
 country=x['ko'].replace(' 사람','')
 if country in flags:x['flag']=flags[country]
 if not x.get('image'):
  same=next((a for a in items if a['ko']==x['ko'] and a.get('image') and not a.get('contextImage')),None)
  x['image']=same['image'] if same else f"assets/scene-{x['group']}.jpg";x['contextImage']=same is None
# No OCR output is imported into the released bank: Korean entries are explicitly transcribed.
(root/'content.js').write_text('window.COURSE = '+json.dumps({'title':'서울대 한국어+ 1A','scope':'PDF pages 1–145 · Hangul + units 1–4','items':items,'consonants':consonants,'vowels':vowels,'names':names},ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print('final items',len(items))
# Correct crop positions after visual inspection of the scanned page layout.
setgrid(31,['오|이|아이|오이'],.154,.839,[.824])
setgrid(36,['가구|가수|거기|고기|구두'],.176,.860,[.717])
setgrid(43,['야구|야자수|여우|여기|여자'],.176,.860,[.717])
setgrid(44,['요가|요리|우유|유리|이야기','벼|혀|겨자|교수|휴가|휴지'],.176,.859,[.203,.371])
setgrid(49,['코|키|파|표|차','고추|기차|버터|슈퍼|우표'],.154,.837,[.673,.835])
setgrid(55,['뼈|가짜|까치|꼬리|도끼'],.154,.837,[.807])
setgrid(62,['개|게|귀|뭐|왜','가게|과자|노래|돼지|매워요','메뉴|세계|세수|시계|얘기','어깨|예쁘다|웨이터|의사|의자','제주도|지우개|키위|화가|회사'],.176,.86,[.206,.362,.518,.673,.829])
setgrid(68,['수박|약|부엌|밖','산|레몬|신문|부산'],.313,.86,[.695,.837],.063)
setgrid(69,['빗|낮|꽃|밑','물|팔|딸기|할머니','김치|이름|엄마|컴퓨터','집|밥|숲|무릎','공|가방|시장|영화'],.286,.837,[.147,.290,.433,.576,.718],.065)
items=[x for x in items if x['ko'] not in ['기상','뺨','잘 자요.']]
for term,page in [('키~height',49),('가짜~fake',55),('도로~road',39),('두부~tofu',39),('하나~one',39),('도시~city',41),('나무~tree',42),('고구마~sweet potato',42),('고모~aunt (father’s sister)',53),('수시~frequently',53),('기차표~train ticket',54),('아래~below',67),('세배~New Year bow',67),('야채~vegetables',67)]:
 ko,en=term.split('~');add(ko,en,page)
setgrid(49,['코|키|파|표|차','고추|기차|버터|슈퍼|우표'],.154,.837,[.673,.835])
setgrid(55,['뼈|가짜|까치|꼬리|도끼'],.154,.837,[.807])
# Use actual cropped labels-free photograph for the added Hangul vocabulary.
setgrid(42,['고기|나라|나무|라디오','모자|바지|사자|다리미','소리|지도|호수|고구마'],.154,.838,[.165,.409,.649],.065)
# Fill any added items and synchronize shared word photos after corrected crops.
for x in items:
 if x['kind']=='word':
  same=next((a for a in items if a['ko']==x['ko'] and a.get('image') and not a.get('contextImage')),None)
  if same:x['image']=same['image'];x['contextImage']=False
 if not x.get('image'):x['image']=f"assets/scene-{x['group']}.jpg";x['contextImage']=True
# IDs stay unique after deletions / additions.
for i,x in enumerate(items):x['id']=f'k{i+1:04}'
(root/'content.js').write_text('window.COURSE = '+json.dumps({'title':'서울대 한국어+ 1A','scope':'PDF pages 1–145 · Hangul + units 1–4','items':items,'consonants':consonants,'vowels':vowels,'names':names},ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print('release items',len(items))
# Final visual QA adjustments and dedicated pictures for the chapter vocabulary.
for ko,page,box in [
('야구',43,(.156,.783,.282,.853)),('야자수',43,(.292,.783,.419,.853)),('여우',43,(.429,.783,.558,.853)),('여기',43,(.566,.783,.693,.853)),('여자',43,(.703,.783,.832,.853)),
('나무',42,(.494,.139,.621,.201)),('고구마',42,(.658,.65,.856,.713)),('나라',37,(.156,.163,.280,.233)),('다리미',37,(.706,.163,.831,.233)),('모자',37,(.294,.330,.419,.400)),('바지',37,(.570,.330,.693,.400)),('사자',37,(.294,.497,.419,.567)),('지도',37,(.294,.665,.419,.735)),('고기',36,(.588,.717,.716,.787)),
('교실',99,(.177,.192,.860,.466)),('창문',100,(.12,.357,.234,.441)),('책상',100,(.197,.508,.364,.677)),('공책',101,(.32,.362,.545,.447)),('휴대폰',101,(.545,.367,.703,.468)),('책',101,(.402,.556,.514,.599)),('볼펜',101,(.422,.411,.476,.480)),('필통',101,(.483,.489,.653,.556)),
('침대',107,(.425,.435,.650,.500)),('노트북',107,(.680,.277,.737,.305)),('세탁기',107,(.341,.560,.404,.600)),('냉장고',107,(.404,.506,.455,.624)),('텔레비전',107,(.575,.534,.685,.585)),('에어컨',107,(.727,.510,.761,.600)),
('샌드위치',116,(.365,.601,.450,.638)),('빵',116,(.195,.516,.254,.539)),('사과',116,(.695,.512,.786,.550)),
('하나',117,(.200,.178,.286,.278)),('둘',117,(.398,.179,.565,.278)),('셋',117,(.629,.179,.889,.278)),('넷',117,(.182,.360,.295,.440)),('다섯',117,(.385,.360,.564,.440)),('여섯',117,(.655,.361,.866,.440)),('일곱',117,(.153,.526,.320,.592)),('여덟',117,(.390,.526,.585,.592)),('아홉',117,(.145,.695,.344,.759)),('열',117,(.385,.695,.615,.759)),
('앞',123,(.163,.220,.306,.380)),('뒤',123,(.451,.220,.632,.380)),('옆',123,(.732,.224,.905,.380)),('위',123,(.175,.447,.308,.590)),('아래',123,(.451,.440,.588,.590)),('안',123,(.413,.656,.630,.759)),('밖',123,(.648,.658,.907,.759)),
('학교',138,(.180,.250,.323,.337)),('병원',138,(.350,.327,.507,.420)),('약국',138,(.573,.341,.725,.445)),('도서관',138,(.740,.235,.905,.339)),('식당',138,(.111,.586,.296,.663)),('우체국',138,(.291,.479,.482,.572)),('영화관',138,(.594,.528,.755,.626)),
('서점',139,(.144,.305,.297,.417)),('공원',139,(.536,.280,.710,.395)),('백화점',139,(.094,.493,.313,.585)),('은행',139,(.187,.633,.325,.725)),('스포츠 센터',139,(.359,.577,.595,.673))]:crop_for(ko,page,box)
for term,page in [('라디오~radio',42),('지하~basement',42),('두유~soy milk',52),('치아~tooth',51),('동네~neighborhood',126),('자주~often',126),('물건~item',105)]:
 ko,en=term.split('~');add(ko,en,page)
crop_for('라디오',42,(.658,.138,.856,.201));crop_for('지하',42,(.339,.650,.482,.713))
# Phrases use the most relevant noun / action illustration and an exact meaning cue.
for x in items:
 if x['kind']=='phrase':
  candidates=[a for a in items if a['kind']=='word' and len(a['ko'])>1 and a['ko'] in x['ko'] and a.get('image') and not a.get('contextImage')]
  if not candidates:
   verbs={'공부해':'공부하다','마셔':'마시다','먹':'먹다','읽':'읽다','만나':'만나다','배워':'배우다','자요':'자다','좋아해':'좋아하다','전화해':'전화하다','운동해':'운동하다'}
   candidates=[a for a in items if a['ko'] in [v for k,v in verbs.items() if k in x['ko']] and a.get('image') and not a.get('contextImage')]
  if candidates:x['image']=max(candidates,key=lambda a:len(a['ko']))['image'];x['contextImage']=True
 if not x.get('image'):x['image']=f"assets/scene-{x['group']}.jpg";x['contextImage']=True
for i,x in enumerate(items):x['id']=f'k{i+1:04}'
(root/'content.js').write_text('window.COURSE = '+json.dumps({'title':'서울대 한국어+ 1A','scope':'PDF pages 1–145 · Hangul + units 1–4','items':items,'consonants':consonants,'vowels':vowels,'names':names},ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print('final release',len(items))
# Minimal-pair distractors and the complete final-consonant sorting list also belong to the syllabus.
for page,terms in [
(39,'모기~mosquito|수도~capital city / water supply|고리~ring / loop|거리~street / distance'),
(40,'다리~leg / bridge|해마~seahorse'),(45,'여유~leisure / composure'),(51,'기사~news article / driver|코드~code|파티~party'),
(57,'사다~to buy|지다~to lose|바르다~to apply / to be correct|빠르다~to be fast|트다~to open / to crack|부리~beak'),
(64,'애기~baby (colloquial)|어제~yesterday|취미~hobby|세기~century / strength|호의~goodwill|회의~meeting'),
(71,'곰~bear|골~goal / valley|살~flesh / age counter|삼~three (Sino-Korean)|암~cancer|앗~oh!|점~point / shop|절~temple / bow|적~enemy|한~one / Korean prefix|학~crane|함~box|청소~cleaning|사진~photograph|불고기~bulgogi|곧~soon|곱~times / fold|짐~luggage|부엉~owl hoot|걷다~to walk|검다~to be black|신장~kidney / height|사직~resignation'),
(72,'아차산~Achasan mountain|건물~building'),
(73,'손~hand|컵~cup|형~older brother (male speaker)|맛~taste|곰~bear|답~answer|높다~to be high|언니~older sister (female speaker)|축구~soccer|시험~exam|여행~travel|계절~season|가을~autumn|마음~heart / mind|농구~basketball|고향~hometown|숙제~homework|부모님~parents|기숙사~dormitory|지하철~subway'),
(76,'강릉~Gangneung|서울~Seoul|전주~Jeonju|대구~Daegu|부산~Busan|제주~Jeju')]:
 for t in terms.split('|'):
  ko,en=t.split('~');add(ko,en,page)
for x in items:
 if not x.get('image'):x['image']='assets/scene-hangul.jpg';x['contextImage']=True
for i,x in enumerate(items):x['id']=f'k{i+1:04}'
(root/'content.js').write_text('window.COURSE = '+json.dumps({'title':'서울대 한국어+ 1A','scope':'PDF pages 1–145 · Hangul + units 1–4','items':items,'consonants':consonants,'vowels':vowels,'names':names},ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
coverage={g:{'items':len([x for x in items if x['group']==g]),'words':len([x for x in items if x['group']==g and x['kind']=='word']),'phrases':len([x for x in items if x['group']==g and x['kind']=='phrase']),'pages':sorted(set(x['page'] for x in items if x['group']==g))} for g in ['hangul','1','2','3','4']}
(root/'coverage.json').write_text(json.dumps(coverage,indent=2),encoding='utf-8')
print('Audited bank:',len(items),'entries;',len(set(x['ko'] for x in items if x['kind']=='word')),'unique words;',len(set(x['ko'] for x in items if x['kind']=='phrase')),'unique expressions')
# Complete alphabet reading phrases, greetings and remaining minimal pairs.
items=[x for x in items if x['ko'] not in ['고모','수시'] and not (x['page']==65 and x['ko'] in ['누구예요?','매워요.','더워요.','네. 그래요.'])]
for page,terms,kind in [
(45,'유자~citron|겨우~barely','word'),(51,'피~blood|자~ruler|수표~check (payment)|우비~raincoat|코피~nosebleed|보리~barley|보도~news report / sidewalk','word'),
(65,'누구세요?~Who is it? (polite)|저예요.~It is me.|쉬어요.~I am resting.|또 봐요.~See you again.|네. 고마워요.~Yes, thank you.','phrase'),
(66,'가위~scissors|소개~introduction|모레~the day after tomorrow|채소~vegetables|교외~suburbs|아내~wife|서예~calligraphy','word'),
(66,'쉬워요.~It is easy.','phrase'),(78,'안녕하세요?~Hello.|만나서 반가워요.~Nice to meet you.|반가워요.~Nice to meet you too.|안녕히 가세요.~Goodbye (to someone leaving).|안녕히 계세요.~Goodbye (to someone staying).|감사합니다.~Thank you.|죄송합니다.~I am sorry.','phrase')]:
 for term in terms.split('|'):
  ko,en=term.split('~');add(ko,en,page,'hangul',kind)
# Syllables from the actual writing tables (not vocabulary from later units).
lroman=['g','kk','n','d','tt','r','m','b','pp','s','ss','','j','jj','ch','k','t','p','h']
for page,letters,vs in [(32,['ㅇ'],['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ']),(38,list('ㄱㄴㄷㄹㅁㅂㅅㅈㅎ'),['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ']),(44,['ㅇ'],['ㅑ','ㅕ','ㅛ','ㅠ']),(50,list('ㅋㅌㅍㅊ'),['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ']),(56,list('ㄲㄸㅃㅆㅉ'),['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ']),(63,['ㅇ'],['ㅐ','ㅒ','ㅔ','ㅖ','ㅘ','ㅙ','ㅚ','ㅝ','ㅞ','ㅟ','ㅢ'])]:
 for l in letters:
  for v in vs:
   li=consonants.index(l);vi=vowels.index(v);ko=chr(0xac00+(li*21+vi)*28)
   add(ko,lroman[li]+sounds[vi]+' · syllable',page,'hangul','syllable')
for x in items:
 if not x.get('image'):x['image']=f"assets/scene-{x['group']}.jpg";x['contextImage']=True
for i,x in enumerate(items):x['id']=f'k{i+1:04}'
(root/'content.js').write_text('window.COURSE = '+json.dumps({'title':'서울대 한국어+ 1A','scope':'PDF pages 1–145 · Hangul + units 1–4','items':items,'consonants':consonants,'vowels':vowels,'names':names},ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
coverage={g:{'items':len([x for x in items if x['group']==g]),'words':len([x for x in items if x['group']==g and x['kind']=='word']),'phrases':len([x for x in items if x['group']==g and x['kind']=='phrase']),'alphabet':len([x for x in items if x['group']==g and x['kind'] in ['letter','letter-name','syllable']]),'pages':sorted(set(x['page'] for x in items if x['group']==g))} for g in ['hangul','1','2','3','4']}
(root/'coverage.json').write_text(json.dumps(coverage,indent=2),encoding='utf-8')
print('Final:',len(items),'items;',len(set(x['ko'] for x in items if x['kind']=='word')),'words;',len(set(x['ko'] for x in items if x['kind']=='phrase')),'phrases;',len([x for x in items if x['kind']=='syllable']),'syllables')

import hashlib
for x in items:x["id"]="k-"+hashlib.sha256((x["group"]+"|"+x["kind"]+"|"+x["ko"]).encode()).hexdigest()[:12]
(root/"content.js").write_text("window.COURSE = "+json.dumps({"title":"서울대 한국어+ 1A","scope":"PDF pages 1–145 · Hangul + units 1–4","items":items,"consonants":consonants,"vowels":vowels,"names":names},ensure_ascii=False,indent=2)+";\n",encoding="utf-8")
